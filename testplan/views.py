import json
import uuid

import coreapi
import coreschema
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, pagination, permissions, status
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from automation.settings import logger
from celery_tasks.tasks import ApiTestPlan
from interface.models import InterfaceModel
from testplan.models import ApiTestPlanModel, ApiTestPlanTaskModel, CaseTestPlanModel, CaseTestPlanTaskModel, \
    CaseJobModel
from utils.job_status_enum import ApiTestPlanTaskState, CaseTestPlanTaskState
from .runner import CaseRunner
from .serializers import ApiTestPlanSerializer, CaseTestPlanSerializer


class ApiTestPlanViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    pagination_class = pagination.LimitOffsetPagination
    serializer_class = ApiTestPlanSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return ApiTestPlanModel.objects.all()

    def create(self, request, *args, **kwargs):
        """
        【创建Api测试计划】
        """
        try:
            projectId = request.data.get('project', None)
            interfaceIds = json.loads(request.data.get('interfaceIds', "[]"))
            test_plan_name = request.data.get("name", None)
        except Exception as es:
            logger.error(es)
            return Response({"error": "不符合格式的接口列表"})
        if not projectId:
            return Response({"error": "项目Id不能为空"})
        if not test_plan_name:
            return Response({"error": "测试计划名不能为空"})
        if not interfaceIds:
            return Response({"error": "接口id未提供"})
        for id in interfaceIds:
            interfaceObj = InterfaceModel.objects.filter(id=id).first()
            if not interfaceObj:
                return Response({"error": "接口id为{}的api不存在".format(id)})
        plan_id = uuid.uuid4()
        ApiTestPlanModel.objects.create(name=test_plan_name, plan_id=plan_id,
                                        project=int(projectId),
                                        interfaceIds=json.dumps(interfaceIds),
                                        create_user=request.user, )
        return Response(
            {'success': True, "test_plan_name": test_plan_name, "interfaceIds": interfaceIds, "projectId": projectId})

    def list(self, request, *args, **kwargs):
        api_test_plans = self.get_queryset()
        page = self.paginate_queryset(api_test_plans)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


@method_decorator(csrf_exempt, name='post')
class TriggerApiPlan(APIView):
    """
    【触发API接口测试计划】
    """
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="projectId", required=True, location="form",
                      schema=coreschema.String(description='项目id')),
        coreapi.Field(name="testPlanId", required=True, location="form",
                      schema=coreschema.String(description='接口测试计划uid'))
    ])
    schema = Schema
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        receive_data = request.data
        testplan_id = receive_data.get('testPlanId', None)
        project_id = receive_data.get('projectId', None)
        if not all([testplan_id, project_id]):
            return Response({"error": "缺少必要的参数"}, status=status.HTTP_400_BAD_REQUEST)
        api_testplan = ApiTestPlanModel.objects.filter(
            plan_id=testplan_id, project=project_id).first()
        if not api_testplan:
            return Response({"error": "testplanId为：{}不存在".format(testplan_id)})
        interfaceIds = json.loads(api_testplan.interfaceIds)
        api_test_plan_task = ApiTestPlanTaskModel.objects.create(test_plan_uid=testplan_id,
                                                                 state=ApiTestPlanTaskState.WAITING, api_job_number=0,
                                                                 success_num=0, failed_num=0)
        # 使用celery task 处理testplan runner
        ApiTestPlan.delay(testplan_id, interfaceIds, api_test_plan_task.id)
        return Response({"success": True})


class CaseTestPlanViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    pagination_class = pagination.LimitOffsetPagination
    serializer_class = CaseTestPlanSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return CaseTestPlanModel.objects.all()


@method_decorator(csrf_exempt, name='post')
class TriggerCasePlan(APIView):
    """
    【触发case测试计划】
    """
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="projectId", required=True, location="form",
                      schema=coreschema.String(description='项目id')),
        coreapi.Field(name="testPlanId", required=True, location="form",
                      schema=coreschema.String(description='接口测试计划uid'))
    ])
    schema = Schema
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        receive_data = request.data
        testplan_id = receive_data.get('testPlanId', None)
        project_id = receive_data.get('projectId', None)
        if not all([testplan_id, project_id]):
            return Response({"error": "缺少必要的参数"}, status=status.HTTP_400_BAD_REQUEST)
        case_test_plan = CaseTestPlanModel.objects.filter(project=project_id, plan_id=testplan_id).first()
        if not case_test_plan:
            return Response({"error": "testplan {} not find".format(testplan_id)}, status=status.HTTP_400_BAD_REQUEST)
        case_paths = json.loads(case_test_plan.case_paths)
        case_test_plan_task = CaseTestPlanTaskModel.objects.create(test_plan_uid=testplan_id,
                                                                   state=CaseTestPlanTaskState.WAITING,
                                                                   case_job_number=len(case_paths),
                                                                   finish_num=0)
        CaseRunner.distributor(case_test_plan_task)
        case_jobs = CaseJobModel.objects.filter(case_task_id=case_test_plan_task.id)
        for case_job in case_jobs:
            # TODO 完成case job调度逻辑
            pass
        return Response({"success": True})


@method_decorator(csrf_exempt, name='get')
class test_return_file(APIView):
    def get(self, request):
        with open('case_house/feature/wcs_dingTalk/dingTalk.py', 'r', encoding='utf-8') as f:
            data = f.read()
            return HttpResponse(data, content_type='text/plain')
