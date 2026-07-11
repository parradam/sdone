# Architecture

## Pages

`/` - Home

## Backend module layout

```
backend/
  alembic/               Database migrations (env.py wired to Settings + Base.metadata)
    versions/            Migration revisions
  app/
    main.py              FastAPI app: /health (DB ping), handler + logging wiring
    core/
      config.py          Settings (pydantic-settings) + cached get_settings()
      logging.py         configure_logging()
      errors.py          AppError + JSON error-envelope handler
    db/
      base.py            DeclarativeBase + constraint naming convention
      session.py         engine, SessionLocal, get_db dependency
  tests/
    conftest.py          in-memory engine, transactional db_session, client fixtures
    test_health.py       /health 200 + 503 paths
    test_settings.py     settings defaults + env override
```

Persistence is sync SQLAlchemy 2.0 over SQLite (see `DECISIONS.md`, ADR-001).
The shared error envelope is `{"error": {"code": ..., "message": ...}}`.

## Status

Setup
