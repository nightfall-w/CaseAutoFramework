import json

from project.models import ProjectModel
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    create_date = serializers.SerializerMethodField()
    env_dict = serializers.SerializerMethodField()

    class Meta:
        model = ProjectModel
        exclude = ['create_time', 'update_time']
        read_only_fields = ["id", "create_time", "update_time", "env_dict"]
        extra_kwargs = {
            "env_variable": {"write_only": True},
            "create_by": {'required': False},
            "update_by": {'required': False}
        }
        depth = 1

    def get_create_date(self, obj):
        return obj.create_time.strftime("%Y-%m-%d %H:%M:%S")

    def get_env_dict(self, obj):
        return json.loads(obj.env_variable)
