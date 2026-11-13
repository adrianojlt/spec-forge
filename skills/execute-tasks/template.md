---
task: [task ID, e.g. auth-task-01]
attempt: [integer, matches the task's current Attempts]
verdict: [PASS | FAIL]
failed_checks:
  # One line per Validate command that did not exit 0. Empty on PASS.
  # This list is the re-entry payload a later executor run fixes. Format:
  # "<command>: exit <code>, <the line of its output that shows why>".
  - "[command]: exit [code], [short actionable description]"
---

# Validate Report: [prefix-task-NN]

Source: [relative path to the task file, e.g. ../done/auth-task-01.md - never absolute]
Date: [date]
Run from: [the codebase root the commands ran in]

---

## Commands

- [pass | fail] `[command]` - exit [code] - [the last lines of its output that show the result]
- [pass | fail] `[command]` - exit [code] - [output]
