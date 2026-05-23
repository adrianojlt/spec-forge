# analysis-plan validation checklist

Run before writing output. Fail any item = revise before writing.

## Structure checks

- [ ] Sequence is explicit and numbered
- [ ] Each slice has a clear deliverable
- [ ] Each slice states its dependencies (or "none")
- [ ] All slices are covered in the sequence section

## Completeness checks

- [ ] Every risk from analysis.md is addressed or acknowledged
- [ ] All open questions from analysis.md are carried forward or resolved
- [ ] Data model impact is stated (even if "none")
- [ ] API impact is stated (even if "none")
- [ ] UI impact is stated (even if "none")
- [ ] Testing strategy covers all slices

## Quality checks

- [ ] Approach summary explains why this approach, not just what
- [ ] Dependencies are named specifically, not vaguely
- [ ] Rollout gates are checkable (not "when it's ready")
- [ ] Plan is specific enough to decompose into individual tasks

## Hard stops

- Output blocked if: sequence is missing or has no ordering rationale
- Output blocked if: a major risk from analysis is omitted
- Output blocked if: plan is too vague to decompose ("implement auth system" with no slices)
- Output blocked if: dependencies between slices are not explicit
