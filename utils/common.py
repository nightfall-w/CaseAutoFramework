import datetime
import time


def ts_10():
    # 生成10位时间戳
    return int(time.time())


def ts_13():
    # 生成13位时间戳
    return int(time.time() * 1000)


def is_chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def current_time_format():
    """
    当前时间格式化
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
