---
name: discussion-analysis
description: Read a discussion document and produce a structured analysis separating facts from assumptions. No implementation plan yet.
argument-hint: "i=<path> o=<path> [c=<path>]"
disable-model-invocation: true
---

# discussion-analysis

## Purpose
Transform `discussion.md` into `analysis.md` by analyzing the problem space, separating confirmed facts from assumptions, and surfacing risks and dependencies. No implementation plan at this stage.

## Inputs
- `$i` - path to discussion.md
- `$o` - path where analysis.md should be written
- `$c` - optional path to the existing codebase root. If set, ground the analysis in real code (brownfield). If unset, behavior is unchanged (greenfield).

## Hard rules
- No code.
- No implementation plan.
- No task list.
- Do not mix facts and assumptions in the same list.
- Do not hide unresolved questions.
- Preserve all open questions from the source document.

## Procedure

**Step 1 - Read**
Read `$i` in full. If `overview/principles.md` exists, read it and treat its rules as binding constraints.

**Step 1b - Ground in code (only if `$c` set)**
Dispatch an Explore subagent over `$c` to map the existing code relevant to this work: files and modules touched, current behavior, and constraints already in place. Use the findings to inform Confirmed Facts and Dependencies (existing behavior is fact, not assumption). Record them in the `Codebase Findings` section of the output. Skip this step entirely if `$c` is unset.

**Step 2 - Separate**
Identify and categorize:
- Confirmed facts (stated explicitly in discussion, agreed by stakeholders)
- Assumptions (inferred, not confirmed, or stated as assumption)
- Open questions (unresolved from discussion)

**Step 3 - Analyze**
For each goal:
- Identify dependencies (what must exist or be true for this goal to be achievable)
- Identify risks (what could block or degrade this goal)
- Identify edge cases (boundary conditions, exceptional inputs, failure modes)

**Step 4 - Write output**
Write `$o` using the structure in `template.md`.
Confirm file written. Do not proceed to planning.

## Readiness gate
- Facts and assumptions are in separate sections
- No confirmed fact is labeled as assumption or vice versa
- All open questions from source are preserved
- Dependencies are named specifically (not just "depends on backend")
- Risks are named specifically

## Output contract
See `template.md` for required sections.

## Validation
Verify against `checklist.md` before writing. Block on any failure.
