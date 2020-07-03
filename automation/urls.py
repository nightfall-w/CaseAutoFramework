from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from automation.settings import MEDIA_ROOT
from case.views import CaseViewSet, CaseTypeViewSet, CodeBaseViewSet
from interface.views import InterfaceViewSet, InterfaceTestViewSet
from project.views import ProjectViewSet
from testplan.views import ApiTestPlanViewSet, CaseTestPlanViewSet

router = DefaultRouter()
router.register(r'project', ProjectViewSet, basename='api-project')
router.register(r'interface', InterfaceViewSet, basename='api-interface')
router.register(r'interfaceTest', InterfaceTestViewSet, basename='api-interface-test')
router.register(r'apiTestPlan', ApiTestPlanViewSet, basename='api-test-plan')
router.register(r'caseTestPlan', CaseTestPlanViewSet, basename='case-test-plan')
router.register(r'case', CaseViewSet, basename='api-case')
router.register(r'codeBase', CodeBaseViewSet, basename='code-base')
router.register(r'caseType', CaseTypeViewSet, basename='api-case-type')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/docs/', include_docs_urls(title='API文档')),
    path('api/case/', include('case.urls', namespace='case')),
    path('api/user/', include('user.urls', namespace='user')),
    path('api/testPlan/', include('testplan.urls', namespace='testPlan')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT})
]
