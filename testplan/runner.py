# -*- coding:utf-8 -*-
import itertools
import json
import os
import re
import subprocess
import time
from functools import reduce

import requests
from django.conf import settings

from automation.settings import MEDIA_ROOT, logger
from interface.models import InterfaceJobModel, InterfaceModel, InterfaceCacheModel
from standard.enum import InterFaceType
from testplan import operation
from testplan.models import ApiTestPlanTaskModel, CaseTestPlanModel, CaseJobModel
from utils.job_status_enum import ApiJobState, ApiTestPlanTaskState, CaseJobState


class cartesian(object):
    """
    【api测试数据的笛卡儿积计算器】
    """

    def __init__(self):
        self._data_list = list()

    def add_data(self, data=[]):  # 添加生成笛卡尔积的数据列表
        self._data_list.append(data)

    def build(self):  # 计算笛卡尔积
        items = []
        for item in itertools.product(*self._data_list):
            items.append(item)
        return items


def update_api_total_number(api_test_plan_task_id, add_num):
    """
    【更新当前测试计划的api job总数】
    """
    api_testplan_task_obj = ApiTestPlanTaskModel.objects.get(id=api_test_plan_task_id)
    current_job_num = api_testplan_task_obj.api_job_number + add_num
    api_testplan_task_obj.api_job_number = current_job_num
    api_testplan_task_obj.save()


def merge(dict1, dict2):
    if not isinstance(dict1, dict):
        dict1 = json.loads(dict1)
    if not isinstance(dict2, dict):
        dict2 = json.loads(dict2)
    res = {**dict1, **dict2}
    return res


def parse_parameters(parameters):
    key_list = []
    car = cartesian()
    for k, v in parameters.items():
        key_list.append(k)
        if not isinstance(v, list):
            v = [v, ]
        car.add_data(v)
    items = car.build()
    return items, key_list


def get_all_extracts(test_plan_id, task_id):
    extracts_list = InterfaceJobModel.objects.filter(test_plan_id=test_plan_id, api_test_plan_task_id=task_id,
                                                     extracts__isnull=False).values_list(
        'extracts', flat=True)
    extracts_dict = reduce(merge, extracts_list)
    return extracts_dict


def data_drive(interfaceIds, plan_id, api_test_plan_task_id):
    for interfaceId in interfaceIds:
        interface = InterfaceModel.objects.get(id=interfaceId)
        if not interface.parameters:  # api没有测试数据集  直接创建api job
            InterfaceJobModel.objects.create(interfaceType=InterFaceType.INSTANCE.value, interface_id=interfaceId,
                                             test_plan_id=plan_id, api_test_plan_task_id=api_test_plan_task_id,
                                             state=ApiJobState.WAITING)
            update_api_total_number(api_test_plan_task_id=api_test_plan_task_id, add_num=1)

        else:  # api有测试数据集， 解析测试数据
            parameters = interface.parameters
            items, key_list = parse_parameters(parameters)
            update_api_total_number(api_test_plan_task_id=api_test_plan_task_id, add_num=len(items))
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
                            # 需要对笛卡尔积组合中包含单个元素的情况做统一处理  例如:([1,2,3],[4,5,6],7) 转为([1,2,3],[4,5,6],[7,])
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
                        if '$%s' % key in json.dumps(interfaceCache.headers):
                            interfaceCache.headers = json.loads(json.dumps(interfaceCache.headers).replace('$%s' % key,
                                                                                                           item[
                                                                                                               keys_index][
                                                                                                               key_index],
                                                                                                           10))
                        if '$%s' % key in json.dumps(interfaceCache.formData):
                            interfaceCache.formData = json.loads(
                                json.dumps(interfaceCache.formData).replace('$%s' % key,
                                                                            item[keys_index][
                                                                                key_index], 10))
                        if '$%s' % key in json.dumps(interfaceCache.urlencoded):
                            interfaceCache.urlencoded = json.loads(
                                json.dumps(interfaceCache.urlencoded).replace('$%s' % key,
                                                                              item[keys_index][
                                                                                  key_index],
                                                                              10))
                        if '$%s' % key in json.dumps(interfaceCache.raw):
                            interfaceCache.raw = json.loads(json.dumps(interfaceCache.raw).replace('$%s' % key,
                                                                                                   item[keys_index][
                                                                                                       key_index],
                                                                                                   10))
                        if '$%s' % key in json.dumps(interfaceCache.asserts):
                            interfaceCache.asserts = json.loads(json.dumps(interfaceCache.asserts).replace('$%s' % key,
                                                                                                           item[
                                                                                                               keys_index][
                                                                                                               key_index],
                                                                                                           10))

                        interfaceCache.save()
                InterfaceJobModel.objects.create(interfaceType=InterFaceType.CACHE.value,
                                                 api_test_plan_task_id=api_test_plan_task_id,
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
        return result.group(1)
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
        result = json.loads(response.text)
        for tier in hierarchy:
            try:
                tier = int(tier)
            except ValueError:
                tier = tier
            if isinstance(tier, int):
                try:
                    result = result[tier]
                except IndexError as es:
                    logger.error(es)
                    return "EXCEPTION"
            else:
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
    更新interfaceJob状态为SUCCESS
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

    def __init__(self, test_plan_id, test_plan_task_id):
        self.test_plan_id = test_plan_id
        self.test_plan_task_id = test_plan_task_id
        self.session = requests.session()

    def dispose_response(self, interface, response):
        """
        请求处理器
        """
        # 处理断言
        for _assert in interface.asserts:
            if _assert['assertType'] == "regular":
                # 正则判断逻辑
                if not isRegular(_assert['expressions']):
                    logger.error(
                        'interface Id：{}, testPlan Id：{} expressions：{} is not regular'.format(interface.id,
                                                                                               self.test_plan_id,
                                                                                               _assert['expressions']))
                    update_api_job_fail(self.test_plan_id, interface.id, response)
                    break
                else:
                    pattern = isRegular(_assert['expressions'])
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
                delimiter_result = assert_delimiter(_assert['expressions'], response)
                if delimiter_result == 'EXCEPTION':
                    logger.error(
                        "delimiter error：{}, interfaceJobId: {}, test_plan Id:{}".format(_assert['expressions'],
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

        # 处理提取规则
        extracts_result = {}  # 提取结果的集合
        for extract in interface.extract:
            if extract['extractType'] == "regular":
                if not isRegular(extract['expressions']):
                    logger.error(
                        'interface Id：{}, testPlan Id：{} expressions：{} is not regular'.format(interface.id,
                                                                                               self.test_plan_id,
                                                                                               extract['expressions']))
                pattern = isRegular(extract['expressions'])
                re_result = assert_regular(pattern, response.text)
                if not re_result:  # 没有匹配到结果
                    extracts_result[extract['variable_name']] = ''
                else:
                    extracts_result[extract['variable_name']] = re_result

            elif extract['extractType'] == "delimiter":
                delimiter_result = assert_delimiter(extract['expressions'], response)
                if delimiter_result == 'EXCEPTION':
                    logger.error(
                        "delimiter error：{}, interfaceJobId: {}, test_plan Id:{}".format(extract['expressions'],
                                                                                         interface.id,
                                                                                         self.test_plan_id))
                    extracts_result[extract['variable_name']] = ''
                else:
                    extracts_result[extract['variable_name']] = delimiter_result
        return extracts_result

    def processing_plant(self, interface_job):
        """
        测试计划处理
        """
        # 获取interface对象
        if interface_job.interfaceType == InterFaceType.INSTANCE.value:
            interface = InterfaceModel.objects.get(id=interface_job.interface_id)
        else:
            interface = InterfaceCacheModel.objects.get(id=interface_job.interface_id)
        extracts_dict = get_all_extracts(interface_job.test_plan_id, interface_job.api_test_plan_task_id)
        for key, value in extracts_dict.items():
            if '$%s' % key in interface.addr:
                interface.addr = interface.addr.replace('$%s' % key, value, 10)
            if '$%s' % key in interface.name:
                interface.name = interface.name.replace('$%s' % key, value, 10)
            if '$%s' % key in interface.desc:
                interface.desc = interface.desc.replace('$%s' % key, value, 10)
            if '$%s' % key in json.dumps(interface.headers):
                interface.headers = json.dumps(interface.headers).replace('$%s' % key, value, 10)
            if '$%s' % key in json.dumps(interface.formData):
                interface.formData = json.dumps(interface.formData).replace('$%s' % key, value, 10)
            if '$%s' % key in json.dumps(interface.urlencoded):
                interface.urlencoded = json.dumps(interface.urlencoded).replace('$%s' % key, value, 10)
            if '$%s' % key in json.dumps(interface.raw):
                interface.raw = json.dumps(interface.raw).replace('$%s' % key, value, 10)
            if '$%s' % key in json.dumps(interface.asserts):
                interface.asserts = json.dumps(interface.asserts).replace('$%s' % key, value, 10)
        interface.save()

        headers = interface.headers  # 请求头
        # 根据请求方式动态选择requests的请求方法
        requests_fun = getattr(self.session, interface.get_request_mode_display().lower())
        if interface.formData:  # form-data文件请求
            data = interface.formData
            response = requests_fun(url=interface.addr, headers=headers, data=data)
        elif interface.urlencoded:  # form 表单
            data = interface.urlencoded
            response = requests_fun(url=interface.addr, headers=headers, params=data)
        elif interface.raw:  # json请求
            data = json.dumps(interface.raw).encode("utf-8")
            response = requests_fun(url=interface.addr, headers=headers, data=data)
        else:
            response = requests_fun(url=interface.addr, headers=headers)
        extracts_result = self.dispose_response(interface=interface, response=response)
        InterfaceJobModel.objects.filter(id=interface_job.id).update(extracts=extracts_result)

    def distributor(self):
        # 分配器
        interfaceJobs = InterfaceJobModel.objects.filter(test_plan_id=self.test_plan_id,
                                                         api_test_plan_task_id=self.test_plan_task_id)
        start_time = time.time()
        # ApiTestPlanTaskModel.objects.filter(test_plan_uid=self.test_plan_id, id=self.test_plan_task_id).update(
        #     state=ApiTestPlanTaskState.RUNNING)
        test_plan_task = ApiTestPlanTaskModel.objects.filter(test_plan_uid=self.test_plan_id,
                                                             id=self.test_plan_task_id).first()
        test_plan_task.state = ApiTestPlanTaskState.RUNNING
        test_plan_task.save()
        for interfaceJob in interfaceJobs:
            self.processing_plant(interfaceJob)
            # upInterfaces = InterfaceJobModel.objects.get(id=interfaceJob.id)
            interfaceJob.refresh_from_db()  # 载入字段更新过后的对象或查询集 避免拿到缓存在内存的老数据
            test_plan_task.refresh_from_db()
            # if upInterfaces.state == ApiJobState.SUCCESS:
            if interfaceJob.state == ApiJobState.SUCCESS:
                test_plan_task.success_num = test_plan_task.success_num + 1
                test_plan_task.save()
            else:
                test_plan_task.failed_num = test_plan_task.failed_num + 1
                test_plan_task.save()
        used_time = time.time() - start_time
        ApiTestPlanTaskModel.objects.filter(id=self.test_plan_task_id).update(state=ApiTestPlanTaskState.FINISH,
                                                                              used_time=used_time)


class CaseRunner:
    """
    【case的运行管理器】
    """

    @classmethod
    def distributor(cls, test_plan_task):
        """

        :param test_plan_task: case测试计划对象
        :return: 分配结果
        """
        case_test_plan = CaseTestPlanModel.objects.filter(plan_id=test_plan_task.test_plan_uid).first()
        case_paths = case_test_plan.case_paths
        for case_path in case_paths:
            CaseJobModel.objects.create(case_task_id=test_plan_task.id, case_path=case_path,
                                        state=CaseJobState.WAITING)
        return True

    @classmethod
    def executor(cls, case_job, project_id, test_plan_uid, task_id):
        """
        执行器
        :param case_job:
        :param project_id:
        :param test_plan_uid:
        :param task_id:
        :return:
        """
        case_job.state = CaseJobState.RUNNING
        case_job.save()
        report_name = case_job.case_path.split('/')[-1].split('.')[0] + '.html'
        report_path = os.path.join(MEDIA_ROOT, 'html-report', str(project_id), test_plan_uid, str(task_id))
        if not os.path.exists(report_path):
            os.makedirs(report_path)
        try:
            p = subprocess.Popen(
                'pytest {} -vv -s --html={} --self-contained-html'.format(
                    os.path.join(settings.BASE_DIR, 'case_house', case_job.case_path),
                    os.path.join(report_path, report_name)),
                shell=True, stdout=subprocess.PIPE)
            out = p.stdout
            read_data = out.read().decode("utf-8", "ignore")
            case_job.log = read_data
            case_job.report_path = '/media/html-report/{}/{}/{}/{}'.format(project_id, test_plan_uid, task_id,
                                                                           report_name)
            case_result = case_job.log.split('\n')[-2]
            case_job.result = case_result.replace('=', '').strip(' ')
            case_job.state = CaseJobState.FINISH
            case_job.save()
            return True
        except Exception as es:
            logger.error("case job excepted:{}".format(es))
            case_job.state = CaseJobState.FAILED
            case_job.save()
            return False
