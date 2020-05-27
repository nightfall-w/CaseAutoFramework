import json
import uuid

import coreapi
import coreschema
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView

from Logger import logger
from interface.models import InterfaceModel, InterfaceJobModel
from testplan.models import ApiTestPlanModel
from utils.job_status_enum import ApiTestPlanState, ApiJobState
from .runner import ApiRunner


@method_decorator(csrf_exempt, name='post')
class ApiTestPlanView(APIView):
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="interfaceIds", required=True, location="form",
                      schema=coreschema.String(description='接口id集合')),
        coreapi.Field(name="name", required=True, location="form", schema=coreschema.String(description='计划名'))
    ])
    schema = Schema
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """
        【创建Api测试计划】
        """
        try:
            interfaceIds = json.loads(request.data.get('interfaceIds', "[]"))
            test_plan_name = request.data.get("name", None)
        except Exception as es:
            logger.error(es)
            return Response({"error": "不符合格式的接口列表"})
        if not test_plan_name:
            return Response({"error": "测试计划名不能为空"})
        if not interfaceIds:
            return Response({"error": "接口id未提供"})
        for id in interfaceIds:
            interfaceObj = InterfaceModel.objects.filter(id=id).first()
            print(interfaceObj.get_request_mode_display())
            if not interfaceObj:
                return Response({"error": "接口名为{},地址为{}的api不存在".format(interfaceObj.name, interfaceObj.addr)})
        else:
            # 创建接口测试计划
            plan_id = uuid.uuid4()
            api_testplan_obj = ApiTestPlanModel.objects.create(name=test_plan_name, plan_id=plan_id,
                                                               state=ApiTestPlanState.WAITING,
                                                               result="0/{}".format(len(interfaceIds)))
            if not api_testplan_obj:
                return Response({"error": "创建api测试计划失败"})
            for interfaceId in interfaceIds:
                InterfaceJobModel.objects.create(interface_id=interfaceId, test_plan_id=plan_id,
                                                 state=ApiJobState.WAITING)
            ApiRunner(test_plan_id=plan_id).distributor()
            return Response({"trigger_success": True})


@method_decorator(csrf_exempt, name='get')
class test_return_file(APIView):
    def get(self, request):
        with open('case_house/feature/wcs_dingTalk/dingTalk.py', 'r', encoding='utf-8') as f:
            data = f.read()
            return HttpResponse(data, content_type='text/plain')
