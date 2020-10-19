# -*- coding:utf-8 -*-
import time

import redis
from django.db.models import F

from automation.settings import logger
from celery_tasks.celery import app
from testplan.models import CaseTestPlanTaskModel, CaseTestPlanModel, CaseJobModel
from testplan.runner import ApiRunner, data_drive, CaseRunner
from utils.job_status_enum import CaseTestPlanTaskState
from utils.redis_tool import RedisPoll


@app.task(name="api_testplan_executor")
def api_testplan_executor(test_plan_id, interfaceIds, api_test_plan_task_id):
    """
    【api测试计划的执行器】
    """
    data_drive(interfaceIds, test_plan_id, api_test_plan_task_id)
    ApiRunner(test_plan_id=test_plan_id, test_plan_task_id=api_test_plan_task_id).distributor()
    return True


@app.task(name="case_test_task_executor")
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
        CaseRunner.executor(case_job=case_job, project_id=case_test_plan.project, test_plan_uid=case_test_plan.plan_id,
                            task_id=case_task_id)
        # case_task = CaseTestPlanTaskModel.objects.filter(id=case_task_id).first()
        case_task.rerefresh_from_db()
        case_task.finish_num = case_task.finish_num + 1
        case_task.save()
    # case_task = CaseTestPlanTaskModel.objects.filter(id=case_task_id).first()
    case_task.rerefresh_from_db()
    used_time = case_task.update_data - case_task.create_data
    case_task.state = CaseTestPlanTaskState.FINISH
    case_task.used_time = used_time.total_seconds()
    case_task.save()
    return True


@app.task(name="case_test_job_executor")
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
                case_task.finish_num = case_task.finish_num + 1
                case_task.save()
                if case_task.finish_num == case_task.case_job_number:
                    # 已完成数等于case总数 那整个case test plan全部完成
                    case_task.state = CaseTestPlanTaskState.FINISH
                    case_task.save()
                    used_time = case_task.update_data - case_task.create_data
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
