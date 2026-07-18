"""Page routes that render the app shell."""

from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.templating import templates

router = APIRouter()


def _today_label() -> str:
    """Human-readable date for the header (no leading zero, portable)."""
    now = datetime.now(tz=UTC)
    return f"{now:%A}, {now.day} {now:%B %Y}"


@router.get("/", response_class=HTMLResponse)
def today(request: Request) -> HTMLResponse:
    """Render the app shell with the placeholder Today page.

    Annotated ``-> HTMLResponse`` (the runtime base class of Jinja2's
    ``_TemplateResponse``) so FastAPI treats it as a Response and does not try
    to build an OpenAPI schema from the return type.
    """
    return templates.TemplateResponse(
        request,
        "pages/today.html",
        {"page_title": "Today", "page_date": _today_label(), "active": "today"},
    )
