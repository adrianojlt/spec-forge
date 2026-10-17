---
name: tdd
description: Implement a task test-first with red-green-refactor, until every Given/When/Then is covered by a passing test
argument-hint: "i=<task.md> [c=<codebase>]"
disable-model-invocation: true
---

# tdd

## Purpose
An executor alternative to `task-execute` for test-first work. Same inputs, same feedback files, same task state transitions; the difference is that every acceptance criterion must end up covered by a test written before the code that makes it pass.

## Inputs
- `$i` - task file from `tasks/todo/`, or from `tasks/done/` when a review or verify failed on it
- `$c` - codebase root (optional; inferred from `$i` location if not given)

## Rules
- Follow `task-execute/SKILL.md` for scope, dependencies, retry detection, and recording the outcome. On a retry, write a failing test for each failed check, then make it pass.
- Before coding, state the interface: new functions, endpoints or types, and changes to existing signatures or side effects. When invoked directly by a user, wait for them to confirm or adjust it. When driven non-interactively (`execute-tasks`, `orchestrate`, `sf-scheduler`), proceed and record the assumed interface in the attempt report.
- Use the project's existing test framework, locations and naming. Follow the task's `Patterns to mirror` and `Validate` as `task-execute` does.
- Red-green-refactor per behavior: see the new test fail for the expected reason, write the minimum code to pass, then refactor with the suite green. Do not batch several failing tests.
- Success means every Given/When/Then maps to a named, passing test, listed in the report. An unmapped criterion is a failure and goes in `failed_checks`.
- Write the report's `Source:` as a path relative to the report's folder (e.g. `../todo/auth-task-01.md`), never absolute.

## Output
Tests and implementation in the codebase, plus `tasks/feedback/<task-id>-attempt-<NN>.md` following `template.md`.
