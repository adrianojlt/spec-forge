# draft-discussion validation checklist

Run before writing output. Fail any item = ask more questions first.

## Content checks

- [ ] Problem statement is one specific problem, not a category of problems
- [ ] Goals are outcomes, not activities ("users can X" not "we will build X")
- [ ] At least one success criterion is measurable
- [ ] Non-goals list at least one explicit exclusion
- [ ] Constraints are concrete (not "must be fast", but "p99 < 200ms")
- [ ] Users are identified (not just "end users")
- [ ] All major open questions are listed, even if unanswered
- [ ] Assumptions are separated from confirmed facts
- [ ] Risks are named, not omitted

## Gate checks

- [ ] No section is empty or contains only "TBD"
- [ ] Scope boundary is explicit
- [ ] No contradiction between goals and constraints
- [ ] Readiness status reflects actual state

## Hard stops

- Output blocked if: Goals are vague or aspirational only
- Output blocked if: Success criteria are missing entirely
- Output blocked if: Constraints are unstated
- Output blocked if: "TBD" appears in Goals, Constraints, or Users sections
