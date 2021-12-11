from django.contrib.auth import get_user_model


def get_user_by_username(username):
    """
    根据同户名获取用户信息
    """
    User = get_user_model()
    user = User.objects.filter(username=username).values('username', 'first_name', 'email')
    if user:
        return user[0]
    else:
        return {"email": "", "first_name": "", "username": ""}


def get_user_by_display_name(display_name):
    """
    根据同户名获取用户信息
    """
    User = get_user_model()
    user = User.objects.filter(first_name=display_name).values('username', 'first_name', 'email')
    if user:
        return user[0]
    else:
        return {"email": "", "first_name": "", "username": ""}
