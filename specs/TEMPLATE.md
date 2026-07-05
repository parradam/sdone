# Spec: [Feature Name]

**Status:** Draft | Ready | In Progress | Done
**Spec ID:** xxxx
**Owner:** Adam
**Related:** #issue-link, specs/004-auth.md

## Goal

One or two sentences. What this feature does and why it exists.
A reader should understand the point without scrolling further.

## Context

What already exists that this touches. Link to relevant code paths,
existing modules, or ARCHITECTURE.md sections. Note anything Claude
would otherwise have to guess about.

## User-facing behaviour

- As a [user type], I can [action] so that [outcome]
- Edge cases and what should happen in each
- Empty states, error states, loading states

## Scope

### In scope

- Concrete, checkable items

### Out of scope

- Things explicitly NOT to build (prevents over-engineering)

## Technical approach

Testing: always start by confirming existing test cases, or writing new ones.
Commits: break changes into logical, atomic commits; only proceed with commits if all tests pass.
Backend: endpoints, data model changes, migrations, services.
Frontend: components, routes, state, API calls.
Be specific where you have an opinion; say "Claude's discretion" where
you don't. List exact file paths you expect to be created/modified.

## Data model / API contract

\`\`\`
POST /api/widgets
Request:  { name: string, type: "a" | "b" }
Response: 201 { id, name, type, createdAt }
Errors:   400 invalid type, 409 duplicate name
\`\`\`

## Acceptance criteria

- [ ] Checkable, testable statements
- [ ] Each maps to something that can be verified
- [ ] Include the test expectation: "unit tests for X, integration test for Y"

## Open questions

- Anything unresolved. Claude should ask rather than assume.

## Implementation plan

AI: update this with an implementation plan before writing code.
