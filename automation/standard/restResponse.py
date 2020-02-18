from enum import Enum, unique


@unique
class Code(Enum):
    HANDLE_SUCCESS = {'respCode': '000000', 'message': '处理成功'}
    IDENTITY_EXISTED = {'respCode': '10001', 'message': '已经被注册'}
    USERNAME_OR_PASSWORD_ERROR = {'respCode': '10002', 'message': '用户名或密码错误'}
    REQUEST_DATA_ERROR = {'respCode': '10003', 'message': '请求数据格式或类型错误'}