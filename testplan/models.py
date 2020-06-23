# -*- coding=utf-8 -*-
from django.db import models


class ApiTestPlanModel(models.Model):
    """
    接口测试计划模型
    """
    name = models.CharField(verbose_name="计划名称", max_length=30, null=False, help_text="测试计划名")
    plan_id = models.CharField(verbose_name="计划id", max_length=50, null=False, help_text="计划编号")
    interfaceIds = models.CharField(verbose_name="api id 集合", help_text="api id 集合", null=False, max_length=2000)
    project = models.IntegerField(verbose_name="接口名称", null=False, help_text="项目id")
    create_user = models.CharField(verbose_name="创建人", max_length=10, null=False, help_text="创建人")
    create_data = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, help_text="创建时间")
    update_data = models.DateTimeField(verbose_name="更新时间", auto_now=True, help_text="更新时间")

    class Meta:
        db_table = "api_test_plan"
        verbose_name = verbose_name_plural = "接口测试计划"

    def __str__(self):
        return self.name


class ApiTestPlanTaskModel(models.Model):
    test_plan_uid = models.CharField(verbose_name="测试计划uid", max_length=50, null=False, help_text="测试计划uid")
    state = models.CharField(verbose_name="执行状态", max_length=10, null=True, help_text="执行状态")
    api_job_number = models.IntegerField(verbose_name="api job总数", help_text="api job总数", null=True)
    success_num = models.IntegerField(verbose_name="成功条数", null=True, help_text="成功条数")
    failed_num = models.IntegerField(verbose_name="失败条数", null=True, help_text="失败条数")
    create_data = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    update_data = models.DateTimeField(auto_now=True, verbose_name="创建时间", help_text="创建时间")
    used_time = models.FloatField(verbose_name="用时", help_text="用时", null=True)

    class Meta:
        db_table = "api_test_task_plan"
        verbose_name = verbose_name_plural = "接口测试计划任务"

    def __str__(self):
        return self.test_plan_uid
