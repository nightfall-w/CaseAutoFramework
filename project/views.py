from rest_framework import viewsets, pagination, status, permissions
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import ProjectSerializer
from .models import ProjectModel


class ProjectViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProjectSerializer
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        return ProjectModel.objects.all().order_by("-id")

    def list(self, request, *args, **kwargs):
        projects = self.get_queryset()
        page = self.paginate_queryset(projects)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = ProjectModel.objects.get(id=kwargs.get('pk'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
