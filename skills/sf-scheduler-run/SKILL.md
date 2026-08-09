---
name: sf-scheduler-run
description: Perform one sf-scheduler task (analysis, review, or implementation) headlessly and write its output into the run's results directory. Invoked unattended by the sf-scheduler launcher.
argument-hint: "task=<path> out=<results-dir>"
---

# sf-scheduler-run

## Purpose
Execute a single sf-scheduler task file end to end while the user is away, then
write the result into the run's results directory. The sf-scheduler launcher
invokes this skill via a headless agent and has already enforced eligibility,
run-count, and a hard token/time cap; this skill only does the work and writes
output. See `sf-scheduler/docs/task-file-schema.md` for the task-file contract.

## Inputs
The launcher prompt provides:
- The task file path (markdown + YAML frontmatter; the body is the instructions).
- The task `task-type`: `analysis`, `review`, or `implementation`.
- The target `path` (code to act on).
- The output directory (`results/<run>/`) where all artifacts must be written.

## Hard rules
- Write every artifact inside the given output directory. Write nothing elsewhere except, for `implementation`, commits on a dedicated branch.
- `analysis` and `review` are READ-ONLY. Do not modify any code.
- `implementation` must work on a dedicated git branch only. Never commit to `main` (or the repo's default branch). Never push.
- Stay within the task's instructions. Do not invent extra scope.
- Respect the token budget. Be concise; do not pad output.
- If the task cannot be done (bad path, unclear instructions), write `report.md` explaining why rather than guessing.

## Procedure

**Step 1 - Read**
Read the task file in full: the frontmatter and the instructions body. Read the
target `path` as needed for the task type.

**Step 2 - Do the work by task-type**

- `analysis` (read-only): study the code at `path` per the instructions. Produce
  a report describing structure, behavior, dependencies, and risk areas useful
  for planning later work. Write it to `<out>/report.md`.

- `review` (read-only): review the code at `path` per the instructions. Produce
  a findings report: each finding with location, severity, and a suggested fix,
  framed so it can become an implementation task later. Write it to
  `<out>/report.md`. You may use the repo's `task-review` skill to structure the
  review.

- `implementation` (mutating, branch-isolated):
  1. Confirm `path` is a git repo. Determine its default branch.
  2. Create and check out a dedicated branch named
     `sf-sched/<task-file-stem>-<run-dir-name>` (e.g.
     `sf-sched/add-healthz-run-001`). Never work on the default branch.
  3. Make the minimum change that satisfies the instructions; add a test if the
     project has tests.
  4. Commit on the dedicated branch. Do not push, do not merge, do not touch the
     default branch.
  5. Write `<out>/summary.md` recording the branch name, the files changed, and a
     short summary of what was done and how to review it.

**Step 3 - Finish**
Ensure the expected artifact exists in the output directory
(`report.md` for analysis/review, `summary.md` for implementation). Keep output
focused and within budget.

## Output contract
- `analysis` / `review`: `<out>/report.md`.
- `implementation`: a commit on a dedicated branch (default branch untouched) and
  `<out>/summary.md` recording the branch name and changes.

## Notes
- The launcher writes `STOPPED` (cap/timeout) or `FAILED` (error) markers and
  manages run state. This skill does not manage state or markers.
