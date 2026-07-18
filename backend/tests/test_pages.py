"""Integration tests for the app shell pages."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

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
