from __future__ import absolute_import, unicode_literals

import os
from datetime import datetime

import pytz
from celery import Celery


def app_now():
    tzinfo = pytz.timezone('Asia/Shanghai')
    return datetime.now(tz=tzinfo)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'automation.settings')

app = Celery('celery_tasks')

app.config_from_object('celery_tasks.celeryconfig', namespace='CELERY')
app.now = app_now
app.autodiscover_tasks(["celery_tasks"])


def app_now():
    tzinfo = pytz.timezone('Asia/Shanghai')
    return datetime.datetime.now(tz=tzinfo)
