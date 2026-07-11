from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.errors import AppError, app_error_handler
from app.core.logging import configure_logging
from app.db.session import get_db

configure_logging()

app = FastAPI(title="Sdone")
app.add_exception_handler(AppError, app_error_handler)

DbSession = Annotated[Session, Depends(get_db)]


@app.get("/health")
def health(db: DbSession) -> dict[str, str]:
    """Liveness check that also verifies database connectivity."""
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise AppError(
            code="db_unavailable",
            message="Database connectivity check failed.",
            status_code=503,
        ) from exc
    return {"status": "ok", "db": "ok"}
