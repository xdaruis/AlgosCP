from django.core.wsgi import get_wsgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from . import consumers

application = ProtocolTypeRouter({
    "http": get_wsgi_application(),
    "websocket": URLRouter([
        path("ws/solution/", consumers.SolutionConsumer.as_asgi()),
    ]),
})