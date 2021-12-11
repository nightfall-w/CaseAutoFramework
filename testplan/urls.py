from django.urls import re_path

from testplan.views import TriggerApiPlan, TriggerCasePlan, CaseTask, ApiTask

app_name = 'testPlan'
urlpatterns = [
    re_path('^runApiTestPlan/$', TriggerApiPlan.as_view(), name='runApiTestPlan'),
    re_path('^runCaseTestPlan/$', TriggerCasePlan.as_view(), name='runCaseTestPlan'),
    re_path('^caseTask/$', CaseTask.as_view(), name='CaseTask'),
    re_path('^apiTask/$', ApiTask.as_view(), name='ApiTask'),
]
