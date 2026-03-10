from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get(
    "/docs/websocket",
    summary="WebSocket usage help",
    description="Returns instructions for connecting to the backend WebSocket endpoint used for real-time game sync.",
    response_class=PlainTextResponse,
    operation_id="websocket_usage_help",
)
# PUBLIC_INTERFACE
def websocket_usage_help() -> PlainTextResponse:
    """Describe how to use the WebSocket endpoint.

    The WebSocket interface isn't represented in OpenAPI; this endpoint documents it explicitly.
    """
    text = """Universal Chess Platform — WebSocket

Endpoint:
  WS /ws?game_id=<game_id>&client_id=<any>

Usage:
  - Connect and send JSON messages.
  - Supported message shape (scaffold):
      {"type":"ping"}
      {"type":"broadcast","game_id":"game_1","payload":{"hello":"world"}}

Behavior:
  - Connections are grouped by game_id.
  - Messages of type "broadcast" are forwarded to all clients in that game room.
  - This is a scaffold; authentication and authoritative game state sync will be added later.
"""
    return PlainTextResponse(text)
