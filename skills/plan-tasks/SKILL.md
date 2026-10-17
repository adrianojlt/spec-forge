---
name: plan-tasks
description: Decompose an approved spec into task files, one per vertical slice, each with Given/When/Then acceptance criteria.
argument-hint: "i=<path> o=<path> p=<prefix>"
disable-model-invocation: true
---

# plan-tasks

## Purpose
Turn an approved spec (`<p>-spec.md` from `orchestrate`, or any plan with `Status: Approved` and dependency-ordered slices) into task files, one per task, written to `$o`. Each task file is what a single executor run (`task-execute` or `tdd`, often in a fresh subagent with no other context) implements and verifies on its own, so it must carry everything that run needs.

## Inputs
- `$i` - path to the approved spec
- `$o` - directory where task files will be written (e.g. `features/user-auth/tasks/todo/`)
- `$p` - prefix for file names and task IDs (e.g. `user-auth`)

## Rules
- The plan must be approved (`Status: Approved`). If it is not, or it has unresolved open questions, confirm with the user before decomposing.
- Default to one task per slice of the plan. Split a slice only when it is too big for one executor run, or when it holds parts that ship independently.
- Never split by layer. "Set up the database schema" is not a task; "User can log in with email and password" is. Every task delivers something a user or stakeholder can observe working.
- Acceptance criteria are Given/When/Then, checkable without judgment, and cover at least one failure path besides the happy path. Carry over the slice's criteria from the plan when it has them, and add what is missing.
- Order and number tasks by dependency, matching the plan's sequence. `Depends on:` names only earlier task IDs.
- When the spec's `Codebase Findings` lists `Patterns` or `Validation commands`, copy into each task only the entries it touches, as `Patterns to mirror` and `Validate`, so the executor never has to search for them. Reference code as `file#symbol`, never by line number: earlier tasks move lines. If the spec has none, omit both sections; never invent a pattern.
- No `TBD` in scope, criteria, or Done.
- Write each task file's `Source:` header as a path relative to the task file's own folder (e.g. `../../auth-spec.md` from `tasks/todo/`), never absolute.

## Output
One file per task in `$o`, named `$p-task-<NN>.md` with `<NN>` zero-padded (01, 02, ...), following `template.md`.

The H1 is exactly `# [<p>-task-<NN>] <Title>`, brackets included: `execute-tasks` strips the bracketed ID and uses the title as the commit message. The title is an imperative phrase under 60 characters.

Report the number of files written and list each task ID and title.
