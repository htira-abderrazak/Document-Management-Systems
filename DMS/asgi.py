"""
ASGI config for DMS project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from DMS.routing import websocket_urlpatterns  

# Ensure django.setup() is called before anything else.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DMS.settings')
django.setup()  # ✅ this must come BEFORE importing any models/middleware


from user.middleware import JWTAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DMS.settings')

django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})