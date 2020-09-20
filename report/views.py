# -*- coding:utf-8 -*-
import json
from automation.settings import logger

from dwebsocket.decorators import accept_websocket


@accept_websocket
def case_report(request):
    if request.is_websocket():
        # websocket请求处理
        while True:
            try:
                msg = request.websocket.wait()
                print(str(msg, encoding="utf-8"))
                request.websocket.send(json.dumps(eval(msg)))
            except Exception as es:
                logger.error(es)
                continue
    else:
        # TODO http请求处理
        pass


@accept_websocket
def interface_report(request):
    if request.is_websocket():
        # websocket请求处理
        while True:
            try:
                msg = request.websocket.wait()
                print(str(msg, encoding="utf-8"))
                request.websocket.send(json.dumps(eval(msg)))
            except Exception as es:
                logger.error(es)
                continue
    else:
        # TODO http请求处理
        pass
