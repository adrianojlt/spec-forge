---
task: [task ID, e.g. auth-task-01]
attempt: [integer, matches the task's current Attempts]
verdict: [PASS | FAIL]
failed_checks:
  # One line per failed acceptance criterion / Done condition. Empty on PASS.
  # This list is the re-entry payload a later task-execute fixes. Format:
  # "<criterion ref>: <what was observed vs expected>".
  - "[AC3]: [short actionable description]"
---

# Verification Report: [prefix-task-NN]

Task: [path to task file]
Date: [date]
Overall: [all pass | failures found]

---

## Acceptance criteria

- [pass | fail] Given ... When ... Then ...  - [evidence: test name, command output, or observed behavior]
- [pass | fail] Given ... When ... Then ...  - [evidence]

## Done condition

- [met | not met]: [the task's Done definition] - [evidence]

## Failures

- [criterion that failed and what was observed instead | none]
