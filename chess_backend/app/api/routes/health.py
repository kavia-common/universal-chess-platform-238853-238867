from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class HealthResponse(BaseModel):
    """Response payload for health checks."""

    status: str = Field(..., description="Service health status string.")


@router.get(
    "/health",
    summary="Health check",
    description="Simple liveness endpoint. Returns 200 if the service is running.",
    response_model=HealthResponse,
    operation_id="health_check",
)
# PUBLIC_INTERFACE
def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="ok")
