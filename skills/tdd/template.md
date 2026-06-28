---
task: [task ID, e.g. auth-task-01]
attempt: [integer, matches the task's Attempts after this run]
result: [Done | Revise | Blocked]
failed_checks:
  # One line per Given/When/Then left uncovered by a passing test. Empty on Done.
  # Format: "<criterion ref>: <what is missing>".
  - "[AC2]: [short actionable description]"
---

# TDD Execution Report: [Task ID] [Task Title]

Source: [path to task file]
Date: [date]
Status: [Done | Revise | Blocked]

---

## Task
[One sentence: what this task implemented.]

## Interface Changes
[Functions, endpoints, or types added or modified. Empty if none.]

| Item | Change |
|------|--------|
| [function/endpoint] | [added/modified: description] |

## Behaviors Tested

### Behavior 1: [Given/When/Then summary]

| Phase | Result |
|-------|--------|
| RED | Test `[test name]` fails: `[failure message]` |
| GREEN | Test passes. Code: `[file:line]` |
| REFACTOR | [changes made, or "none needed"] |

---

*(repeat per behavior)*

## Coverage Summary

| AC Criterion | Test Name | Status |
|-------------|-----------|--------|
| Given... When... Then... | `[test name]` | PASS |

## Notes
[Any non-obvious decisions, workarounds, or deferred follow-ups.]
