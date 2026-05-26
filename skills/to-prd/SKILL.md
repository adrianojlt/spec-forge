---
name: to-prd
description: Convert grilled notes or a discussion document into a structured Product Requirements Document with user stories and acceptance criteria
argument-hint: "i=<notes-or-discussion.md> o=<prd.md> [c=<codebase>]"
disable-model-invocation: true
---

# to-prd

## Purpose
Transform conversation artifacts (grilled-notes.md, discussion.md, or raw notes) into a structured PRD with user stories and Given/When/Then acceptance criteria.

Sits between exploration (`/grill-me` or `/draft-discussion`) and decomposition (`/to-issues` or `/plan-tasks`).

## Inputs
- `$i` - source notes or discussion document
- `$o` - path to write prd.md
- `$c` - codebase root (optional). When given, verify any repo-specific assertions before writing.

## Hard rules
- No code at this stage.
- No task decomposition - that is `/to-issues`.
- No implementation decisions (framework choices, schema design, etc.).
- Every user story must have at least one Given/When/Then acceptance criterion.
- Scope boundary (in/not-in) must be explicit.
- Do not write output until the readiness gate passes.

## Procedure

**Step 1 - Read**
Read `$i` in full. If `$c` is given, explore the relevant codebase areas to verify any assertions made in the source document.

**Step 2 - Identify stakeholders and roles**
Extract all user roles and stakeholders from the source. Name them explicitly - these become the subjects of user stories.

**Step 3 - Derive user stories**
For each goal in the source, write one or more user stories:
  `As a [role], I want [feature], so that [outcome].`
Group related stories under a module or capability.

**Step 4 - Define acceptance criteria**
For each user story, write at least one Given/When/Then criterion:
  `Given [initial context or state]`
  `When [action is taken]`
  `Then [expected outcome]`

**Step 5 - Identify system modules and scope**
List the major system modules touched or created. State explicitly what is in scope and what is not.

**Step 6 - Draft PRD**
Write `$o` using the structure in `template.md`.

**Step 7 - Readiness gate check**
Verify gate before finalizing. Ask follow-up questions if any item fails.

## Readiness gate
All must pass before writing output:
- Every user story has at least one Given/When/Then criterion
- Scope boundary is explicit (in and not-in sections present)
- No critical ambiguity remains in goals or stakeholders
- System modules are named (even if rough)
- Open questions section is empty or contains only acknowledged deferrals

## Output contract
One artifact:
- `$o` - the PRD document. See `template.md` for required sections.

## Validation
Before writing, check every `template.md` section is present and non-empty. Incomplete sections require more questions.
