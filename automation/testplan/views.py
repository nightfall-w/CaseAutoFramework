import json
import uuid

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from Logger import logger
from interface.models import InterfaceModel
from testplan.models import ApiTestPlanModel
from utils.job_status_enum import ApiTestPlanState


class TestPlanView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
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
            if not interfaceObj:
                return Response({"error": "接口名为{},地址为{}的api不存在".format(interfaceObj.name, interfaceObj.addr)})
        else:
            # 创建接口测试计划
            ApiTestPlanModel.objects.create(name=test_plan_name, plan_id=uuid.uuid4(), state=ApiTestPlanState.WAITING)
            pass
