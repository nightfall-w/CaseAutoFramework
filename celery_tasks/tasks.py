# -*- coding=utf-8 -*-
from celery_tasks.celery import app
from testplan.runner import ApiRunner, data_drive
import time

@app.task(name="ApiTestPlan")
def ApiTestPlan(test_plan_id, interfaceIds):
    """
    【api测试计划的触发器】
    """
    data_drive(interfaceIds, test_plan_id)
    time.sleep(100)
    ApiRunner(test_plan_id=test_plan_id).distributor()
    return True
