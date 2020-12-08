from channels.routing import ProtocolTypeRouter

from django.urls import re_path

from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/macros/', consumers.SettingsConsumer.as_asgi()),
]
