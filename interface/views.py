import json

import coreapi
import coreschema
import requests
from rest_framework import viewsets, pagination, permissions, status
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import InterfaceModel, InterfaceHistory
from .serializers import InterfaceSerializer, InterfaceTestSerializer


class InterfaceViewSet(viewsets.ModelViewSet):
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="projectId", required=False, location="query",
                      schema=coreschema.Integer(description='项目id'), )
    ])
    schema = Schema
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = InterfaceSerializer
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        if self.request.GET.get('projectId'):
            return InterfaceModel.objects.filter(project=self.request.GET.get('projectId')).order_by("-id")
        else:
            return InterfaceModel.objects.all().order_by("-id")

    def list(self, request, *args, **kwargs):
        """
        【获取接口列表】
        """
        interfaces = self.get_queryset()
        if not all([request.GET.get('limit'), request.GET.get('offset')]):
            serializer = self.get_serializer(interfaces, many=True)
            return Response({"count": len(interfaces), "results": serializer.data})
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

    def destroy(self, request, *args, **kwargs):
        instance = InterfaceModel.objects.get(id=kwargs.get('pk'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class InterfaceTestViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = InterfaceTestSerializer
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        return InterfaceHistory.objects.filter(user=self.request.user).order_by('-id')

    def create(self, request, *args, **kwargs):
        """
        【接收前端页面postman的数据进行处理】
        """
        request.data['user'] = request.user.username
        receive_data = request.data
        serializer = self.get_serializer(data=receive_data)
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
        headers = interface.get('headers', {})  # 请求头
        request_body = None
        try:
            if interface['request_mode'] == "GET":
                data = interface['params']
                response = requests_fun(url=interface.get('addr'), headers=headers, params=data)
            else:
                if interface.get('formData', {}):  # form-data文件请求
                    request_body = data = interface['formData']
                    response = requests_fun(url=interface.get('addr'), headers=headers, data=data)
                elif interface.get('urlencoded', {}):  # urlencoded
                    request_body = data = interface.get('urlencoded')
                    response = requests_fun(url=interface.get('addr'), headers=headers, data=data)
                elif interface.get('raw', {}):  # json请求
                    request_body = interface.get('raw')
                    data = json.dumps(interface.get('raw')).encode("utf-8")
                    response = requests_fun(url=interface.get('addr'), headers=headers,
                                            data=data)
                else:
                    response = requests_fun(url=interface.get('addr'), headers=headers)
            request_headers = response.request.headers
            request_content_type = request_headers.get("Content-Type")
            response_headers = response.headers
            return Response(
                {"response": response.json() if "application/json" in response_headers.get(
                    "Content-Type") else response.text, "request_headers": request_headers,
                 "request_body": request_body, "request_content_type": request_content_type,
                 "response_headers": response_headers,
                 "status_code": response.status_code,
                 "elapsed": response.elapsed.total_seconds()})
        except Exception as es:
            return Response({"error": str(es)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializers = InterfaceTestSerializer(page, many=True, fields=('id', 'request_mode', 'addr'))
        return Response({"success": True, "data": serializers.data})
