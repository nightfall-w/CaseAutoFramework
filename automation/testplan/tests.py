# import json
#
#
# # Create your tests here.
# def assert_delimiter(key_str, response_json):
#     """
#     分隔符处理
#     """
#     # TODO
#     hierarchy = key_str.split('.')
#     try:
#         response = json.loads(response_json)
#         result = response
#         for tier in hierarchy:
#             result = result.get(tier, dict())
#             print(result)
#         return result
#     except Exception as es:
#         return None
#
#
# assert_delimiter("a.b.c", '{"a":1,"b":"4"}')
# from testplan import operation
#
# result = getattr(operation, 'dd')
# print(result)
import itertools


class cartesian(object):
    def __init__(self):
        self._data_list = list()

    def add_data(self, data=list()):  # 添加生成笛卡尔积的数据列表
        self._data_list.append(data)

    def build(self):  # 计算笛卡尔积
        for item in itertools.product(*self._data_list):
            print(item)


car = cartesian()
car.add_data([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
car.add_data([[10, 11, 12], [13, 14, 15], [16, 17, 18]])
car.add_data([66, 88, 99])
car.build()
