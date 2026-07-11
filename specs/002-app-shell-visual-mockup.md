# 002: App shell visual mockup

## Status

Exploratory — not implementation-ready

## Goal

I'm designing the visual shell for a personal task-tracking/journaling app called Sdone — calm, minimal, low-friction. Create a static HTML mockup of the app shell: nav, header, footer, base layout, with placeholder content in the body. This is pure design exploration, not wired to any backend — just a standalone HTML file I can view in the browser.

## Context

The user will likely have this open to the side or in the background, so it needs to be straightforward with a comfortable and clean feel.

## Constraints

- Use /impeccable frontend design skill
- Jinja2 + HTMX + Tailwind (no JS framework)
- Tailwind via CDN for this design
- Standalone HTML file(s), viewable directly in the browser for iteration

## Design details

Add any relevant details of the design below here so they can be referenced in future spec files. This includes colours, fonts, and design decisions taken.

### Deliverables

Three standalone mockups in `mockups/002-app-shell/`, plus an `index.html`
launcher. They cover both navigation layouts and all three colour moods
explored during design:

| File | Layout | Colour mood |
| ------ | -------- | ------------- |
| `01-sidebar-cool-slate.html` | Left sidebar | Cool neutral + slate blue |
| `02-topnav-cool-slate.html` | Top nav bar | Cool neutral + slate blue |
| `03-sidebar-paper-terracotta.html` | Left sidebar | Paper + terracotta |

### Decision

**Adopted: left sidebar + cool slate blue.** The sidebar scales best for the
feature set (7+ destinations); cool slate read as calmer and more focused than
the warm sage originally paired with the sidebar (a `01-sidebar-warm-sage.html`
mockup was explored and dropped). Top nav (`02`) and paper terracotta (`03`)
are kept as the record of what was explored.

Refinements applied to the chosen mockup after first review:

- **Search** enlarged to a proper 18rem-wide, 44px-tall field with a "Search
  tasks, notes…" placeholder and a ⌘K hint — no longer a cramped button.
- **"This week"** reworked: it was a flat 2×2 grid of equal serif numbers (the
  generic "hero metric" pattern) that felt weightless. Now a contained panel
  with a clear hierarchy — a date range, one lead metric (focus time, with a
  small "+2h vs last" delta), then a divided list of supporting figures. Data
  is set in the sans face (tabular), not the serif, so it reads as a summary
  rather than decoration.

### Shell structure (shared across all mockups)

- **Nav destinations:** Today, Tasks, Calendar, Journal (primary group);
  Achievements, Statistics, Resources (a "Reflect" secondary group). Account +
  Settings and a persistent "Log a note" quick action sit at the bottom of the
  sidebar / right of the top bar.
- **Header:** current view title + date, Search (⌘K), "Log a note", and a
  primary "Start session" action.
- **Body (placeholder):** a "Today" dashboard — a running-session banner (the
  single loud element), an "Up next" task list with type tags and durations,
  and a right rail with a quiet "This week" summary and recent journal notes.
- **Footer:** slim, "All changes saved" status + build tag.

### Theme

Light, in all moods. Derived from context: a daytime, background-open,
journaling app wants light, not a "safe" or "cool" default.

### Typography

- **Literata** (warm literary serif) — brand, headings, and reading content
  (journal notes). Chosen for a calm notebook feel; it is designed for reading.
- **Hanken Grotesk** (humanist sans) — UI chrome, labels, metadata, numbers.
- Deliberately avoided the AI-default fonts (Inter, DM Sans, Fraunces, etc.).

### Colour (OKLCH, light; neutrals tinted toward the accent)

Semantic tokens per mockup: `--bg`, `--surface`, `--surface-sunk`, `--ink`,
`--ink-soft`, `--ink-faint`, `--line`, `--accent`, `--accent-soft`,
`--accent-ink`. Accent is used sparingly (~10%): active nav, running session,
primary action.

- **Warm sage** — cream `oklch(0.984 0.006 95)`, sage accent `oklch(0.575 0.058 152)`.
- **Cool slate** — cool white `oklch(0.985 0.004 240)`, slate-blue accent `oklch(0.545 0.087 249)`.
- **Paper terracotta** — warm paper `oklch(0.974 0.011 74)`, clay accent `oklch(0.605 0.118 46)`.

### Motion

Gentle staggered fade/rise on load, a slow "breathe" pulse on the live-session
dot, fast ease-out hover transitions. All disabled under
`prefers-reduced-motion`.

### Design principles applied

Low friction, quiet by default (colour is earned), notebook-like readability,
calm motion, nav that scales with the feature set. See `.impeccable.md` for the
persisted project design context.

### Open decision

Which layout + mood to carry forward into the real Jinja2/HTMX/Tailwind shell
is not decided here — this spec is exploratory. Pick a direction before
implementing the production shell.
