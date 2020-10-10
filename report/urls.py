from django.urls import path

from report.views import case_report, interface_report, send_report_mail

app_name = 'report'
urlpatterns = [
    path('case_report/', case_report, name='case_report'),
    path('interface_report/', interface_report, name="interface_report"),
    path('send_report_mail/', send_report_mail, name="send_report_mail")
]
