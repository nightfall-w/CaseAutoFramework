# -*- coding=utf-8 -*-
import json
import re

import requests

from Logger import logger
from interface.models import InterfaceJobModel, InterfaceModel
from testplan.models import ApiTestPlanModel
from utils.job_status_enum import ApiJobState, ApiTestPlanState


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
    if not result:
        return False
    try:
        result.group(1)
    except IndexError as es:
        logger.warning(es)
        return result.group(0)


def assert_delimiter(key_str, response_json):
    """
    分隔符处理
    """
    # TODO
    hierarchy = key_str.split('.')
    try:
        response = json.loads(response_json)
        result = response
        for tier in hierarchy:
            result = result.get(tier, dict())
            print(result)
        return result
    except Exception as es:
        logger.warning(es)
        return None


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
        for key, value in json.loads(interface.asserts).items():
            if key == "status_code":
                if response.status_code != value:
                    InterfaceJobModel.objects.filter(test_plan_id=self.test_plan_id,
                                                     interface_id=interface.id).update(result=response.text,
                                                                                       state=ApiJobState.FAILED)
            elif json.loads(response.text).get(key, None) != value:
                InterfaceJobModel.objects.filter(test_plan_id=self.test_plan_id,
                                                 interface_id=interface.id).update(result=response.text,
                                                                                   state=ApiJobState.FAILED)
                return False
        else:
            InterfaceJobModel.objects.filter(test_plan_id=self.test_plan_id,
                                             interface_id=interface.id).update(result=response.text,
                                                                               state=ApiJobState.SUCCESS)

    def processing_plant(self, interface):
        """
        测试计划处理
        """
        # 获取interface对象
        interface = InterfaceModel.objects.get(id=interface.interface_id)
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
