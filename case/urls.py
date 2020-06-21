from django.urls import path
from case.views import GitTool, CaseTree

app_name = 'case'
urlpatterns = [
    path('pull', GitTool.as_view(), name='case_pull'),
    path('tree', CaseTree.as_view(), name="case_tree")
]
