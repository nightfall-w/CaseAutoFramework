import os
import re
from threading import Thread

import coreapi
import coreschema
import git
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from rest_framework import permissions, pagination, viewsets, status
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from automation.settings import logger
from case.models import CaseModel, CaseTypeModel
from case.serializers import CaseSerializer, CaseTypeSerializer
from standard.config import ConfigParser
from standard.enum import CaseStatus
from standard.enum import ResponseCode
from .models import GitCase


class PathTree(object):
    def __init__(self, branch):
        self.index = 0
        self.branch = branch

    def path_tree(self, path):
        tree = dict()
        self.index += 1
        if os.path.isdir(path):
            tree["id"] = self.index
            tree["label"] = os.path.basename(path)
            tree['children'] = [self.path_tree(os.path.join(path, x)) for x in os.listdir(path)]
        elif not os.path.isdir(path):
            tree["id"] = self.index
            tree["label"] = os.path.basename(path)
            tree['filepath'] = path
        return tree


class GitTool(APIView):
    """
    通过git拉取case代码
    """
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="branch", required=False, location="form", schema=coreschema.String(description='case所在分支')),
    ])
    schema = Schema
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)  # 登陆成功的token

    def git_pull(self, branch, case_address, branch_path):
        """
        拉取代码实操
        """
        author = ''
        try:
            logger.info('开始从远端拉取case')
            case_obj = GitCase.objects.filter(branch_name=branch).first()
            if case_obj:
                case_obj.status = CaseStatus.PULLING.value
                case_obj.save()
            else:
                GitCase.objects.create(lester_user=author, branch_name=branch, status=CaseStatus.PULLING.value)
            if not os.path.exists(os.path.join(branch_path, '.git')):
                git.Repo.clone_from(case_address, branch_path)
            else:
                repo = git.Repo(branch_path)
                repo.git.pull()
        except git.GitCommandError as es:
            logger.warning(es)
        try:
            logger.info('即将切换分支到: {}'.format(branch))
            repo = git.Repo(branch_path)
            logger.info('当前分支: {}'.format(repo.active_branch))
            repo.git.checkout(branch)
            info = repo.git.show()
            author = re.search(r'Author: (.*?) <', info).group(1)
            logger.info('切换分支到: {} 成功'.format(branch))
        except Exception as es:
            logger.error('切换分支到：{} 失败'.format(branch))
            logger.error(es)
            case_obj = GitCase.objects.get(branch_name=branch)
            case_obj.status = CaseStatus.DONE.value
            case_obj.save()
            return False
        case_obj = GitCase.objects.get(branch_name=branch)
        case_obj.lester_user = author
        case_obj.status = CaseStatus.DONE.value
        case_obj.save()

    def post(self, request):
        branch = request.data.get('branch', 'master')
        case_house = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'case_house')
        branch_path = os.path.join(case_house, branch)
        if not os.path.exists(branch_path):
            # 分支路径已经存在
            os.makedirs(branch_path)
        case_address = ConfigParser.get_config('git', 'address')
        t = Thread(target=self.git_pull, args=(branch, case_address, branch_path))
        t.start()
        return JsonResponse(ResponseCode.HANDLE_SUCCESS.value)


class CaseTree(APIView):
    """
    case管理器
    """
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="branch", required=False, location="query",
                      schema=coreschema.String(description='case所在分支')),
        coreapi.Field(name="label", required=False, location="query", schema=coreschema.String(description='case名称')),
        coreapi.Field(name="path", required=False, location="query", schema=coreschema.String(description='case路径')),
    ])
    schema = Schema
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        【获取case信息】
        """
        case_branch = request.query_params.dict().get('branch', 'master')
        case_name = request.query_params.dict().get('label')
        case_path = request.query_params.dict().get('path')
        if case_path:
            # 有指定文件 表示要获取case详情
            try:
                with open(os.path.join(settings.BASE_DIR, 'case_house', case_branch, case_path), 'r',
                          encoding='utf-8') as f:
                    case_data = f.read()
                    return HttpResponse(case_data, content_type='text/plain')
            except FileNotFoundError as es:
                logger.error(es)
                return JsonResponse({"error": "case:{}不存在".format(case_name)})
        else:
            # 没有指定到case路径 则返回case目录树
            case_tree = PathTree(case_branch).path_tree(os.path.join(settings.BASE_DIR, 'case_house', case_branch))
            return JsonResponse({"branch": case_branch, "case_tree": [case_tree]})


class CaseViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CaseSerializer
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        return CaseModel.objects.all()

    def list(self, request, *args, **kwargs):
        cases = self.get_queryset()
        page = self.paginate_queryset(cases)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        case_type_id = request.data.get('case_type_id')
        case_type_obj = CaseTypeModel.objects.filter(id=case_type_id).first()
        if not case_type_obj:
            return Response({'respError': 'case类型不存在'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        case_data = request.data
        case_data.pop('case_type_id')
        case_data['case_type'] = case_type_obj
        serializer = self.get_serializer(data=case_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CaseTypeViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CaseTypeSerializer
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        return CaseTypeModel.objects.all()

    def list(self, request, *args, **kwargs):
        case_types = self.get_queryset()
        page = self.paginate_queryset(case_types)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
