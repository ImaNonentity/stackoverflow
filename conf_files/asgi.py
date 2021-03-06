"""
ASGI config for conf_files project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

import chat
from chat import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf_files.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
  "http": django_asgi_app,
  "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        )
    ),
})

# application = ProtocolTypeRouter({
#   'http': get_asgi_application(),
#   'websocket': URLRouter(
#       chat.routing.websocket_urlpatterns
#     ),
# })
