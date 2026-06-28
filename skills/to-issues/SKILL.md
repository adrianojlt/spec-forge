---
name: to-issues
description: Break a PRD into vertically-sliced task files using the tracer-bullet approach - each task delivers end-to-end user-visible value
argument-hint: "i=<prd.md> o=<tasks/todo/> p=<prefix> [c=<codebase>]"
disable-model-invocation: true
---

# to-issues

## Purpose
Decompose a PRD into independently executable tasks where each task cuts vertically through all layers (UI + API + data + test). Every task delivers observable user value, even if thin.

Contrast with `/plan-tasks`, which decomposes from a sequenced plan.md. `/to-issues` works directly from a PRD using the tracer-bullet / vertical-slice principle: no layer-only tasks.

## Inputs
- `$i` - prd.md to decompose
- `$o` - output directory for task files (e.g. `tasks/todo/`)
- `$p` - task ID prefix (e.g. `auth` produces `auth-task-01.md`, `auth-task-02.md`)
- `$c` - codebase root (optional). When given, explore to understand existing layers and integration points.

## Hard rules
- Write each task file's `Source:` header as a path relative to the task file's own folder (e.g. `../../auth-prd.md` from `tasks/todo/`), never absolute - keeps links valid if the specs folder is moved.
- No horizontal slices. "Set up the database schema" is not a valid task. "User can log in with email and password" is.
- Every task must deliver user-visible value - something a user or stakeholder can observe working.
- Blocking dependencies between tasks must be named explicitly.
- Every task file must use the Given/When/Then format for acceptance criteria.
- Output files must be compatible with `/task-execute` and `/task-verify` (same format as `/plan-tasks` output).
- Do not emit the dependency summary until all task files are written.

## Procedure

**Step 1 - Read**
Read `$i` in full. If `$c` is given, explore the codebase to understand existing layers, conventions, and integration points relevant to the PRD.

**Step 2 - Identify vertical slices**
Map each user story (or group of trivial stories) to one vertical slice. A vertical slice is the thinnest end-to-end cut that delivers the story's outcome. Name each slice by the user-visible outcome, not the technical component.

Good slice name: "User can register with email and password"
Bad slice name: "Create users table and registration endpoint"

**Step 3 - Size and split**
If a slice is too large for a single session, split it further. Each slice should be completable in one focused work session. If two slices have no dependency between them, they should be separate tasks.

**Step 4 - Identify blocking dependencies**
For each slice, name which other slices (if any) must complete before it can start. A task with no dependencies is independently startable. Flag these explicitly - do not leave dependencies implicit.

**Step 5 - Readiness gate check**
Verify gate before writing any files.

**Step 6 - Write task files**
Write one `.md` file per slice to `$o` using the format below. File names: `$p-task-01.md`, `$p-task-02.md`, etc. (ordered by suggested execution order, respecting dependencies).

Task file format (compatible with `/plan-tasks` output):
```
# [$p-task-NN] [Slice Title - user-visible outcome]

Source: [relative path to prd.md from this task file, e.g. ../../auth-prd.md - never absolute]
Date: [date]
Status: Draft
Attempts: 0
Max attempts: 3

---

**Purpose:** [One sentence: what user value this slice delivers.]

**Depends on:** [task file names | none]

**Scope notes:**
- In: [what this task covers]
- Not in: [what is explicitly excluded]

**Acceptance criteria:**

Given [initial context or state]
When [action is taken]
Then [expected outcome]

**INVEST check:**
- Independent: [yes/no - explain if no]
- Negotiable: [yes/no]
- Valuable: [yes/yes - always yes for vertical slices]
- Estimable: [yes/no]
- Small: [yes/no]
- Testable: [yes/no]

**Done:** [Specific completion condition.]
```

**Step 7 - Emit summary**
After all files are written, emit a one-line summary per task showing: task ID, title, dependencies (or "none"), and suggested order.

## Readiness gate
All must pass before writing any files:
- Every slice delivers user-visible value (no layer-only tasks)
- Every slice has at least one Given/When/Then criterion
- All blocking dependencies are named
- No slice depends on itself or creates a cycle
- Slice granularity is small enough for one session

## Output contract
One file per vertical slice in `$o`:
- `$p-task-01.md`, `$p-task-02.md`, etc.
- Format matches `/plan-tasks` output for compatibility with `/task-execute` and `/task-verify`.

## Validation
Before emitting summary, verify:
- No task has "In:" scope that spans only one layer
- Every "Depends on:" references a real sibling task file or "none"
- All Given/When/Then criteria are concrete (no vague "it works")
