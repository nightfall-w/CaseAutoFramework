import coreapi
import coreschema
from rest_framework import viewsets, pagination, status, permissions
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import ProjectModel
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    Schema = AutoSchema(manual_fields=[
        coreapi.Field(name="projectName", required=False, location="query",
                      schema=coreschema.String(description='项目名'), )
    ])
    schema = Schema
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProjectSerializer
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        project_name = self.request.GET.get('projectName')
        if project_name:
            return ProjectModel.objects.filter(name__icontains=project_name).order_by("-id")
        else:
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
