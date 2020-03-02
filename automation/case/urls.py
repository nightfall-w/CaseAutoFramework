from django.urls import re_path
from case.views import GitTool, CaseTree

app_name = 'case'
urlpatterns = [
    re_path('^pull/$', GitTool.as_view({'get': 'case_pull'}), name='case_pull'),
    re_path('^tree/$', CaseTree.as_view(), name="case_tree")
]
