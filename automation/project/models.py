from django.db import models
from standard.model import JSONField


class ProjectModel(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='项目名')
    desc = models.TextField(verbose_name='项目描述', default='')
    env_variable = JSONField(verbose_name="环境变量", null=False)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="最后一次更新时间", auto_now=True)
    create_by = models.CharField(max_length=20, verbose_name="创建人")
    update_by = models.CharField(max_length=20, verbose_name="最后一次修改人")

    class Meta:
        db_table = 'project'
        verbose_name = verbose_name_plural = "项目"

    def __str__(self):
        return self.name
