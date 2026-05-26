---
name: project-principles
description: Write a short, durable project principles document (constitution-lite) to overview/principles.md. The pipeline reads it as binding constraints.
argument-hint: "o=<path>"
disable-model-invocation: true
---

# project-principles

## Purpose
Capture the durable, project-wide rules that every feature should inherit: tech constraints, conventions, decision defaults, and non-negotiables. Other skills (`discussion-analysis`, `analysis-plan`, `task-execute`) read this file when present and treat it as binding. Kept deliberately short so it stays cheap to load.

## Inputs
- `$o` - path to write (default `overview/principles.md`)

## Hard rules
- Keep it short. Target under 400 words. Long principles do not get read.
- Durable rules only. No task state, no file paths that will move, no temporary decisions.
- State each rule so it can be checked, not admired. "Use Postgres, not new datastores" beats "value good data".
- If `$o` already exists, read it first and update in place. Do not discard existing rules without confirming.

## Procedure

**Step 1 - Gather**
Ask the user (or read from existing project docs) for: required/forbidden tech, coding conventions, default choices when a decision is ambiguous, and hard non-negotiables (security, compliance, performance floors).

**Step 2 - Write**
Write `$o` using `template.md`. One line per rule. Cut anything vague.

**Step 3 - Confirm**
Report the path written and the rule count.

## Readiness gate
- Every rule is specific and checkable
- No volatile detail (task progress, moving paths) is included
- Document is under the length target

## Output contract
See `template.md`.
