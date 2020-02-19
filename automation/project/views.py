from rest_framework import viewsets, pagination
from .serializers import ProjectSerializer
from .models import ProjectModel


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        return ProjectModel.objects.all()

    def list(self, request, *args, **kwargs):
        projects = self.get_queryset()
        page = self.paginate_queryset(projects)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
