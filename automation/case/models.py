from django.db import models


# Create your models here.
class GitCase(models.Model):
    lester_user = models.CharField(max_length=25, verbose_name="最后提交用户")
    branch_name = models.CharField(max_length=20, verbose_name="当前分支")
    status = models.CharField(max_length=10, verbose_name="case状态")
    lester_time = models.DateTimeField(verbose_name="上次更新时间", auto_now=True)

    class Meta:
        db_table = "case_status"
        verbose_name = verbose_name_plural = "case状态"

    def __str__(self):
        return self.branch_name
