# -*- coding=utf-8 -*-

from django.db import models
from django_jsonfield_backport.models import JSONField


class ApiTestPlanModel(models.Model):
    """
    接口测试计划模型
    """
    name = models.CharField(verbose_name="计划名称", max_length=30, null=False, help_text="测试计划名")
    description = models.TextField(verbose_name="描述", null=True, blank=True, help_text="描述说明")
    plan_id = models.CharField(verbose_name="计划id", max_length=50, null=False, help_text="计划编号")
    interfaceIds = JSONField(verbose_name="api id 集合", help_text="api id 集合", null=False)
    project_id = models.IntegerField(verbose_name="项目id", null=False, help_text="项目id")
    create_user = models.CharField(verbose_name="创建人", max_length=30, null=False, help_text="创建人")
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, help_text="创建时间")
    update_date = models.DateTimeField(verbose_name="更新时间", auto_now=True, help_text="更新时间")

    class Meta:
        db_table = "api_test_plan"
        verbose_name = verbose_name_plural = "接口测试计划"

    def __str__(self):
        return self.name


class ApiTestPlanTaskModel(models.Model):
    api_task_uid = models.CharField(verbose_name="api task uid", max_length=50, null=False, blank=True,
                                    help_text="api_task_uid")
    test_plan_uid = models.CharField(verbose_name="测试计划uid", max_length=50, null=False, help_text="测试计划uid")
    state = models.CharField(verbose_name="执行状态", max_length=10, null=True, help_text="执行状态")
    api_job_number = models.IntegerField(verbose_name="api job总数", help_text="api job总数", null=True)
    success_num = models.IntegerField(verbose_name="成功条数", null=True, help_text="成功条数")
    failed_num = models.IntegerField(verbose_name="失败条数", null=True, help_text="失败条数")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    update_date = models.DateTimeField(auto_now=True, verbose_name="创建时间", help_text="创建时间")
    used_time = models.FloatField(verbose_name="用时", help_text="用时", null=True)

    class Meta:
        db_table = "api_test_plan_task"
        verbose_name = verbose_name_plural = "接口测试计划任务"

    def __str__(self):
        return self.test_plan_uid


class CaseTestPlanModel(models.Model):
    name = models.CharField(verbose_name="计划名称", max_length=30, null=False, help_text="测试计划名")
    description = models.TextField(verbose_name="描述", null=True, blank=True, default='', help_text="描述说明")
    parallel = models.BooleanField(verbose_name="是否并行方式执行", default=False, help_text="是否并行执行")
    timer_enable = models.BooleanField(verbose_name="是否启用定时器", default=False, help_text="是否启用定时器")
    crontab = models.CharField(verbose_name="crontab", max_length=300, null=True, blank=True, help_text="crontab")
    plan_id = models.CharField(verbose_name="计划id", max_length=50, null=False, help_text="计划编号")
    case_paths = JSONField(verbose_name="case路径集合", help_text="case路径集合", null=False)
    env_file = models.CharField(verbose_name="环境配置文件路径", max_length=300, null=True, blank=True, help_text="环境配置文件路径")
    project_id = models.IntegerField(verbose_name="项目id", null=False, help_text="项目id")
    gitlab_url = models.CharField(max_length=100, verbose_name="gitlab地址", help_text="gitlab地址")
    gitlab_project_name = models.CharField(max_length=100, verbose_name="gitlab项目名", help_text="gitlab项目名")
    branch_name = models.CharField(max_length=20, verbose_name="当前分支", help_text="分支名称")
    create_user = models.CharField(verbose_name="创建人", max_length=30, null=False, help_text="创建人")
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, help_text="创建时间")
    update_date = models.DateTimeField(verbose_name="更新时间", auto_now=True, help_text="更新时间")

    class Meta:
        db_table = "case_test_plan"
        verbose_name = verbose_name_plural = "case测试计划"

    def __str__(self):
        return self.name


class CaseTestPlanTaskModel(models.Model):
    case_task_uid = models.CharField(verbose_name="case task uid", max_length=50, null=False, blank=True,
                                     help_text="case_task_uid")
    test_plan_uid = models.CharField(verbose_name="测试计划uid", max_length=50, null=False, help_text="测试计划uid")
    state = models.CharField(verbose_name="执行状态", max_length=10, null=True, help_text="执行状态")
    case_job_number = models.IntegerField(verbose_name="case job总数", help_text="case job总数", null=True)
    finish_num = models.IntegerField(verbose_name="成功条数", null=True, help_text="成功条数")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    update_date = models.DateTimeField(auto_now=True, verbose_name="创建时间", help_text="创建时间")
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
