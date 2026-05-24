---
name: analysis-plan
description: Read analysis.md and produce a sequenced implementation plan. No code, no task explosion.
argument-hint: "source_file=<path> target_file=<path>"
disable-model-invocation: true
---

# analysis-plan

## Purpose
Transform `analysis.md` into `plan.md` by sequencing work logically, making dependencies explicit, and keeping tradeoffs visible. No code. No task list yet.

## Inputs
- `$source_file` - path to analysis.md
- `$target_file` - path where plan.md should be written

## Hard rules
- No code.
- No task explosion (individual tasks are produced by plan-tasks, not here).
- No implementation detail below design level.
- Dependencies must be stated, not implied.
- Tradeoffs must be visible, not hidden.

## Procedure

**Step 1 - Read**
Read `$source_file` in full. Note unresolved open questions before proceeding.

**Step 2 - Identify scope slices**
Break the work into logical slices (phases, layers, or components). Each slice must be:
- Independently completable
- Testable in isolation
- Clearly bounded

**Step 3 - Sequence**
Order slices by dependency. Slices that block others come first. Label dependencies between slices explicitly.

**Step 4 - Assess impact**
For each slice, identify impact on:
- Data model (schema changes, migrations)
- API surface (new endpoints, changed contracts)
- UI (new screens, changed flows)

**Step 5 - Testing strategy**
State at a high level how each slice will be tested. Unit, integration, end-to-end, or manual.

**Step 6 - Write output**
Write `$target_file` using the structure in `template.md`.
Confirm file written. Do not generate tasks. STOP. Inform the user the plan is written and they should invoke `plan-tasks` to decompose it into tasks. Take no further action.

## Readiness gate
- Sequence is explicit and numbered
- Every dependency is named
- No major risk from analysis.md is omitted
- Plan is specific enough to decompose into tasks

## Output contract
See `template.md` for required sections.

## Validation
Verify against `checklist.md` before writing. Block on any failure.
