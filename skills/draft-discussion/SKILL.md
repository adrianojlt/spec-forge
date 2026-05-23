---
name: draft-discussion
description: Turn a rough draft into a structured discussion document through staged clarifying questions. No output until readiness gate passes.
argument-hint: "source_file=<path> target_file=<path>"
disable-model-invocation: true
---

# draft-discussion

## Purpose
Read a draft, ask structured clarifying questions across multiple rounds, then write `discussion.md` once the readiness gate passes.

## Inputs
- `$source_file` - draft file to read
- `$target_file` - where to write the discussion document

## Hard rules
- No code at this stage.
- No architecture decisions unless confirmed by user.
- Do not skip open questions.
- Do not write output until the readiness gate passes.
- First round must contain 8-12 grouped questions.

## Procedure

**Step 1 - Read**
Read `$source_file` in full.

**Step 2 - Clarification round 1**
Ask 8-12 grouped questions covering all of:
1. Problem / context (what is broken or missing, why now)
2. Goals and success criteria (what does success look like, how measured)
3. Non-goals (what is explicitly out of scope)
4. Constraints (time, budget, tech stack, org, legal, existing dependencies)
5. Users and stakeholders (who uses this, who approves it)
6. Known risks and unknowns
7. Existing state (what exists, what is partially done, what is broken)
8. Definition of done (when is this feature considered complete)

**Step 3 - Follow-up rounds**
If major gaps remain after answers, ask targeted follow-up questions. Repeat until readiness gate passes.

**Step 4 - Write output**
Write `$target_file` using the structure in `template.md`.
Confirm file was written. Do not proceed to analysis.

## Readiness gate
All must be satisfied before writing output:
- Problem statement is unambiguous
- Goals are stated and bounded
- At least one success criterion is defined
- Constraints are named
- Scope boundary is explicit (what is NOT in scope)
- No critical open questions remain unacknowledged

## Output contract
See `template.md` for required sections.

## Validation
Before writing, verify against `checklist.md`. Ask more questions if any item fails.
