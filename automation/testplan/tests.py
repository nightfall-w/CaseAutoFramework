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
# import itertools
#
#
# class cartesian(object):
#     def __init__(self):
#         self._data_list = list()
#
#     def add_data(self, data=list()):  # 添加生成笛卡尔积的数据列表
#         self._data_list.append(data)
#
#     def build(self):  # 计算笛卡尔积
#         for item in itertools.product(*self._data_list):
#             print(item)
#
#
# car = cartesian()
# car.add_data([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# car.add_data([[10, 11, 12], [13, 14, 15], [16, 17, 18]])
# car.add_data([66, 88, 99])
# car.build()
#
# import requests
# r = requests.get("http://www.cnblogs.com/yoyoketang/")
# print(r.elapsed)
# print(r.elapsed.total_seconds())
# print(r.elapsed.microseconds)
# print(r.elapsed.seconds)
# print(r.elapsed.days)
# print(r.elapsed.max)
# print(r.elapsed.min)
# print(r.elapsed.resolution)
import json

# def assert_delimiter(key_str, response_text):
#     """
#     分隔符处理
#     """
#     hierarchy = key_str.split('.')[1:]
#     try:
#         if hierarchy[0] == 'status_code':
#             # result = response.status_code
#             return 200
#         response_json = json.loads(response_text)
#         result = response_json
#         for tier in hierarchy:
#             try:
#                 tier = int(tier)
#             except ValueError:
#                 tier = tier
#             if isinstance(tier, int):
#                 try:
#                     result = result[tier]
#                 except IndexError as es:
#                     # logger.error(es)
#                     return "EXCEPTION"
#             else:
#                 result = result.get(tier, dict())
#         print(result)
#         return result
#     except Exception as es:
#         return "EXCEPTION"
#
# assert_delimiter('r.aa.5.name', '{"aa":[{"name":"wang"},{"name":"li"}]}')
# from functools import reduce
#
#
# def Merge(dict1, dict2):
#     if not isinstance(dict1, dict):
#         dict1 = json.loads(dict1)
#     if not isinstance(dict2, dict):
#         dict2 = json.loads(dict2)
#     res = {**dict1, **dict2}
#     return res
#
#
# a = ['{"a":4,"b":5}', '{"c":7,"d":8}']
# s = reduce(Merge, a)
# print(s)