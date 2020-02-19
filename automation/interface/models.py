from django.db import models
from standard.model import JSONField


class InterfaceModel(models.Model):
    MODE_LIST = [
        (1, 'GET'), (2, 'POST'), (3, 'PUT'), (4, 'DELETE'), (5, 'PATCH')
    ]
    name = models.CharField(verbose_name="接口名称", max_length=50, null=False)
    desc = models.TextField(verbose_name="接口描述", default='')
    addr = models.CharField(verbose_name="接口地址", null=False, max_length=1000)
    request_mode = models.CharField(verbose_name="请求方式", choices=MODE_LIST, max_length=8)
    params = JSONField(verbose_name="url参数", null=True)
    headers = JSONField(verbose_name="请求头", null=True)
    formData = JSONField(verbose_name="formData", null=True)
    urlencoded = JSONField(verbose_name="x-www-form-urlencoded", null=True)
    raw = JSONField(verbose_name="requestBody", null=True)
    asserts = JSONField(verbose_name="断言", null=True)

    class Meta:
        db_table = 'interface'
        verbose_name = verbose_name_plural = "接口"

    def __str__(self):
        return self.name
