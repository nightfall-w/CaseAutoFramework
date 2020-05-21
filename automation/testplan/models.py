from django.db import models


class ApiTestPlanModel(models.Model):
    name = models.CharField(verbose_name="计划名称", max_length=30, null=False, help_text="测试计划名")
    plan_id = models.CharField(verbose_name="计划id", max_length=30, null=False, help_text="计划编号")
    state = models.CharField(verbose_name="执行状态", max_length=10, null=False, help_text="执行状态")
    create_data = models.DateTimeField(verbose_name="创建时间", auto_created=True, help_text="创建时间")
    update_data = models.DateTimeField(verbose_name="更新时间", auto_now=True, help_text="更新时间")

    class Meta:
        db_table = "api_test_plan"
        verbose_name = verbose_name_plural = "接口测试计划"

    def __str__(self):
        return self.name
