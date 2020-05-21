import json

from rest_framework.validators import UniqueTogetherValidator

from interface.models import InterfaceModel, InterfaceJobModel
from rest_framework import serializers


class InterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterfaceModel
        fields = '__all__'
        depth = 1
        validators = [
            UniqueTogetherValidator(
                queryset=InterfaceModel.objects.all(),
                fields=('name', 'addr'),
                message="已经存在相同名称和url的接口"
            )
        ]

    def validate(self, attrs):
        for item in attrs:
            if item in ['headers', 'formData', 'urlencoded', 'raw', 'asserts']:
                try:
                    json.loads(attrs[item])
                except Exception as es:
                    raise serializers.ValidationError('字段{}不是json格式'.format(item))
        return attrs
