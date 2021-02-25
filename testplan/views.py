import json
import uuid

import coreapi
import coreschema
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, pagination, permissions, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from automation.settings import logger
from celery_tasks.tasks import api_testplan_executor, case_test_task_executor, case_test_job_executor
from interface.models import InterfaceModel
from testplan.models import ApiTestPlanModel, ApiTestPlanTaskModel, CaseTestPlanModel, CaseTestPlanTaskModel, \
    CaseJobModel
from utils.job_status_enum import ApiTestPlanTaskState, CaseTestPlanTaskState
from .runner import CaseRunner
from .serializers import ApiTestPlanSerializer, CaseTestPlanSerializer, CaseTaskSerializer, InterfaceTaskSerializer, \
    CaseJobSerializer


class ApiTestPlanViewSet(viewsets.ModelViewSet):
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="projectId", required=False, location="query",
                      schema=coreschema.Integer(description='项目id'), )
    ])
    schema = Schema
    authentication_classes = (JSONWebTokenAuthentication,)
    pagination_class = pagination.LimitOffsetPagination
    serializer_class = ApiTestPlanSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return ApiTestPlanModel.objects.filter(project_id=self.request.GET.get('projectId'))

    def create(self, request, *args, **kwargs):
        """
        【创建Api测试计划】
        """
        try:
            projectId = request.data.get('project_id', None)
            interfaceIds = json.loads(request.data.get('interfaceIds', "[]"))
            test_plan_name = request.data.get("name", None)
            description = request.data.get('description', '')
        except Exception as es:
            logger.error(es)
            return Response({"error": "不符合格式的接口列表"})
        if not projectId:
            return Response({"error": "项目Id不能为空"})
        if not test_plan_name:
            return Response({"error": "测试计划名不能为空"})
        if not interfaceIds:
            return Response({"error": "接口id未提供"})
        for _id in interfaceIds:
            interfaceObj = InterfaceModel.objects.filter(id=_id).first()
            if not interfaceObj:
                return Response({"error": "接口id为{}的api不存在".format(_id)})
        plan_id = uuid.uuid4()
        ApiTestPlanModel.objects.create(name=test_plan_name, plan_id=plan_id, description=description,
                                        project_id=int(projectId),
                                        interfaceIds=json.dumps(interfaceIds),
                                        create_user=request.user, )
        return Response(
            {'success': True, "test_plan_name": test_plan_name, "interfaceIds": interfaceIds, "projectId": projectId})

    def list(self, request, *args, **kwargs):
        api_test_plans = self.get_queryset()
        page = self.paginate_queryset(api_test_plans)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


@method_decorator(csrf_exempt, name='get')
class ApiTask(APIView):
    """
    【case task接口】
    """
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="ApiTestPlanUid", required=True, location="query",
                      schema=coreschema.String(description='接口测试计划uid')),
        coreapi.Field(name="limit", required=True, location="query",
                      schema=coreschema.String(description='limit')),
        coreapi.Field(name="offset", required=True, location="query",
                      schema=coreschema.String(description='offset')),
    ])
    schema = Schema
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        receive_data = request.GET
        interface_test_plan_uid = receive_data.get('ApiTestPlanUid', None)
        if not interface_test_plan_uid:
            return Response({"error": "缺少必要参数caseTestPlanUid"}, status=status.HTTP_400_BAD_REQUEST)
        pg = LimitOffsetPagination()
        case_tasks = ApiTestPlanTaskModel.objects.filter(test_plan_uid=interface_test_plan_uid)
        page_api_tasks = pg.paginate_queryset(queryset=case_tasks, request=request, view=self)
        case_tasks_serializer = InterfaceTaskSerializer(page_api_tasks, many=True)
        return Response(case_tasks_serializer.data)


@method_decorator(csrf_exempt, name='post')
class TriggerApiPlan(APIView):
    """
    【触发API接口测试计划】
    """
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="projectId", required=True, location="form",
                      schema=coreschema.Integer(description='项目id')),
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
            plan_id=testplan_id, project_id=project_id).first()
        if not api_testplan:
            return Response({"error": "testplanId为：{}不存在".format(testplan_id)})
        interfaceIds = json.loads(api_testplan.interfaceIds)
        api_test_plan_task = ApiTestPlanTaskModel.objects.create(test_plan_uid=testplan_id,
                                                                 state=ApiTestPlanTaskState.WAITING, api_job_number=0,
                                                                 success_num=0, failed_num=0)
        # 使用celery task 处理testplan runner
        api_testplan_executor(testplan_id, interfaceIds, api_test_plan_task.id)
        return Response({"success": True})


class CaseTestPlanViewSet(viewsets.ModelViewSet):
    """
    【case测试计划】
    """
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="projectId", required=False, location="query",
                      schema=coreschema.Integer(description='项目id'), ),
        coreapi.Field(name="case_testplan_name", required=False, location="query",
                      schema=coreschema.String(description='case测试计划名称'), )
    ])
    schema = Schema
    authentication_classes = (JSONWebTokenAuthentication,)
    pagination_class = pagination.LimitOffsetPagination
    serializer_class = CaseTestPlanSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.request.method == "GET":
            return CaseTestPlanModel.objects.filter(project_id=self.request.GET.get('projectId'),
                                                    name__icontains=self.request.GET.get('case_testplan_name',
                                                                                         '')).order_by('-id')
        return CaseTestPlanModel.objects.all().order_by('id')

    def destroy(self, request, *args, **kwargs):
        instance = CaseTestPlanModel.objects.get(id=kwargs.get('pk'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(csrf_exempt, name='get')
class CaseTask(APIView):
    """
    【case task接口】
    """
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="caseTestPlanUid", required=True, location="query",
                      schema=coreschema.String(description='case测试计划uid')),
        coreapi.Field(name="limit", required=True, location="query",
                      schema=coreschema.Integer(description='limit')),
        coreapi.Field(name="offset", required=True, location="query",
                      schema=coreschema.Integer(description='offset')),
    ])
    schema = Schema
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        receive_data = request.GET
        case_test_plan_uid = receive_data.get('caseTestPlanUid', None)
        if not case_test_plan_uid:
            return Response({"error": "缺少必要参数caseTestPlanUid"}, status=status.HTTP_400_BAD_REQUEST)
        pg = LimitOffsetPagination()
        case_tasks = CaseTestPlanTaskModel.objects.filter(test_plan_uid=case_test_plan_uid).order_by('-id')
        page_case_tasks = pg.paginate_queryset(queryset=case_tasks, request=request, view=self)
        case_tasks_serializer = CaseTaskSerializer(page_case_tasks, many=True)
        return pg.get_paginated_response(case_tasks_serializer.data)


class CaseJobViewSet(viewsets.ModelViewSet):
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="task_id", required=False, location="query",
                      schema=coreschema.Integer(description='case task id'), ),
    ])
    schema = Schema
    authentication_classes = (JSONWebTokenAuthentication,)
    pagination_class = pagination.LimitOffsetPagination
    serializer_class = CaseJobSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return CaseJobModel.objects.filter(case_task_id=self.request.GET.get('task_id'))


@method_decorator(csrf_exempt, name='post')
class TriggerCasePlan(APIView):
    """
    【触发case测试计划】
    """
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="projectId", required=True, location="form",
                      schema=coreschema.Integer(description='项目id')),
        coreapi.Field(name="testPlanId", required=True, location="form",
                      schema=coreschema.String(description='接口测试计划uid')),
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
        case_test_plan = CaseTestPlanModel.objects.filter(project_id=project_id, plan_id=testplan_id).first()
        if not case_test_plan:
            return Response({"error": "testplan {} not find".format(testplan_id)}, status=status.HTTP_400_BAD_REQUEST)
        case_paths = case_test_plan.case_paths
        case_test_plan_task = CaseTestPlanTaskModel.objects.create(test_plan_uid=testplan_id,
                                                                   state=CaseTestPlanTaskState.WAITING,
                                                                   case_job_number=len(case_paths),
                                                                   finish_num=0)
        CaseRunner.distributor(case_test_plan_task)

        # 根据是否并行执行case选择不用的触发器
        if case_test_plan.parallel:
            '''并行执行'''
            case_jobs_id = CaseJobModel.objects.filter(case_task_id=case_test_plan_task.id).values_list('id', flat=True)
            for case_job_id in case_jobs_id:
                case_test_job_executor.delay(case_job_id, project_id, case_test_plan.plan_id, case_test_plan_task.id)
        else:
            '''串行执行'''
            case_test_task_executor.delay(case_test_plan_task.id)
        return Response({"success": True, "data": "测试用例计划已经成功触发"})
