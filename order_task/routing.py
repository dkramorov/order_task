from channels.routing import ProtocolTypeRouter, URLRouter
from channels_app.routing import websockets

application = ProtocolTypeRouter({
    'websocket': websockets,
})