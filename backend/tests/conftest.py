"""Shared test fixtures: in-memory engine, transactional session, TestClient."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app

if TYPE_CHECKING:
    from collections.abc import Iterator

    from sqlalchemy import Engine


@pytest.fixture(scope="session")
def engine() -> Iterator[Engine]:
    """Session-wide in-memory SQLite engine shared across connections."""
    eng = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(eng)
    yield eng
    eng.dispose()


@pytest.fixture
def db_session(engine: Engine) -> Iterator[Session]:
    """Per-test session wrapped in a transaction that is rolled back on teardown.

    Each test runs against the shared schema but sees its own writes rolled
    back, keeping tests isolated. ``join_transaction_mode="create_savepoint"``
    lets application code call ``commit()`` without ending the outer
    transaction.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection, join_transaction_mode="create_savepoint")
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session: Session) -> Iterator[TestClient]:
    """TestClient with ``get_db`` overridden to use the transactional session."""

    def override_get_db() -> Iterator[Session]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
