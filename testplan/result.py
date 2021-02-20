# -*- coding:utf-8 -*-
from abc import abstractmethod, ABCMeta

from automation.settings import logger
from interface.models import InterfaceJobModel
from testplan.models import CaseTestPlanTaskModel, CaseJobModel, ApiTestPlanTaskModel


class StatusManager(metaclass=ABCMeta):

    @abstractmethod
    def get_task_result(self, test_plan_uid): pass

    @abstractmethod
    def get_job_result(self, task_id): pass


class CaseStatusManager(StatusManager):

    def get_task_result(self, request_data):
        return CaseTestPlanTaskModel.objects.filter(test_plan_uid=request_data.get('case_test_plan_uid')).order_by(
            '-id').values(
            'test_plan_uid', 'id', 'state',
            'finish_num', 'create_date', 'used_time')[request_data.get('offset'):request_data.get('limit')]

    def get_job_result(self, request_data):
        return CaseJobModel.objects.filter(case_task_id=request_data.get('case_task_id')).values('id', 'state',
                                                                                                 'result',
                                                                                                 'report_path')


class ApiStatusManager(StatusManager):
    def get_task_result(self, api_test_plan_uid):
        return ApiTestPlanTaskModel.objects.filter(test_plan_uid=api_test_plan_uid).order_by('-id').values(
            'test_plan_uid', 'state',
            'success_num', 'failed_num')

    def get_job_result(self, api_task_id):
        return InterfaceJobModel.objects.filter(api_test_plan_task_id=api_task_id).values('interface_id',
                                                                                          'test_plan_id',
                                                                                          'api_test_plan_task_id',
                                                                                          'state',
                                                                                          'result')


def adapter(receive_data):
    try:
        mode_type = receive_data.get('mode_type')
        task_or_job = receive_data.get('task_or_job')
        value = receive_data.get('value')
    except AttributeError as es:
        logger.error(str(es))
        send_msg = {"success": False, "error": str(es)}
        return send_msg
    try:
        if mode_type not in ['api', 'case'] or task_or_job not in ['task', 'job'] or not value:
            error_data = 'Illegal parameter value: {}, {}'.format(mode_type, task_or_job)
            logger.error(error_data)
            send_msg = {"success": False, "error": error_data}
            return send_msg
        elif mode_type == "api":
            result = ApiStatusManager().get_task_result(value)
        elif mode_type == "case":
            result = CaseStatusManager().get_task_result(value)
        else:
            error_data = 'Illegal parameter value： {}'.format(mode_type)
            logger.error(error_data)
            send_msg = {"success": False, "error": error_data}
            return send_msg
        return {"success": True, "mode": "task", "data": list(result)}
    except Exception as es:
        logger.error(str(es))
        send_msg = {"success": False, "error": str(es)}
        return send_msg
