# -*- coding=utf-8 -*-
import itertools
import json
import re

import requests
from Logger import logger
from interface.models import InterfaceJobModel, InterfaceModel, InterfaceCacheModel
from testplan import operation
from testplan.models import ApiTestPlanModel
from utils.job_status_enum import ApiJobState, ApiTestPlanState
from standard.enum import InterFaceType


class cartesian(object):
    """
    【api测试数据的笛卡儿积计算器】
    """

    def __init__(self):
        self._data_list = list()

    def add_data(self, data=list()):  # 添加生成笛卡尔积的数据列表
        self._data_list.append(data)

    def build(self):  # 计算笛卡尔积
        items = []
        for item in itertools.product(*self._data_list):
            items.append(item)
        return items


def data_drive(interfaceIds, plan_id):
    for interfaceId in interfaceIds:
        interface = InterfaceModel.objects.get(id=interfaceId)
        if not interface.parameters:  # api没有测试数据集  直接创建api job
            InterfaceJobModel.objects.create(interfaceType=InterFaceType.INSTANCE.value, interface_id=interfaceId,
                                             test_plan_id=plan_id,
                                             state=ApiJobState.WAITING)
            api_testplan_obj = ApiTestPlanModel.objects.get(plan_id=plan_id)
            current_job_num = api_testplan_obj.result.split('/')[1]
            api_testplan_obj.result = "0/{}".format(1 + int(current_job_num))
            api_testplan_obj.save()
        else:  # api有测试数据集， 解析测试数据
            key_list = []
            car = cartesian()
            parameters = json.loads(interface.parameters)
            for k, v in parameters.items():
                key_list.append(k)
                if not isinstance(v, list):
                    v = [v, ]
                car.add_data(v)
            items = car.build()
            api_testplan_obj = ApiTestPlanModel.objects.get(plan_id=plan_id)
            current_job_num = api_testplan_obj.result.split('/')[1]
            api_testplan_obj.result = "0/{}".format(len(items) + int(current_job_num))
            api_testplan_obj.save()
            for item in items:
                interfaceCache = InterfaceCacheModel.objects.create(project=interface.project,
                                                                    name=interface.name, desc=interface.desc,
                                                                    addr=interface.addr,
                                                                    request_mode=interface.request_mode,
                                                                    headers=interface.headers,
                                                                    formData=interface.formData,
                                                                    urlencoded=interface.urlencoded,
                                                                    raw=interface.raw,
                                                                    asserts=interface.asserts,
                                                                    extract=interface.extract)
                for keys_index, keys in enumerate(key_list):
                    keys_break_down = keys.split('-')
                    for key_index, key in enumerate(keys_break_down):
                        if len(keys_break_down) == 1:
                            item = list(item)
                            item[keys_index] = [item[keys_index], ]
                            item = tuple(item)
                        if '$%s' % key in interfaceCache.addr:
                            interfaceCache.addr = interfaceCache.addr.replace('$%s' % key, item[keys_index][key_index],
                                                                              10)
                        if '$%s' % key in interfaceCache.name:
                            interfaceCache.name = interfaceCache.name.replace('$%s' % key, item[keys_index][key_index],
                                                                              10)
                        if '$%s' % key in interfaceCache.desc:
                            interfaceCache.desc = interfaceCache.desc.replace('$%s' % key, item[keys_index][key_index],
                                                                              10)
                        if '$%s' % key in interfaceCache.headers:
                            interfaceCache.headers = interfaceCache.headers.replace('$%s' % key,
                                                                                    item[keys_index][key_index], 10)
                        if '$%s' % key in interfaceCache.formData:
                            interfaceCache.formData = interfaceCache.formData.replace('$%s' % key,
                                                                                      item[keys_index][key_index], 10)
                        if '$%s' % key in interfaceCache.urlencoded:
                            interfaceCache.urlencoded = interfaceCache.urlencoded.replace('$%s' % key,
                                                                                          item[keys_index][key_index],
                                                                                          10)
                        if '$%s' % key in interfaceCache.raw:
                            interfaceCache.raw = interfaceCache.raw.replace('$%s' % key, item[keys_index][key_index],
                                                                            10)
                        if '$%s' % key in interfaceCache.asserts:
                            interfaceCache.asserts = interfaceCache.asserts.replace('$%s' % key,
                                                                                    item[keys_index][key_index], 10)
                        if '$%s' % key in interfaceCache.extract:
                            interfaceCache.extract = interfaceCache.extract.replace('$%s' % key,
                                                                                    item[keys_index][key_index], 10)
                        interfaceCache.save()
                InterfaceJobModel.objects.create(interfaceType=InterFaceType.CACHE.value,
                                                 interface_id=interfaceCache.id,
                                                 test_plan_id=plan_id,
                                                 state=ApiJobState.WAITING)


def isRegular(expression):
    """
    判断是否为正则表达式
    """
    if not isinstance(expression, str):
        return False
    try:
        term = re.compile(expression)
    except Exception as es:
        logger.error(es)
        return False
    else:
        return term


def assert_regular(pattern, str_obj):
    result = pattern.search(str_obj)
    if result is None:
        return False
    try:
        result.group(1)
    except IndexError as es:
        logger.warning(es)
        return result.group(0)


def assert_delimiter(key_str, response):
    """
    分隔符处理
    """
    hierarchy = key_str.split('.')[1:]
    try:
        if hierarchy[0] == 'status_code':
            result = response.status_code
            return result
        response_json = json.loads(response.text)
        result = response_json
        for tier in hierarchy:
            result = result.get(tier, dict())
        return result
    except Exception as es:
        return "EXCEPTION"


def update_api_job_fail(test_plan_id, interface_id, response):
    """
    更新interfaceJob状态为FAIL
    """
    InterfaceJobModel.objects.filter(test_plan_id=test_plan_id,
                                     interface_id=interface_id).update(result=response.text,
                                                                       state=ApiJobState.FAILED,
                                                                       status_code=response.status_code,
                                                                       elapsed=response.elapsed.total_seconds())


def update_api_job_success(test_plan_id, interface_id, response):
    """
    更新interfaceJob状态为FAIL
    """
    InterfaceJobModel.objects.filter(test_plan_id=test_plan_id,
                                     interface_id=interface_id).update(result=response.text,
                                                                       state=ApiJobState.SUCCESS,
                                                                       status_code=response.status_code,
                                                                       elapsed=response.elapsed.total_seconds())


class ApiRunner:
    """
    Api case测执行调度器
    """

    def __init__(self, test_plan_id):
        self.test_plan_id = test_plan_id
        self.session = requests.session()

    def dispose_response(self, interface, response):
        """
        请求处理器
        """
        for _assert in json.loads(interface.asserts):
            if _assert['assertType'] == "regular":
                # 正则判断逻辑
                if not isRegular(_assert['rule']):
                    logger.debug(
                        'interface Id：{}, testPlan Id expression {} is not regular'.format(interface.id,
                                                                                           self.test_plan_id,
                                                                                           _assert['expression']))
                    update_api_job_fail(self.test_plan_id, interface.id, response)
                    break
                else:
                    pattern = isRegular(_assert['expression'])
                    re_result = assert_regular(pattern, response.text)
                    if not re_result:  # 断言失败
                        update_api_job_fail(self.test_plan_id, interface.id, response)  # 跟新interfaceJob状态失败
                        break
                    else:
                        try:
                            calculate_fun = getattr(operation, _assert['calculate'])
                        except AttributeError as es:
                            logger.error("calculate rule {} is not exist！".format(_assert['calculate']))
                            update_api_job_fail(self.test_plan_id, interface.id, response)
                            break
                        if not calculate_fun(re_result, _assert['expect']):
                            update_api_job_fail(self.test_plan_id, interface.id, response)  # 跟新interfaceJob状态失败
                            break
            elif _assert['assertType'] == "delimiter":
                # 分隔符取值
                delimiter_result = assert_delimiter(_assert['expression'], response)
                if delimiter_result == 'EXCEPTION':
                    logger.error("delimiter error：{}, interfaceJobId: {}, test_plan Id:{}".format(_assert['expression'],
                                                                                                  interface.id,
                                                                                                  self.test_plan_id))
                    update_api_job_fail(self.test_plan_id, interface.id, response)
                    break
                elif delimiter_result == dict():
                    update_api_job_fail(self.test_plan_id, interface.id, response)
                    break
                else:
                    try:
                        calculate_fun = getattr(operation, _assert['calculate'])
                    except AttributeError as es:
                        logger.error("calculate rule {} is not exist！".format(_assert['calculate']))
                        update_api_job_fail(self.test_plan_id, interface.id, response)
                        break
                    if not calculate_fun(delimiter_result, _assert['expect']):
                        update_api_job_fail(self.test_plan_id, interface.id, response)
                        break
        else:  # 所有断言验证通过
            update_api_job_success(self.test_plan_id, interface.id, response)

    def processing_plant(self, interface_job):
        """
        测试计划处理
        """
        # 获取interface对象
        if interface_job.interfaceType == InterFaceType.INSTANCE.value:
            interface = InterfaceModel.objects.get(id=interface_job.interface_id)
        else:
            interface = InterfaceCacheModel.objects.get(id=interface_job.interface_id)
        headers = json.loads(interface.headers)  # 请求头
        # 根据请求方式动态选择requests的请求方法
        logger.debug(id(self.session))
        requests_fun = getattr(self.session, interface.get_request_mode_display().lower())
        ApiTestPlanModel.objects.filter(plan_id=self.test_plan_id).update(state=ApiTestPlanState.RUNNING)
        if json.loads(interface.formData):  # form-data文件请求
            data = json.loads(interface.formData)
            response = requests_fun(url=interface.addr, headers=headers, data=data)
            self.dispose_response(interface=interface, response=response)
        elif json.loads(interface.urlencoded):  # form 表单
            data = json.loads(interface.urlencoded)
            response = requests_fun(url=interface.addr, headers=headers, data=data)
            self.dispose_response(interface=interface, response=response)
        elif json.loads(interface.raw):  # json请求
            response = requests_fun(url=interface.addr, headers=headers, data=interface.raw.encode("utf-8"))
            self.dispose_response(interface=interface, response=response)
        else:
            response = requests_fun(url=interface.addr, headers=headers)
            self.dispose_response(interface=interface, response=response)

    def distributor(self):
        # 分配器
        interfaceJobs = InterfaceJobModel.objects.filter(test_plan_id=self.test_plan_id)
        for interfaceJob in interfaceJobs:
            self.processing_plant(interfaceJob)
            upInterfaces = InterfaceJobModel.objects.get(id=interfaceJob.id)
            if upInterfaces.state == ApiJobState.SUCCESS:
                test_plan = ApiTestPlanModel.objects.get(plan_id=self.test_plan_id)
                test_plan_result = test_plan.result.split('/')
                test_plan.result = str(int(test_plan_result[0]) + 1) + '/' + str(test_plan_result[1])
                test_plan.save()
        ApiTestPlanModel.objects.filter(plan_id=self.test_plan_id).update(state=ApiTestPlanState.FINISH)
