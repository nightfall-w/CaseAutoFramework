import git
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from standard.config import ConfigParser
from .models import GitCase
import json
import os


class GitTool(GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)  # 登陆成功的token

    @action(methods=['get'], detail=False)
    def get_case_tree(self, request):
        request_data = json.loads(request.body)
        branch = request_data.get('branch', 'master')
        try:
            case_house = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'case_house')
            branch_path = os.path.join(case_house, branch)
            if not os.path.exists(branch_path):
                os.makedirs(branch_path)
            case_address = ConfigParser.get_config('git', 'address')
            git.Repo(branch)
            git.clone()

        except:
            GitCase.objects.update_or_create()
        return JsonResponse({'ds': 'u'})
