# Spec: Backend scaffolding

**Status:** Ready
**Spec ID:** 001
**Owner:** Adam
**Related:** ARCHITECTURE.md, CLAUDE.md, DECISIONS.md

## Goal

Establish the backend foundations — persistent SQLite storage with Alembic
migrations, `.env`-driven configuration via Pydantic Settings, and a Pytest
harness using in-memory SQLite — so subsequent feature specs can add models
and endpoints without touching infrastructure.

## Context

- `backend/app/main.py` — current FastAPI app, only exposes `/health`.
- `backend/pyproject.toml` — uv project, Python 3.14, ruff (`select = ["ALL"]`)
  and mypy already configured. `alembic/` already listed in ruff `exclude`.
- `ARCHITECTURE.md` — sparse; will be updated with the new module layout.
- `CLAUDE.md` — stack: FastAPI, Uvicorn, SQLite, Jinja2 + HTMX + Tailwind
  (frontend arrives in a later spec).

## User-facing behaviour

Infrastructure spec — no direct end-user behaviour. Developer-facing:

- `uv run uvicorn app.main:app` boots against the SQLite file configured in `.env`.
- `uv run alembic upgrade head` applies migrations.
- `uv run pytest` runs against a fresh in-memory SQLite; no on-disk DB is created.
- `GET /health` is extended to also verify DB connectivity (`SELECT 1`).

## Scope

### In scope

- Add dependencies: `sqlalchemy`, `alembic`, `pydantic-settings`, `pytest`,
  `httpx` (for `TestClient`).
- `app/core/config.py` — `Settings` (Pydantic `BaseSettings`) reading from `.env`.
- `app/core/logging.py` — minimal stdlib logging config (level from settings).
- `app/core/errors.py` — one `AppError` + JSON exception handler.
- `app/db/base.py` — `DeclarativeBase` with a `MetaData` naming convention
  (stable Alembic constraint names).
- `app/db/session.py` — engine, `SessionLocal`, `get_db` dependency.
  For in-memory SQLite, use `StaticPool` + `check_same_thread=False` so all
  sessions in a test share the same DB.
- `alembic/` initialised; `env.py` wired to `Base.metadata` and reads
  `database_url` from `Settings` rather than `alembic.ini`.
- `app/main.py` — extend `/health` with a DB ping; register the exception
  handler; configure logging on startup.
- `.env.example` committed; `.env` gitignored.
- `tests/conftest.py` — session-scoped in-memory engine fixture, per-test
  transactional `db_session`, `TestClient` fixture overriding `get_db`.
- `tests/test_health.py`, `tests/test_settings.py`.
- `backend/README.md` — updated with run/test/migrate commands.
- `DECISIONS.md` — ADR: "Sync SQLAlchemy over async" (rationale: SQLite scale,
  simpler fixtures, FastAPI still runs sync routes in a threadpool).

### Out of scope

- CORS middleware (add when the frontend spec lands).
- Pre-commit hooks.
- Auth, users, real domain models (tasks, sessions, journalling).
- Production deployment config, Docker, CI.
- Async DB layer.

## Technical approach

Testing: write `tests/test_settings.py` and `tests/test_health.py` before
wiring the app changes they cover. Commits: atomic and only when
`ruff`, `mypy`, and `pytest` all pass.

**DB style:** Sync SQLAlchemy 2.0. Route handlers may stay `def` or
`async def`; DB sessions are sync and injected via `Depends(get_db)`.

**Layout** (new files marked `+`, modified `~`):

```md
backend/
  .env.example                +
  alembic.ini                 +
  alembic/
    env.py                    +  (imports Settings + Base; target_metadata = Base.metadata)
    script.py.mako            +  (alembic default)
    versions/                 +
  app/
    main.py                   ~  (/health + handlers + logging startup)
    core/
      config.py               +  Settings via pydantic-settings
      logging.py              +  configure_logging()
      errors.py               +  AppError + handler
    db/
      base.py                 +  DeclarativeBase + naming convention
      session.py              +  engine, SessionLocal, get_db
  tests/
    conftest.py               +  engine / db_session / client fixtures
    test_health.py            +
    test_settings.py          +
```

**Config.** `Settings(BaseSettings)` with
`model_config = SettingsConfigDict(env_file=".env", env_prefix="SDONE_", extra="ignore")`.
Fields: `database_url: str = "sqlite:///./sdone.db"`, `log_level: str = "INFO"`,
`env: Literal["dev", "test", "prod"] = "dev"`. Export `get_settings()` cached
with `functools.lru_cache` so tests can override via
`app.dependency_overrides` or by clearing the cache.

**Alembic.** `uv run alembic init alembic`, then edit `env.py` to import
`Settings` and `Base`, set `target_metadata = Base.metadata`, and pull the URL
from settings. Generate an initial empty revision so `alembic upgrade head`
is idempotent from day one.

**Health check.** Inject a session, run `SELECT 1`; return
`{"status": "ok", "db": "ok"}` or a 503 via the shared error envelope on
failure.

**Test harness.** Session-scoped in-memory engine:
`create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)`.
`Base.metadata.create_all(engine)` at session start (Alembic itself is
validated locally / in future CI, not on every test). Per-test `db_session`
opens a transaction and rolls back on teardown. The `client` fixture sets
`app.dependency_overrides[get_db] = lambda: db_session`.

## Data model / API contract

No new endpoints. `/health` is extended:

```md
GET /health
Response: 200 { "status": "ok", "db": "ok" }
          503 { "error": { "code": "db_unavailable", "message": "..." } }
```

Error envelope (used by `AppError` handler and any future 4xx/5xx):

```md
{ "error": { "code": string, "message": string } }
```

## Acceptance criteria

- [ ] `uv sync` installs `sqlalchemy`, `alembic`, `pydantic-settings`, `pytest`, `httpx`.
- [ ] `uv run uvicorn app.main:app` boots without errors against a fresh SQLite file.
- [ ] `uv run alembic revision --autogenerate -m "init"` produces a valid (empty) migration;
      `uv run alembic upgrade head` applies it.
- [ ] `uv run pytest` passes; no `sdone.db` artefact is created by the test run.
- [ ] `GET /health` returns `{"status":"ok","db":"ok"}` in the happy path
      (integration test via `TestClient`) and 503 with the error envelope
      when the DB dependency raises.
- [ ] `Settings` loads values from `.env` — test monkeypatches
      `SDONE_DATABASE_URL` and asserts the override is picked up.
- [ ] `.env` is gitignored; `.env.example` is committed.
- [ ] `uv run ruff check` and `uv run mypy .` pass on all new code.
- [ ] `DECISIONS.md` contains an ADR entry for sync-vs-async SQLAlchemy.
- [ ] `ARCHITECTURE.md` reflects the new module layout.
- [ ] `backend/README.md` documents run, test, and migrate commands.

## Open questions

- SQLite file location: default to `backend/sdone.db` (repo-relative from the
  `backend/` working directory). Revisit if a deploy path forces otherwise.

## Implementation plan

1. **Deps + settings + logging skeleton.** `uv add` the new dependencies;
   create `core/config.py`, `core/logging.py`, `.env.example`; update
   `.gitignore`. Add `tests/test_settings.py`. Commit.
2. **DB layer.** `db/base.py`, `db/session.py`. No models yet. Commit.
3. **Alembic init.** `uv run alembic init alembic`; wire `env.py` to
   `Settings` + `Base.metadata`; generate initial empty revision. Commit.
4. **Health + errors.** Extend `/health` with a DB ping; add `core/errors.py`
   and register the handler in `main.py`; wire `configure_logging()` at
   import time. Add `tests/test_health.py` covering the 200 and 503 paths.
   Commit.
5. **Test harness polish.** Finalise `conftest.py` fixtures
   (session engine, per-test transactional `db_session`, `client` with
   `get_db` override).
6. **Docs.** Update `backend/README.md`, append the sync-SQLAlchemy ADR to
   `DECISIONS.md`, refresh `ARCHITECTURE.md` with the module layout. Commit.
