from django.urls import re_path
from testplan.views import ApiTestPlanView, test_return_file

app_name = 'testPlan'
urlpatterns = [
    re_path('ApiTestPlan/$', ApiTestPlanView.as_view(), name='createApiTestPlan'),
    re_path('test_return_file/$', test_return_file.as_view(), name='test_return_file'),
]
