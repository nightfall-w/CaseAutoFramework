import asyncio
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache

from case.models import GitCaseModel, GitlabModel
from utils.encryption import decrypt_token


class ResultConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        await self.close()

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
        except json.decoder.JSONDecodeError:
            await self.send(text_data=json.dumps({"success": False, "error": "Illegal data type"}))
            return False
        while True:
            token = text_data_json.get('token')
            project_id = text_data_json.get('project_id')
            branch_name = text_data_json.get('branch_name')
            if not all([token, project_id, branch_name]):
                await self.send(text_data=json.dumps({"success": False, "error": "Missing required parameters"}))
                return False
            else:
                private_token = decrypt_token(token)
                cache_key = "private_token:" + private_token + "-" + "project_id:" + str(
                    project_id) + "-" + "branch_name:" + branch_name
                branch_status = cache.get(cache_key)
                progress = cache.get(cache_key + "progress")
                if progress == 100:
                    cache.set(cache_key + "progress", 0, 1)
                if not branch_status:
                    await asyncio.sleep(2)
                    # 缓存中没有值 从mysql读取
                    gitlab_info = GitlabModel.objects.filter(private_token=private_token).first()
                    branch_status = GitCaseModel.objects.filter(gitlab_url=gitlab_info.gitlab_url,
                                                                gitlab_project_id=project_id,
                                                                branch_name=branch_name).first().status
                response_data = {"project_id": project_id, "branch_name": branch_name, "status": branch_status,
                                 "progress": progress}
                await self.send(text_data=json.dumps(response_data))
                await asyncio.sleep(2)
