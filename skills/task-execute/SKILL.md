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
- If any criterion fails, stop, leave the file in `tasks/todo/`, and report which criterion failed and why.
- Redact secrets from any output.

## Procedure

**Step 1 - Read**
Read `$i` in full. Read `overview/principles.md` if it exists and treat its rules as binding constraints.

**Step 2 - Check dependencies**
For each ID in `Depends on:`, confirm the matching file is already in `tasks/done/` (not `tasks/todo/`). If any dependency is unmet, stop and report. Take no further action.

**Step 3 - Implement**
Implement only the work in `Scope notes: In`. Make the minimum code change that satisfies the acceptance criteria. Stay inside the task boundary.

**Step 4 - Verify**
Check every `Acceptance criteria` (Given/When/Then) against the resulting state. Run tests or commands where the criterion is testable. Confirm the `Done` condition holds. Record pass/fail per criterion.

**Step 5 - Move and mark (only if all pass)**
If and only if all criteria and the Done condition pass:
- Set the task file `Status:` to `Done`.
- Move the file from `tasks/todo/` to the sibling `tasks/done/` directory.
- Report using `template.md`.

If any criterion fails, leave the file in place, leave Status unchanged, and report the failure.

## Readiness gate
- All `Depends on:` tasks are in `tasks/done/`
- Every acceptance criterion verified pass
- Done condition met
- No edits outside the task's declared scope

## Output contract
An execution report. See `template.md`. On success, the task file lives in `tasks/done/` with `Status: Done`.

## Validation
Verify against `checklist.md` before moving the file. Do not move on any failure.
