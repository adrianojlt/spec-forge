---
name: draft-discussion
description: Turn a rough draft into a structured discussion document through staged clarifying questions. No output until readiness gate passes.
argument-hint: "i=<path> o=<path> [n=<min>-<max>]"
disable-model-invocation: true
---

# draft-discussion

## Purpose
Read a draft, ask structured clarifying questions across multiple rounds, then write `discussion.md` once the readiness gate passes.

## Inputs
- `$i` - draft file to read
- `$o` - where to write the discussion document
- Q&A transcript path - derived from `$o`, no separate argument: same directory, filename `<o-basename-without-ext>-qa.md` (e.g. `discussion.md` -> `discussion-qa.md`).

## Hard rules
- No code at this stage.
- No architecture decisions unless confirmed by user.
- Do not skip open questions.
- Do not write output until the readiness gate passes.
- First round must contain $n grouped questions. $n defaults to 8-12; override with n=<min>-<max> argument (e.g. n=3-5).
- Never discard the raw Q&A. Persist it to the transcript file after every round, before asking the next round.

## Procedure

**Step 1 - Read**
Read `$i` in full.

**Step 2 - Clarification round 1**
Ask $n grouped questions covering all of:
1. Problem / context (what is broken or missing, why now)
2. Goals and success criteria (what does success look like, how measured)
3. Non-goals (what is explicitly out of scope)
4. Constraints (time, budget, tech stack, org, legal, existing dependencies)
5. Users and stakeholders (who uses this, who approves it)
6. Known risks and unknowns
7. Existing state (what exists, what is partially done, what is broken)
8. Definition of done (when is this feature considered complete)

After the user answers, immediately record this round to the Q&A transcript: create it using `qa-template.md` and write Round 1 with the grouped questions and the user's verbatim answers. Do this before asking any follow-up round.

**Step 3 - Follow-up rounds**
If major gaps remain after answers, ask targeted follow-up questions. Repeat until readiness gate passes. After each round's answers, append that round (questions + verbatim answers) to the Q&A transcript before continuing.

**Step 4 - Write output**
Write `$o` using the structure in `template.md`. Set the Q&A transcript Status to `Complete`.
Confirm both files were written (`$o` and the Q&A transcript). Do not proceed to analysis.

## Readiness gate
All must be satisfied before writing output:
- Problem statement is unambiguous
- Goals are stated and bounded
- At least one success criterion is defined
- Constraints are named
- Scope boundary is explicit (what is NOT in scope)
- No critical open questions remain unacknowledged

## Output contract
Two artifacts:
- `$o` - the discussion document. See `template.md` for required sections.
- The Q&A transcript (`<o-basename>-qa.md`). See `qa-template.md`.

## Validation
Before writing, verify against `checklist.md`. Ask more questions if any item fails.
