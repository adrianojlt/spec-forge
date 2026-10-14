---
name: execute-tasks
description: Run a contiguous range of task files unattended. Each task goes to a fresh subagent, and each completed task gets one commit titled after the task.
argument-hint: "i=<first task.md> to=<last task number> [e=tdd] [r=yes] [v=yes] [c=<codebase>] [p=<commit prefix>]"
disable-model-invocation: true
---

# execute-tasks

## Purpose
Drive a range of task files from `tasks/todo/` to `tasks/done/` with nobody watching. This skill writes no code and edits no task file: the executor (`task-execute`, or `tdd` with `e=tdd`) implements and owns every task state transition, and `task-review` / `task-verify` are optional gates. What this skill adds is the range, subagent isolation, one commit per task, and stopping conditions.

## Inputs
- `$i` - first task file of the range, in `tasks/todo/` (e.g. `features/auth/tasks/todo/auth-task-01.md`). The start number comes from its `-task-NN` suffix.
- `$to` - **inclusive** last task number (a number, not a count): `i=.../auth-task-01.md to=5` runs 01 to 05.
- `$e` - `e=tdd` uses `tdd` as executor; default `task-execute`. Any other value refuses the run.
- `$r` - `r=yes` runs `task-review` after each task (default no).
- `$v` - `v=yes` runs `task-verify` after each task (default no).
- `$c` - codebase root, forwarded to `task-review` as `c=` only when supplied.
- `$p` - commit prefix, used verbatim plus one space (`p=[auth]` -> `[auth] Add token expiry check`). No separator of its own; no extra space if `$p` already ends with whitespace; empty or whitespace-only counts as not supplied. Applies to every commit of the run and to nothing else.

## Rules
- Sequential, ascending task number only. Never two tasks at once, never reorder by `Depends on:` (an unmet dependency surfaces as a block, which is correct: the range was wrong).
- Locate tasks by matching `*-task-<NN>.md` on the filesystem in `tasks/todo/` and `tasks/done/`, never by building a filename.
- Never push, branch, or open a PR. Commits are local.
- Never edit a task file.
- Never ask the user anything once the run has started.

## Preflight
Check once, before the first task. On any failure, refuse the run, say which check failed, and change nothing.
1. `$i` exists and its filename yields a start number.
2. `$to` >= start number. An inverted range is an error, never an empty success.
3. `$i` is in `tasks/todo/` with a sibling `tasks/done/`. Create a missing sibling `tasks/feedback/`.
4. The working directory is a git repository, and `git config user.name` and `user.email` are both set.
5. `git status --porcelain` is empty. Each task commit runs `git add -A`, so pre-existing changes would be swept into the first commit. List dirty paths and ask the user to commit or stash.

## Running one task
Each attempt uses up to two **fresh subagents**, never reused and never sharing context:
- **Executor**: read and follow `task-execute/SKILL.md` (or `tdd/SKILL.md` with `e=tdd`) with `i=<task file>`.
- **Checker**: only when the executor left the task `Done` in `tasks/done/` and a gate is enabled. Runs `task-review/SKILL.md` (if `$r`, with `c=` when supplied) then `task-verify/SKILL.md` (if `$v`). Read-only; it writes its reports and nothing else.

This keeps task five out of the context of tasks one to four, and keeps any agent from grading its own work. Tell every subagent explicitly: no git writes of any kind (commit, add, push, stash, branch, tag); no work outside the task's `Scope notes: In`; no touching other tasks' files.

## Outcome and commit
Judge from disk, never from a subagent's narrative. Success is all of:
- task `Status: Done` and the file in `tasks/done/`;
- for each enabled gate, its report for this attempt (`tasks/feedback/<task-id>-review-<NN>.md` / `-verify-<NN>.md`, `<NN>` = current `Attempts`) has `verdict: PASS` or `PASS_WITH_WARNINGS`.

An enabled gate with no report for this attempt means the checker failed: halt.

On success, `git add -A` and commit. The message is the task's H1 with the bracketed ID stripped (`# [auth-task-03] Add token expiry check` -> `Add token expiry check`), with `$p` in front when supplied, and nothing else: no task ID, no `Co-Authored-By` trailer, no generated-with footer, no emoji. Authorship comes from the repo's git config. If the H1 does not match that shape, use the task ID from the filename and note it in the report. If nothing is staged, skip the commit and record "no changes"; never force an empty commit.

No other outcome produces a commit.

## Control flow
For each number from start to `$to`:
- **No matching file**: skipped-missing.
- **In `tasks/done/`**: skipped-already-done, no commit. Exception: if its latest review or verify report is `verdict: FAIL` (an earlier run stopped mid-retry), run it like a todo task.
- **In `tasks/todo/`**: run it, then branch on disk state:
  - success: committed, next number;
  - `Done` but a gate `FAIL`, or `Status: Revise`: retry with a brand-new executor subagent. The executor reads the latest failing report, fixes only its `failed_checks`, and sets `Blocked` itself once `Max attempts` is used up;
  - `Status: Blocked`: halt.

**Halt** stops the whole run at that task; later tasks usually build on it. Leave the working tree exactly as it is (no stash, revert, or commit) so the user can see what the failed attempt produced. Because preflight needs a clean tree, rerunning the range is refused until the user deals with that work. This is deliberate: the failed task is never buried in the next task's commit.

## Reporting
Between tasks, one line each: `task-03 done, committed "[auth] Add token expiry check" (3 of 7)`.

At the end or at a halt:
1. Every number in the range with exactly one outcome: `executed-and-committed` (or "no changes to commit"), `skipped-missing`, `skipped-already-done`, `blocked`.
2. Every commit subject created, in order.
3. Where the run stopped and why.
4. Whether uncommitted work remains, and that a rerun is refused until it is handled.

If nothing was executed, say plainly that the run was a no-op. Never report a no-op as success.
