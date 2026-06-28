---
name: task-verify
description: Read-only check of a task's acceptance criteria against current repo state. Reports pass/fail per criterion. Never edits code or moves files.
argument-hint: "i=<path>"
disable-model-invocation: true
---

# task-verify

## Purpose
Independently verify that a task's acceptance criteria hold against the current state of the repo. Read-only: writes no code, moves no files, changes no status. Use it to audit work done by `task-execute`, by a human, or by another agent.

## Inputs
- `$i` - path to a task file (in `tasks/todo/` or `tasks/done/`)

## Hard rules
- Read-only. Never edit source files. Never move the task file. Never change its `Status:`.
- Check every acceptance criterion. Do not skip.
- Each verdict must cite evidence (test result, command output, observed behavior), not assertion.
- Do not implement missing work. If a criterion fails, report it; fixing is `task-execute`'s job.

## Procedure

**Step 1 - Read**
Read `$i` in full. Note its `Acceptance criteria` (Given/When/Then) and `Done` condition.

**Step 2 - Verify each criterion**
For each Given/When/Then, establish the Given state, perform or trace the When, and check the Then against actual repo state. Run tests or read-only commands where applicable. Record pass/fail with evidence.

**Step 3 - Check Done condition**
Confirm the task's `Done` definition holds against current state.

**Step 4 - Report**
Write the verdict using `template.md` and persist it to the sibling `tasks/feedback/` directory (create it if absent):
```
<feature>/tasks/feedback/<task-id>-verify-<NN>.md
```
`<NN>` = the task's current `Attempts` value, zero-padded. Each attempt gets its own file; never overwrite an earlier one. Populate the frontmatter: `verdict` (PASS if every criterion and the Done condition pass, else FAIL) and `failed_checks` (one line per failure; empty on PASS). On FAIL, this list is what a later `/task-execute` targets. Also state the overall result in chat.

## Readiness gate
- Every acceptance criterion was checked
- Every verdict carries evidence
- The Done condition was assessed

## Output contract
A verification report written to `<feature>/tasks/feedback/<task-id>-verify-<NN>.md` and stated in chat. See `template.md`. Writing this report is the only file the skill creates; it still never edits source or the task file and never changes the task `Status:`.

## Validation
Verify against `checklist.md` before reporting.
