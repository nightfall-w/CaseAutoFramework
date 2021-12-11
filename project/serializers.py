import json

from rest_framework import serializers

from project.models import ProjectModel
from user.models import get_user_by_username


class ProjectSerializer(serializers.ModelSerializer):
    create_date = serializers.SerializerMethodField()
    user_info = serializers.SerializerMethodField()
    env_variable = serializers.JSONField()

    class Meta:
        model = ProjectModel
        exclude = ['create_time', 'update_time']
        read_only_fields = ["id", "create_time", "update_time"]
        extra_kwargs = {
            "create_user": {'required': False},
            "update_user": {'required': False}
        }
        depth = 1

    def get_create_date(self, obj):
        return obj.create_time.strftime("%Y-%m-%d")

    def get_env_dict(self, obj):
        return json.loads(obj.env_variable)

    def get_user_info(self, obj):
        return get_user_by_username(obj.create_user)
