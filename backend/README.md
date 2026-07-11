# Sdone — backend

Sdone (a contraction of "it's done") is a web application for task tracking.
This is the FastAPI backend.

## Requirements

- Python 3.14
- [uv](https://docs.astral.sh/uv/) for dependency management

## Setup

```sh
uv sync
cp .env.example .env   # then edit as needed
```

Configuration is read from `.env` (variables use the `SDONE_` prefix). See
`.env.example` for the available settings.

## Run

```sh
uv run uvicorn app.main:app --reload
```

`GET /health` returns `{"status": "ok", "db": "ok"}` and verifies database
connectivity.

## Test

```sh
uv run pytest
```

Tests run against an in-memory SQLite database; no on-disk `sdone.db` is
created by the test run.

## Migrate

```sh
uv run alembic upgrade head          # apply migrations
uv run alembic revision --autogenerate -m "message"   # create a new migration
```

The database URL comes from application settings (`app.core.config.Settings`),
not `alembic.ini`.

## Lint & type-check

```sh
uv run ruff check .
uv run mypy .
```
