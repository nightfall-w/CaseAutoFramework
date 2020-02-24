import git
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from Logger import log_path
from standard.config import ConfigParser
from .models import GitCase
import json
class gitTool(GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)  # 登陆成功的token

    @action(methods=['get'], detail=False)
    def get_case_tree(self, request):
        request_data = request.body
        request_data
        try:
            case_address = ConfigParser.get_config('git', 'address')
            git.Repo.clone_from(case_address, '../casedir/')
        except :
            GitCase.objects.update_or_create()
        return JsonResponse({'ds': 'u'})
