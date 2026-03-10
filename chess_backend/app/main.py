"""
FastAPI application entrypoint for the Universal Chess Platform backend.

This scaffold exposes:
- REST API under /api/v1 (see routers)
- WebSocket endpoint at /ws for real-time game synchronization

The WebSocket interface isn't represented in OpenAPI; see GET /docs/websocket for usage.
"""

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from app.api.router import api_router
from app.core.logging import configure_logging
from app.core.settings import get_settings
from app.ws.endpoints import websocket_game_sync

openapi_tags = [
    {"name": "Health", "description": "Service health and readiness checks."},
    {"name": "Auth", "description": "User authentication and profile endpoints (scaffold)."},
    {"name": "Matchmaking", "description": "Online matchmaking queue endpoints (scaffold)."},
    {"name": "Games", "description": "Game state retrieval and move submission endpoints (scaffold)."},
    {"name": "Docs", "description": "Additional documentation endpoints."},
    {"name": "WebSocket", "description": "Real-time game synchronization (documented via /docs/websocket)."},
]


def _configure_cors(app: FastAPI) -> None:
    """Configure CORS based on Settings."""
    settings = get_settings()
    allow_origins = settings.allowed_origins or ["*"]
    allow_methods = settings.allowed_methods or ["*"]
    allow_headers = settings.allowed_headers or ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=allow_methods,
        allow_headers=allow_headers,
        max_age=settings.cors_max_age,
    )


# PUBLIC_INTERFACE
def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    settings = get_settings()
    configure_logging("INFO")

    app = FastAPI(
        title=settings.app_name,
        description=(
            "Backend API for the Universal Chess Platform. "
            "Includes scaffold endpoints for auth/matchmaking/games and a WebSocket for real-time sync."
        ),
        version=settings.version,
        openapi_tags=openapi_tags,
    )

    if settings.trust_proxy:
        # Trust X-Forwarded-* headers from reverse proxies in hosted deployments.
        app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

    _configure_cors(app)

    app.include_router(api_router)

    @app.get(
        "/",
        summary="API root",
        description="Returns basic service metadata.",
        operation_id="api_root",
        tags=["Health"],
    )
    # PUBLIC_INTERFACE
    def root() -> JSONResponse:
        """API root endpoint with basic metadata."""
        return JSONResponse(
            {
                "name": settings.app_name,
                "version": settings.version,
                "environment": settings.environment,
                "rest_base": "/api/v1",
                "websocket": "/ws (see /docs/websocket)",
            }
        )

    @app.websocket("/ws")
    async def ws_endpoint(websocket: WebSocket) -> None:
        """WebSocket endpoint for real-time game sync.

        Query parameters:
          - game_id: Required room identifier.
          - client_id: Optional client identifier (defaults to 'anonymous').

        For detailed usage instructions see: GET /docs/websocket
        """
        game_id = websocket.query_params.get("game_id")
        client_id = websocket.query_params.get("client_id") or "anonymous"
        if not game_id:
            await websocket.accept()
            await websocket.send_json({"type": "error", "error": "Missing required query param: game_id"})
            await websocket.close(code=1008)
            return
        await websocket_game_sync(websocket=websocket, game_id=game_id, client_id=client_id)

    return app


app = create_app()
