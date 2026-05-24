---
name: plan-tasks
description: Decompose plan.md into atomic, testable tasks. One file per task written to tasks_dir. Enforce INVEST and Given/When/Then format.
argument-hint: "source_file=<path> tasks_dir=<path> prefix=<prefix>"
disable-model-invocation: true
---

# plan-tasks

## Purpose
Transform `plan.md` into individual task files, one per task, written to `$tasks_dir`. Each task must be independently implementable, testable, and have clear acceptance criteria.

## Inputs
- `$source_file` - path to plan.md
- `$tasks_dir` - directory where task files will be written (e.g. `features/user-auth/tasks/todo/`)
- `$prefix` - file name prefix derived from the feature name (e.g. `user-auth`)

## Hard rules
- No giant umbrella tasks.
- No tasks that combine implementation with unrelated work.
- Each task must be independently implementable and reviewable.
- All acceptance criteria in Given/When/Then format.
- All tasks must pass INVEST check.
- Dependency ordering must match plan.md sequence.

## Procedure

**Step 1 - Read**
Read `$source_file` in full.

**Step 2 - Slice to tasks**
For each scope slice in the plan, decompose into the minimum number of atomic tasks. A task should be completable in one focused session.

**Step 3 - Order**
Order tasks by dependency. Task IDs are sequential and derived from `$prefix` (e.g. user-auth-task-01, user-auth-task-02).

**Step 4 - Write each task**
For each task, compose:
- ID (e.g. `user-auth-task-01`, derived from `$prefix` and sequence number)
- Title (imperative verb phrase, under 60 chars)
- Purpose (one sentence: why this task, what it unlocks)
- Depends on (task IDs or "none")
- Scope notes (what is in and what is NOT in this task)
- Acceptance criteria (Given/When/Then, minimum 2 criteria)
- INVEST check (one word each: Independent/Negotiable/Valuable/Estimable/Small/Testable)
- Done definition

**Step 5 - Write output**
Write one file per task into `$tasks_dir`. File name pattern: `$prefix-task-<NN>.md` where NN is zero-padded (01, 02, ...). Write files in dependency order. Confirm count of files written.

## Readiness gate
- No task is broader than one focused work session
- No task has undefined dependencies
- Every task has at least 2 Given/When/Then criteria
- All tasks pass INVEST check

## Output contract
One file per task. See `template.md` for the single-task file structure.

## Validation
Verify against `checklist.md` before writing. Reject and split tasks that fail.
