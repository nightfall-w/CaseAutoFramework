import os
import re
from threading import Thread
from django.conf import settings
import git
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from Logger import logger
from standard.config import ConfigParser
from standard.enum import CaseStatus
from standard.enum import ResponseCode
from .models import GitCase


class PathTree(object):
    def __init__(self):
        self.index = 1
        self.suffixs = ConfigParser.get_config('case', 'suffixs')

    def path_tree(self, path):
        tree = dict()
        self.index += 1
        if os.path.isdir(path):
            tree["id"] = self.index
            tree["label"] = os.path.basename(path)
            tree['children'] = [self.path_tree(os.path.join(path, x)) for x in os.listdir(path)]
        elif os.path.splitext(path)[1] in self.suffixs:
            tree["id"] = self.index
            tree["label"] = os.path.basename(path)
            tree['filepath'] = path
        return tree


class GitTool(GenericViewSet):
    """
    通过git拉取case代码
    """

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

    @action(methods=['get'], detail=False)
    def case_pull(self, request):
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
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        获取case信息
        """
        case_branch = request.data.get('branch')
        case_name = request.data.get('label')
        case_path = request.data.get('path')
        if case_path:
            # 有指定文件 表示要获取case详情
            with open(os.path.join(settings.BASE_DIR, 'case_house', case_branch, case_path), 'r',
                      encoding='utf-8') as f:
                case_data = f.read()
                return JsonResponse({"case_name": case_name, "case_data": case_data})
        else:
            # 没有指定到case路径 则返回case目录树
            case_tree = PathTree().path_tree(os.path.join(settings.BASE_DIR, 'case_house', case_branch))
            return JsonResponse({"branch": case_branch, "case_tree": case_tree})
