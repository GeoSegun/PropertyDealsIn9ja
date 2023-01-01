"""
ASGI config for propertyDealsIn9ja project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from apps.chats import consumers


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'propertyDealsIn9ja.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/<str:username>/', consumers.PersonalChatConsumer.as_asgi()),
            # path('ws/<str:username>', consumers.EchoConsumer.as_asgi()),
        ]),
    )
})