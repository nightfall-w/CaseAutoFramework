from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from testplan.models import ApiTestPlanModel, CaseTestPlanModel, CaseTestPlanTaskModel, ApiTestPlanTaskModel


class ApiTestPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiTestPlanModel
        exclude = ['create_user', 'create_data', 'update_data']
        extra_kwargs = {'plan_id': {'required': False}, 'description': {'required': False}}
        depth = 1
        validators = [
            UniqueTogetherValidator(
                queryset=ApiTestPlanModel.objects.all(),
                fields=('project_id', 'name'),
                message="已经存在相同名称的api测试计划"
            )
        ]


class CaseTestPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseTestPlanModel
        exclude = ['create_user', 'create_data', 'update_data']
        extra_kwargs = {'plan_id': {'required': False}, 'description': {'required': False}}
        depth = 1
        validators = [
            UniqueTogetherValidator(
                queryset=CaseTestPlanModel.objects.all(),
                fields=('project_id', 'name'),
                message="已经存在相同名称的case测试计划"
            )
        ]

    def create(self, validated_data):
        validated_data["create_user"] = self.context["request"].user
        return CaseTestPlanModel.objects.create(**validated_data)


class CaseTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseTestPlanTaskModel
        fields = "__all__"
        depth = 1


class InterfaceTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiTestPlanTaskModel
        fields = "__all__"
        depth = 1
