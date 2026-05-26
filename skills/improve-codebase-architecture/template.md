# Architecture Report: [Project or Directory Name]

Date: [date]
Directory: [current directory path]

---

## Summary
[2-4 sentences: overall structural health, main problem patterns found, number of candidates flagged.]

## Candidates

### Candidate 1: [Short name for the problem]

**Pattern:** [scattered concepts | testability extraction | tight coupling | shallow module]

**Current state:**
- Files involved: [file paths]
- Evidence: [line counts, import counts, call graph notes]
- Problem: [what makes this hard to work with]

**Proposed design:**
[Specific: what to merge, rename, encapsulate, or delete. Name the target file/module.]

**Expected benefit:**
[Concrete: "editing X will require touching N fewer files" or "callers no longer need to know about Y"]

**Effort:** [small | medium | large]

---

*(repeat per candidate)*

## Quick Wins
[Candidates with small effort and clear benefit. Act on these first.]

- [Candidate name] - [one line on what to do]

## Deferred
[Candidates that are real problems but high effort or require architectural decisions above code level.]

- [Candidate name] - [one line on why deferred]

## Notes
[Any cross-cutting observations that don't fit a single candidate.]
