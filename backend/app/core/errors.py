"""Application error type and its JSON exception handler.

All handled errors serialise to a single envelope::

    {"error": {"code": <str>, "message": <str>}}
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from fastapi.responses import JSONResponse

if TYPE_CHECKING:
    from fastapi import Request


class AppError(Exception):
    """An error that should be rendered as the shared JSON error envelope."""

    def __init__(self, code: str, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code


async def app_error_handler(request: Request, exc: Exception) -> JSONResponse:  # noqa: ARG001
    """Render an :class:`AppError` as the shared error envelope.

    Typed with ``Exception`` to satisfy Starlette's handler signature; only
    registered for :class:`AppError`, so the cast is safe.
    """
    err = cast("AppError", exc)
    return JSONResponse(
        status_code=err.status_code,
        content={"error": {"code": err.code, "message": err.message}},
    )
