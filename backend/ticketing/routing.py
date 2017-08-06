from channels.routing import include

channel_routing = [
    include("users.routing.channel_routing", path=r"^/users"),
]