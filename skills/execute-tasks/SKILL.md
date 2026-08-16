---
name: execute-tasks
description: Run a contiguous range of task files unattended. Each task goes to a fresh subagent, and each completed task gets one commit titled after the task.
argument-hint: "i=<first task.md> to=<last task number> [r=yes] [v=yes] [c=<codebase>] [p=<commit prefix>]"
disable-model-invocation: true
---

# execute-tasks

## Purpose
Drive a range of task files from `tasks/todo/` to `tasks/done/` without human intervention between tasks. Each task is delegated to a fresh subagent so no task inherits the accumulated context of the one before it, and each task that finishes cleanly is committed with the task's own title as the commit message.

This skill orchestrates. It writes no code itself and it edits no task file. `task-execute` does the implementation and owns every task state transition; `task-review` and `task-verify` are optional gates layered on top. What this skill adds is the range, the isolation, the commits, and the stopping conditions.

## Inputs
- `$i` - path to the first task file of the range, in a `tasks/todo/` directory (e.g. `features/auth/tasks/todo/auth-task-01.md`). The starting task number is parsed from the `-task-NN` suffix of this filename.
- `$to` - the **inclusive** upper task number of the range. It is a task number, not a count: `i=<dir>/auth-task-01 to=5` runs tasks 01, 02, 03, 04 and 05. `to=1` with the same `i` runs task 01 alone.
- `$r` - run `task-review` after each task. Defaults to **no**. Enable with `r=yes`.
- `$v` - run `task-verify` after each task. Defaults to **no**. Enable with `v=yes`.
- `$c` - optional path to the codebase root. When supplied it is forwarded to `task-review` as its `c=` argument. When omitted, `task-review` is invoked without `c=`.
- `$p` - optional commit prefix. When supplied, every commit this skill creates during the run is prefixed with it, so all the commits belonging to one feature can be identified in the log. When omitted, commit messages are the task title alone, exactly as before.

### The commit prefix

`$p` is used verbatim, followed by a single space, in front of the commit message. Formatting is yours to choose: the skill adds no brackets, no colon, and no separator of its own.

    p=[auth]      ->  [auth] Add token expiry check
    p=auth:       ->  auth: Add token expiry check
    p=feat(auth): ->  feat(auth): Add token expiry check

Rules:
- The prefix is applied to every commit of the run, without exception, including the fallback commit written when a task's H1 is malformed.
- The prefix is applied only to the commit message. It never changes the task file, the task ID, or the report.
- If `$p` is supplied but empty or whitespace only, treat it as not supplied rather than committing a leading space.
- If `$p` already ends with whitespace, do not add a second space.

Task files are located by matching `*-task-<NN>.md` in the same directory as `$i`, not by string-concatenating a filename. This keeps the range working with any prefix and with task numbers that are not two digits.

## Hard rules
- Tasks run sequentially, in ascending task number. Never run two tasks at once.
- Never push, never create a branch, never open a pull request. Commits are local only.
- Never modify an existing skill. `task-execute`, `task-review`, and `task-verify` are consumed through their published argument contracts and left untouched.
- Never edit a task file. Only `task-execute` changes `Status:`, increments `Attempts:`, and moves files between `tasks/todo/` and `tasks/done/`.
- Never ask the user a question once the run has started. Unattended operation is the point: after preflight passes, the run proceeds to completion or to a halt.
- Redact secrets from any output.

## Preflight

Run these checks once, before the first task. They exist because the run is unattended and each task commit stages every change in the tree - a bad range or a dirty repository would be discovered only after work had already been committed.

If any check fails, refuse the run: report which check failed and why, and change nothing. No task is executed, no file is moved, no commit is created.

1. **Input file exists.** `$i` resolves to an existing file. If not, refuse and name the path that could not be found.
2. **Start number parses.** The filename of `$i` matches `*-task-<NN>.md` and yields a start number. If it does not, refuse and state that the range cannot be derived from that filename.
3. **Range is not inverted.** `$to` is greater than or equal to the start number. If `$to` is lower, refuse and name both numbers. Never treat an inverted range as an empty run that succeeds.
4. **Task directory layout.** `$i` sits in a directory named `tasks/todo/` with a sibling `tasks/done/`. If `tasks/done/` is missing, refuse. If the sibling `tasks/feedback/` is missing, create it - `task-execute` writes its reports there.
5. **Git repository.** The working directory is inside a git repository. If not, refuse and state that the run cannot commit outside a repository.
6. **Commit identity is configured.** Both `git config user.name` and `git config user.email` return a value. If either is empty, refuse and name the missing one. Correct authorship is a requirement of this skill, not an afterthought, so an unattended run must not start without it.
7. **Working tree is clean.** `git status --porcelain` produces no output. If the tree is dirty, refuse, list the dirty paths, and tell the user to commit or stash them first. This check exists because each task commit runs `git add -A`: without it, pre-existing unrelated changes would be swept into the first task's commit and attributed to work that did not produce them.

## Running one task

This is the body of the loop. It covers a single task file and is repeated for every task in the range.

Delegate the task to a **fresh subagent**. Every task gets its own, and every retry attempt gets its own: a subagent is never reused, and never inherits the context of a previous task or a previous attempt. That isolation is the reason this skill exists - it is what keeps task five from being executed inside the accumulated context of tasks one through four.

Give the subagent this mandate, and nothing beyond it:

1. Read and follow `task-execute/SKILL.md` with `i=<task file>`.
2. Only if `$r` is enabled: read and follow `task-review/SKILL.md` with `i=<task file>`. Add `c=<codebase>` when `$c` was supplied to this skill; when `$c` was not supplied, omit the `c=` argument entirely rather than passing it empty.
3. Only if `$v` is enabled: read and follow `task-verify/SKILL.md` with `i=<task file>`.

When `$r` is disabled, step 2 does not happen at all. When `$v` is disabled, step 3 does not happen at all. `task-execute` self-checks its own acceptance criteria either way, so a task still reaches a real verdict with both gates off.

State these prohibitions to the subagent explicitly:

- **No git writes.** The subagent must never run `git commit`, `git add`, `git push`, `git stash`, or create a branch or tag. Committing is the caller's job and happens after the subagent has finished. A subagent that judged its own work must not also be the thing that writes that judgement into history.
- **No work outside the task.** It implements only what the task file's `Scope notes: In` describes, exactly as `task-execute` already requires.
- **No touching other tasks.** It reads and writes only this task's file and its own report; it must not advance, skip, or modify any other task in the range.

Report progress for this task, then continue to the outcome step below.

## Outcome and commit

When the subagent returns, do not take its word for what happened. Re-read the task file from disk.

The authoritative success signal is both of these together:
- the task file's `Status:` reads `Done`, and
- the file now sits in `tasks/done/` rather than `tasks/todo/`.

If the subagent reports success but the file says otherwise, the file wins. `task-execute` owns those transitions and only sets them after its own verification passed, so disk state is evidence and the subagent's narrative is not.

**On success**, commit the task:

1. Derive the commit message from the task file's H1. The H1 has the shape `# [prefix-task-NN] Task Title`; strip the leading bracketed ID and use the remaining title. `# [auth-task-03] Add token expiry check` becomes `Add token expiry check`.
2. If `$p` was supplied, prepend it and a single space to that message, as described under "The commit prefix".
3. `git add -A`.
4. Commit with that message.

Commit hygiene, all of it required:
- Authorship comes from the repository's own `git config user.name` and `user.email`. Do not override the author.
- No `Co-Authored-By` trailer of any kind.
- No "Generated with" footer, no tool attribution, no emoji added to the subject.
- The message is the task title, with `$p` in front when it was supplied, and nothing else. No task ID, and no conventional-commit type unless `$p` itself supplies one.

**On anything other than success**, create no commit. A task left in `tasks/todo/` with `Status: Revise` is going to be retried, and a task at `Status: Blocked` halts the run; neither has produced work that belongs in history. The retry and halt behavior itself is defined in the control-flow section.

Two edge cases:
- **Nothing to commit.** If the task completed but staged no changes, `git commit` would fail on an empty commit. Skip the commit, record the task as completed with no changes, and continue. Do not force an empty commit.
- **Malformed H1.** If the task file has no H1, or its H1 does not match `# [prefix-task-NN] Title`, do not guess a message. Use the task ID taken from the filename as the commit message, still prefixed with `$p` when it was supplied, and note the malformed H1 in the report, so the commit is still traceable and the deviation is visible.

## Control flow

Walk task numbers ascending, from the start number parsed out of `$i` through `$to` inclusive. For each number `NN`, locate the task by matching `*-task-<NN>.md` in the `tasks/todo/` directory of `$i`, and in its sibling `tasks/done/`. Match on the filesystem; never build a filename by string arithmetic. That keeps the walk working across prefixes, and across task numbers whose padding is not two digits.

Order is numeric and nothing else. Do not reorder by `Depends on:`. If a task depends on one that has not run, `task-execute` refuses it, which surfaces as a block and stops the run - the correct outcome, since the range was specified wrongly.

For each number in the range:

**No file matches `NN`.** Note it as skipped-missing and continue to the next number. A gap is not an error, and it produces no commit.

**The match is already in `tasks/done/`.** Note it as skipped-already-done and continue. This is what makes re-invoking a range after a halt work: everything finished on the earlier run is passed over. It produces no commit - never manufacture an empty commit to mark a task that was already complete.

**The match is in `tasks/todo/`.** Run it:

1. Delegate to a fresh subagent, per the "Running one task" section.
2. Re-read the task file and apply the "Outcome and commit" section.
3. Branch on what the file now says:
   - **`Status: Done`** - the commit has been made. Advance to the next number.
   - **`Status: Revise`** and `Attempts` is below `Max attempts` - retry. Go back to step 1 with a **brand-new subagent**. Never reuse the subagent that just failed; `task-execute` reads the latest report in `tasks/feedback/` and re-enters targeted at the failed checks only.
   - **`Status: Blocked`**, or `Attempts` has reached `Max attempts` - halt.

**Halting.** A blocked task stops the entire run at that task. Do not advance to the next number, and do not attempt the rest of the range - later tasks generally build on earlier ones, so continuing past a block produces damage rather than progress.

On halt, leave the working tree exactly as it is. Do not stash, do not revert, do not commit the partial work. The user needs to see what the blocked attempt produced. Name the blocked task, the reason, and the uncommitted work in the report.

This has a consequence worth stating plainly: because preflight requires a clean tree, re-invoking the range after a halt will be refused until the user commits, stashes, or discards that partial work. That is deliberate. It forces a decision about the failed task instead of quietly burying it in the next task's commit.

**Degenerate ranges.**
- `$to` equals the start number: a one-task range. Run it exactly as above.
- Every task in the range is already in `tasks/done/`: the walk completes having executed nothing. Report it as a no-op, never as success. See the reporting section.

## Reporting

Nobody is watching an unattended run while it happens, so the output has one job: make a halt, a skip, and a no-op each impossible to mistake for completed work.

**Between tasks**, emit a single line naming the task and its outcome. One line, not the execution report - the point of the range is that the user reads the end, not the middle. Keep the full detail for the end of the run or for a halt.

```
task-03 done, committed "[auth] Add token expiry check"   (3 of 7)
task-04 skipped, already done                        (4 of 7)
```

**At the end of the run, or at a halt**, report:

1. **Every task in the range**, each with exactly one outcome:
   - `executed-and-committed` - ran, reached `Status: Done`, and produced a commit.
   - `skipped-missing` - no task file matched that number.
   - `skipped-already-done` - the task file was already in `tasks/done/`.
   - `blocked` - reached `Status: Blocked` or exhausted `Max attempts`. This is where the run stopped.

   A task that completed but staged no changes is still `executed-and-committed` in shape, with its commit line reading "no changes to commit". Never leave a task out of the list.

2. **Every commit subject** created during the run, in order, as committed - including the `$p` prefix when one was used. This is the audit trail: with both gates off, these commits were written on the strength of `task-execute`'s self-check alone, so the user needs to see exactly what landed in order to judge or unwind it.

3. **Where the run stopped and why.** Either the range completed, or it halted at a named task for a named reason.

4. **Whether uncommitted work remains** in the working tree. On a halt this is almost always yes, and it must be stated, along with the consequence: preflight will refuse to re-run the range until that work is committed, stashed, or discarded.

**The no-op rule.** If the walk executed nothing - every number skipped as missing or already done - say so plainly: the range was a no-op and no work was performed. Do not report a no-op as a successful run. An empty range that reads like success is the one failure mode of this skill that a user cannot detect from the output alone.
