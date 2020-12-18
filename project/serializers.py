import json

from project.models import ProjectModel
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    create_date = serializers.SerializerMethodField()
    env_variable = serializers.JSONField()

    class Meta:
        model = ProjectModel
        exclude = ['create_time', 'update_time']
        read_only_fields = ["id", "create_time", "update_time"]
        extra_kwargs = {
            "create_by": {'required': False},
            "update_by": {'required': False}
        }
        depth = 1

    def get_create_date(self, obj):
        return obj.create_time.strftime("%Y-%m-%d")

    def get_env_dict(self, obj):
        return json.loads(obj.env_variable)
