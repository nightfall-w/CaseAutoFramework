# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import time

import redis
from django.core.cache import cache
from django.forms.models import model_to_dict

from automation.settings import logger, BASE_DIR
from case.models import GitCaseModel
from celery_tasks import celery_app
from testplan.models import CaseTestPlanTaskModel, CaseTestPlanModel, CaseJobModel
from testplan.runner import ApiRunner, data_drive, CaseRunner
from utils.common import current_time_format
from utils.gitlab_tool import GitlabAPI
from utils.job_status_enum import CaseTestPlanTaskState, BranchState
from utils.redis_tool import RedisPoll
from utils.snow import IdWorker


# 由于是递归方式下载的所以要先创建项目相应目录
def create_dir(dir_name):
    if not os.path.isdir(dir_name):
        logger.info("\033[0;32;40m开始创建目录: \033[0m{0}".format(dir_name))
        os.makedirs(dir_name)
        time.sleep(0.1)


@celery_app.task(name="branch_pull")
def branch_pull(gitlab_info, project_id, branch_name):
    """
    录取gitlab指定分支代码
    """
    instance = GitlabAPI(gitlab_url=gitlab_info.get('gitlab_url'),
                         private_token=gitlab_info.get('private_token'))
    project = instance.gl.projects.get(project_id)
    obj_tuple = GitCaseModel.objects.update_or_create(gitlab_url=gitlab_info.get('gitlab_url'),
                                                      gitlab_project_name=project.name,
                                                      gitlab_project_id=project.id,
                                                      branch_name=branch_name)
    obj_tuple[0].status = BranchState.PULLING
    obj_tuple[0].save()
    cache_key = "private_token:" + gitlab_info.get('private_token') + "-" + "project_id:" + str(
        project_id) + "-" + "branch_name:" + branch_name
    cache.set(cache_key, BranchState.PULLING)
    try:
        info = project.repository_tree(ref=branch_name, all=True, recursive=True, as_list=True)
        file_list = []
        root_path = os.path.join(BASE_DIR, 'case_house',
                                 gitlab_info.get('gitlab_url').replace(':', '-').replace('.', '-').replace('/', ''),
                                 branch_name,
                                 project.name)
        if not os.path.isdir(root_path):
            os.makedirs(root_path)
        os.chdir(root_path)
        # 调用创建目录的函数并生成文件名列表
        for info_dir in range(len(info)):
            if info[info_dir]['type'] == 'tree':
                dir_name = info[info_dir]['path']
                create_dir(dir_name)
            else:
                file_name = info[info_dir]['path']
                file_list.append(file_name)
        file_list_len = len(file_list)
        for index, info_file in enumerate(range(file_list_len)):
            # 开始下载
            getf = project.files.get(file_path=file_list[info_file], ref=branch_name)
            content = getf.decode()
            with open(file_list[info_file], 'wb') as code:
                logger.info("\033[0;32;40m开始下载文件: \033[0m{0}".format(file_list[info_file]))
                code.write(content)
            finish_progress = float('%.2f' % ((index + 1) / file_list_len)) * 100
            cache.set(cache_key + "progress", finish_progress, 3)
        branch_obj = GitCaseModel.objects.get(gitlab_url=gitlab_info.get('gitlab_url'), gitlab_project_id=project.id,
                                              gitlab_project_name=project.name, branch_name=branch_name,
                                              )
        branch_obj.status = BranchState.DONE
        branch_obj.save()
        cache.set(cache_key, BranchState.DONE)
        return True
    except Exception as es:
        logger.error(str(es))
        branch_obj = GitCaseModel.objects.get(gitlab_url=gitlab_info.get('gitlab_url'), gitlab_project_id=project.id,
                                              gitlab_project_name=project.name, branch_name=branch_name,
                                              )
        branch_obj.status = BranchState.FAILED
        branch_obj.save()
        cache.set(cache_key, BranchState.FAILED)
        return False


@celery_app.task(name="api_testplan_executor")
def api_testplan_executor(test_plan_id, interfaceIds, api_test_plan_task_id):
    """
    【api测试计划的执行器】
    """
    data_drive(interfaceIds, test_plan_id, api_test_plan_task_id)
    ApiRunner(test_plan_id=test_plan_id, test_plan_task_id=api_test_plan_task_id).distributor()
    return True


@celery_app.task(name="case_test_task_executor")
def case_test_task_executor(case_task_id):
    """
    【case测试计划执行器】
    :param case_task_id: case的task id
    """
    case_task = CaseTestPlanTaskModel.objects.filter(id=case_task_id).first()
    case_test_plan = CaseTestPlanModel.objects.filter(plan_id=case_task.test_plan_uid).first()
    case_jobs = CaseJobModel.objects.filter(case_task_id=case_task_id)
    case_task.state = CaseTestPlanTaskState.RUNNING
    case_task.save()
    for index, case_job in enumerate(case_jobs):
        CaseRunner.executor(case_job=case_job, project_id=case_test_plan.project_id,
                            test_plan_uid=case_test_plan.plan_id,
                            task_id=case_task_id)
        # case_task = CaseTestPlanTaskModel.objects.filter(id=case_task_id).first()
        case_task.refresh_from_db()
        case_task.finish_num += 1
        case_task.save()
    # case_task = CaseTestPlanTaskModel.objects.filter(id=case_task_id).first()
    case_task.refresh_from_db()
    used_time = case_task.update_date - case_task.create_date
    case_task.state = CaseTestPlanTaskState.FINISH
    case_task.used_time = used_time.total_seconds()
    case_task.save()
    return True


# noinspection PyUnresolvedReferences
@celery_app.task(name="case_test_task_timing_executor")
def case_test_task_timing_executor(project_id, case_testplan_uid):
    """
    定时任务 执行case task
    :param project_id: 项目的project ID
    :param case_testplan_uid: case testplan的 UUID
    :return:
    """
    case_test_plan = CaseTestPlanModel.objects.filter(project_id=project_id, plan_id=case_testplan_uid).first()
    if not case_test_plan:
        logger.error("case testplan uid: {} not found")
        return False
    case_paths = case_test_plan.case_paths
    case_task_uid = "CASETASKTIMED_" + str(IdWorker(0, 1).get_id())
    case_test_plan_task = CaseTestPlanTaskModel.objects.create(test_plan_uid=case_testplan_uid,
                                                               case_task_uid=case_task_uid,
                                                               state=CaseTestPlanTaskState.WAITING,
                                                               case_job_number=len(case_paths),
                                                               finish_num=0)
    CaseRunner.distributor(case_test_plan_task)

    # 根据是否并行执行case选择不用的触发器
    if case_test_plan.parallel:
        '''并行执行'''
        case_jobs_id = CaseJobModel.objects.filter(case_task_id=case_test_plan_task.id).values_list('id', flat=True)
        for case_job_id in case_jobs_id:
            case_test_job_executor.delay(case_job_id, project_id, case_test_plan.plan_id, case_test_plan_task.id)
    else:
        '''串行执行'''
        case_test_task_executor(case_test_plan_task.id)


@celery_app.task(name="case_test_job_executor")
def case_test_job_executor(case_job_id, project_id, test_plan_uid, task_id):
    """
    【case job执行处理器】
    :param case_job_id: case job的id
           project_id: 项目id
           test_plan_uid: 测试计划uid
           task_id: CaseTestPlanTaskModel模型的id主键
    """
    # 根据case testPlan task id获取模型并更新状态为RUNNING
    CaseTestPlanTaskModel.objects.filter(id=task_id).update(state=CaseTestPlanTaskState.RUNNING)
    case_job = CaseJobModel.objects.get(id=case_job_id)
    # 执行case job(运行case并生成报告)
    result = CaseRunner.executor(case_job=case_job, project_id=project_id, test_plan_uid=test_plan_uid,
                                 task_id=task_id)
    # 因为使用celery进行异步执行case，会出现在同一时刻多个case同时完成时一起修改finish num导致数据出错的问题，因此使用分布式锁保证数据一致性

    # 用testplanid与taskid组成redis锁的key，可以唯一定位一个case testplan
    lock_key = test_plan_uid + str(task_id)
    # 从redis连接池获取一个连接实例
    r = redis.Redis(connection_pool=RedisPoll().instance)
    while True:
        if r.setnx(lock_key, 1):  # 只有在key不存在的情况下才能设置成功 条件成立
            try:
                # 修改已完成数
                case_task = CaseTestPlanTaskModel.objects.get(id=task_id)
                case_task.finish_num += 1
                case_task.save()
                if case_task.finish_num == case_task.case_job_number:
                    # 已完成数等于case总数 那整个case test plan全部完成
                    case_task.state = CaseTestPlanTaskState.FINISH
                    case_task.save()
                    used_time = case_task.update_date - case_task.create_date
                    case_task.used_time = used_time.total_seconds()
                    case_task.save()
            except Exception as es:
                logger.error("Update CaseTestPlanTask finish_num Fail, es:{}, testplan id:{}".format(es, task_id))
            finally:
                # 为了防止造成死锁  无论成功与否都需要释放锁
                r.delete(lock_key)
                break
        else:
            # 已经被其他celery任务上锁 等待0.5s后重试
            time.sleep(0.2)
            continue
    return result
