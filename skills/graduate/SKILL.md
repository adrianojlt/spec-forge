---
name: graduate
description: Retire a shipped feature's spec folder. Distill the process artifacts into one durable decision record, keep the human-authored draft, and archive the rest.
argument-hint: "o=<feature-dir> p=<prefix>"
disable-model-invocation: true
---

# graduate

## Purpose
A feature's spec folder accumulates process artifacts (spec, task files, feedback). Once the feature is built, merged, and stable, they become stale and misleading: the code is now the source of truth for behavior. `graduate` distills the *decisions* (historical facts, which don't rot) into one `<p>-decision.md`, keeps the human-authored draft, and archives everything else.

Run it when you stop touching the feature, not when the build loop ends. "Tasks verified" is not "feature shipped".

## Inputs
- `$o` - the feature directory (e.g. `features/pin/`)
- `$p` - the artifact prefix (e.g. `pin`)

## Rules
- If the feature does not look shipped (task files still in `tasks/todo/`, spec `Status: Draft`, unresolved open questions), confirm with the user before archiving.
- The seed draft is the human-authored file every `Source:` chain traces back to (typically `*-draft.md` or `*-idea.md`). If ambiguous, ask. It stays in the feature root.
- Never delete. Move everything except the seed draft and the new decision record into `$o/archive/`, preserving subfolders (e.g. `archive/tasks/done/...`). Use `git mv` when tracked; otherwise `mv`, and warn that history is not preserved.
- Record only decisions the draft, spec, task files and feedback actually state: what the feature does, decisions and why, rejected alternatives, gotchas found during implementation. Where a rationale is missing, write "rationale not recorded".
- The decision record is at most one page, date-stamped as a snapshot, and links the draft and archived files by paths relative to its own folder.

## Output
- `$o/<p>-decision.md`, following `template.md`
- `$o/archive/` with the moved artifacts
- The seed draft, unchanged

Report the final folder shape and list what was moved.
