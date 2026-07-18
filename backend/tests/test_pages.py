"""Integration tests for the app shell pages."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest

from app.main import STATIC_DIR

if TYPE_CHECKING:
    from fastapi.testclient import TestClient

NAV_LABELS = (
    "Today",
    "Tasks",
    "Calendar",
    "Journal",
    "Achievements",
    "Statistics",
    "Resources",
)


def test_home_renders_shell(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.headers["content-type"].startswith("text/html")
    body = response.text
    for label in NAV_LABELS:
        assert label in body


def test_home_journal_link(client: TestClient) -> None:
    response = client.get("/")
    assert 'href="/journal"' in response.text


def test_app_css_served_when_built(client: TestClient) -> None:
    if not (STATIC_DIR / "app.css").exists():
        pytest.skip("app.css not built; run `npm run build:css`")
    response = client.get("/static/app.css")
    assert response.status_code == HTTPStatus.OK
    assert "text/css" in response.headers["content-type"]


def test_htmx_vendored_and_served(client: TestClient) -> None:
    response = client.get("/static/js/htmx.min.js")
    assert response.status_code == HTTPStatus.OK
    assert "javascript" in response.headers["content-type"]


def test_home_includes_htmx(client: TestClient) -> None:
    response = client.get("/")
    assert "/static/js/htmx.min.js" in response.text


def test_openapi_schema_available(client: TestClient) -> None:
    # Regression: an HTML page route annotated with an unresolved response type
    # used to break OpenAPI schema generation.
    response = client.get("/openapi.json")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["openapi"]
