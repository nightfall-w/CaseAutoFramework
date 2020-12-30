from django.db import models
from django_jsonfield_backport.models import JSONField
from standard.enum import InterFaceType


class InterfaceModel(models.Model):
    MODE_LIST = [
        ('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE'), ('PATCH', 'PATCH')
    ]
    project = models.IntegerField(verbose_name="项目id", null=False, help_text="项目id")
    name = models.CharField(verbose_name="接口名称", max_length=50, null=False, help_text="接口名称")
    desc = models.TextField(verbose_name="接口描述", default='', help_text="接口描述")
    addr = models.CharField(verbose_name="接口地址", null=False, max_length=1000, help_text="接口地址")
    request_mode = models.CharField(verbose_name="请求方式", choices=MODE_LIST, max_length=8,
                                    help_text="请求方式")
    protocol = models.CharField(verbose_name="协议", max_length=5, help_text="请求协议")
    headers = JSONField(verbose_name="请求头", null=True, default=dict, help_text="请求头")
    formData = JSONField(verbose_name="formData", null=True, default=dict, help_text="表单数据包括文件")
    urlencoded = JSONField(verbose_name="x-www-form-urlencoded", null=True, default=dict,
                           help_text="url参数params,数据转换为键值对，&分隔后用?拼接在url后面")
    raw = JSONField(verbose_name="requestBody", null=True, default=dict,
                    help_text="可以上传任意格式的文本，可以上传text、json、xml、html等")
    asserts = JSONField(verbose_name="断言", null=True, default=list, help_text="断言")
    parameters = JSONField(verbose_name="参数集", null=True, default=dict, help_text="参数集")
    extract = JSONField(verbose_name="出参", null=True, default=list, help_text="出参")

    class Meta:
        db_table = 'interface'
        verbose_name = verbose_name_plural = "接口"

    def __str__(self):
        return self.name


class InterfaceCacheModel(models.Model):
    MODE_LIST = [
        ('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE'), ('PATCH', 'PATCH')
    ]
    project = models.IntegerField(verbose_name="项目id", null=False, help_text="项目id")
    name = models.CharField(verbose_name="接口名称", max_length=50, null=True, help_text="接口名称")
    desc = models.TextField(verbose_name="接口描述", null=True, default='', help_text="接口描述")
    addr = models.CharField(verbose_name="接口地址", null=False, max_length=1000, help_text="接口地址")
    request_mode = models.CharField(verbose_name="请求方式", choices=MODE_LIST, max_length=8,
                                    help_text="请求方式")
    headers = JSONField(verbose_name="请求头", null=True, default=dict, help_text="请求头")
    formData = JSONField(verbose_name="formData", null=True, default=dict, help_text="表单数据包括文件")
    urlencoded = JSONField(verbose_name="x-www-form-urlencoded", null=True, default=dict,
                           help_text="url参数params,数据转换为键值对，&分隔后用?拼接在url后面")
    raw = JSONField(verbose_name="requestBody", null=True, default=dict,
                    help_text="可以上传任意格式的文本，可以上传text、json、xml、html等")
    asserts = JSONField(verbose_name="断言", null=True, default=list, help_text="断言")
    extract = JSONField(verbose_name="出参", null=True, default=list, help_text="出参")

    class Meta:
        db_table = 'interface_cache'
        verbose_name = verbose_name_plural = "数据映射接口实例"

    def __str__(self):
        return self.name


class InterfaceHistory(models.Model):
    MODE_LIST = [
        ('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE'), ('PATCH', 'PATCH')
    ]
    addr = models.CharField(verbose_name="接口地址", null=False, max_length=1000, help_text="接口地址")
    request_mode = models.CharField(verbose_name="请求方式", choices=MODE_LIST, max_length=8,
                                    help_text="请求方式")
    headers = JSONField(verbose_name="请求头", null=True, blank=True, default=dict, help_text="请求头")
    formData = JSONField(verbose_name="formData", null=True, blank=True, default=dict, help_text="表单数据包括文件")
    urlencoded = JSONField(verbose_name="x-www-form-urlencoded", null=True, blank=True, default=dict,
                           help_text="url参数params,数据转换为键值对，&分隔后用?拼接在url后面")
    raw = JSONField(verbose_name="requestBody", null=True, blank=True, default=dict,
                    help_text="可以上传任意格式的文本，可以上传text、json、xml、html等")
    user = models.CharField(verbose_name="用户", max_length=40, null=False, help_text="用户")

    class Meta:
        db_table = 'interface_history'
        verbose_name = verbose_name_plural = "在线postman测试历史记录"

    def __str__(self):
        return self.addr


class InterfaceJobModel(models.Model):
    interfaceType = models.CharField(verbose_name="接口类型", null=False, default=InterFaceType.INSTANCE.value,
                                     max_length=10, help_text="接口类型")

    interface_id = models.IntegerField(verbose_name="接口id", null=False, help_text="接口id")
    test_plan_id = models.CharField(verbose_name="测试计划id", max_length=50, null=False, help_text="测试计划id")
    api_test_plan_task_id = models.IntegerField(verbose_name="测试计划任务id", null=False, help_text="测试计划任务id")
    extracts = models.TextField(verbose_name="提取结果", null=False, default=dict, help_text="提取结果")
    state = models.CharField(verbose_name="接口测试状态", null=False, max_length=10, help_text="接口测试状态")
    result = models.TextField(verbose_name="接口响应结果", null=True, help_text="接口响应结果")
    status_code = models.IntegerField(verbose_name="响应状态码", help_text="响应状态码", null=True)
    elapsed = models.FloatField(verbose_name="响应时间", null=True, help_text="响应时间")
    create_data = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, help_text="创建时间")

    class Meta:
        db_table = "interface_job"
        verbose_name = verbose_name_plural = "接口任务"

    def __str__(self):
        return str(self.test_plan_id) + "&&" + str(self.interface_id)
