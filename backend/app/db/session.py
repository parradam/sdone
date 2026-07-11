"""Database engine, session factory, and FastAPI session dependency."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

if TYPE_CHECKING:
    from collections.abc import Iterator

settings = get_settings()

# ``check_same_thread`` must be disabled for SQLite because FastAPI may run a
# sync route (and its session) in a threadpool worker. Harmless for other
# backends, but only added when talking to SQLite.
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}

engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Iterator[Session]:
    """Yield a database session, closing it when the request finishes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
