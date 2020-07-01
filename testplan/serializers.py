from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from testplan.models import ApiTestPlanModel, CaseTestPlanModel


class ApiTestPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiTestPlanModel
        exclude = ['create_data', 'update_data']
        extra_kwargs = {'plan_id': {'required': False}}
        depth = 1
        validators = [
            UniqueTogetherValidator(
                queryset=ApiTestPlanModel.objects.all(),
                fields=('project', 'name'),
                message="已经存在相同名称的api测试计划"
            )
        ]


class CaseTestPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseTestPlanModel
        exclude = ['create_data', 'update_data']
        extra_kwargs = {'plan_id': {'required': False}}
        depth = 1
        validators = [
            UniqueTogetherValidator(
                queryset=CaseTestPlanModel.objects.all(),
                fields=('project', 'name'),
                message="已经存在相同名称的case测试计划"
            )
        ]
