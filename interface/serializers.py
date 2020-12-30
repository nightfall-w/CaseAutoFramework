import json

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from automation.settings import logger
from interface.models import InterfaceModel, InterfaceHistory


class InterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterfaceModel
        fields = '__all__'
        depth = 1
        extra_kwargs = {
            "protocol": {'required': False},
            "headers": {'required': False},
            "formData": {'required': False},
            "urlencoded": {'required': False},
            "raw": {'required': False},
            "asserts": {'required': False},
            "parameters": {'required': False},
            "extract": {'required': False}
        }
        validators = [
            UniqueTogetherValidator(
                queryset=InterfaceModel.objects.all(),
                fields=('project', 'name', 'addr'),
                message="已经存在相同名称和url的接口"
            )
        ]

    def create(self, validated_data):
        interface = InterfaceModel.objects.create(**validated_data)
        if interface.addr.lower().startswith('https://'):
            interface.protocol = "HTTPS"
        else:
            interface.protocol = "HTTP"
        interface.save()
        return interface

    def validate(self, attrs):
        for item in attrs:
            if item in ['headers', 'formData', 'urlencoded', 'asserts', 'parameters']:
                if not any([isinstance(attrs[item], dict), isinstance(attrs[item], list)]):
                    raise serializers.ValidationError('字段{}不是json格式'.format(item))
        return attrs


class InterfaceTestSerializer(serializers.ModelSerializer):
    """
     此处的`fields`字段是用来替换上面Serializer内部Meta类中指定的`fields`属性值
    """

    def __init__(self, *args, **kwargs):
        # 在super执行之前
        # 将传递的`fields`中的字段从kwargs取出并剔除，避免其传递给基类ModelSerializer
        # 注意此处`fields`中在默认`self.fields`属性中不存在的字段将无法被序列化 也就是`fields`中的字段应该
        # 是`self.fields`的子集
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            # 从默认`self.fields`属性中剔除非`fields`中指定的字段
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = InterfaceHistory
        # exclude = ["user"]
        fields = '__all__'
        depth = 1
        extra_kwargs = {
            "headers": {'required': False},
            "formData": {'required': False},
            "urlencoded": {'required': False},
            "raw": {'required': False}
        }
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
