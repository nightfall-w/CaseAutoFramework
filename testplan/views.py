import json
import uuid

import coreapi
import coreschema
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView

from Logger import logger
from celery_tasks.tasks import ApiTestPlan
from interface.models import InterfaceModel
from testplan.models import ApiTestPlanModel
from utils.job_status_enum import ApiTestPlanState
from .runner import data_drive


@method_decorator(csrf_exempt, name='post')
class ApiTestPlanView(APIView):
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="projectId", required=True, location="form",
                      schema=coreschema.String(description='项目id')),
        coreapi.Field(name="interfaceIds", required=True, location="form",
                      schema=coreschema.String(description='接口id集合')),
        coreapi.Field(name="testPlanName", required=True, location="form", schema=coreschema.String(description='计划名'))
    ])
    schema = Schema
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """
        【创建Api测试计划】
        """
        try:
            projectId = json.loads(request.data.get('projectId', None))
            interfaceIds = json.loads(request.data.get('interfaceIds', "[]"))
            test_plan_name = request.data.get("testPlanName", None)
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
                                        state=ApiTestPlanState.WAITING, create_user=request.user,
                                        result="0/0")
        return Response(
            {'success': True, "test_plan_name": test_plan_name, "interfaceIds": interfaceIds, "projectId": projectId})


@method_decorator(csrf_exempt, name='post')
class TriggerPlan(APIView):
    """
    【触发接口测试计划】
    """
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="projectId", required=True, location="form",
                      schema=coreschema.String(description='项目id')),
        coreapi.Field(name="testPlanId", required=True, location="form",
                      schema=coreschema.String(description='接口测试计划uid'))
    ])
    schema = Schema
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        receive_data = request.data
        testplan_id = receive_data.get('testPlanId', None)
        project_id = receive_data.get('projectId', None)
        if not all([testplan_id, project_id]):
            return Response({"error": "缺少必要的参数"}, status=status.HTTP_400_BAD_REQUEST)
        api_testplan = ApiTestPlanModel.objects.filter(plan_id=testplan_id, project=project_id).first()
        if not api_testplan:
            return Response({"error": "testplanId为：{}不存在".format(testplan_id)})
        if api_testplan.state == ApiTestPlanState.RUNNING:
            return Response({"error": "testplanId为：{}已经在执行".format(testplan_id)})
        interfaceIds = json.loads(api_testplan.interfaceIds)
        api_testplan.state = ApiTestPlanState.RUNNING
        api_testplan.result = "0/0"
        api_testplan.save()
        ApiTestPlan.delay(testplan_id, interfaceIds)  # 使用celery task 处理testplan runner
        return Response({"success": True})


@method_decorator(csrf_exempt, name='get')
class test_return_file(APIView):
    def get(self, request):
        with open('case_house/feature/wcs_dingTalk/dingTalk.py', 'r', encoding='utf-8') as f:
            data = f.read()
            return HttpResponse(data, content_type='text/plain')
