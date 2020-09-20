from django.urls import re_path
from user.views import RegisterView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

app_name = 'user'
urlpatterns = [
    re_path('register/$', RegisterView.as_view(), name='register'),
    re_path('login/$', obtain_jwt_token),
    re_path('apiTokenAuthRefresh/$', refresh_jwt_token),
]
