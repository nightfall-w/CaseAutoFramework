# -*- coding=utf-8 -*-
import json

import requests
from Logger import logger
from interface.models import InterfaceJobModel, InterfaceModel
from testplan.models import ApiTestPlanModel
from utils.job_status_enum import ApiJobState, ApiTestPlanState


class ApiRunner:
    def __init__(self, test_plan_id):
        self.test_plan_id = test_plan_id
        self.session = requests.session()

    def dispose_response(self, interface, response):
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
