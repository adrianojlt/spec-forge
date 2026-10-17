---
name: task-execute
description: Implement a single task file, verify its acceptance criteria, and move it from tasks/todo to tasks/done. The one skill that produces code.
argument-hint: "i=<path>"
disable-model-invocation: true
---

# task-execute

## Purpose
Implement one task file end to end: write the code in its scope, verify every acceptance criterion, and record the outcome on disk so the loop (`execute-tasks`, a later session, or a human) can continue from it.

## Inputs
- `$i` - path to a single task file in `tasks/todo/` (e.g. `features/user-auth/tasks/todo/user-auth-task-01.md`), or in `tasks/done/` when a review or verify failed on it

## Rules
- Implement only `Scope notes: In`; nothing in `Not in`. If `overview/principles.md` exists, its rules are binding.
- Every task ID in `Depends on:` must already be in `tasks/done/`. If one is not, stop and report without implementing.
- Follow the task's `Patterns to mirror`. Deviate only with a reason, recorded under `Notes` in the attempt report.
- Verify each Given/When/Then and the Done condition against the result, running tests or commands where possible, starting with the task's `Validate` commands. Evidence, not assertion.

## Retry or first attempt
Look in the sibling `tasks/feedback/` for this task's `<task-id>-attempt-<NN>.md`, `-review-<NN>.md` and `-verify-<NN>.md`. The latest is the highest `<NN>`; at equal `<NN>`, a review or verify report is newer than the attempt report.
- No report: first attempt, implement the full scope.
- Latest has `result: Revise` or `verdict: FAIL`: retry. Fix only its `failed_checks`; do not re-touch what already passed. If `Attempts` already equals `Max attempts`, do no work: set `Status: Blocked`, make sure the file is in `tasks/todo/`, and report.
- `$i` is in `tasks/done/` and this is not a retry: the task is already done. Report and stop.

## Recording the outcome
1. Increment `Attempts:` in the task file. The new value is `<NN>`.
2. Write `tasks/feedback/<task-id>-attempt-<NN>.md` following `template.md` (create the folder if absent; never overwrite an earlier report). Its `failed_checks` drives the next retry.
3. All criteria and the Done condition pass: set `Status: Done` and move the file to `tasks/done/` (a retry that started there stays there).
4. Anything fails: the file goes to (or stays in) `tasks/todo/` with `Status: Revise`, or `Status: Blocked` once `Attempts` reaches `Max attempts`. Report which criteria failed and why.
