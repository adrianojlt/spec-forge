---
name: project-principles
description: Write a short, durable project principles document (constitution-lite) to overview/principles.md. The pipeline reads it as binding constraints.
argument-hint: "o=<path>"
disable-model-invocation: true
---

# project-principles

## Purpose
Capture the durable, project-wide rules every feature should inherit: required or forbidden tech, conventions, decision defaults, non-negotiables, and the Definition of Done every task must pass. `orchestrate`, the executors and `execute-tasks` read this file when present and treat it as binding, so it must stay short enough to be cheap to load.

## Inputs
- `$o` - path to write (default `overview/principles.md`)

## Rules
- Under 400 words, one line per rule. Long principles do not get read.
- Durable rules only: no task state, no paths that will move, no temporary decisions.
- Each rule is checkable, not admirable. "Use Postgres, not new datastores" beats "value good data".
- Take rules from the user or from existing project docs. Cut anything vague.
- If `$o` exists, update it in place and confirm before dropping an existing rule.
- `Definition of Done` lists the commands every task must pass on top of its own acceptance criteria (full test suite, build, lint). The executors run them and `execute-tasks` gates each commit on their exit codes, so each one runs from the codebase root, ends by itself, exits 0 only on success, and is fast enough to run after every task. Take them from the project's own scripts and CI; never invent one. They must pass on the current codebase before you write them.

## Output
`$o`, following `template.md`. Report the path and the rule count.
