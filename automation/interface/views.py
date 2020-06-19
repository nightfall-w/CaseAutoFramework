import json

import requests
from rest_framework import viewsets, pagination, permissions, status
from rest_framework.response import Response

from .models import InterfaceModel, InterfaceHistory
from .serializers import InterfaceSerializer, InterfaceTestSerializer


class InterfaceViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = InterfaceSerializer
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        return InterfaceModel.objects.all()

    def list(self, request, *args, **kwargs):
        """
        【获取接口列表】
        """
        interfaces = self.get_queryset()
        page = self.paginate_queryset(interfaces)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        【创建接口】
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class InterfaceTestViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = InterfaceTestSerializer

    def get_queryset(self):
        return InterfaceHistory.objects.all()

    def create(self, request, *args, **kwargs):
        """
        【接收前端页面postman的数据进行处理】
        """
        serializer = self.get_serializer(data=request.data)
        inspection = serializer.is_valid(raise_exception=False)
        if not inspection:
            if serializer.errors.get('non_field_errors', None) and serializer.errors['non_field_errors'][
                0] == "existed":
                pass
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
        interface = serializer.data
        requests_fun = getattr(requests, interface.get('request_mode').lower())
        headers = json.loads(interface.get('headers', {}))  # 请求头
        if json.loads(interface.get('formData', {})):  # form-data文件请求
            data = json.loads(interface['formData'])
            response = requests_fun(url=interface.get('addr'), headers=headers, data=data)
        elif json.loads(interface.get('urlencoded')):  # form 表单
            data = json.loads(interface.get('urlencoded'))
            response = requests_fun(url=interface.get('addr'), headers=headers, data=data)
        elif json.loads(interface.get('raw')):  # json请求
            response = requests_fun(url=interface.get('addr'), headers=headers,
                                    data=interface.get('raw').encode("utf-8"))
        else:
            response = requests_fun(url=interface.get('addr'), headers=headers)
        return Response({"response": response.text, "status_code": response.status_code,
                         "elapsed": response.elapsed.total_seconds()})
