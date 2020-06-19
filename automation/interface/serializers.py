import json

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from Logger import logger
from interface.models import InterfaceModel, InterfaceHistory


class InterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterfaceModel
        fields = '__all__'
        depth = 1
        validators = [
            UniqueTogetherValidator(
                queryset=InterfaceModel.objects.all(),
                fields=('project', 'name', 'addr'),
                message="已经存在相同名称和url的接口"
            )
        ]

    def validate(self, attrs):
        for item in attrs:
            if item in ['headers', 'formData', 'urlencoded', 'raw', 'asserts', 'parameters']:
                try:
                    json.loads(attrs[item])
                except Exception as es:
                    logger.error(es)
                    raise serializers.ValidationError('字段{}不是json格式'.format(item))
        return attrs


class InterfaceTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterfaceHistory
        fields = '__all__'
        depth = 1
        validators = [
            UniqueTogetherValidator(
                queryset=InterfaceHistory.objects.all(),
                fields=(
                    'addr', "request_mode", "headers", "formData", "urlencoded", "raw", "user"),
                message="existed"
            )
        ]

    def validate(self, attrs):
        for item in attrs:
            if item in ['headers', 'formData', 'urlencoded', 'raw']:
                try:
                    json.loads(attrs[item])
                except Exception as es:
                    logger.error(es)
                    raise serializers.ValidationError('字段{}不是json格式'.format(item))
        return attrs
