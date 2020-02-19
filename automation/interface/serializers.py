from interface.models import InterfaceModel
from rest_framework import serializers


class InterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterfaceModel
        fields = '__all__'
        depth = 1
