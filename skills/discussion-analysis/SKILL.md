---
name: discussion-analysis
description: Read a discussion document and produce a structured analysis separating facts from assumptions. No implementation plan yet.
argument-hint: "source_file=<path> target_file=<path>"
disable-model-invocation: true
---

# discussion-analysis

## Purpose
Transform `discussion.md` into `analysis.md` by analyzing the problem space, separating confirmed facts from assumptions, and surfacing risks and dependencies. No implementation plan at this stage.

## Inputs
- `$source_file` - path to discussion.md
- `$target_file` - path where analysis.md should be written

## Hard rules
- No code.
- No implementation plan.
- No task list.
- Do not mix facts and assumptions in the same list.
- Do not hide unresolved questions.
- Preserve all open questions from the source document.

## Procedure

**Step 1 - Read**
Read `$source_file` in full.

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
Write `$target_file` using the structure in `template.md`.
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
