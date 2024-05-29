"""
ASGI config for planner project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Added for django channels routing
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from todos.consumers import TestConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "planner.settings")

application = get_asgi_application()

# added for django channels ---------------->
ws_patterns = [
    path("ws/test/", TestConsumer.as_asgi()),
]

application = ProtocolTypeRouter(
    {
        # handle http requests
        "http": get_asgi_application(),
        # handle websocket requests
        "websocket": AuthMiddlewareStack(URLRouter(ws_patterns)),
    }
)
