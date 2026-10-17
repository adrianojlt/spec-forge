---
name: task-review
description: "Review code changes for quality, security, performance, spec compliance, and test quality. Report-only, task-scoped, language-aware."
argument-hint: "i=<task.md> [c=<codebase>]"
disable-model-invocation: true
---

# task-review

## Purpose
Review the code an executor (`task-execute` or `tdd`) produced for one task, and write a report whose verdict and `failed_checks` drive the retry loop.

## Inputs
- `$i` - path to a task file (in `tasks/todo/` or `tasks/done/`)
- `$c` - codebase root (optional; inferred from `$i` location if not given)

## Rules
- Read-only: never edit source, never move the task file, never change its `Status:`.
- Review only this task's changes: the uncommitted diff when run inside `execute-tasks`, otherwise the diff since the task started, or the files its scope names when there is no git.
- Cover five dimensions: code quality, security, performance, spec compliance (against `Scope notes` and every Given/When/Then), and test quality. Mark a dimension N/A with a reason rather than skipping it.
- For code quality, use the matching `<language>-coding-standards/SKILL.md` as the reference when one exists, else `coding-principles/SKILL.md`. Also check the change follows the task's `Patterns to mirror`; a deviation without a reason in the attempt report is at least a warning.
- Every finding has a severity, `file:line`, the issue, and a concrete fix. Skip what the project's formatter or linter already handles. Do not invent requirements beyond the task file.
- Severity: **blocker** = must fix (bugs, security holes, spec violations, data loss risk); **warning** = should fix; **nit** = optional.

## Output
Write `<feature>/tasks/feedback/<task-id>-review-<NN>.md` (create `tasks/feedback/` if absent) following `template.md`. `<NN>` is the task's current `Attempts`, zero-padded; never overwrite an earlier report.

Frontmatter is the contract the executor reads on retry:
- `verdict`: any blocker = `FAIL`; warnings only = `PASS_WITH_WARNINGS`; nits only or clean = `PASS`.
- `failed_checks`: one line per blocker, plus any warning that must be fixed before the next run, as `<finding-id>: <what must change>`. Empty on PASS.

Also present the report in chat.
