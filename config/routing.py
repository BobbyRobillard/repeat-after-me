from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import macros.routing


application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        "websocket": AuthMiddlewareStack(
            URLRouter(macros.routing.websocket_urlpatterns)
        )
    }
)
