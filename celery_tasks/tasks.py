# -*- coding=utf-8 -*-
from celery_tasks.celery import app
from testplan.runner import ApiRunner, data_drive


@app.task(name="ApiTestPlan")
def ApiTestPlan(test_plan_id, interfaceIds, api_test_plan_task_id):
    """
    【api测试计划的触发器】
    """
    data_drive(interfaceIds, test_plan_id, api_test_plan_task_id)
    ApiRunner(test_plan_id=test_plan_id, test_plan_task_id=api_test_plan_task_id).distributor()
    return True
