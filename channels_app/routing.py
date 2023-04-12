from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/test_ws/$', consumers.ChannelsConsumer.as_asgi()),
]