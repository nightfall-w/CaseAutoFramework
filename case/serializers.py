from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from case.models import CaseModel, CaseTypeModel, CodeBaseModel


class CaseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseTypeModel
        fields = '__all__'
        depth = 1


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseModel
        exclude = ['create_time']
        depth = 2

    def create(self, validated_data):
        return CaseModel.objects.create(**self.context['request'].data)


class CodeBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeBaseModel
        fields = '__all__'
        depth = 1
        validators = [
            UniqueTogetherValidator(
                queryset=CodeBaseModel.objects.all(),
                fields=('address',),
                message="已经存在相同地址的代码仓库"
            )
        ]
