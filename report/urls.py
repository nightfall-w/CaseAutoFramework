from django.urls import path

from report.views import send_report_mail

app_name = 'report'
urlpatterns = [
    path('send_report_mail/', send_report_mail, name="send_report_mail")
]
