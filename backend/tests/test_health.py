"""Integration tests for the /health endpoint."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_db
from app.main import app

if TYPE_CHECKING:
    from collections.abc import Iterator

    from fastapi.testclient import TestClient


def test_health_ok(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "ok", "db": "ok"}


def test_health_db_unavailable(client: TestClient) -> None:
    class BrokenSession:
        def execute(self, *_args: object, **_kwargs: object) -> object:
            raise SQLAlchemyError

        def close(self) -> None:
            pass

    def broken_get_db() -> Iterator[object]:
        yield BrokenSession()

    app.dependency_overrides[get_db] = broken_get_db

    response = client.get("/health")

    assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE
    assert response.json() == {
        "error": {
            "code": "db_unavailable",
            "message": "Database connectivity check failed.",
        },
    }
