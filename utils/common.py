import time


def ts_10():
    # 生成10位时间戳
    return int(time.time())


def ts_13():
    int(time.time() * 1000)


print(ts_10())
print(ts_13())
