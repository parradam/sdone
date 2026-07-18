# Architecture

## Pages

- `/` — Today (the app shell landing page)
- `/journal` — Interstitial journal (planned, spec 003)

## Backend module layout

```
backend/
  package.json           Tailwind CLI toolchain (build:css / watch:css)
  tailwind.config.js     fonts + colour tokens + template/JS content globs
  alembic/               Database migrations (env.py wired to Settings + Base.metadata)
    versions/            Migration revisions
  app/
    main.py              FastAPI app: /health (DB ping), /static mount, routers, handler + logging
    templating.py        shared Jinja2Templates instance
    core/
      config.py          Settings (pydantic-settings) + cached get_settings()
      logging.py         configure_logging()
      errors.py          AppError + JSON error-envelope handler
    db/
      base.py            DeclarativeBase + constraint naming convention
      session.py         engine, SessionLocal, get_db dependency
    routers/
      pages.py           GET / — the app shell (Today)
    templates/
      base.html          app shell layout (sidebar, header, footer; title/header/content blocks)
      pages/today.html   placeholder Today page
    static/
      css/input.css      Tailwind entry (OKLCH tokens, quiet scrollbars, pulse/rise, reduced-motion)
      app.css            built Tailwind output (gitignored; `npm run build:css`)
      js/htmx.min.js     vendored HTMX (pinned)
  tests/
    conftest.py          in-memory engine, transactional db_session, client fixtures
    test_health.py       /health 200 + 503 paths
    test_settings.py     settings defaults + env override
    test_pages.py        app shell render + static assets
```

Persistence is sync SQLAlchemy 2.0 over SQLite (see `DECISIONS.md`, ADR-001).
The shared error envelope is `{"error": {"code": ..., "message": ...}}`.

The frontend is server-rendered Jinja2 templates with HTMX for interactivity and
a compiled Tailwind CSS build (see `DECISIONS.md`, ADR-002).

## Status

Setup
