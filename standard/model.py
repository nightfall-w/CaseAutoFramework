import json

from django.db import models


class JSONField(models.TextField):
    description = "Json"
