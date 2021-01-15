from django.urls import path
from case.consumers import ResultConsumer

websocket_urlpatterns = [
    path('ws/casepull/result/', ResultConsumer),
]
