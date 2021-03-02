import uuid

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from interface.models import InterfaceJobModel
from testplan.models import ApiTestPlanModel, CaseTestPlanModel, CaseTestPlanTaskModel, ApiTestPlanTaskModel, \
    CaseJobModel
from utils.job_status_enum import CaseTestPlanTaskState, ApiTestPlanTaskState


class ApiTestPlanSerializer(serializers.ModelSerializer):
    running_task_number = serializers.SerializerMethodField()
    create_date_format = serializers.SerializerMethodField()

    class Meta:
        model = ApiTestPlanModel
        exclude = ['create_date', 'update_date']
        extra_kwargs = {'plan_id': {'required': False}, 'description': {'required': False}}
        read_only_fields = ["id", "plan_id", "create_date", "update_date", "create_user"]
        depth = 1
        validators = [
            UniqueTogetherValidator(
                queryset=ApiTestPlanModel.objects.all(),
                fields=('project_id', 'name'),
                message="已经存在相同名称的api测试计划"
            )
        ]

    def get_running_task_number(self, obj):
        return ApiTestPlanTaskModel.objects.filter(test_plan_uid=obj.plan_id).exclude(
            state=ApiTestPlanTaskState.FINISH).count()

    def get_create_date_format(self, obj):
        return obj.create_date.strftime("%Y-%m-%d %H:%M:%S")

    def create(self, validated_data):
        validated_data["create_user"] = self.context["request"].user
        validated_data["plan_id"] = uuid.uuid4()
        return ApiTestPlanModel.objects.create(**validated_data)


class CaseTestPlanSerializer(serializers.ModelSerializer):
    running_task_number = serializers.SerializerMethodField()
    create_date_format = serializers.SerializerMethodField()

    class Meta:
        model = CaseTestPlanModel
        exclude = ['update_date', 'create_date']
        read_only_fields = ["id", "plan_id", "create_date", "update_date"]
        extra_kwargs = {
            "create_user": {'required': False},
            'plan_id': {'required': False},
            'description': {'required': False}
        }
        depth = 1
        validators = [
            UniqueTogetherValidator(
                queryset=CaseTestPlanModel.objects.all(),
                fields=('project_id', 'name'),
                message="已经存在相同名称的case测试计划"
            )
        ]

    def get_running_task_number(self, obj):
        return CaseTestPlanTaskModel.objects.filter(test_plan_uid=obj.plan_id).exclude(
            state=CaseTestPlanTaskState.FINISH).count()

    def get_create_date_format(self, obj):
        return obj.create_date.strftime("%Y-%m-%d %H:%M:%S")

    def create(self, validated_data):
        validated_data["create_user"] = self.context["request"].user
        validated_data["plan_id"] = uuid.uuid4()
        return CaseTestPlanModel.objects.create(**validated_data)


class CaseTaskSerializer(serializers.ModelSerializer):
    create_date = serializers.SerializerMethodField()

    class Meta:
        model = CaseTestPlanTaskModel
        fields = "__all__"
        depth = 1

    def get_create_date(self, obj):
        return obj.create_date.strftime("%Y-%m-%d %H:%M:%S")


class CaseJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseJobModel
        exclude = ["log", ]
        depth = 1


class InterfaceTaskSerializer(serializers.ModelSerializer):
    create_date = serializers.SerializerMethodField()
    class Meta:
        model = ApiTestPlanTaskModel
        fields = "__all__"
        depth = 1

    def get_create_date(self, obj):
        return obj.create_date.strftime("%Y-%m-%d %H:%M:%S")


class InterfaceJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterfaceJobModel
        fields = "__all__"
        depth = 1
