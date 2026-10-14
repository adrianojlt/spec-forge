---
name: sf-scheduler-run
description: Perform one sf-scheduler task (analysis, review, or implementation) headlessly and write its output into the run's results directory. Invoked unattended by the sf-scheduler launcher.
argument-hint: "task=<path> out=<results-dir>"
---

# sf-scheduler-run

## Purpose
Do one sf-scheduler task while the user is away and leave the result in the run's output directory. The launcher has already enforced eligibility, run count, and the token/time cap, and it owns run state and the `STOPPED` / `FAILED` markers. This skill only does the work. Task-file contract: `sf-scheduler/docs/task-file-schema.md`.

## Inputs
From the launcher prompt: the task file (YAML frontmatter + instructions body), its `task-type` (`analysis`, `review`, `implementation`), the target `path`, and the output directory `<out>` (`results/<run>/`).

## Rules
- Write every artifact inside `<out>`. The only exception is commits on the implementation branch.
- Stay within the task's instructions and the token budget.
- If the task cannot be done (bad path, unclear instructions), write `<out>/report.md` saying why instead of guessing.

## By task type
- **analysis** (read-only): study `path` per the instructions; report structure, behavior, dependencies and risk areas useful for planning. Output `<out>/report.md`.
- **review** (read-only): review `path` per the instructions; each finding has location, severity and a suggested fix, framed so it can become an implementation task. The `task-review` skill may structure it. Output `<out>/report.md`.
- **implementation**: `path` must be a git repo. Create and check out `sf-sched/<task-file-stem>-<run-dir-name>` (e.g. `sf-sched/add-healthz-run-001`); never work on, merge into, or push the default branch, and never push at all. Make the change the instructions ask for, with a test if the project has tests, and commit on that branch. Output `<out>/summary.md` with the branch name, files changed, what was done, and how to review it.
