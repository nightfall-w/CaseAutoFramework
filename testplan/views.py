import json
from datetime import datetime

import coreapi
import coreschema
import pytz
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from rest_framework import viewsets, pagination, permissions, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from automation.settings import logger, TIME_ZONE
from celery_tasks.tasks import api_testplan_executor, case_test_task_executor, case_test_job_executor
from interface.models import InterfaceJobModel
from testplan.models import ApiTestPlanModel, ApiTestPlanTaskModel, CaseTestPlanModel, CaseTestPlanTaskModel, \
    CaseJobModel
from utils.job_status_enum import ApiTestPlanTaskState, CaseTestPlanTaskState
from utils.snow import IdWorker
from .runner import CaseRunner
from .serializers import ApiTestPlanSerializer, CaseTestPlanSerializer, CaseTaskSerializer, InterfaceTaskSerializer, \
    CaseJobSerializer, InterfaceJobSerializer


class ApiTestPlanViewSet(viewsets.ModelViewSet):
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="projectId", required=True, location="query",
                      schema=coreschema.Integer(description='项目id'), ),
        coreapi.Field(name="api_testplan_name", required=False, location="query",
                      schema=coreschema.String(description='api测试计划名称'), )
    ])
    schema = Schema
    authentication_classes = (JSONWebTokenAuthentication,)
    pagination_class = pagination.LimitOffsetPagination
    serializer_class = ApiTestPlanSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.request.method == "GET":
            return ApiTestPlanModel.objects.filter(project_id=self.request.GET.get('projectId'),
                                                   name__icontains=self.request.GET.get('api_testplan_name',
                                                                                        '')).order_by('-id')
        return ApiTestPlanModel.objects.all().order_by('id')

    def list(self, request, *args, **kwargs):
        api_test_plans = self.get_queryset()
        page = self.paginate_queryset(api_test_plans)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = ApiTestPlanModel.objects.get(id=kwargs.get('pk'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        api_tasks = ApiTestPlanTaskModel.objects.filter(test_plan_uid=interface_test_plan_uid).order_by('-id')
        page_api_tasks = pg.paginate_queryset(queryset=api_tasks, request=request, view=self)
        case_tasks_serializer = InterfaceTaskSerializer(page_api_tasks, many=True)
        return pg.get_paginated_response(case_tasks_serializer.data)


class ApiJobViewSet(viewsets.ModelViewSet):
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="task_id", required=False, location="query",
                      schema=coreschema.Integer(description='api task id'), ),
    ])
    schema = Schema
    authentication_classes = (JSONWebTokenAuthentication,)
    pagination_class = pagination.LimitOffsetPagination
    serializer_class = InterfaceJobSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return InterfaceJobModel.objects.filter(api_test_plan_task_id=self.request.GET.get('task_id'))


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
        api_task_uid = "APITASK_" + str(IdWorker(0, 0).get_id())
        api_test_plan_task = ApiTestPlanTaskModel.objects.create(test_plan_uid=testplan_id, api_task_uid=api_task_uid,
                                                                 state=ApiTestPlanTaskState.WAITING, api_job_number=0,
                                                                 success_num=0, failed_num=0)
        # 使用celery task 处理testplan runner
        api_testplan_executor.delay(testplan_id, interfaceIds, api_test_plan_task.id)
        return Response({"success": True})


class CaseTestPlanViewSet(viewsets.ModelViewSet):
    """
    【case测试计划】
    """
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="projectId", required=True, location="query",
                      schema=coreschema.Integer(description='项目id'), ),
        coreapi.Field(name="case_testplan_name", required=True, location="query",
                      schema=coreschema.String(description='case测试计划名称'), ),
        coreapi.Field(name="timer_enable", required=True, location="form",
                      schema=coreschema.String(description='是否开始定时器')),
        coreapi.Field(name="crontab", required=True, location="form",
                      schema=coreschema.String(description='定时任务编排参数')),
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if request.data.get('timer_enable') and request.data.get('crontab'):
            crontab = request.data.get('crontab').replace('?', '*')
            crontab = crontab.split(' ')
            if len(crontab) == 7:
                # 包含秒 包含年
                crontab = crontab[1:-1]
            elif len(crontab) == 6:
                # 包含秒 不包含年
                crontab = crontab[1:]
            crontab_kwargs = {
                'minute': crontab[0],
                'hour': crontab[1],
                'day_of_week': crontab[4],
                'day_of_month': crontab[2],
                'month_of_year': crontab[3]
            }
            with transaction.atomic():
                save_id = transaction.savepoint()
                try:
                    schedule, _ = CrontabSchedule.objects.get_or_create(
                        minute=crontab_kwargs.get('minute', '*'),
                        hour=crontab_kwargs.get('hour', '*'),
                        day_of_week=crontab_kwargs.get('day_of_week', '*'),
                        day_of_month=crontab_kwargs.get('day_of_month', '*'),
                        month_of_year=crontab_kwargs.get('month_of_year', '*'),
                        timezone=pytz.timezone(TIME_ZONE))
                    dt = datetime.now().strftime('%Y%m%d%H%M%S')
                    _periodic_task = PeriodicTask.objects.create(
                        name=dt + '-' + 'case测试计划定时任务' + '-' + serializer.data.get('plan_id'),
                        task='case_test_task_timing_executor',
                        args=json.dumps([serializer.data.get('project_id'),
                                         serializer.data.get('plan_id')]),
                        enabled=True,
                        crontab=schedule
                    )
                    logger.info("timing case testplan:{} create success!".format(serializer.data.get('plan_id')))
                except Exception as e:
                    transaction.savepoint_rollback(save_id)
                    logger.error(
                        'timing case testplan:{} create failed!，error：{}'.format(serializer.data.get('plan_id'), e))
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        if not request.data.get('timer_enable'):
            periodic_tasks = PeriodicTask.objects.filter(
                name__icontains='case测试计划定时任务' + '-' + serializer.data.get('plan_id'),
            )
            if len(periodic_tasks) >= 0:
                for task in periodic_tasks:
                    task.enabled = False
                    task.save()
        else:
            if request.data.get('crontab'):
                crontab = request.data.get('crontab').replace('?', '*')
                crontab = crontab.split(' ')
                if len(crontab) == 7:
                    # 包含秒 包含年
                    crontab = crontab[1:-1]
                elif len(crontab) == 6:
                    # 包含秒 不包含年
                    crontab = crontab[1:]
                crontab_kwargs = {
                    'minute': crontab[0],
                    'hour': crontab[1],
                    'day_of_week': crontab[4],
                    'day_of_month': crontab[2],
                    'month_of_year': crontab[3]
                }
                schedule, _ = CrontabSchedule.objects.get_or_create(
                    minute=crontab_kwargs.get('minute', '*'),
                    hour=crontab_kwargs.get('hour', '*'),
                    day_of_week=crontab_kwargs.get('day_of_week', '*'),
                    day_of_month=crontab_kwargs.get('day_of_month', '*'),
                    month_of_year=crontab_kwargs.get('month_of_year', '*'),
                    timezone=pytz.timezone(TIME_ZONE))
            else:
                raise ValueError("参数crontab 不能为空")
            periodic_task = PeriodicTask.objects.filter(
                name__icontains='case测试计划定时任务' + '-' + serializer.data.get('plan_id'),
            )
            if not periodic_task:
                dt = datetime.now().strftime('%Y%m%d%H%M%S')
                _periodic_task = PeriodicTask.objects.create(
                    name=dt + '-' + 'case测试计划定时任务' + '-' + serializer.data.get('plan_id'),
                    task='case_test_task_timing_executor',
                    args=json.dumps([serializer.data.get('project_id'),
                                     serializer.data.get('plan_id')]),
                    enabled=True,
                    crontab=schedule
                )
            else:
                periodic_task.update(enabled=True, crontab=schedule)
        return Response(serializer.data)

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
        task_id = self.request.GET.get('task_id')
        if task_id:
            return CaseJobModel.objects.filter(case_task_id=task_id)
        else:
            return CaseJobModel.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = serializer.data
        if instance.log:
            log = instance.log.split('\n')[-200:]
            response_data['log'] = "\n".join(log)
        else:
            response_data['log'] = ""
        return Response(response_data)


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
            return Response({"error": "testplan {} not found".format(testplan_id)}, status=status.HTTP_404_NOT_FOUND)
        case_paths = case_test_plan.case_paths
        case_task_uid = "CASETASK_" + str(IdWorker(0, 0).get_id())
        case_test_plan_task = CaseTestPlanTaskModel.objects.create(test_plan_uid=testplan_id,
                                                                   case_task_uid=case_task_uid,
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
