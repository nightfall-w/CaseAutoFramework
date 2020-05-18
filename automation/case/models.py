from django.db import models


# Create your models here.
class GitCase(models.Model):
    lester_user = models.CharField(max_length=25, verbose_name="最后提交用户", help_text="上一次提交的用户")
    branch_name = models.CharField(max_length=20, verbose_name="当前分支", help_text="分支名称")
    status = models.CharField(max_length=10, verbose_name="case状态", help_text="状态")
    lester_time = models.DateTimeField(verbose_name="上次更新时间", auto_now=True, help_text="上一次提交时间")

    class Meta:
        db_table = "case_status"
        verbose_name = verbose_name_plural = "case状态"

    def __str__(self):
        return self.branch_name


class CaseTypeModel(models.Model):
    name = models.CharField(max_length=40, verbose_name="case类型名称", help_text="case类型名称")
    description = models.TextField(max_length=200, null=True, blank=True, verbose_name="类型表述", help_text="case类型表述")

    class Meta:
        db_table = "case_type"
        verbose_name = verbose_name_plural = "case_type"

    def __str__(self):
        return self.name


class CaseModel(models.Model):
    case_name = models.CharField(max_length=25, verbose_name="case名称", help_text="case名称")
    case_desc = models.TextField(max_length=200, null=True, blank=True, verbose_name="case描述", help_text="case描述")
    case_type = models.ForeignKey(CaseTypeModel, null=True, blank=True, on_delete=models.SET_NULL,
                                  verbose_name="case类型")
    case_path = models.CharField(max_length=200, verbose_name="case路径", help_text="case路径")
    create_user = models.CharField(max_length=20, verbose_name="创建人", help_text="case创建人")
    create_time = models.DateTimeField(auto_now_add=True, help_text="case创建时间")

    class Meta:
        db_table = "case"
        verbose_name = verbose_name_plural = "case"

    def __str__(self):
        return self.case_name
