from django.db import models
from standard.model import JSONField


class ProjectModel(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='项目名', help_text="项目名称")
    desc = models.TextField(verbose_name='项目描述', default='', help_text="项目描述")
    env_variable = JSONField(verbose_name="环境变量", null=False, help_text="环境变量")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, help_text="创建时间")
    update_time = models.DateTimeField(verbose_name="最后一次更新时间", auto_now=True, help_text="最后一次更新时间")
    create_by = models.CharField(max_length=20, verbose_name="创建人", help_text="创建人")
    update_by = models.CharField(max_length=20, verbose_name="最后一次修改人", help_text="最后一次修改人")

    class Meta:
        db_table = 'project'
        verbose_name = verbose_name_plural = "项目"

    def __str__(self):
        return self.name
