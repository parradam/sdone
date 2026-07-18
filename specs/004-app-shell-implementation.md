# 004: App shell implementation

**Status:** Done
**Owner:** Adam
**Related:** ARCHITECTURE.md, CLAUDE.md, DECISIONS.md, specs/001-scaffolding-backend.md, specs/002-app-shell-visual-mockup.md, specs/003-interstitial-journal.md, mockups/002-app-shell/01-sidebar-cool-slate.html

## Goal

Turn the adopted design mockup into a real, served application shell and stand up
the frontend stack so feature pages can be built on a shared layout.

- Implement the chosen mockup (`mockups/002-app-shell/01-sidebar-cool-slate.html`)
  as Jinja2 templates rendered by FastAPI.
- Establish the frontend stack: `Jinja2Templates`, a `StaticFiles` mount, HTMX,
  and a Tailwind CSS build.
- Provide a shared `base.html` (sidebar, header, content block, sidebar footer)
  that feature specs — starting with **003 (interstitial journal)** — extend.

This spec delivers the **frame**, not features: page bodies are placeholder
content, and nav destinations that aren't built yet are inert links.

## Context

- Spec 002 was a pure visual exploration; it adopted the **left sidebar + cool
  slate** mockup (`01-sidebar-cool-slate.html`) and recorded the other variants
  (top nav, paper terracotta) as design history only. This spec implements that
  one mockup; the others are out of scope.
- Spec 001 delivered the backend foundations (FastAPI app, SQLite + SQLAlchemy,
  settings, logging, error envelope, Pytest harness). There are currently **no
  templates, no static assets, and no HTML-serving routes** — only `/health`,
  registered directly on `app`.
- This is the first frontend work in the repo, so it also introduces the
  conventions later specs reuse: a templating helper, a static mount, a router
  package, and the Tailwind build pipeline.
- **Unblocks spec 003**, which assumes `base.html`, the static mount, HTMX, and
  the Tailwind build all exist.

## User-facing behaviour

- Visiting `GET /` renders the full app shell:
  - **Sidebar** (visible ≥ `md`): brand (Sdone logo + wordmark); primary nav —
    **Today, Tasks, Calendar, Journal**; a **Reflect** group — **Achievements,
    Statistics, Resources**; and a sidebar footer with a **Log a note** action
    (⌘N hint) and an account / settings link.
  - **Header**: page title + date, a search button (⌘K hint, "Search tasks,
    notes…"), and primary actions ("Log a note", "Start session"). On mobile the
    sidebar is hidden and a compact brand shows in the header.
  - **Main content**: a placeholder "Today" body (calm placeholder, real copy —
    not lorem ipsum) rendered inside the shared content block.
- The layout is **responsive**: the sidebar collapses below `md`; content remains
  usable on small screens.
- Fonts (Literata serif, Hanken Grotesk sans), the cool-slate OKLCH colour
  tokens, and the calm motion (`pulse`, `rise`) match the mockup. Motion is
  disabled under `prefers-reduced-motion`.
- The nav "Journal" link points at the route 003 will add; other unbuilt
  destinations are inert (`href="#"`) placeholders.

## Scope

### In scope

- **Templating**: `app/templating.py` exposing a shared
  `Jinja2Templates(directory="app/templates")` instance (later extended by 003
  with the `highlight_todo` filter).
- **Static files**: a `StaticFiles` mount at `/static` in `main.py`.
- **`base.html`**: the shell layout — `<head>` (fonts, built `app.css`, HTMX
  script); `<body>` with the sidebar `aside`, header, `{% block content %}`, and
  sidebar footer. Named blocks: `title`, `header`, `content` (+ an optional
  `head_extra` / `body_end` for per-page assets).
- **Tailwind build**: `package.json`, `tailwind.config.js` (porting the mockup's
  `fontFamily` and colour tokens), a CSS entrypoint (`static/css/input.css`), and
  an `npm run build:css` script producing `app/static/app.css`. `content` globs
  cover `app/templates/**/*.html` and `app/static/js/**/*.js`.
- **Design tokens**: the OKLCH CSS custom properties, the `pulse` / `rise`
  keyframe animations, and the `prefers-reduced-motion` block from the mockup,
  carried into the build (via `input.css` / config).
- **HTMX**: vendored as a pinned `app/static/js/htmx.min.js` and included from
  `base.html` (self-hosted, no third-party CDN at runtime).
- **Routing**: an `app/routers/pages.py` `APIRouter` with `GET /` rendering the
  shell with the placeholder Today body; included in `main.py`.
- **Tests**: `tests/test_pages.py`.
- **Docs**: README build/run instructions; ARCHITECTURE layout; a DECISIONS ADR.

### Out of scope

- The interstitial journal feature and any real feature content (spec 003+).
- The top-nav and paper-terracotta mockups.
- Authentication / users; dark mode / theme switching.
- Client interactivity beyond loading HTMX (no feature behaviours yet).
- A JS bundler / framework — HTMX + a tiny amount of vanilla JS only.

## Technical approach

**Testing (TDD, per CLAUDE.md).** Write `tests/test_pages.py` first, then wire the
route/templates. Reuse the spec 001 `client` fixture. Cover: `GET /` returns
200 and `text/html`; the response contains the key nav labels (Today, Tasks,
Calendar, Journal, Achievements, Statistics, Resources); `base.html` renders
without a Jinja error; `/static/app.css` and `/static/js/htmx.min.js` are served
(200). Commit atomically; only commit when `ruff check`, `mypy .`, and `pytest`
pass **and** `npm run build:css` succeeds.

**Frontend stack decisions.**

- **Tailwind via a real build** (npm + Tailwind CLI) — the user-approved choice
  and the CLAUDE.md "flag before installing packages" trigger: this spec
  introduces a Node/npm toolchain, justified because the mockup's utility classes
  need compiling/purging for production rather than shipping the full CDN runtime.
- **HTMX vendored** (pinned file under `static/`) rather than a runtime CDN, to
  keep the app self-contained and version-stable.
- Templates and the built CSS are served by FastAPI's `StaticFiles`; there is no
  separate front-end server.
- **Built CSS is gitignored.** `npm run build:css` is a prerequisite for running
  the app and for the CSS-serving test; the app's HTML still renders without it
  (only unstyled), so the shell/nav tests do not depend on a build. CI runs
  `build:css` before `pytest`; the CSS-serving test skips when `app.css` is absent
  so a local Node-less `pytest` stays green.

**Reuse from mockup 01.** Port the sidebar/header/footer markup and the token /
animation CSS directly from `mockups/002-app-shell/01-sidebar-cool-slate.html`
(it already reflects the refinements recorded in spec 002 — the wider search
field and the reworked "This week" hierarchy). Replace the inline
`cdn.tailwindcss.com` script and inline `tailwind.config` with the compiled
`app.css`; move the config into `tailwind.config.js`.

**Files created / modified:**

```md
backend/
  package.json                 +  Node toolchain (tailwindcss, build:css script)
  tailwind.config.js           +  fontFamily + colour tokens + content globs
  .gitignore                   ~  node_modules/ + app/static/app.css (built, gitignored)
  README.md                    ~  frontend build/run instructions
  app/
    main.py                    ~  StaticFiles mount + include_router(pages.router)
    templating.py              +  shared Jinja2Templates instance
    routers/
      __init__.py              +
      pages.py                 +  GET / (renders the shell)
    templates/
      base.html                +  shell layout (blocks: title, header, content)
      pages/today.html         +  placeholder Today body
    static/
      css/input.css            +  Tailwind entry (@tailwind + tokens + animations)
      app.css                  +  built output (generated by build:css)
      js/htmx.min.js           +  vendored, pinned
  tests/test_pages.py          +
ARCHITECTURE.md                ~  frontend module layout
DECISIONS.md                   ~  ADR: Tailwind build + vendored HTMX
```

## Data model / API contract

No data model changes; no new persistence.

```md
GET /
Response: 200 text/html — the app shell (base.html + placeholder Today body)
```

`/health` from spec 001 is unchanged.

## Acceptance criteria

- [x] `GET /` returns 200 `text/html` and renders `base.html` with the sidebar,
      header, and content region. **Integration test** via `TestClient`.
- [x] The rendered shell contains the nav labels Today, Tasks, Calendar, Journal,
      Achievements, Statistics, Resources. **Integration test.**
- [x] `npm run build:css` produces `app/static/app.css` (gitignored) from the
      Tailwind config; after a build, `GET /static/app.css` returns 200. The
      integration test asserts the mount serves the file **once built**; it may
      `skip` (not fail) when `app.css` is absent so a Node-less `pytest` run stays
      green, while CI runs `build:css` before `pytest` so it actually exercises.
- [x] HTMX is vendored at `app/static/js/htmx.min.js` and `GET /static/js/htmx.min.js`
      returns 200; `base.html` includes it. **Integration test.**
- [x] The shell is responsive (sidebar hidden below `md`, mobile brand shown) and
      honours `prefers-reduced-motion`. **Verified structurally** — the compiled
      CSS contains the `md` breakpoint rules (`.md:flex`/`.md:hidden`) and the
      `prefers-reduced-motion` block. (A true sub-`md` browser capture was not
      possible — the automation viewport would not reflow below the breakpoint.)
- [x] Fonts and cool-slate colour tokens visually match mockup 01. **Verified**
      via a desktop browser pass at 1440px: Literata serif (brand/headings),
      Hanken Grotesk sans (UI), the cool-slate accent, surfaces/borders, and the
      active-nav highlight all match mockup 01.
- [x] `ruff check` and `mypy .` pass on all new Python code.
- [x] `ARCHITECTURE.md` reflects the frontend layout and `DECISIONS.md` records
      the Tailwind-build + vendored-HTMX ADR.

## Resolved decisions

- **HTMX delivery**: vendored, pinned `app/static/js/htmx.min.js` (self-hosted;
  no runtime CDN).
- **Home path**: the shell is served at `/` (Today is the landing page). The
  **Journal** nav link points to `/journal`, the route spec 003 will add; other
  unbuilt destinations are inert (`href="#"`).
- **Tailwind invocation**: `tailwindcss` as an npm **devDependency**, run via the
  `build:css` script (`npx`), for reproducible builds.
- **Built CSS**: `app/static/app.css` is **gitignored**; `npm run build:css` is a
  prerequisite for running the app and for the CSS-serving test. CI must run the
  build before `pytest`. (See the note under Technical approach.)
- **Placeholder body**: a trimmed, honest placeholder — a heading, a short intro,
  and at most one empty-state card — proving the shell without fabricating live
  session/task/stats data.

## Open questions

- Revisit committing built assets (vs building in CI) once a CI pipeline exists.
- **Header date timezone.** The placeholder header renders
  `datetime.now(tz=UTC)`, so the date reflects UTC, not the viewer's local day
  (e.g. a UK/BST viewer in the early hours sees the previous day). Deferred to
  the Today-page spec, which must choose a timezone strategy — a configured app
  timezone in `Settings`, client-side rendering from the browser clock, or
  server-local `datetime.now().astimezone()`.

## Implementation plan

Test-first and atomic; each step committed only when `ruff`, `mypy`, and `pytest`
pass (and the CSS build succeeds where relevant).

1. **Templating + static mount + placeholder route.** Write `tests/test_pages.py`
   (200/HTML, nav labels). Add `app/templating.py`, `app/routers/pages.py`
   (`GET /`), a minimal `base.html` + `pages/today.html`, and the `StaticFiles`
   mount + `include_router` in `main.py`. Commit.
2. **Tailwind build.** Add `package.json` (tailwindcss devDependency),
   `tailwind.config.js`, `static/css/input.css` (tokens + `pulse`/`rise` +
   reduced-motion), and `build:css` → `app/static/app.css`; link it from
   `base.html`. Gitignore `node_modules/` and `app/static/app.css`; document
   `build:css` in the README. Commit.
3. **Vendor HTMX.** Add pinned `static/js/htmx.min.js`; include it in `base.html`;
   assert it is served. Commit.
4. **Port the shell markup.** Bring the sidebar (brand, primary nav, Reflect
   group, footer) and header (title/date, search, actions) over from mockup 01
   into `base.html`; point "Journal" at `/journal` (the route 003 adds), other
   destinations inert (`href="#"`). Commit.
5. **Responsive + motion.** Confirm the sidebar collapse, mobile header brand, and
   `prefers-reduced-motion`. Verify manually / via browser MCP. Commit.
6. **Docs.** Update `ARCHITECTURE.md` (frontend layout) and append the DECISIONS
   ADR (Tailwind build over CDN; vendored HTMX). Commit.
