# plan-tasks validation checklist

Run before writing output. Fail any item = split or revise the task.

## INVEST checks (per task)

- [ ] Independent: task does not require another in-progress task to complete
- [ ] Negotiable: task has bounded scope, not a vague directive
- [ ] Valuable: completing the task alone delivers something testable or usable
- [ ] Estimable: scope is clear enough to estimate (not "investigate and fix")
- [ ] Small: task fits one focused session (not a multi-day sprint)
- [ ] Testable: acceptance criteria can be verified without subjective judgment

## Acceptance criteria checks (per task)

- [ ] Minimum 2 Given/When/Then criteria per task
- [ ] "Given" states a concrete precondition, not a vague context
- [ ] "When" states a specific action or event
- [ ] "Then" states a verifiable outcome (not "it works well")
- [ ] Criteria cover both happy path and at least one failure path

## Structure checks

- [ ] Each task is written to its own file
- [ ] File names follow `<prefix>-task-<NN>.md` pattern (zero-padded)
- [ ] Files are written in dependency order (task-01 before task-02, etc.)
- [ ] Each task has a unique ID matching its file name
- [ ] Depends-on references valid task file names
- [ ] Done definition is specific and not "it works"

## Hard stops

- Reject tasks titled "Implement [feature]" with no scope breakdown
- Reject tasks with "TBD" in scope, criteria, or done definition
- Reject tasks that combine implementation + documentation + testing into one item
- Reject tasks with only happy-path acceptance criteria
