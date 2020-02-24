from django.urls import path
from case.views import gitTool

app_name = 'case'
urlpatterns = [
    path('tree/', gitTool.as_view({'get': 'get_case_tree'}), name='tree'),
]
