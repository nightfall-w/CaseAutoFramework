from django.urls import re_path
from case.views import CaseTree, GitlabBranch, GitlabPull, CaseCollectList

app_name = 'case'
urlpatterns = [
    re_path('^branch/$', GitlabBranch.as_view(), name='branch_list'),
    re_path('^branch_pull/$', GitlabPull.as_view(), name='branch_pull'),
    re_path('^tree/$', CaseTree.as_view(), name="case_tree"),
    re_path('^case_collect_list/$', CaseCollectList.as_view(), name="case_collect_list")
]
