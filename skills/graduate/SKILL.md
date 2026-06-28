---
name: graduate
description: Retire a shipped feature's spec folder. Distill the process artifacts into one durable decision record, keep the human-authored draft, and archive the rest.
argument-hint: "o=<feature-dir> p=<prefix>"
disable-model-invocation: true
---

# graduate

## Purpose
A feature's spec folder accumulates ephemeral process artifacts (discussion, Q&A, analysis, plan, task files, feedback). Once the feature is built, merged, and stable, these become stale and misleading - the code is now the source of truth for behavior. `graduate` retires the folder: it distills the *decisions* (which don't rot, because they are historical facts) into one durable `<p>-decision.md`, keeps the human-authored draft (the seed), and archives everything else.

Run this when you stop touching the feature - not when the build loop ends. "Tasks verified" is not "feature shipped".

## Inputs
- `$o` - the feature directory (e.g. `features/pin/`)
- `$p` - the artifact prefix (e.g. `pin`)

## Hard rules
- Keep the human-authored draft and the new `<p>-decision.md` in the feature root. Archive everything else.
- Never delete. Move files to `archive/` only.
- Use `git mv` when the folder is tracked by git; otherwise use plain `mv` and warn the user that history is not preserved.
- The decision record references files by path relative to its own folder (e.g. `./pin-draft.md`, `./archive/pin-plan.md`), never absolute.
- The decision record is at most one page. Summarize; do not duplicate archived content.
- Do not invent decisions or rationale. Record only what the draft, plan, and task files actually state. Where a rationale is not recorded, write "rationale not recorded" rather than guessing.
- If the feature does not look shipped (tasks still in `tasks/todo/`, plan `Status: Draft`, unresolved open questions), stop and confirm with the user before archiving.

## Procedure

**Step 1 - Confirm it is ready to graduate**
Check the folder state. If any task files remain in `tasks/todo/`, or the plan is still `Status: Draft`, or open questions are unresolved, the feature may not be shipped. Report this and ask the user to confirm before continuing.

**Step 2 - Identify the seed draft**
Find the human-authored draft (the file every generated artifact's `Source:` chain traces back to, typically `*-draft.md` or `*-idea.md`). If ambiguous, ask the user which file is the original draft. This file is kept, never archived.

**Step 3 - Extract decisions**
Read the draft, the plan (`<p>-plan.md`), and the completed task files in `tasks/done/`. Pull out:
- What the feature does (behavior, 2-3 lines)
- Key decisions made and why (chose X over Y because ...)
- Alternatives that were considered and rejected, and why
- Constraints or gotchas discovered during implementation

Take rejected alternatives and tradeoffs from the analysis/plan; take gotchas from task files and feedback. Do not invent.

**Step 4 - Write the decision record**
Write `$o/<p>-decision.md` using the structure in `template.md`. Date-stamp it. Make clear it is a snapshot as of that date, not a live spec of current behavior. Link the kept draft and the archived files by relative path.

**Step 5 - Archive the scaffolding**
Create `$o/archive/`. Move every artifact except the seed draft and the new decision record into it (discussion, Q&A, analysis, plan, `tasks/`, `feedback/`). Preserve subfolder structure under `archive/` (e.g. `archive/tasks/done/...`). Use `git mv` if tracked, else `mv` with a warning.

**Step 6 - Confirm**
Report the final folder shape: seed draft + `<p>-decision.md` + `archive/`. List what was moved.

## Readiness gate
- The decision record exists and is at most one page.
- The seed draft and the decision record remain in the feature root.
- Everything else is under `archive/`; nothing was deleted.
- All paths in the decision record are relative and resolve correctly.
- No decision or rationale was invented; gaps are marked "rationale not recorded".

## Output contract
- `$o/<p>-decision.md` - the durable record (see `template.md`)
- `$o/archive/` - the moved process artifacts
- `$o/<seed-draft>.md` - unchanged, kept in place

## Validation
Verify against `checklist.md` before reporting completion.
