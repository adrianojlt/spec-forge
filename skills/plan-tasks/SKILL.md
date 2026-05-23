---
name: plan-tasks
description: Decompose plan.md into atomic, testable tasks with acceptance criteria. Enforce INVEST and Given/When/Then format.
argument-hint: "source_file=<path> target_file=<path>"
disable-model-invocation: true
---

# plan-tasks

## Purpose
Transform `plan.md` into `BACKLOG.md` (or a task artifact file) by decomposing scope slices into atomic, independently implementable tasks. Each task must be testable and have clear acceptance criteria.

## Inputs
- `$source_file` - path to plan.md
- `$target_file` - path where BACKLOG.md should be written

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
Order tasks by dependency. Task IDs are sequential within a slice prefix (e.g. AUTH-001, AUTH-002).

**Step 4 - Write each task**
For each task, write:
- ID (e.g. AUTH-001)
- Title (imperative verb phrase, under 60 chars)
- Purpose (one sentence: why this task, what it unlocks)
- Depends on (task IDs or "none")
- Scope notes (what is in and what is NOT in this task)
- Acceptance criteria (Given/When/Then, minimum 2 criteria)
- INVEST check (one word each: Independent/Negotiable/Valuable/Estimable/Small/Testable)
- Done definition

**Step 5 - Write output**
Write `$target_file`. Confirm written.

## Readiness gate
- No task is broader than one focused work session
- No task has undefined dependencies
- Every task has at least 2 Given/When/Then criteria
- All tasks pass INVEST check

## Output contract
See `template.md` for required task structure.

## Validation
Verify against `checklist.md` before writing. Reject and split tasks that fail.
