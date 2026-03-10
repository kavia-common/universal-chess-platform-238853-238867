from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import Any, DefaultDict, Dict, Set

from fastapi import WebSocket


class ConnectionManager:
    """Manages WebSocket connections grouped by game_id (room)."""

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._rooms: DefaultDict[str, Set[WebSocket]] = defaultdict(set)

    async def connect(self, game_id: str, websocket: WebSocket) -> None:
        """Accept and add a WebSocket to a room."""
        await websocket.accept()
        async with self._lock:
            self._rooms[game_id].add(websocket)

    async def disconnect(self, game_id: str, websocket: WebSocket) -> None:
        """Remove a WebSocket from a room."""
        async with self._lock:
            if game_id in self._rooms and websocket in self._rooms[game_id]:
                self._rooms[game_id].remove(websocket)
            if game_id in self._rooms and not self._rooms[game_id]:
                del self._rooms[game_id]

    async def broadcast(self, game_id: str, message: Dict[str, Any]) -> None:
        """Broadcast a JSON message to all clients in a room."""
        async with self._lock:
            targets = list(self._rooms.get(game_id, set()))
        for ws in targets:
            try:
                await ws.send_json(message)
            except Exception:
                # Best-effort: ignore failures; client will reconnect.
                pass
