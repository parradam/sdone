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
