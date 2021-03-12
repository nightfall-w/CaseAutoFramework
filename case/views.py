import json
import os
import subprocess

import coreapi
import coreschema
from django.conf import settings
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from gitlab.exceptions import GitlabAuthenticationError
from requests.exceptions import ConnectTimeout
from requests.exceptions import MissingSchema
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from automation.settings import AES_IV, AES_KEY
from automation.settings import logger
from case.models import GitlabModel, GitCaseModel
from case.serializers import GitlabAuthenticationSerializer
from celery_tasks.tasks import branch_pull
from standard.config import ConfigParser
from utils.encryption import PrpCrypt, decrypt_token
from utils.gitlab_tool import GitlabAPI
from utils.job_status_enum import BranchState


class PathTree(object):
    def __init__(self, branch):
        self.index = 0
        self.branch = branch
        self.temp = len(os.path.join(settings.BASE_DIR, 'case_house'))

    def path_tree(self, path):
        tree = dict()
        self.index += 1
        if os.path.isdir(path):
            tree["id"] = self.index
            tree["label"] = os.path.basename(path)
            tree['children'] = [self.path_tree(os.path.join(path, x)) for x in os.listdir(path)]
        elif not os.path.isdir(path) and os.path.splitext(path)[1] in json.loads(
                ConfigParser.get_config('case', 'suffixs')):
            tree["id"] = self.index
            tree["label"] = os.path.basename(path)
            tree['filepath'] = path[self.temp + 1:]
        return tree

    def value_is_not_empty(self, value):
        return value not in ['', None, {}, []]

    def empty_json_data(self, data):
        if isinstance(data, dict):
            temp_data = dict()
            for key, value in data.items():
                if self.value_is_not_empty(value):
                    new_value = self.empty_json_data(value)
                    if self.value_is_not_empty(new_value):
                        temp_data[key] = new_value
            return None if not temp_data else temp_data

        elif isinstance(data, list):
            temp_data = list()
            for value in data:
                if self.value_is_not_empty(value):
                    new_value = self.empty_json_data(value)
                    if self.value_is_not_empty(new_value):
                        temp_data.append(new_value)
            return None if not temp_data else temp_data

        elif self.value_is_not_empty(data):
            return data


# class GitTool(APIView):
#     """
#     通过git拉取case代码
#     """
#     Schema = AutoSchema(manual_fields=[
#         coreapi.Field(name="branch", required=False, location="form", schema=coreschema.String(description='case所在分支')),
#     ])
#     schema = Schema
#     authentication_classes = (JSONWebTokenAuthentication,)
#     permission_classes = (permissions.IsAuthenticated,)  # 登陆成功的token
#
#     def git_pull(self, branch, case_address, branch_path):
#         """
#         拉取代码实操
#         """
#         try:
#             logger.info('开始从远端拉取case')
#             case_obj = GitCase.objects.filter(branch_name=branch).first()
#             if case_obj:
#                 case_obj.status = CaseStatus.PULLING.value
#                 case_obj.save()
#             else:
#                 GitCase.objects.create(branch_name=branch, status=CaseStatus.PULLING.value)
#             if not os.path.exists(os.path.join(branch_path, '.git')):
#                 git.Repo.clone_from(case_address, branch_path)
#             else:
#                 repo = git.Repo(branch_path)
#                 repo.git.pull()
#         except git.GitCommandError as es:
#             logger.warning(es)
#         try:
#             logger.info('即将切换分支到: {}'.format(branch))
#             repo = git.Repo(branch_path)
#             logger.info('当前分支: {}'.format(repo.active_branch))
#             repo.git.fetch()
#             repo.git.checkout(branch)
#             info = repo.git.show()
#             author = re.search(r'Author: (.*?) <', info).group(1)
#             logger.info('切换分支到: {} 成功'.format(branch))
#         except Exception as es:
#             logger.error('切换分支到：{} 失败'.format(branch))
#             logger.error(es)
#             case_obj = GitCase.objects.get(branch_name=branch)
#             case_obj.status = CaseStatus.FAILED.value
#             case_obj.save()
#             return False
#         case_obj = GitCase.objects.get(branch_name=branch)
#         case_obj.lester_user = author
#         case_obj.status = CaseStatus.DONE.value
#         case_obj.save()
#
#     def post(self, request):
#         branch = request.data.get('branch', 'master')
#         case_house = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'case_house')
#         branch_path = os.path.join(case_house, branch)
#         if not os.path.exists(branch_path):
#             # 分支路径已经存在
#             os.makedirs(branch_path)
#         case_address = ConfigParser.get_config('git', 'address')
#         t = Thread(target=self.git_pull, args=(branch, case_address, branch_path))
#         t.start()
#         return JsonResponse(ResponseCode.HANDLE_SUCCESS.value)


class GitLabAddToken(viewsets.ModelViewSet):
    """
    通过git拉取case代码
    """
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="gitlab_url", required=False, location="form", schema=coreschema.String(description='仓库地址')),
        coreapi.Field(name="private_token", required=False, location="form",
                      schema=coreschema.String(description='private_token')),
    ])
    schema = Schema
    serializer_class = GitlabAuthenticationSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)  # 登陆成功的token

    def create(self, request, *args, **kwargs):
        if not all([request.data.get('gitlab_url'), request.data.get('private_token')]):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'success': False, 'err_msg': '缺少必填参数'})
        try:
            if request.data.get('gitlab_url')[-1] == '/':  # 去除url结尾的 '/' 符号　统一规范
                request.data['gitlab_url'] = request.data.get('gitlab_url')[0:-1]
            instance = GitlabAPI(gitlab_url=request.data.get('gitlab_url'),
                                 private_token=request.data.get('private_token'))
            projects = instance.gl.projects.list(all=True, as_list=True)
            project_list = {project.name: project.id for project in projects}
            GitlabModel.objects.create(**request.data)
            prpcrypt_instance = PrpCrypt(AES_KEY, AES_IV)  # AES加密实例
            encrypt_token = prpcrypt_instance.encrypt(request.data.get('private_token'))  # 加密private_token
            return Response({'success': True, 'result': project_list, 'token': encrypt_token})
        except GitlabAuthenticationError:
            # 验证gitlab地址以及private token无效处理
            gitlab_infos = GitlabModel.objects.filter(gitlab_url=request.data.get('gitlab_url'),
                                                      private_token=request.data.get('private_token'))
            if gitlab_infos:
                gitlab_infos.delete()
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"success": False, "err_msg": "无效的git地址或者token"})
        except IntegrityError as e:
            # 已经被数据库记录过的gitlab url, private token, 直接返回数据库创建过的数据，　不再重新创建
            prpcrypt_instance = PrpCrypt(AES_KEY, AES_IV)
            encrypt_token = prpcrypt_instance.encrypt(request.data.get('private_token'))
            return Response({'success': True, 'result': project_list, 'token': encrypt_token})
        except ConnectTimeout:
            return Response(status=status.HTTP_408_REQUEST_TIMEOUT,
                            data={"success": False, "err_msg": "连接gitlab地址%s超时" % request.data.get('gitlab_url')})
        except MissingSchema as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"success": False,
                                                                      "err_msg": "Invalid URL '{}': No schema supplied. Perhaps you meant http://{}?".format(
                                                                          request.data.get('gitlab_url'),
                                                                          request.data.get('gitlab_url'))})


class GitlabBranch(APIView):
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="project_id", required=True, location="form",
                      schema=coreschema.Integer(description='gitlab项目id')),
        coreapi.Field(name="token", required=False, location="form", schema=coreschema.String(description='加密后的token')),
        coreapi.Field(name="branch", required=False, location="form", schema=coreschema.String(description='分支名')),
    ])
    schema = Schema
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        '''项目下所有分支'''
        encrypt_token = request.data.get('token')
        project_id = request.data.get('project_id')
        if not all([encrypt_token, project_id]):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        _decrypt_token = decrypt_token(encrypt_token)
        gitlab_info = GitlabModel.objects.filter(private_token=_decrypt_token).first()
        if gitlab_info:
            instance = GitlabAPI(gitlab_url=gitlab_info.gitlab_url,
                                 private_token=gitlab_info.private_token)
            project = instance.gl.projects.get(project_id)
            branches = project.branches.list()
            branches_list = [branch.name for branch in branches]
            return Response({"success": True, "result": branches_list})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class GitlabPull(APIView):
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="project_id", required=True, location="form",
                      schema=coreschema.Integer(description='gitlab项目id')),
        coreapi.Field(name="token", required=False, location="form", schema=coreschema.String(description='加密后的token')),
        coreapi.Field(name="branch", required=False, location="form", schema=coreschema.String(description='分支名')),
    ])
    schema = Schema
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def decrypt_token(self, encrypt_token):
        prpcrypt_instance = PrpCrypt(AES_KEY, AES_IV)  # AES加密实例
        decrypt_token = prpcrypt_instance.decrypt(encrypt_token)
        return decrypt_token

    def post(self, request):
        '''pull指定分支'''
        encrypt_token = request.data.get('token')
        project_id = request.data.get('project_id')
        branch_name = request.data.get('branch')
        if not all([encrypt_token, project_id]):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        _decrypt_token = decrypt_token(encrypt_token)
        gitlab_info = GitlabModel.objects.filter(private_token=_decrypt_token).first()
        serializer = GitlabAuthenticationSerializer(instance=gitlab_info, many=False)
        if gitlab_info:  # gitlab　token存在于数据库中
            branch_instance = GitCaseModel.objects.filter(gitlab_url=gitlab_info.gitlab_url,
                                                          gitlab_project_id=project_id,
                                                          branch_name=branch_name).first()
            if not branch_instance or branch_instance.status != BranchState.PULLING:
                branch_pull.delay(serializer.data, project_id, branch_name)
            return Response({'success': True, 'pull_status': 'STARTING'})
        else:
            # gitlab token不存在数据库
            return Response(status=status.HTTP_404_NOT_FOUND)


class CaseTree(APIView):
    """
    case管理器
    """
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="gitlab_url", required=False, location="query",
                      schema=coreschema.String(description='gitlab地址')),
        coreapi.Field(name="project_name", required=False, location="query",
                      schema=coreschema.String(description='gitlab项目名')),
        coreapi.Field(name="branch_name", required=False, location="query",
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
        gitlab_url = request.query_params.dict().get('gitlab_url')
        project_name = request.query_params.dict().get('project_name')
        branch_name = request.query_params.dict().get('branch_name', 'master')
        case_name = request.query_params.dict().get('label')
        case_path = request.query_params.dict().get('path')
        if case_path:
            # 有指定文件 表示要获取case详情
            try:
                with open(os.path.join(settings.BASE_DIR, 'case_house', case_path), 'r',
                          encoding='utf-8') as f:
                    case_data = f.read()
                    return HttpResponse(case_data, content_type='text/plain')
            except FileNotFoundError as es:
                logger.error(str(es))
                return JsonResponse({"error": "case:{}不存在".format(case_name)})
        else:
            # 没有指定到case路径 则返回case目录树
            path_tree_instance = PathTree(branch_name)
            gitlab_path = gitlab_url.replace(':', '-').replace('.', '-').replace('/', '')
            tree = path_tree_instance.path_tree(
                os.path.join(settings.BASE_DIR, 'case_house', gitlab_path, branch_name, project_name))
            refine_tree = path_tree_instance.empty_json_data(tree)
            return JsonResponse({"branch": branch_name, "case_tree": [refine_tree]})


class CaseCollectList(APIView):
    """
    case管理器
    """
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="path", required=False, location="query", schema=coreschema.String(description='case路径')),
    ])
    schema = Schema
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        【获取指定case中的条目信息】
        :return
        """
        case_path = request.query_params.dict().get('path')
        if case_path:
            # 有指定文件 表示要获取case详情
            try:
                absolute_path = os.path.join(settings.BASE_DIR, 'case_house', case_path)
                p = subprocess.Popen(
                    "pytest {} --collect-only -q | head -n -2".format(absolute_path),
                    shell=True, stdout=subprocess.PIPE)
                out = p.stdout
                read_data = out.read().decode("utf-8", "ignore")
                subCasesList = read_data.split('\n')[:-1]
                return JsonResponse({"success": True, "subCaseList": subCasesList})
            except FileNotFoundError as es:
                logger.error(str(es))
                return JsonResponse({"success": False, "error": "case:{} not find".format(case_path)})
        else:
            return Response(data={"success": False, "error": "Lack of necessary parameters:case_path}"},
                            status=status.HTTP_404_NOT_FOUND)

# class CaseViewSet(viewsets.ModelViewSet):
#     authentication_classes = (JSONWebTokenAuthentication,)
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = CaseSerializer
#     pagination_class = pagination.LimitOffsetPagination
#
#     def get_queryset(self):
#         return CaseModel.objects.all()
#
#     def list(self, request, *args, **kwargs):
#         cases = self.get_queryset()
#         page = self.paginate_queryset(cases)
#         serializer = self.get_serializer(page, many=True)
#         return self.get_paginated_response(serializer.data)
#
#     def create(self, request, *args, **kwargs):
#         case_type_id = request.data.get('case_type_id')
#         case_type_obj = CaseTypeModel.objects.filter(id=case_type_id).first()
#         if not case_type_obj:
#             return Response({'respError': 'case类型不存在'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
#         case_data = request.data
#         case_data.pop('case_type_id')
#         case_data['case_type'] = case_type_obj
#         serializer = self.get_serializer(data=case_data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
#
# class CaseTypeViewSet(viewsets.ModelViewSet):
#     authentication_classes = (JSONWebTokenAuthentication,)
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = CaseTypeSerializer
#     pagination_class = pagination.LimitOffsetPagination
#
#     def get_queryset(self):
#         return CaseTypeModel.objects.all()
#
#     def list(self, request, *args, **kwargs):
#         case_types = self.get_queryset()
#         page = self.paginate_queryset(case_types)
#         serializer = self.get_serializer(page, many=True)
#         return self.get_paginated_response(serializer.data)
