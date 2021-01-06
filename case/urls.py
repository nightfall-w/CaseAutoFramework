from django.urls import path
from case.views import CaseTree, GitlabBranch, GitlabPull

app_name = 'case'
urlpatterns = [
    path('branch', GitlabBranch.as_view(), name='branch_list'),
    path('branch_pull', GitlabPull.as_view(), name='branch_pull'),
    path('tree', CaseTree.as_view(), name="case_tree")
]
