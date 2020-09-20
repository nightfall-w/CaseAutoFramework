# -*- coding=utf-8 -*-
import uuid

from django.db import models


class ApiTestPlanModel(models.Model):
    """
    接口测试计划模型
    """
    name = models.CharField(verbose_name="计划名称", max_length=30, null=False, help_text="测试计划名")
    plan_id = models.CharField(verbose_name="计划id", max_length=50, null=False, help_text="计划编号")
    interfaceIds = models.CharField(verbose_name="api id 集合", help_text="api id 集合", null=False, max_length=2000)
    project = models.IntegerField(verbose_name="项目id", null=False, help_text="项目id")
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
        db_table = "api_test_plan_task"
        verbose_name = verbose_name_plural = "接口测试计划任务"

    def __str__(self):
        return self.test_plan_uid


class CaseTestPlanModel(models.Model):
    name = models.CharField(verbose_name="计划名称", max_length=30, null=False, help_text="测试计划名")
    plan_id = models.CharField(verbose_name="计划id", max_length=50, null=False, help_text="计划编号", default=uuid.uuid4())
    case_paths = models.CharField(verbose_name="case路径集合", help_text="case路径集合", null=False, max_length=5000)
    project = models.IntegerField(verbose_name="项目id", null=False, help_text="项目id")
    create_user = models.CharField(verbose_name="创建人", max_length=10, null=False, help_text="创建人")
    create_data = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, help_text="创建时间")
    update_data = models.DateTimeField(verbose_name="更新时间", auto_now=True, help_text="更新时间")

    class Meta:
        db_table = "case_test_plan"
        verbose_name = verbose_name_plural = "case测试计划"

    def __str__(self):
        return self.name


class CaseTestPlanTaskModel(models.Model):
    test_plan_uid = models.CharField(verbose_name="测试计划uid", max_length=50, null=False, help_text="测试计划uid")
    state = models.CharField(verbose_name="执行状态", max_length=10, null=True, help_text="执行状态")
    case_job_number = models.IntegerField(verbose_name="api job总数", help_text="api job总数", null=True)
    finish_num = models.IntegerField(verbose_name="成功条数", null=True, help_text="成功条数")
    create_data = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    update_data = models.DateTimeField(auto_now=True, verbose_name="创建时间", help_text="创建时间")
    used_time = models.FloatField(verbose_name="用时", help_text="用时", null=True)

    class Meta:
        db_table = "case_test_plan_task"
        verbose_name = verbose_name_plural = "case测试计划任务"

    def __str__(self):
        return self.test_plan_uid


class CaseJobModel(models.Model):
    case_task_id = models.IntegerField(verbose_name="case task id", null=False, help_text="测试计划uid")
    case_path = models.CharField(verbose_name="case绝对路径", max_length=300, null=False, help_text="case绝对路径")
    state = models.CharField(verbose_name="case执行状态", max_length=10, null=False, help_text="case执行状态")
    result = models.CharField(verbose_name="case执行结果", max_length=100, null=True, help_text="case执行结果")
    log = models.TextField(verbose_name="执行日志", help_text="执行日志", null=True)
    report_path = models.CharField(verbose_name="报告路径", help_text="报告路径", null=True, max_length=200)

    class Meta:
        db_table = "case_job"
        verbose_name = verbose_name_plural = "case测试计划任务"

    def __str__(self):
        return self.case_task_id
