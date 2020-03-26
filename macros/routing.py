from channels.routing import ProtocolTypeRouter

from django.urls import re_path

from . import consumers


application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
})


websocket_urlpatterns = [
    re_path(r'ws/macros/updates/$', consumers.PlayConsumer),
]
