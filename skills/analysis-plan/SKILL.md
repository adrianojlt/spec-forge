---
name: analysis-plan
description: Read analysis.md and produce a sequenced implementation plan. No code, no task explosion.
argument-hint: "i=<path> o=<path> [c=<path>]"
disable-model-invocation: true
---

# analysis-plan

## Purpose
Transform `analysis.md` into `plan.md` by sequencing work logically, making dependencies explicit, and keeping tradeoffs visible. No code. No task list yet.

## Inputs
- `$i` - path to analysis.md
- `$o` - path where plan.md should be written
- `$c` - optional path to the existing codebase root. If set, ground Data/API/UI impact in real code paths instead of hypotheticals.

## Hard rules
- Write the `Source:` header as a path relative to the output file's own folder (e.g. `./auth-analysis.md`), never absolute - keeps links valid if the specs folder is moved.
- No code.
- No task explosion (individual tasks are produced by plan-tasks, not here).
- No implementation detail below design level.
- Dependencies must be stated, not implied.
- Tradeoffs must be visible, not hidden.
- Do not advance to task decomposition. Require explicit user approval of the plan first.

## Procedure

**Step 1 - Read**
Read `$i` in full. Note unresolved open questions before proceeding. If `overview/principles.md` exists, read it and treat its rules as binding constraints. If `$c` is set, consult the existing code when assessing impact so Data/API/UI sections name real paths.

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
Write `$o` using the structure in `template.md`. Confirm file written. Do not generate tasks.

**Step 7 - Review gate (STOP for approval)**
Do not advance to task decomposition. Present a short review summary in chat:
- The numbered slice sequence
- Key tradeoffs
- Top risks
- Any unresolved open questions

Then ask the user to choose one of:
1. Approve the plan as-is
2. Request edits (apply them to `$o`, then re-present this summary)
3. Edit `$o` themselves and tell you when done

Only after the user explicitly approves, set the plan's `Status:` to `Approved`, then tell them to invoke `plan-tasks` to decompose the plan. Take no further action until then.

## Review gate (human approval)
This is the one human checkpoint in the pipeline that gates real design decisions (slicing, sequencing, tradeoffs). A wrong `plan.md` is cheap to fix here; a wrong set of task files is expensive to fix later. Never auto-advance to `plan-tasks`. Wait for explicit approval.

## Readiness gate
- Sequence is explicit and numbered
- Every dependency is named
- No major risk from analysis.md is omitted
- Plan is specific enough to decompose into tasks

## Output contract
See `template.md` for required sections.

## Validation
Verify against `checklist.md` before writing. Block on any failure.
