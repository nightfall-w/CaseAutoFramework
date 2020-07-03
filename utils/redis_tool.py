import redis


def singleton(cls):
    _instance = {}

    def wrapper(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return wrapper


@singleton
class RedisPoll:
    def __init__(self):
        self.instance = redis.ConnectionPool(host='127.0.0.1', port=6379, max_connections=30, decode_responses=True)
