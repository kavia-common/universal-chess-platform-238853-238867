# Chess Backend (FastAPI) — Scaffold

This directory contains the FastAPI backend scaffold for the Universal Chess Platform. It provides:

- REST API under `/api/v1` (health, auth, matchmaking, games) — currently scaffold/placeholder behavior
- WebSocket endpoint at `/ws` for real-time game synchronization (room-based)
- Centralized settings via environment variables (CORS, host/port, proxy trust, etc.)
- OpenAPI metadata + tagged routers, plus an extra docs endpoint for WebSocket usage (`/docs/websocket`)

## Quick start (local dev)

1) Create and activate a virtualenv
```bash
python -m venv .venv
source .venv/bin/activate
```

2) Install dependencies
```bash
pip install -r requirements.txt
```

3) Export environment variables

This project expects environment variables to be set (your platform/orchestrator may load them automatically).
If you want to load from the provided `.env` manually in your shell:
```bash
set -a
source .env
set +a
```

4) Run the API
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 3001
```

## API docs

- Swagger UI: `GET /docs`
- OpenAPI JSON: `GET /openapi.json`
- WebSocket usage help: `GET /docs/websocket`

## Notes

- Database integration is scaffolded (SQLAlchemy engine/session) but not yet wired into endpoints.
  Set `DATABASE_URL` to connect to PostgreSQL (recommended) or SQLite for development.
- Auth endpoints are placeholders and not production-ready (no password hashing, etc.).
- Chess move validation/checkmate logic is not implemented in this scaffold; game endpoints store minimal state in memory.
