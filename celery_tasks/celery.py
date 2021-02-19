from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'automation.settings')

app = Celery('automation')

app.config_from_object('celery_tasks.celeryconfig', namespace='CELERY')
app.now = timezone.now

app.autodiscover_tasks()
