# Principles: [Project]

Date: [date]
Status: [Draft | Approved]

---

> Binding, project-wide rules. Read by orchestrate, the
> executors and execute-tasks. Keep short. One line per rule.

## Principles

- [Durable principle that guides decisions, e.g. "Prefer boring, proven tech over novel."]

## Constraints

- [Required or forbidden tech, e.g. "Backend is Postgres; do not introduce new datastores."]
- [Platform/runtime limits, e.g. "Must run on Node 20."]

## Conventions

- [Coding convention, e.g. "Tests colocated with source as *.test.ts."]
- [Naming/style rule that is not obvious from the code.]

## Decision Defaults

- [What to choose when ambiguous, e.g. "When unsure, choose the smaller change."]

## Non-Negotiables

- [Hard rule with no exceptions, e.g. "No secrets in source. No PII in logs."]

## Definition of Done

> Commands every task must pass, whatever its acceptance criteria. Run from the
> codebase root after each task; each ends by itself and exits 0 only on success.
> Omit the section if the project has none.

- `[command]` - [what it proves, e.g. full test suite, build, lint]
