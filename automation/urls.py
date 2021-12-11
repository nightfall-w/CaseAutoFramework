from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from automation.settings import MEDIA_ROOT
from case.views import GitLabAddToken
from interface.views import InterfaceViewSet, InterfaceTestViewSet
from project.views import ProjectViewSet
from testplan.views import ApiTestPlanViewSet, CaseTestPlanViewSet, CaseJobViewSet, ApiJobViewSet


router = DefaultRouter()
router.register(r'project', ProjectViewSet, basename='api-project')
router.register(r'interface', InterfaceViewSet, basename='api-interface')
router.register(r'interfaceTest', InterfaceTestViewSet, basename='api-interface-test')
router.register(r'apiTestPlan', ApiTestPlanViewSet, basename='api-test-plan')
router.register(r'caseTestPlan', CaseTestPlanViewSet, basename='case-test-plan')
router.register(r'apiJob', ApiJobViewSet, basename='api-job')
router.register(r'caseJob', CaseJobViewSet, basename='case-job')
router.register(r'gitlabAuthentication', GitLabAddToken, basename='api-case')
# router.register(r'case', CaseViewSet, basename='api-case')
# router.register(r'caseType', CaseTypeViewSet, basename='api-case-type')


urlpatterns = [
    path('cap/admin/', admin.site.urls),
    path('cap/api/', include(router.urls)),
    path('cap/api/docs/', include_docs_urls(title='API文档')),
    path('cap/api/case/', include('case.urls', namespace='case')),
    path('cap/api/user/', include('user.urls', namespace='user')),
    path('cap/api/testPlan/', include('testplan.urls', namespace='testPlan')),
    path('cap/api/report/', include('report.urls', namespace='report')),
    re_path(r'^cap/media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT})
]
