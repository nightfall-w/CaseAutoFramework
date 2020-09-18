# -*- coding:utf-8 -*-
from abc import abstractmethod, ABCMeta
from json import JSONDecodeError

from automation.settings import logger
from interface.models import InterfaceJobModel
from testplan.models import CaseTestPlanTaskModel, CaseJobModel, ApiTestPlanTaskModel


class StatusManager(metaclass=ABCMeta):

    @abstractmethod
    def get_task_result(self, test_plan_uid): pass

    @abstractmethod
    def get_job_result(self, task_id): pass


class CaseStatusManager(StatusManager):

    def get_task_result(self, case_test_plan_uid):
        return CaseTestPlanTaskModel.objects.filter(test_plan_uid=case_test_plan_uid).values('test_plan_uid', 'id',
                                                                                             'state',
                                                                                             'finish_num')

    def get_job_result(self, case_task_id):
        return CaseJobModel.objects.filter(case_task_id=case_task_id).values('id', 'state', 'result', 'report_path')


class ApiStatusManager(StatusManager):
    def get_task_result(self, api_test_plan_uid):
        return ApiTestPlanTaskModel.objects.filter(test_plan_uid=api_test_plan_uid).values('test_plan_uid', 'state',
                                                                                           'success_num', 'failed_num')

    def get_job_result(self, api_task_id):
        return InterfaceJobModel.objects.filter(api_test_plan_task_id=api_task_id).values('interface_id',
                                                                                          'test_plan_id',
                                                                                          'api_test_plan_task_id',
                                                                                          'state',
                                                                                          'result')


def adapter(receive_data):
    mode_type = receive_data.get('mode_type')
    task_or_job = receive_data.get('task_or_job')
    try:
        if mode_type not in ['api', 'case'] or task_or_job not in ['task', 'job']:
            error_data = 'Illegal parameter value: {}, {}'.format(mode_type, task_or_job)
            logger.error(error_data)
            send_msg = {"success": False, "error": error_data}
            return send_msg
        elif mode_type == "api":
            if task_or_job == "job":
                result = ApiStatusManager().get_job_result(receive_data.get('task_id'))
            if task_or_job == "task":
                result = ApiStatusManager().get_task_result(receive_data.get('test_plan_uid'))
        elif mode_type == "case":
            if task_or_job == "job":
                result = CaseStatusManager().get_job_result(receive_data.get('task_id'))
            if task_or_job == "task":
                result = CaseStatusManager().get_task_result(receive_data.get('test_plan_uid'))
        else:
            error_data = 'Illegal parameter value： {}'.format(mode_type)
            logger.error(error_data)
            send_msg = {"success": False, "error": error_data}
            return send_msg
        return {"success": True, "data": result}
    except (JSONDecodeError, TypeError) as es:
        logger.error(es)
        send_msg = {"success": False, "error": str(es)}
        return send_msg
    except Exception as es:
        logger.error(es)
        send_msg = {"success": False, "error": str(es)}
        return send_msg
