---
task: [task ID, e.g. auth-task-01]
attempt: [integer, matches the task's current Attempts]
verdict: [PASS | FAIL]
failed_checks:
  # One line per floor hit and per command that did not exit 0. Empty on PASS.
  # This list is the re-entry payload a later executor run fixes. Formats:
  # "floor: <move> at <file:line>"
  # "<command>: exit <code>, <the line of its output that shows why>".
  - "floor: [move, e.g. test skipped] at [file:line]"
  - "[command]: exit [code], [short actionable description]"
---

# Validate Report: [prefix-task-NN]

Source: [relative path to the task file, e.g. ../done/auth-task-01.md - never absolute]
Date: [date]
Run from: [the codebase root the commands ran in]

---

## Floor

- [clean | hit: <move> at <file:line> - <the added or removed line>]

## Commands

- [pass | fail] `[command]` ([Validate | Definition of Done]) - exit [code] - [the last lines of its output that show the result]
- [none: the task has no Validate section and principles.md no Definition of Done]
