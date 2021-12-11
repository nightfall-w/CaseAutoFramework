from django.urls import path

from case.consumers import ResultConsumer

websocket_urlpatterns = [
    path('cap/ws/casepull/result/', ResultConsumer),
]
