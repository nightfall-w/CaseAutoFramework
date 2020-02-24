from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from project.views import ProjectViewSet
from interface.views import InterfaceViewSet
from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
router.register(r'project', ProjectViewSet, basename='api-project')
router.register(r'interface', InterfaceViewSet, basename='api-interface')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/docs/', include_docs_urls(title='API文档')),
    path('api/case/', include('case.urls', namespace='case')),
    path('api/user/', include('user.urls', namespace='user')),
]
