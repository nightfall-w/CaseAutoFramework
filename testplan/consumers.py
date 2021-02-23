import asyncio
import json

from channels.generic.websocket import AsyncWebsocketConsumer

from automation.settings import logger
from testplan.result import CaseStatusManager, ApiStatusManager
from utils.data_processor import DateEncoder


class ResultConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        await self.close()

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            print(text_data_json)
        except json.decoder.JSONDecodeError:
            await self.send(text_data=json.dumps({"success": False, "error": "Illegal data type"}))
            return False
        while True:
            try:
                mode_type = text_data_json.get('mode_type')
                task_or_job = text_data_json.get('task_or_job')
                value = text_data_json.get('value')
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
                    if task_or_job == "task":
                        result = await ApiStatusManager().get_task_result(value)
                        msg = {"success": True, "mode": "task", "data": list(result)}
                    elif task_or_job == "job":
                        result = await ApiStatusManager().get_job_result(value)
                        msg = {"success": True, "mode": "job", "data": list(result)}
                elif mode_type == "case":
                    if task_or_job == "task":
                        result = await CaseStatusManager().get_task_result(value)
                        msg = {"success": True, "mode": "task", "data": list(result)}
                    elif task_or_job == "job":
                        result = await CaseStatusManager().get_job_result(value)
                        msg = {"success": True, "mode": "job", "data": list(result)}
                else:
                    error_data = 'Illegal parameter value： {}'.format(mode_type)
                    logger.error(error_data)
                    msg = {"success": False, "error": error_data}
            except Exception as es:
                logger.error(str(es))
                msg = {"success": False, "error": str(es)}
            await self.send(json.dumps(msg, cls=DateEncoder))
            await asyncio.sleep(5)
