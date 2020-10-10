from django.core.mail import send_mail
from django.conf import settings


def send_case_report_mail(send_email, now_time, name, mobile, email, company, content):
    with open(
            "/media/baojunw/85DEE7E74A5E9202/Documents/code/vue/CaseAutoFramework/media/html-report/1/945bf652-424c-4f2e-af5f-7b9f4cffffe6/47/test_demo2.html",
            'r') as f:
        data = f.read()
    send_mail(
        subject='网站留言通知',
        message='-----------------------------------------------------------------------',
        from_email=settings.EMAIL_FROM,
        recipient_list=[send_email],
        html_message=data
    )


def send_interface_report_mail(recipients: list, now_time, title, report_type, test_plan_name, detail_url):
    return send_mail(
        subject='QA测试报告',
        message='',
        from_email=settings.EMAIL_FROM,
        recipient_list=recipients,
        html_message=''
    )
