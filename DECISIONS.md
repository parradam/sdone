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
