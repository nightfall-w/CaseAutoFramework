from django.urls import re_path
from testplan.views import ApiTestPlanView

app_name = 'testPlan'
urlpatterns = [
    re_path('ApiTestPlan/$', ApiTestPlanView.as_view(), name='createApiTestPlan'),
]