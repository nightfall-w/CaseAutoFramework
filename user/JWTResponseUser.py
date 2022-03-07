# -*- coding:utf-8 -*-
import re

from django.contrib.auth import login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django_auth_ldap.backend import LDAPBackend


def jwt_response_payload_handler(token, user, request):
    """
    自定义jwt认证成功返回数据
    """
    user = User.objects.get(id=user.id)
    login(request, user)
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username,
        'display_name': user.first_name,
        'email': user.email
    }


def get_user_by_account(account):
    """
    根据帐号获取user对象
    :param account: 账号，可以是用户名，也可以是邮箱
    :return: User对象 或者 None
    """
    email_pat = re.compile('^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$')
    try:
        if re.match(email_pat, account):
            # 帐号为邮箱
            user = User.objects.get(email=account)
        else:
            # 帐号为用户名
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


def ldap_authenticate(request, username, password):
    return LDAPBackend().authenticate(request, username, password)


class UsernameMobileAuthBackend(ModelBackend):
    """
    自定义用户名或邮箱认证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        print(username)
        print(password)
        # ldap认证
        try:
            user = ldap_authenticate(request, username, password)
            if user:
                return user
        except Exception as e:
            pass
        # mysql数据库user表验证
        user = get_user_by_account(username)
        if user is not None and user.check_password(password):
            return user
        else:
            return None
