---
name: task-review
description: "Review code changes for quality, security, performance, spec compliance, and test quality. Report-only, task-scoped, language-aware."
argument-hint: "i=<task.md> [c=<codebase>]"
disable-model-invocation: true
---

# task-review

## Purpose
Review the code changes produced by `/task-execute` or `/tdd` for a single task. Produce a structured report with findings across five dimensions: code quality, security, performance, spec compliance, and test quality.

Read-only: writes no code, moves no files, changes no status. The report is for the human (or a future `/task-execute` run) to act on.

Sits between execution and verification:
```
task-execute / tdd -> task-review -> task-verify
```

## Inputs
- `$i` - path to a task file (in `tasks/todo/` or `tasks/done/`)
- `$c` - codebase root (optional; inferred from `$i` location if not given)

## Hard rules
- Read-only. Never edit source files. Never move the task file. Never change its `Status:`.
- Review only the changes in scope for this task (git diff against the base branch, or the files the task touched).
- Every finding must cite evidence: file path, line number or range, and a concrete quote or description of the issue.
- Every finding must have a severity: blocker, warning, or nit.
- Do not flag style issues that are already handled by the project's formatter or linter.
- Do not invent requirements beyond what the task file specifies.
- If the language can be detected, load the corresponding coding-standards skill (e.g. `/java-coding-standards`, `/go-coding-standards`) and use it as the reference for code quality findings.

## Procedure

**Step 1 - Read task and identify scope**
Read `$i` in full. Note:
- Acceptance criteria (Given/When/Then)
- Scope notes (In / Not in)
- Dependencies

**Step 2 - Identify changed files**
Determine which files were changed for this task:
- If inside a git repo: use `git diff` against the base branch or the last commit before this task
- If no git: read the files mentioned in the task's scope notes
- List all changed files with line ranges

**Step 3 - Detect language and load standards**
Identify the primary language from file extensions. If a matching coding-standards skill exists, load it and use its rules as the reference for code quality findings. If no matching skill exists, use `/coding-principles` as the reference.

**Step 4 - Review across five dimensions**

For each dimension, scan the changed files and record findings:

**4a - Code quality and style**
- Naming clarity (variables, functions, types)
- Function length and complexity
- DRY violations (duplicated logic)
- KISS violations (over-engineering, unnecessary abstractions)
- Code smells (deep nesting, magic numbers, dead code)
- Consistency with existing codebase patterns
- Reference: loaded coding-standards skill

**4b - Security**
- Hardcoded secrets, tokens, or credentials
- SQL injection or command injection vectors
- Missing input validation on external inputs
- Insecure defaults (open permissions, disabled auth)
- Sensitive data in logs or error messages
- Missing authentication or authorization checks

**4c - Performance**
- N+1 query patterns
- Unnecessary allocations in hot paths
- Missing database indexes for new queries
- Unbounded queries (no LIMIT, no pagination)
- Blocking calls where async is expected
- Redundant computation or repeated I/O

**4d - Spec compliance**
- Does the implementation match the task's `Scope notes: In`?
- Is there code outside `Scope notes: Not in` (scope creep)?
- Are all `Depends on` tasks respected?
- Do the acceptance criteria map to actual behavior?
- Are there undocumented side effects?

**4e - Test quality**
- Do tests cover all Given/When/Then criteria?
- Are assertions meaningful (not just "no exception thrown")?
- Are tests deterministic (no flaky timing, no external dependencies without mocks)?
- Test naming describes the scenario
- No test smells (testing implementation details, excessive mocking, shared mutable state)

**Step 5 - Classify findings**
For each finding, assign severity:
- **Blocker** - Must fix before merging. Bugs, security vulnerabilities, spec violations, data loss risks.
- **Warning** - Should fix. Code quality issues, performance problems, missing edge cases.
- **Nit** - Nice to fix. Style preferences, minor readability improvements.

**Step 6 - Write report**
Write the report using `template.md` and persist it so the loop can re-enter from it.

Write to the task's sibling `feedback/` directory (create it if absent), next to `tasks/todo/` and `tasks/done/`:
```
<feature>/tasks/feedback/<task-id>-review-<NN>.md
```
`<NN>` = the task's current `Attempts` value, zero-padded (`01`, `02`, ...). Highest `<NN>` = latest review. Do not overwrite an earlier attempt's report; each attempt gets its own file so the loop history stays on disk.

Populate the frontmatter exactly:
- `task` / `attempt` - from the task file.
- `verdict` - per the Verdict rules below.
- `failed_checks` - one line per BLOCKER, plus any WARNING that must be fixed before re-execution. Each line is `<finding-id>: <what must change>`. On PASS, leave the list empty. This list is the contract a later `/task-execute` reads to retry only the failed items.

Also present the report in chat.

## Readiness gate
- All five dimensions were reviewed (or explicitly marked as N/A with rationale)
- Every finding has: severity, file path, line reference, description, and suggested fix
- No finding is a style issue already handled by the project's formatter
- Summary includes: total findings by severity, overall verdict (pass/fail)

## Output contract
A structured report written to `<feature>/tasks/feedback/<task-id>-review-<NN>.md` and presented in chat. See `template.md` for required sections and the frontmatter contract. Writing this report file is the only file the skill creates; it still never edits source or the task file.

**Verdict rules:**
- Any blocker = **FAIL** (must fix before task-verify)
- Warnings only = **PASS WITH WARNINGS** (can proceed, but should address)
- Nits only or clean = **PASS**

## Validation
Before presenting the report, verify:
- Every blocker and warning has a concrete suggested fix (not just "improve this")
- The spec compliance section explicitly references the task's acceptance criteria
- The summary counts match the findings listed
