from project.models import ProjectModel
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModel
        exclude = ['create_time', 'update_time']
        depth = 1
