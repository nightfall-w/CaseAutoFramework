from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.utils import timezone

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'automation.settings')

app = Celery('automation')

# app.config_from_object('django.conf:settings', namespace='CELERY')
app.config_from_object('celery_tasks.config', namespace='CELERY')
app.now = timezone.now
# app.conf.update(
#     timezone='Asia/Shanghai',
#     enable_utc=False,
#
# )

# Load task modules from all registered Django app configs.

app.autodiscover_tasks()
