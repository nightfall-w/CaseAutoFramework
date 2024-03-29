from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import case.routing
import testplan.routing

routingList = []
routingList.extend(testplan.routing.websocket_urlpatterns)
routingList.extend(case.routing.websocket_urlpatterns)

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routingList
        )
    ),
})
