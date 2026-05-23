# discussion-analysis validation checklist

Run before writing output. Fail any item = revise before writing.

## Separation checks

- [ ] Confirmed facts contain only items explicitly stated or confirmed in discussion
- [ ] Assumptions section contains no confirmed facts
- [ ] No item appears in both facts and assumptions
- [ ] Assumptions are individually labeled, not buried in prose

## Completeness checks

- [ ] All goals from discussion.md are preserved
- [ ] All constraints from discussion.md are preserved
- [ ] All open questions from discussion.md are listed
- [ ] New questions surfaced during analysis are added to open questions

## Quality checks

- [ ] Risks are specific ("JWT expiry not checked on refresh" not "security risk")
- [ ] Dependencies name what they depend on (not "depends on backend being ready")
- [ ] Edge cases cover: empty inputs, max inputs, concurrent access, failure paths
- [ ] Readiness assessment is honest, not optimistic

## Hard stops

- Output blocked if: facts and assumptions are mixed in same list
- Output blocked if: an open question from source is omitted
- Output blocked if: a risk is acknowledged but not named
- Output blocked if: dependencies say "TBD"
