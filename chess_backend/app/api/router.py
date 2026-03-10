from fastapi import APIRouter

from app.api.routes import auth, docs, games, health, matchmaking

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(matchmaking.router, prefix="/matchmaking", tags=["Matchmaking"])
api_router.include_router(games.router, prefix="/games", tags=["Games"])
api_router.include_router(docs.router, tags=["Docs"])
