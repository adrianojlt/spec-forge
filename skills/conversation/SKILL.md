---
name: conversation
description: "Q&A-only exploration session. Answer questions about the codebase, explore files, and save the full conversation as structured Markdown artifacts, with optional HTML."
argument-hint: "[o=<path>] [i=<existing-path>] [d=<level>]"
disable-model-invocation: true
---

# conversation

## Purpose
A read-only Q&A session about the codebase or a design problem. On request, save it as a structured summary (for reuse by agents) plus a file with the Q&A rounds, and optionally a standalone HTML page.

## Inputs
- `$o` - output path without extension. Optional at start; ask for it at save time if missing.
- `$i` - existing conversation `.md` to load and continue. If it does not exist, start a new conversation without error, and say how many rounds were loaded when it does.
- `$d` - answer detail level `01`-`05` (`d=1` = `d=01`), default `05`. Named values are invalid. An invalid value warns once (`Unknown detail level 'd=9'. Falling back to 05 normal.`) and never aborts.

## Session rules
- Read-only: read, search, and read-only shell commands. No edits, no file writes, no implementation, no running tests.
- Cite `file:line` when referencing code, at every detail level.

## Detail levels
| d | name | budget |
|---|---|---|
| 01 | minimal | 1-2 sentences, ~40 words, answer plus citations |
| 02 | very concise | ~80 words, plus one supporting fact |
| 03 | concise | ~150 words, plus a short why |
| 04 | balanced | ~350 words, plus reasoning and caveats |
| 05 | normal | unbounded |

- Budgets are targets: if an answer cannot be correct within one, escalate silently for that answer only.
- Change mid-session only on a plain-language request (`now use detail level 3`), acknowledged with one line: `Detail level: 03 concise`. A bare `d=3` or "be more concise" is not a change. It applies from the next round.
- The level applies to answers, procedural messages (wording only, never dropping an option), and saved files. `Files Explored`, `Key findings` and `Open questions` keep every entry at every level; `Overview` scales from 1 paragraph (`01`) to 2-5 (`05`).
- Each round keeps the level it was answered at. Rounds loaded from `$i` are written back verbatim.
- Load precedence: explicit `d=` > `Detail:` line in `$i` > `05`.

## Save
Only when the user says so ("save", "write it", "done"). "save html" or similar also asks for HTML.
1. List every round with a short preview of its question and ask which to keep (`all`, `1,3,4`, `1-3,5`; default all). Renumber kept rounds from 1.
2. Write `<o>.md` (`md-template.md`) and `<o>-qa.md` (`qa-template.md`) from the kept rounds only, including loaded ones. Both carry `Detail:` (the level at save time, e.g. `03 concise`) next to `Status:`, and an `Output:` header relative to the file's own folder, never absolute.
3. With HTML: write `<o>.html` from `html-template.html`, standalone with the summary and the kept rounds. Copy the template's CSS verbatim and use only its classes (`Files Explored` as `.files-table`, `.steps` instead of `.flow` for pipelines over 5 stages, tables for repeated same-shape items). Leave out the pattern-library comment block.
4. Saving again overwrites all files in place. Confirm which files were written, then keep the session open.
