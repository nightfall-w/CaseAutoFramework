from django.urls import path
from case.views import GitTool

app_name = 'case'
urlpatterns = [
    path('tree/', GitTool.as_view({'get': 'get_case_tree'}), name='tree'),
]
