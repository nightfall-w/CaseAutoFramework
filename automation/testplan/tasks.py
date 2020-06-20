# -*- coding=utf-8 -*-
from celery import task

from testplan.runner import ApiRunner


@task(name="ApiTestPlan")
def ApiTestPlan(test_plan_id):
    ApiRunner(test_plan_id=test_plan_id).distributor()
    return True
