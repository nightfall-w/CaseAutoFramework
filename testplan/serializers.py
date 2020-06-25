from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from testplan.models import ApiTestPlanModel


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
                message="已经存在相同名称的测试计划"
            )
        ]
