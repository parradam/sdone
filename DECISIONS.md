# Decisions

A lightweight log of non-obvious technical choices. Append a new entry whenever
you (or Claude) make a decision that someone would later ask "why did we do it
this way?" about. Newest at the top. Never edit or delete past entries — if a
decision is reversed, add a new one that supersedes it and link back.

**When to log:** picking a library, choosing a pattern, rejecting an obvious
alternative, a trade-off with real consequences. **When not to:** routine,
self-evident choices with no real alternative.

Format per entry:

- **ID** — sequential, `ADR-NNN`
- **Date** — ISO `YYYY-MM-DD`
- **Status** — Accepted | Superseded by ADR-NNN | Deprecated
- **Context** — the forces at play; what made this a decision rather than a default
- **Decision** — what was chosen, stated plainly
- **Alternatives** — what was rejected and why
- **Consequences** — what this makes easier, harder, or locks us into

---

## ADR-002 — Frontend: server-rendered Jinja2 + HTMX, compiled Tailwind, vendored assets

- **Date** — 2026-07-18
- **Status** — Accepted
- **Context** — The app shell (spec 004) is the first frontend work and sets the
  conventions later feature pages reuse. The design mockups used the Tailwind
  Play CDN and Google-hosted scripts, which is fine for static mockups but not
  for a served app (unpurged CSS, a runtime dependency on third-party CDNs, and
  version drift).
- **Decision** — Server-render Jinja2 templates, use HTMX for interactivity, and
  compile Tailwind via the CLI (`npm run build:css` → `app/static/app.css`,
  gitignored). Vendor a pinned `htmx.min.js` under `app/static/js/`. Assets are
  served by FastAPI's `StaticFiles`; there is no separate frontend server or JS
  bundler.
- **Alternatives** — (a) Tailwind Play CDN at runtime: rejected — ships the full
  engine and can't purge. (b) HTMX from a CDN: rejected — adds a runtime
  third-party dependency and version drift. (c) An SPA / JS framework + bundler:
  rejected — over-engineered for a notebook-like, mostly-server-rendered app.
- **Consequences** — Introduces a Node/npm toolchain and a build step: the CSS
  must be built before running the app or the static-CSS test (CI runs
  `build:css` before `pytest`; the test skips when the file is absent so a
  Node-less `pytest` stays green). In exchange: small purged CSS, a
  self-contained app with no runtime CDNs, and stable pinned asset versions.
  Revisit committing built assets vs building in CI once a CI pipeline exists.

---

## ADR-001 — Sync SQLAlchemy over async

- **Date** — 2026-07-11
- **Status** — Accepted
- **Context** — The backend needs a persistence layer. SQLAlchemy 2.0 offers
  both a sync and an async API. Async would let route handlers `await` DB calls,
  but it complicates the test harness (async fixtures, async sessions, an event
  loop per test) and the engine/session wiring.
- **Decision** — Use the sync SQLAlchemy 2.0 API. Sessions are injected into
  route handlers via `Depends(get_db)`; handlers may be `def` or `async def`.
- **Alternatives** — Async SQLAlchemy (`create_async_engine`, `AsyncSession`):
  rejected because SQLite is the store and expected load is low, so the async
  benefit is marginal, while the fixture and wiring cost is real. FastAPI runs
  sync routes in a threadpool, so a blocking DB call does not block the event
  loop.
- **Consequences** — Simpler engine/session setup and straightforward
  transactional test fixtures. If we later outgrow SQLite and need genuine async
  I/O throughput, migrating to the async API will require reworking the session
  dependency and tests; a new ADR would supersede this one.
