---
task: [task ID, e.g. auth-task-01]
attempt: [integer, matches the task's Attempts after this run]
result: [Done | Revise | Blocked]
failed_checks:
  # One line per failed acceptance criterion / Done condition. Empty on Done.
  # Format: "<criterion ref>: <what was observed vs expected>".
  - "[AC2]: [short actionable description]"
---

# Execution Report: [prefix-task-NN]

Task: [path to task file]
Date: [date]
Result: [Done | Revise | Blocked]

---

## Changes

- [file path: what changed]
- [file path: what changed]

## Acceptance criteria

- [pass | fail] Given ... When ... Then ...  - [evidence: test name, command output, or observed behavior]
- [pass | fail] Given ... When ... Then ...  - [evidence]

## Done condition

- [met | not met]: [the task's Done definition] - [evidence]

## File move

- [moved tasks/todo/<file> -> tasks/done/<file>, Status: Done | left in tasks/todo/ because <reason>]

## Notes

- [anything deferred, or "none"]
