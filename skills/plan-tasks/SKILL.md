---
name: plan-tasks
description: Decompose plan.md into atomic, testable tasks. One file per task written to tasks_dir. Enforce INVEST and Given/When/Then format.
argument-hint: "i=<path> o=<path> p=<prefix>"
disable-model-invocation: true
---

# plan-tasks

## Purpose
Transform `plan.md` into individual task files, one per task, written to `$o`. Each task must be independently implementable, testable, and have clear acceptance criteria.

## Inputs
- `$i` - path to plan.md
- `$o` - directory where task files will be written (e.g. `features/user-auth/tasks/todo/`)
- `$p` - file name prefix derived from the feature name (e.g. `user-auth`)

## Hard rules
- Write each task file's `Source:` header as a path relative to the task file's own folder (e.g. `../../auth-plan.md` from `tasks/todo/`), never absolute - keeps links valid if the specs folder is moved.
- No giant umbrella tasks.
- No tasks that combine implementation with unrelated work.
- Each task must be independently implementable and reviewable.
- All acceptance criteria in Given/When/Then format.
- All tasks must pass INVEST check.
- Dependency ordering must match plan.md sequence.
- Assume `plan.md` is user-approved (via the analysis-plan review gate). If it still reads as a raw draft (Status: Draft, or unresolved open questions), confirm with the user before decomposing.

## Procedure

**Step 1 - Read**
Read `$i` in full. Confirm the plan was approved at the analysis-plan review gate before proceeding.

**Step 2 - Slice to tasks**
For each scope slice in the plan, decompose into the minimum number of atomic tasks. A task should be completable in one focused session.

**Step 3 - Order**
Order tasks by dependency. Task IDs are sequential and derived from `$p` (e.g. user-auth-task-01, user-auth-task-02).

**Step 4 - Write each task**
For each task, compose:
- ID (e.g. `user-auth-task-01`, derived from `$p` and sequence number)
- Title (imperative verb phrase, under 60 chars)
- Purpose (one sentence: why this task, what it unlocks)
- Depends on (task IDs or "none")
- Scope notes (what is in and what is NOT in this task)
- Acceptance criteria (Given/When/Then, minimum 2 criteria)
- INVEST check (one word each: Independent/Negotiable/Valuable/Estimable/Small/Testable)
- Done definition

**Step 5 - Write output**
Write one file per task into `$o`. File name pattern: `$p-task-<NN>.md` where NN is zero-padded (01, 02, ...). Write files in dependency order. Confirm count of files written.

## Readiness gate
- No task is broader than one focused work session
- No task has undefined dependencies
- Every task has at least 2 Given/When/Then criteria
- All tasks pass INVEST check

## Output contract
One file per task. See `template.md` for the single-task file structure.

## Validation
Verify against `checklist.md` before writing. Reject and split tasks that fail.
