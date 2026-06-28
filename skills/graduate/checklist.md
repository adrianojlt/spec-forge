# graduate validation checklist

Run before reporting completion. Fail any item = revise.

## Preservation checks

- [ ] The human-authored seed draft is still in the feature root (not archived, not deleted)
- [ ] Nothing was deleted - every moved file exists under `archive/`
- [ ] `git mv` was used if the folder is tracked; if plain `mv` was used, the user was warned history is not preserved

## Decision record checks

- [ ] `<p>-decision.md` exists in the feature root
- [ ] It is at most one page
- [ ] It is date-stamped and labelled as a snapshot, not a live spec
- [ ] No decision or rationale was invented; gaps are marked "rationale not recorded"
- [ ] It does not duplicate large blocks of archived content - it summarizes and links

## Path checks

- [ ] All paths in the decision record are relative (e.g. `./pin-draft.md`), never absolute
- [ ] The seed-draft link and archive links resolve correctly

## Hard stops

- Output blocked if: the feature is not shipped (tasks in `tasks/todo/`, plan `Status: Draft`) and the user did not confirm
- Output blocked if: any file would be deleted rather than archived
- Output blocked if: the decision record contains an absolute path
