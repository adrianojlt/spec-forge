# [ID] [Title]

Backlog: [relative path to the backlog, e.g. ../modb-backlog.md] (title and description: `### [ID]` there)
Kind: [Bug | Minor | Major]
Status: [📋 Todo | ❓ Waiting answers | 🟢 Ready | ❌ Dropped]
Round: [n]
Tier: [trivial | small | standard] - [signal that set it]
Route: [one go | /orchestrate] - [signal that set it] [(provisional) while questions are open]
Confidence: ~[n]% [- what is still unresolved, required below 70%]
Updated: [date]

---

## Findings

- [Fact from the codebase, with file:line.]
- [Bug: symptom -> cause path; root cause, or ranked hypotheses with the evidence for each.]

## Verdict

[Worth doing / not worth it / trivial (make the change directly). One paragraph with the reason.]

## Questions

### Q[n]. [One focused question]
Context: [why it matters, what it changes]
- A) [option] (Recommended: [reason])
- B) [option]
- C) [option]

Answer:

## Notes

[Write this section with no content; any text here makes the item eligible. The user's free text: context, corrections, constraints that fit no question. Folded into Decisions on the next run.]

## Decisions

- Q[n] (round [r]): [question] -> [answer, and the option text if a letter or `rec` was given]
- Note (round [r]): [the user's note]

## Understanding

[Only when the stop test passes. Draft until the user answers `yes` to the confirm question.]
- Outcome:      [one line]
- User:         [one line - who benefits]
- Why now:      [one line - what changed]
- Success:      [one line - how we know it worked]
- Constraint:   [one line - the binding limit]
- Out of scope: [one line - what we are explicitly not doing]
