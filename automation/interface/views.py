import json

from rest_framework import viewsets, pagination, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import InterfaceModel
from .serializers import InterfaceSerializer, InterfaceTaskSerializer
from Logger import logger


class InterfaceViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = InterfaceSerializer
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        return InterfaceModel.objects.all()

    def list(self, request, *args, **kwargs):
        interfaces = self.get_queryset()
        page = self.paginate_queryset(interfaces)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class InterfaceTaskViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = InterfaceTaskSerializer
    pagination_class = pagination.LimitOffsetPagination


class InterfaceTrigger(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            interfaceIds = json.loads(request.data.get('interfaceIds', "[]"))
        except Exception as es:
            logger.error(es)
            return Response({"error": "不符合格式的接口列表"})
        if not interfaceIds:
            return Response({"error": "接口id未提供"})
        for id in interfaceIds:
            interfaceObj = InterfaceModel.objects.filter(id=id).first()
            if not interfaceObj:
                return Response({"error": "接口名为{},地址为{}的api不存在".format(interfaceObj.name, interfaceObj.addr)})
        else:
            # 执行提交的api
            # TODO
            pass
