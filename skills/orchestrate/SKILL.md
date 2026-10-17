---
name: orchestrate
description: "Take a feature from idea to committed code: size the change, interview, one spec with an approval gate, task files, then an unattended execute-tasks run. Ceremony scales with the change; trivial ones are sent back to be made directly."
argument-hint: "[i=<idea-file>] [o=<output-dir>] [p=<prefix>] [c=<codebase>]"
disable-model-invocation: true
---

# orchestrate

## Purpose
Take an idea to committed code with two human touchpoints: approving the spec, and confirming the task list before the unattended run (small changes merge them into one). Everything else is driven by files on disk, so any step can be resumed in a fresh session.

```
idea / draft / grilling summary
  -> size -> tier                      trivial: stop, make the change directly
  -> interview -> <p>-spec.md          gate 1: approve spec
  -> plan-tasks -> tasks/todo/*.md     gate 2: confirm tasks + run options
  -> execute-tasks (fresh subagent per task, one commit per task)
  -> final report
```

This is the only skill that produces a spec. To plan without executing, stop at gate 2: the spec and task files stay on disk, and `/execute-tasks` can run them later.

## Inputs
- `$i` - idea, draft, or a summary written by `/grilling`. Optional: if omitted, take the idea from the conversation.
- `$o` - feature directory for all artifacts (e.g. `features/auth/`). Ask if missing.
- `$p` - prefix for artifact filenames and task IDs. If missing, use the last segment of `$o` and say so.
- `$c` - codebase root. Optional, defaults to the current working directory.

## Rules
- Two gates: spec approval (step 2) and task confirmation (step 4). Tier small merges them into one approval; no tier skips them. Advance only on an explicit yes.
- This skill writes the spec and nothing else by hand. Task files belong to `plan-tasks`; code, task status and commits belong to `execute-tasks` and the executor it drives. The only exceptions are creating `tasks/done/` and the optional artifacts commit in step 4.
- If a delegated skill fails, stop and report. No silent recovery.
- If the user says stop, stop and report what exists on disk and what remains.

## Procedure

### 0. Size
Read `$i` and look up in `$c` what the change touches. Rate three signals and take the highest tier any of them reaches:

| Tier | Files touched | New dependency, contract or schema | Design choice left to the user |
|------|---------------|------------------------------------|--------------------------------|
| trivial | 1, a few lines | none | none, the change is obvious |
| small | 1 file or function | none | none once the code is read |
| standard | 2 or more | any | at least one |

A change that touches security (authentication, authorization, user input, database queries, file paths, cryptography, secrets) or a public API is at least standard.

State the tier and the signals behind it in one line. The user can override it; their tier wins.
- trivial: say the change is faster made directly, without a spec, and stop. If the user still wants it on record, continue as small.
- small: no interview questions, a one-slice spec, and one gate for spec and run options.
- standard: every step as written.

When a later step finds more than the tier assumed (a decision `$c` cannot settle, a second file, a security touch), move up a tier, say so, and continue with that tier's steps. Never move down without the user.

### 1. Interview
Read `$i`. If it records a confirmed understanding (e.g. a `/grilling` summary), treat what it settles as decided and ask only about the gaps. If `overview/principles.md` exists, its rules are binding.

Interview in the style of `grilling/SKILL.md`: one question at a time, each with your recommended answer. Look facts up in `$c` instead of asking; the decisions are the user's.

While looking things up, collect for the spec's `Codebase Findings` what a fresh executor would otherwise have to search for: one canonical example (`file#symbol`) per convention the change touches (naming, error handling, logging, data access, tests, local gotchas), and the commands that build and test the affected code. Where the codebase has no equivalent, write "none found"; never invent a pattern.

Stop when you can write the spec without inventing anything. Skip questions whose answer would not change the spec.

Tier small: ask no questions, but still collect the findings. A decision the spec needs and `$c` cannot settle makes the tier standard.

### 2. Spec (gate 1)
Write `<o>/<p>-spec.md` from `template.md` with `Status: Draft`. Slices are vertical (each delivers something a user can observe), ordered by dependency, and carry Given/When/Then acceptance criteria.

Present in chat: the slice sequence, key decisions and their tradeoffs, top risks, open questions. Ask the user to approve, request edits (apply them and re-present), or edit the file themselves.

Tier small: present the spec together with the run options from step 4. One explicit yes approves both.

On explicit approval, set `Status: Approved`.

### 3. Tasks
Read and follow `plan-tasks/SKILL.md` with `i=<o>/<p>-spec.md o=<o>/tasks/todo/ p=<p>`.

Create `<o>/tasks/done/` if missing; `execute-tasks` preflight requires it.

### 4. Confirm tasks and run options (gate 2)
Show the task list (ID, title, depends on). Ask for the run options in one message, with defaults:
- executor: `task-execute` (default) or `tdd`
- task-review after each task: no (default) or yes
- task-verify after each task: no (default) or yes
- commit prefix: none (default), e.g. `[<p>]`

"go" accepts all defaults.

Tier small: the run options were settled at gate 1, so show the task and ask nothing. If `plan-tasks` wrote more than one task, the tier was wrong: say so and hold this gate as normal.

Then run `git status --porcelain` in the working directory. `execute-tasks` refuses a dirty tree, because each task commit runs `git add -A`.
- Clean: continue.
- Dirty only with files under `<o>` written by this run: offer one commit of exactly those paths, message `<p>: spec and tasks`, no `Co-Authored-By` trailer or tool footer (same hygiene as `execute-tasks` commits). If the user declines, stop and tell them to commit or stash before resuming.
- Dirty with anything else: list the paths and stop. The user decides what to do with them.

### 5. Execute
Read and follow `execute-tasks/SKILL.md` with `i=<o>/tasks/todo/<p>-task-01.md to=<last task number>`, adding `e=tdd`, `r=yes`, `v=yes` and `p=<commit prefix>` as chosen in step 4, and `c=<c>` when `$c` was given.

The run is unattended from here: no questions until `execute-tasks` completes or halts.

### 6. Final report
- Artifacts: spec path, tasks directory.
- The `execute-tasks` report as produced: per-task outcomes, commit subjects, stop reason, uncommitted work.
- On a halt: the blocked task, its latest report in `tasks/feedback/`, and how to resume (deal with the partial work, then rerun `/execute-tasks` with the same range; done tasks are skipped).
- Next steps, one line each: open a PR (the `pr` skill), and `/graduate o=<o> p=<p>` once the feature is merged and stable.

## Resuming
State lives on disk. Pick up at the first step whose output is missing:
- No spec -> step 0. Spec `Status: Draft` -> step 1 or 2.
- Spec `Status: Approved`, no task files -> step 3.
- Task files in `tasks/todo/` -> step 4.

The tier is not stored, so a resumed run holds every remaining gate as normal.
