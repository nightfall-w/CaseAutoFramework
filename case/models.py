from django.db import models


class GitCaseModel(models.Model):
    gitlab_url = models.CharField(max_length=100, verbose_name="gitlab地址", help_text="gitlab地址")
    gitlab_project_name = models.CharField(max_length=100, verbose_name="gitlab项目名", help_text="gitlab项目名")
    branch_name = models.CharField(max_length=20, verbose_name="当前分支", help_text="分支名称")
    status = models.CharField(max_length=10, verbose_name="case状态", help_text="状态")

    class Meta:
        db_table = "branch_status"
        verbose_name = verbose_name_plural = "分支状态"

    def __str__(self):
        return self.gitlab_project_name


# class CaseTypeModel(models.Model):
#     name = models.CharField(max_length=40, verbose_name="case类型名称", help_text="case类型名称")
#     description = models.TextField(max_length=200, null=True, blank=True, verbose_name="类型表述", help_text="case类型表述")
#
#     class Meta:
#         db_table = "case_type"
#         verbose_name = verbose_name_plural = "case_type"
#
#     def __str__(self):
#         return self.name


# class CaseModel(models.Model):
#     case_name = models.CharField(max_length=25, verbose_name="case名称", help_text="case名称")
#     case_desc = models.TextField(max_length=200, null=True, blank=True, verbose_name="case描述", help_text="case描述")
#     case_type = models.ForeignKey(CaseTypeModel, null=True, blank=True, on_delete=models.SET_NULL,
#                                   verbose_name="case类型")
#     case_path = models.CharField(max_length=200, verbose_name="case路径", help_text="case路径")
#     create_user = models.CharField(max_length=20, verbose_name="创建人", help_text="case创建人")
#     create_time = models.DateTimeField(auto_now_add=True, verbose_name="case创建时间", help_text="case创建时间")
#
#     class Meta:
#         db_table = "case"
#         verbose_name = verbose_name_plural = "case"
#
#     def __str__(self):
#         return self.case_name


class GitlabModel(models.Model):
    gitlab_url = models.CharField(max_length=200, verbose_name="clone代码库地址(http方式)", help_text="clone代码库地址(http方式)")
    desc = models.CharField(max_length=10, verbose_name="描述", help_text="描述", default='')
    private_token = models.CharField(max_length=30, verbose_name="私有令牌", help_text="私有令牌")

    class Meta:
        unique_together = ["gitlab_url", "private_token"]
        db_table = "gitlab_info"
        verbose_name = verbose_name_plural = "gitlab_url"

    def __str__(self):
        return self.gitlab_url
