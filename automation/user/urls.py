from django.urls import path
from user.views import RegisterView, LoginView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

app_name = 'user'
urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('apiTokenAuth', obtain_jwt_token),
    path('apiTokenAuthRefresh', refresh_jwt_token),
]
