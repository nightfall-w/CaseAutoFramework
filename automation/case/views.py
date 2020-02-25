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


class GitTool(GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)  # 登陆成功的token

    @action(methods=['get'], detail=False)
    def get_case_tree(self, request):
        branch = request.data.get('branch', 'master')
        case_house = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'case_house')
        branch_path = os.path.join(case_house, branch)
        if not os.path.exists(branch_path):
            # 分支路径已经存在
            os.makedirs(branch_path)
        case_address = ConfigParser.get_config('git', 'address')
        try:
            git.Repo.clone_from(case_address, branch_path)
        except git.GitCommandError as es:
            logger.warning(es)
        repo = git.Repo(branch_path)
        logger.info('branch: {}'.format(repo.active_branch))
        repo.git.checkout(branch)
        info = repo.git.show()
        author = re.search(r'Author: (.*?) <', info).group(1)
        GitCase.objects.update_or_create(lester_user=author, branch_name=branch, status=CaseStatus.DONE.value)
        return JsonResponse({'status': CaseStatus.DONE.value})
