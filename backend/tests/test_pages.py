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
