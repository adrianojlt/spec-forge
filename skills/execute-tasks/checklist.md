# execute-tasks validation checklist

Run before reporting a range complete. Fail any item = report it; do not present the run as successful.

## Preflight checks

- [ ] `$i` exists and a start number parsed from its `-task-NN` suffix
- [ ] `$to` is greater than or equal to the start number
- [ ] `$i` sits in `tasks/todo/` with a sibling `tasks/done/`; `tasks/feedback/` exists or was created
- [ ] Working directory is a git repository
- [ ] Both `git config user.name` and `user.email` are set
- [ ] `git status --porcelain` was empty before the first task
- [ ] Every failed preflight check refused the run without changing the repository

## Subagent isolation checks

- [ ] Every task was delegated to a subagent, not executed inline
- [ ] Every retry attempt used a new subagent, never the one that just failed
- [ ] No subagent ran a git write command
- [ ] `task-review` ran only when `$r` was enabled; `task-verify` only when `$v` was enabled
- [ ] `c=` was forwarded to `task-review` only when `$c` was supplied

## Commit checks

- [ ] Every commit was created by the caller, after re-reading the task file from disk
- [ ] A commit exists only for tasks reading `Status: Done` and sitting in `tasks/done/`
- [ ] Each commit subject is the task title with the bracketed ID stripped
- [ ] No commit carries a `Co-Authored-By` trailer or a generated-with footer
- [ ] Every commit author matches the repository's `git config user.name` and `user.email`
- [ ] No empty commit was forced for a task that staged no changes

## Control flow checks

- [ ] Tasks ran sequentially in ascending order, never in parallel
- [ ] No task file was edited by this skill
- [ ] A missing number was skipped and noted, producing no commit
- [ ] An already-done task was skipped and noted, producing no commit
- [ ] A blocked task halted the entire run at that task
- [ ] On halt, the working tree was left untouched - not stashed, reverted, or committed
- [ ] Remaining tasks after a halt are still in `tasks/todo/`

## Report checks

- [ ] Every number in the range appears in the final report with exactly one outcome
- [ ] Every commit subject created during the run is listed
- [ ] The stop reason is stated: range completed, or halted at a named task
- [ ] Whether uncommitted work remains in the tree is stated
- [ ] A range that executed nothing was reported as a no-op, not as success

## Hard stops

- Do not start the range if any preflight check fails
- Do not commit a task the file does not show as Done in `tasks/done/`
- Do not continue past a blocked task
- Do not report success for a run that executed nothing
- Do not ask the user a question after the range has started
