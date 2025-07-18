# routing.py

from django.urls import re_path
from user.consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r'chat/', ChatConsumer.as_asgi()),
]
