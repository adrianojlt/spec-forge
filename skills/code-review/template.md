---
task: [task ID, e.g. auth-task-01]
attempt: [integer, matches the task's current Attempts count]
verdict: [PASS | PASS_WITH_WARNINGS | FAIL]
failed_checks:
  # One line per BLOCKER (plus any WARNING that must be fixed before re-execution).
  # Format: "<finding-id>: <one-line what must change>". This list is the re-entry payload:
  # a later task-execute run fixes ONLY these items. Empty list on PASS.
  - "[Q-01]: [short actionable description]"
  - "[SC-02]: [short actionable description]"
---

# Code Review Report

**Task:** [task ID and title]
**Date:** [date]
**Reviewer:** AI (code-review skill)
**Language:** [detected language]
**Standards reference:** [loaded coding-standards skill or coding-principles]

---

## Summary

| Severity | Count |
|----------|-------|
| Blocker  |       |
| Warning  |       |
| Nit      |       |
| **Total**|       |

**Verdict:** [PASS | PASS WITH WARNINGS | FAIL]

---

## Code Quality and Style

### [Q-NN] [Short title] - [BLOCKER|WARNING|NIT]
- **File:** `path/to/file.ext:line`
- **Issue:** [description]
- **Suggestion:** [concrete fix]

---

## Security

### [S-NN] [Short title] - [BLOCKER|WARNING|NIT]
- **File:** `path/to/file.ext:line`
- **Issue:** [description]
- **Suggestion:** [concrete fix]

---

## Performance

### [P-NN] [Short title] - [BLOCKER|WARNING|NIT]
- **File:** `path/to/file.ext:line`
- **Issue:** [description]
- **Suggestion:** [concrete fix]

---

## Spec Compliance

### [SC-NN] [Short title] - [BLOCKER|WARNING|NIT]
- **File:** `path/to/file.ext:line`
- **Criterion:** [Given/When/Then from task file]
- **Issue:** [description]
- **Suggestion:** [concrete fix]

---

## Test Quality

### [T-NN] [Short title] - [BLOCKER|WARNING|NIT]
- **File:** `path/to/file.ext:line`
- **Issue:** [description]
- **Suggestion:** [concrete fix]

---

## Verdict Detail

[One paragraph: overall assessment, what must be fixed before proceeding, what can be deferred.]
