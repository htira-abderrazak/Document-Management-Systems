# routing.py

from django.urls import re_path
from user.consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<user_id>[^/]+)/$', ChatConsumer.as_asgi()),
]
