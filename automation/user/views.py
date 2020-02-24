# -*- coding=utf-8 -*-
import re
import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView

from standard.enum import ResponseCode


class RegisterView(APIView):

    def post(self, request):
        '''
        注册
        :param request: 包含了提交的数据以及上下文
        :return: 返回注册结果
        '''
        try:
            post_data = json.loads(request.body)
        except:
            return Response(ResponseCode.REQUEST_DATA_ERROR.value)
        email = post_data.get('email', None)
        username = post_data.get('username', None)
        password = post_data.get('password', None)

        if not all([email, username, password]):
            response = ResponseCode.REQUEST_DATA_ERROR.value
        elif not re.match(r'^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$', email):
            response = ResponseCode.REQUEST_DATA_ERROR.value
        elif not re.match(r'[\u4e00-\u9fa5_a-zA-Z0-9_]{2,10}', username):
            response = ResponseCode.REQUEST_DATA_ERROR.value
        elif len(password) < 6:
            response = ResponseCode.REQUEST_DATA_ERROR.value
        else:
            if User.objects.filter(email=email).first():
                response = ResponseCode.IDENTITY_EXISTED.value
            else:
                user = User.objects.create(username=username, email=email, is_active=True)
                user.set_password(password)
                user.save()
                response = ResponseCode.HANDLE_SUCCESS.value
        return Response(response)


class LoginView(APIView):

    def post(self, request):
        '''
        处理登录请求
        :param request:包含了提交的数据以及上下文
        :return: 返回登录结果
        '''
        try:
            post_data = json.loads(request.body)
        except:
            return Response(ResponseCode.REQUEST_DATA_ERROR.value)
        username = post_data.get('username', None)
        password = post_data.get('password', None)

        if not all([username, password]):
            return Response(ResponseCode.REQUEST_DATA_ERROR.value)
        user = authenticate(username=username, password=password)
        if not user:
            return Response(ResponseCode.USERNAME_OR_PASSWORD_ERROR.value)
        else:
            login(request, user)
            return Response(ResponseCode.HANDLE_SUCCESS.value)


class RestPasswordView(APIView):

    def post(self, request):
        pass
        return Response({})
