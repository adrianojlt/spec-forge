---
name: task-execute
description: Implement a single task file, verify its acceptance criteria, and move it from tasks/todo to tasks/done. The one skill that produces code.
argument-hint: "i=<path>"
disable-model-invocation: true
---

# task-execute

## Purpose
Implement one task file end to end: write the code in its scope, verify every acceptance criterion, then move the file from `tasks/todo/` to `tasks/done/` and mark it Done. This is the only skill in the pipeline that produces code, and it is scoped to exactly one task.

## Inputs
- `$i` - path to a single task file in `tasks/todo/` (e.g. `features/user-auth/tasks/todo/user-auth-task-01.md`)

## Hard rules
- Implement only what is in this task's `Scope notes: In`. Do nothing in `Not in`.
- Respect `Depends on:`. If any named dependency still sits in `tasks/todo/`, stop and report. Do not implement.
- Surgical changes only. Touch only what the task requires. Match existing code style. Do not refactor unrelated code.
- Do not move the file to `tasks/done/` unless every acceptance criterion and the Done condition pass.
- If any criterion fails, leave the file in `tasks/todo/`, set its `Status:` to `Revise` (or `Blocked` at max attempts), increment `Attempts:`, and report which criterion failed and why.
- Redact secrets from any output.

## Procedure

**Step 1 - Read**
Read `$i` in full. Read `overview/principles.md` if it exists and treat its rules as binding constraints.

Then check for prior loop feedback. Look in the sibling `tasks/feedback/` directory for the highest-numbered report for this task: `<task-id>-review-<NN>.md` and `<task-id>-verify-<NN>.md`. If the latest one has `verdict: FAIL` (or `Overall: failures found`), this is a **retry**:
- Scope the work to the `failed_checks` list only. Fix those items. Do not re-touch code that already passed.
- This is targeted re-entry, not a full redo. If no feedback file exists, this is a first attempt; implement the full task scope per Step 3.

**Step 2 - Check dependencies**
For each ID in `Depends on:`, confirm the matching file is already in `tasks/done/` (not `tasks/todo/`). If any dependency is unmet, stop and report. Take no further action.

**Step 3 - Implement**
Implement only the work in `Scope notes: In`. Make the minimum code change that satisfies the acceptance criteria. Stay inside the task boundary.

**Step 4 - Verify**
Check every `Acceptance criteria` (Given/When/Then) against the resulting state. Run tests or commands where the criterion is testable. Confirm the `Done` condition holds. Record pass/fail per criterion.

**Step 5 - Move and mark**
First, increment the task file's `Attempts:` by 1 (this run counts as an attempt). Use this value as `<NN>` for the report filename.

Write the execution report using `template.md` to the sibling `tasks/feedback/` directory (create it if absent):
```
<feature>/tasks/feedback/<task-id>-attempt-<NN>.md
```
Each attempt gets its own file; never overwrite an earlier attempt. Then:

**On success** (every acceptance criterion and the Done condition pass):
- Set the task file `Status:` to `Done`.
- Move the file from `tasks/todo/` to the sibling `tasks/done/` directory.

**On failure** (any criterion or the Done condition fails):
- Leave the file in `tasks/todo/`.
- If `Attempts` is now `< Max attempts`: set `Status:` to `Revise`. The task is ready for another targeted run.
- If `Attempts` has reached `Max attempts`: set `Status:` to `Blocked`. Stop the loop and report; do not retry again without human intervention.
- Report which criteria failed and why (the report's `failed_checks` drives the next retry's Step 1).

## Readiness gate
- All `Depends on:` tasks are in `tasks/done/`
- Every acceptance criterion verified pass
- Done condition met
- No edits outside the task's declared scope

## Output contract
An execution report written to `<feature>/tasks/feedback/<task-id>-attempt-<NN>.md`. See `template.md`. On success, the task file lives in `tasks/done/` with `Status: Done`. On failure, it stays in `tasks/todo/` with `Status: Revise` (retryable) or `Status: Blocked` (max attempts reached), and `Attempts:` incremented.

## Validation
Verify against `checklist.md` before moving the file. Do not move on any failure.
