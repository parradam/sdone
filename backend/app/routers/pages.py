"""Page routes that render the app shell."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.templating import templates

if TYPE_CHECKING:
    from starlette.templating import _TemplateResponse

router = APIRouter()


def _today_label() -> str:
    """Human-readable date for the header (no leading zero, portable)."""
    now = datetime.now(tz=UTC)
    return f"{now:%A}, {now.day} {now:%B %Y}"


@router.get("/", response_class=HTMLResponse)
def today(request: Request) -> _TemplateResponse:
    """Render the app shell with the placeholder Today page."""
    return templates.TemplateResponse(
        request,
        "pages/today.html",
        {"page_title": "Today", "page_date": _today_label(), "active": "today"},
    )
