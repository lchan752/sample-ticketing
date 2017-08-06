from channels.routing import route
from users.consumers import on_connect, on_disconnect

channel_routing = [
    route("websocket.connect", on_connect, path=r"/(?P<user_id>\d+)/$"),
    route("websocket.disconnect", on_disconnect, path=r"/(?P<user_id>\d+)/$"),
]
