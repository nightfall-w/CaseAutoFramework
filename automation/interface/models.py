from django.db import models
from standard.model import JSONField


class InterfaceModel(models.Model):
    MODE_LIST = [
        (1, 'GET'), (2, 'POST'), (3, 'PUT'), (4, 'DELETE'), (5, 'PATCH')
    ]
    name = models.CharField(verbose_name="接口名称", max_length=50, null=False, help_text="接口名称")
    desc = models.TextField(verbose_name="接口描述", default='', help_text="接口描述")
    addr = models.CharField(verbose_name="接口地址", null=False, max_length=1000, help_text="接口地址")
    request_mode = models.CharField(verbose_name="请求方式", choices=MODE_LIST, max_length=8, help_text="请求方式")
    headers = JSONField(verbose_name="请求头", null=False, default='{}', help_text="请求头")
    formData = JSONField(verbose_name="formData", null=False, default='{}', help_text="表单数据包括文件")
    urlencoded = JSONField(verbose_name="x-www-form-urlencoded", null=True,
                           help_text="url参数params,数据转换为键值对，&分隔后用?拼接在url后面")
    raw = JSONField(verbose_name="requestBody", null=False, default='{}',
                    help_text="可以上传任意格式的文本，可以上传text、json、xml、html等")
    asserts = JSONField(verbose_name="断言", null=False, default='{}', help_text="断言")

    class Meta:
        db_table = 'interface'
        verbose_name = verbose_name_plural = "接口"

    def __str__(self):
        return self.name


class InterfaceTaskModel(models.Model):
    interface_id = models.IntegerField(verbose_name="接口id", null=False, help_text="接口id")
    task_id = models.CharField(verbose_name="任务id", max_length=30, null=False, help_text="任务id")
    state = models.CharField(verbose_name="接口测试状态", null=False, max_length=10, help_text="接口测试状态")
    create_data = models.DateTimeField(verbose_name="接口测试状态", auto_now_add=True, help_text="接口测试状态")
    result = models.TextField(verbose_name="接口响应结果", null=False, help_text="接口响应结果")

    class Meta:
        db_table = "interface_task"
        verbose_name = verbose_name_plural = "接口任务"

    def __str__(self):
        return self.task_id
