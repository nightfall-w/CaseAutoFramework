from django.urls import path

from report.views import case_report, interface_report

app_name = 'report'
urlpatterns = [
    path('case_report/', case_report, name='case_report'),
    path('interface_report/', interface_report, name="interface_report")
]
