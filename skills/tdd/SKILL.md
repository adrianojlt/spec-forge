---
name: tdd
description: Implement a task using strict red-green-refactor TDD - one failing test at a time, minimum code to pass, refactor after green
argument-hint: "i=<task.md> [c=<codebase>]"
disable-model-invocation: true
---

# tdd

## Purpose
Implement one task via strict TDD: confirm the interface, write one failing test, write minimum code to pass, refactor, repeat until all Given/When/Then acceptance criteria are covered by passing tests.

Replaces `/task-execute` for teams that require test-first discipline. Output format is compatible: moves the task file from `tasks/todo/` to `tasks/done/` on completion.

## Inputs
- `$i` - task file from `tasks/todo/`
- `$c` - codebase root (optional; inferred from `$i` location if not given)

## Hard rules
- No test-after. Tests must be written before the implementation code that makes them pass.
- One test at a time. Do not write multiple failing tests before making them pass.
- No skipping RED. Confirm the test fails before writing implementation.
- Refactor only after GREEN. Do not refactor while a test is failing.
- Do not advance to the next behavior until the current test passes and refactoring is done.
- Do not move the task file to `tasks/done/` unless every Given/When/Then criterion is covered by a passing test.
- No scope creep. Implement only what the task file specifies.

## Procedure

**Step 1 - Read and confirm interface**
Read `$i` in full. Before writing any code, confirm with the user:
- What new interfaces, functions, or API endpoints are needed
- What existing interfaces change (signature, return type, side effects)

Do not proceed until the user confirms or adjusts the interface description.

**Step 2 - Explore**
If `$c` is given (or can be inferred), explore the codebase to understand:
- Existing test framework and conventions (test file location, naming, runner command)
- Existing code that this task modifies or extends
- Patterns used in similar tests

**Step 3 - Identify behaviors**
Extract every behavior to test from the Given/When/Then criteria in `$i`. List them in order before writing any code. Each Given/When/Then becomes one or more test cases.

**Step 4 - Red-green-refactor loop**
For each behavior (in order):

  a. **RED** - Write one failing test that captures the behavior. Run the test suite and confirm this test fails (and only this test - no regressions introduced). State the failure message.

  b. **GREEN** - Write the minimum code required to make the test pass. No more. Run the test suite and confirm the test passes. State the pass result.

  c. **REFACTOR** - Identify any duplication, naming issues, or structural problems introduced in GREEN. Apply refactoring. Run tests again to confirm still passing. If no refactoring needed, state that explicitly.

  Repeat for next behavior.

**Step 5 - Readiness gate check**
Verify all criteria pass before moving the task file.

**Step 6 - Write execution report and move task**
Write the execution report using `template.md`. Move `$i` from `tasks/todo/` to `tasks/done/`.

## Readiness gate
All must pass before moving the task file:
- Every Given/When/Then criterion in the task file has at least one passing test
- No tests are failing
- No Given/When/Then was skipped or left untested
- Refactor step completed (or explicitly noted as not needed) for every behavior

## Output contract
Two outcomes:
- Tests and implementation written to codebase
- `$i` moved from `tasks/todo/` to `tasks/done/`
- Execution report written alongside task file. See `template.md` for required sections.

## Validation
Before moving the task file, verify each Given/When/Then maps to a named test in the report. Any unmapped criterion is a blocker.
