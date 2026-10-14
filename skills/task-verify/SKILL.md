---
name: task-verify
description: Read-only check of a task's acceptance criteria against current repo state. Reports pass/fail per criterion. Never edits code or moves files.
argument-hint: "i=<path>"
disable-model-invocation: true
---

# task-verify

## Purpose
Independently check that a task's acceptance criteria and Done condition hold in the current repo. Use it to audit work done by an executor, a human, or another agent.

## Inputs
- `$i` - path to a task file (in `tasks/todo/` or `tasks/done/`)

## Rules
- Read-only: never edit source, never move the task file, never change its `Status:`. Fixing is the executor's job.
- Check every Given/When/Then and the Done condition. Run tests or read-only commands where possible; every verdict cites evidence (test result, command output, observed behavior), not assertion.

## Output
Write `<feature>/tasks/feedback/<task-id>-verify-<NN>.md` (create `tasks/feedback/` if absent) following `template.md`. `<NN>` is the task's current `Attempts`, zero-padded; never overwrite an earlier report.

Frontmatter is the contract the executor reads on retry: `verdict` is PASS only if every criterion and the Done condition pass, else FAIL; `failed_checks` has one line per failure and is empty on PASS.

State the overall result in chat.
