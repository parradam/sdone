# 00X: Interstitial Log — Visual Mockup

## Status

Exploratory — not implementation-ready

## Goal

Explore what the interstitial log UI should feel like: fast to open,
low-friction to dismiss, minimal cognitive load when interrupting a task.

## Constraints

- Jinja2 + HTMX + Tailwind (no JS framework)
- Must work as a modal AND be testable as a standalone page for iteration

## Directions explored

### Option A: Modal overlay

[screenshot/description, what it's good/bad at]

### Option B: Inline slide-down panel

[screenshot/description, what it's good/bad at]

## Open questions

- Does it need a "skip" affordance, or should dismissal always require a word count minimum?
- Where does mood/energy rating fit, if at all?

## Current lean

Option A, pending a decision on the skip affordance question.

## Not decided here

Data model, trigger/nudge logic, backend wiring — see 00Y-interstitial-log.md
