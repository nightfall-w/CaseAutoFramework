# -*- coding=utf-8 -*-
import json
import re
from testplan import operation
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
    if result is None:
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
    hierarchy = key_str.split('.')[1:]
    try:
        response = json.loads(response_json)
        result = response
        for tier in hierarchy:
            result = result.get(tier, dict())
        return result
    except Exception as es:
        return "EXCEPTION"


def update_api_job_fail(test_plan_id, interface_id, response_text):
    """
    更新interfaceJob状态为FAIL
    """
    InterfaceJobModel.objects.filter(test_plan_id=test_plan_id,
                                     interface_id=interface_id).update(result=response_text,
                                                                       state=ApiJobState.FAILED)


def update_api_job_success(test_plan_id, interface_id, response_text):
    """
    更新interfaceJob状态为FAIL
    """
    InterfaceJobModel.objects.filter(test_plan_id=test_plan_id,
                                     interface_id=interface_id).update(result=response_text,
                                                                       state=ApiJobState.SUCCESS)


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
                    update_api_job_fail(self.test_plan_id, interface.id, response.text)
                    break
                else:
                    pattern = isRegular(_assert['expression'])
                    re_result = assert_regular(pattern, response.text)
                    if not re_result:  # 断言失败
                        update_api_job_fail(self.test_plan_id, interface.id, response.text)  # 跟新interfaceJob状态失败
                        break
                    else:
                        if re_result != _assert['expect']:
                            update_api_job_fail(self.test_plan_id, interface.id, response.text)  # 跟新interfaceJob状态失败
                            break
            elif _assert['assertType'] == "delimiter":
                # 分隔符取值
                delimiter_result = assert_delimiter(_assert['expression'], response.text)
                if not delimiter_result == 'EXCEPTION':
                    logger.error("delimiter error：{}, interfaceJobId: {}, test_plan Id:{}".format(_assert['expression'],
                                                                                                  interface.id,
                                                                                                  self.test_plan_id))
                    update_api_job_fail(self.test_plan_id, interface.id, response.text)
                    break
                elif not delimiter_result:
                    update_api_job_fail(self.test_plan_id, interface.id, response.text)
                    break
                else:
                    if not delimiter_result != _assert['expect']:
                        update_api_job_fail(self.test_plan_id, interface.id, response.text)
                        break
        else:  # 所有断言验证通过
            update_api_job_success(self.test_plan_id, interface.id, response.text)

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
