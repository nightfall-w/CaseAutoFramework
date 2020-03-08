from rest_framework import viewsets, pagination, permissions

from .models import InterfaceModel
from .serializers import InterfaceSerializer


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
