import os
import re
import git
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from .models import GitCase
from Logger import logger
from standard.config import ConfigParser
from standard.enum import CaseStatus
from threading import Thread
from standard.enum import ResponseCode


class GitTool(GenericViewSet):
    """
    通过git拉取case代码
    """

    permission_classes = (permissions.IsAuthenticated,)  # 登陆成功的token

    def pull_case(self, branch, case_address, branch_path):
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
    def get_case_tree(self, request):
        branch = request.data.get('branch', 'master')
        case_house = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'case_house')
        branch_path = os.path.join(case_house, branch)
        if not os.path.exists(branch_path):
            # 分支路径已经存在
            os.makedirs(branch_path)
        case_address = ConfigParser.get_config('git', 'address')
        t = Thread(target=self.pull_case, args=(branch, case_address, branch_path))
        t.start()
        return JsonResponse(ResponseCode.HANDLE_SUCCESS.value)

