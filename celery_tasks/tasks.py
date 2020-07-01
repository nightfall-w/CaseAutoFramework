# -*- coding=utf-8 -*-
from celery_tasks.celery import app
from testplan.runner import ApiRunner, data_drive, CaseRunner
from testplan.models import CaseTestPlanTaskModel, CaseTestPlanModel, CaseJobModel
from utils.job_status_enum import CaseTestPlanTaskState


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
        CaseTestPlanTaskModel.objects.filter(id=case_task_id).update(finish_num=index + 1)
    CaseTestPlanTaskModel.objects.filter(id=case_task_id).update(state=CaseTestPlanTaskState.FINISH)


@app.task(name="case_test_job_executor")
def case_test_job_executor(case_job, project_id, test_plan_uid, task_id):
    CaseTestPlanTaskModel.objects.filter(id=task_id).update(state=CaseTestPlanTaskState.RUNNING)
    CaseRunner.executor(case_job=case_job, project_id=project_id, test_plan_uid=test_plan_uid,
                        task_id=task_id)
    case_task = CaseTestPlanTaskModel.objects.get(id=task_id)
    case_task.finish_num = case_task.finish_num + 1
    if case_task.finish_num == case_task.case_job_number:
        case_task.state = CaseTestPlanTaskState.FINISH
    case_task.save()
