from django.urls import re_path
from testplan.views import test_return_file, TriggerApiPlan, TriggerCasePlan

app_name = 'testPlan'
urlpatterns = [
    re_path('^runApiTestPlan/$', TriggerApiPlan.as_view(), name='runApiTestPlan'),
    re_path('^runCaseTestPlan/$', TriggerCasePlan.as_view(), name='runCaseTestPlan'),
    re_path('^test_return_file/$', test_return_file.as_view(), name='test_return_file'),
]
