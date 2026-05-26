# task-execute validation checklist

Run before moving the file to `tasks/done/`. Fail any item = do not move; report the failure.

## Dependency checks

- [ ] Every ID in `Depends on:` has its file in `tasks/done/`
- [ ] No named dependency is still in `tasks/todo/`

## Scope checks

- [ ] All edits trace to this task's `Scope notes: In`
- [ ] Nothing in `Scope notes: Not in` was touched
- [ ] No unrelated refactor, reformat, or cleanup was introduced
- [ ] Existing code style was matched

## Acceptance checks

- [ ] Every Given/When/Then criterion verified and passes
- [ ] Each pass is backed by evidence (test, command output, observed behavior), not assertion
- [ ] At least one failure-path criterion was checked, not only happy path
- [ ] The Done condition is met

## Hard stops

- Do not move the file if any criterion fails
- Do not move the file if a dependency is unmet
- Do not mark Status: Done unless the file is being moved
- Do not edit outside the task's declared scope to force a criterion to pass
