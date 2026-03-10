from typing import List

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()

_QUEUE: List[str] = []


class QueueRequest(BaseModel):
    """Request to join the matchmaking queue."""

    user_id: str = Field(..., description="User identifier.")


class QueueResponse(BaseModel):
    """Queue state response."""

    queued_user_ids: List[str] = Field(..., description="Current queue contents.")


@router.post(
    "/queue/join",
    summary="Join matchmaking queue (scaffold)",
    description="Adds a user to an in-memory matchmaking queue.",
    response_model=QueueResponse,
    operation_id="join_queue",
)
# PUBLIC_INTERFACE
def join_queue(body: QueueRequest) -> QueueResponse:
    """Join the matchmaking queue (scaffold)."""
    if body.user_id not in _QUEUE:
        _QUEUE.append(body.user_id)
    return QueueResponse(queued_user_ids=list(_QUEUE))


@router.post(
    "/queue/leave",
    summary="Leave matchmaking queue (scaffold)",
    description="Removes a user from an in-memory matchmaking queue.",
    response_model=QueueResponse,
    operation_id="leave_queue",
)
# PUBLIC_INTERFACE
def leave_queue(body: QueueRequest) -> QueueResponse:
    """Leave the matchmaking queue (scaffold)."""
    if body.user_id in _QUEUE:
        _QUEUE.remove(body.user_id)
    return QueueResponse(queued_user_ids=list(_QUEUE))


@router.get(
    "/queue",
    summary="Get matchmaking queue (scaffold)",
    description="Returns the current in-memory matchmaking queue.",
    response_model=QueueResponse,
    operation_id="get_queue",
)
# PUBLIC_INTERFACE
def get_queue() -> QueueResponse:
    """Get current queue state (scaffold)."""
    return QueueResponse(queued_user_ids=list(_QUEUE))
