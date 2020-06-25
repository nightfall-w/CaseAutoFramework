from django.urls import re_path
from testplan.views import test_return_file, TriggerPlan

app_name = 'testPlan'
urlpatterns = [
    re_path('^run/$', TriggerPlan.as_view(), name='runApiTestPlan'),
    re_path('^test_return_file/$', test_return_file.as_view(), name='test_return_file'),
]
