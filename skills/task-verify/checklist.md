# task-verify validation checklist

Run before reporting. This skill is read-only.

## Coverage checks

- [ ] Every Given/When/Then criterion was checked, none skipped
- [ ] The Done condition was assessed
- [ ] Both happy-path and failure-path criteria were exercised

## Evidence checks

- [ ] Each pass cites concrete evidence (test, command output, observed behavior)
- [ ] Each fail states what was observed instead of the expected Then
- [ ] No verdict rests on assertion alone

## Read-only checks

- [ ] No source file was edited
- [ ] The task file was not moved
- [ ] The task `Status:` was not changed

## Hard stops

- Do not implement missing work to make a criterion pass (that is task-execute)
- Do not report "all pass" if any criterion lacks evidence
