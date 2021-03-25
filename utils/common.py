import time


def ts_10():
    # 生成10位时间戳
    return int(time.time())


def ts_13():
    # 生成13位时间戳
    return int(time.time() * 1000)
