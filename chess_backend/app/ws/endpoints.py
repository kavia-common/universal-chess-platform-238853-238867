from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import WebSocket, WebSocketDisconnect

from app.ws.connection_manager import ConnectionManager

manager = ConnectionManager()


async def _safe_receive_json(websocket: WebSocket) -> Optional[Dict[str, Any]]:
    """Receive JSON from the websocket, returning None on invalid payloads."""
    try:
        data = await websocket.receive_json()
        if isinstance(data, dict):
            return data
        return None
    except Exception:
        return None


# PUBLIC_INTERFACE
async def websocket_game_sync(websocket: WebSocket, game_id: str, client_id: str) -> None:
    """WebSocket handler for real-time game synchronization (scaffold).

    Query params:
      - game_id: Room identifier (required)
      - client_id: Client identifier (optional; for debugging/logging)

    Supported incoming messages (scaffold):
      - {"type":"ping"} -> responds {"type":"pong"}
      - {"type":"broadcast","game_id":"...","payload":{...}} -> relayed to all clients in room

    This is a scaffold; authentication and authoritative state synchronization will be implemented later.
    """
    await manager.connect(game_id=game_id, websocket=websocket)
    try:
        await websocket.send_json({"type": "welcome", "game_id": game_id, "client_id": client_id})

        while True:
            msg = await _safe_receive_json(websocket)
            if not msg:
                await websocket.send_json({"type": "error", "error": "Invalid JSON message"})
                continue

            msg_type = str(msg.get("type", "")).lower()
            if msg_type == "ping":
                await websocket.send_json({"type": "pong"})
                continue

            if msg_type == "broadcast":
                payload = msg.get("payload", {})
                await manager.broadcast(
                    game_id=game_id,
                    message={"type": "broadcast", "from": client_id, "game_id": game_id, "payload": payload},
                )
                continue

            await websocket.send_json({"type": "error", "error": f"Unsupported message type: {msg_type}"})

    except WebSocketDisconnect:
        # Client disconnected
        pass
    finally:
        await manager.disconnect(game_id=game_id, websocket=websocket)
