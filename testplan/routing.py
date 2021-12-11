from django.urls import path

from testplan.consumers import ResultConsumer

websocket_urlpatterns = [
    path('cap/ws/testplan/result/', ResultConsumer),
]
