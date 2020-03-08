from rest_framework import serializers

from case.models import CaseModel, CaseTypeModel


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
