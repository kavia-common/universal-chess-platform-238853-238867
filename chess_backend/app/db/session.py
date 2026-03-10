from __future__ import annotations

from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import get_settings


def _create_engine() -> Optional[Engine]:
    """Create a SQLAlchemy engine if DATABASE_URL is configured."""
    settings = get_settings()
    if not settings.database_url:
        return None
    # Note: For PostgreSQL use `postgresql+psycopg://...` (requires psycopg installed).
    return create_engine(settings.database_url, pool_pre_ping=True, future=True)


_ENGINE: Optional[Engine] = _create_engine()
_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_ENGINE, future=True) if _ENGINE else None


# PUBLIC_INTERFACE
@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Get a database session (scaffold).

    Raises:
        RuntimeError: If DATABASE_URL is not configured.
    """
    if _SessionLocal is None:
        raise RuntimeError("DATABASE_URL is not configured; database session is unavailable.")
    db: Session = _SessionLocal()
    try:
        yield db
    finally:
        db.close()
