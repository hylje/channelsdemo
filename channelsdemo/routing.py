from channels.routing import route

from channelsdemo.main.consumers import (
    ws_add_board,
    ws_add_thread,
    ws_disconnect_board,
    ws_disconnect_thread
)

channel_routing = [
    route("websocket.connect", ws_add_board, path=r"^/board/$"),
    route("websocket.connect", ws_add_thread, path="^/thread/(?P<thread_id>\d+)/$"),
    route("websocket.disconnect", ws_disconnect_board, path=r"^/board/$"),
    route("websocket.disconnect", ws_disconnect_thread, path="^/thread/(?P<thread_id>\d+)/$"),
]
