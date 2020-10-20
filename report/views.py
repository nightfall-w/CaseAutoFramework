# -*- coding:utf-8 -*-
import datetime

from django.http import JsonResponse

from report.email import send_case_report_mail


def send_report_mail(request):
    now_time = datetime.datetime.now()
    now_strptime = datetime.datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
    send_case_report_mail('rimuli_w@163.com', now_strptime, "王保军", "18901942952", "wangbaojun@flashhold.com",
                          "Quicktron", "你好")
    return JsonResponse({"success": True, "data": "send email success"})
