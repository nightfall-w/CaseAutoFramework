import json

from django.db import models


class JSONField(models.TextField):
    description = "Json"

    def to_python(self, value):
        v = models.TextField.to_python(self, value)
        try:
            return json.loads(v)['v']
        except:
            pass
        return v

    def get_prep_value(self, value):
        return json.dumps({'v': value})
