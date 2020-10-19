import json
import time
from channels.generic.websocket import WebsocketConsumer

from testplan.result import adapter


class ResultConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        self.close()

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
        except json.decoder.JSONDecodeError:
            self.send(text_data=json.dumps({"success": False, "error": "Illegal data type"}))
            return False
        while True:
            send_msg = adapter(text_data_json)
            self.send(text_data=json.dumps(send_msg))
            time.sleep(1)
