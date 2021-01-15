from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import testplan.routing
import case.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            testplan.routing.websocket_urlpatterns
        )
    ),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            case.routing.websocket_urlpatterns
        )
    ),
})
