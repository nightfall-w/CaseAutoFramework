from django.urls import re_path
from user.views import RegisterView, LoginView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

app_name = 'user'
urlpatterns = [
    re_path('login/$', LoginView.as_view(), name='login'),
    re_path('register/$', RegisterView.as_view(), name='register'),
    re_path('apiTokenAuth/$', obtain_jwt_token),
    re_path('apiTokenAuthRefresh/$', refresh_jwt_token),
]
