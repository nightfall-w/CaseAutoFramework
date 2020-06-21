# -*- coding=utf-8 -*-
from celery_tasks.celery import app
from testplan.runner import ApiRunner


@app.task(name="ApiTestPlan")
def ApiTestPlan(test_plan_id):
    """
    【api测试计划的触发器】
    """
    ApiRunner(test_plan_id=test_plan_id).distributor()
    return True
