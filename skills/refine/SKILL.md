---
name: refine
description: "Unattended backlog refinement. Explore the codebase for each backlog item, write findings, a verdict and open questions (each with options and one recommended) to an item file the user answers later. Also normalizes a backlog into the canonical format."
argument-hint: "i=<backlog.md> [id=<ID,ID|all>] [c=<codebase>] [m=normalize]"
disable-model-invocation: true
---

# refine

## Purpose
Capturing an idea is cheap; exploring it is the expensive part. `refine` does the exploration while the user is away: for each backlog item it reads the code, sizes the change, judges whether it is worth doing, and writes the decisions it cannot make as questions in the item's file. The user answers in the file when they have time; the next run folds the answers in and asks the follow-ups, until the item is ready for `/orchestrate`.

```
backlog line (📋)
  -> refine: findings, verdict, questions          -> ❓ (waiting answers)
  -> user writes Answer: lines in the item file
  -> refine: answers -> Decisions, follow-ups      -> ❓ again, or 🟢 (ready)
  -> /orchestrate i=backlog/items/<ID>-<slug>.md
```

It is `grilling` made asynchronous: same recommended answers, confidence and stop test, but questions are batched because nobody is there to answer one at a time.

## Inputs
- `$i` - the backlog file (e.g. `MoDb/backlog/modb-backlog.md`). Required.
- `$id` - comma-separated item IDs (`MODB-3,MODB-5`) or `all`. Default `all`.
- `$c` - codebase root. Optional, defaults to the current working directory.
- `$m` - `normalize` to rewrite `$i` into the canonical format (see Normalize). Omit to refine.

## Backlog format (canonical)
```markdown
# <Project> Backlog

Prefix: MODB
Legend: 📋 todo | ❓ waiting answers | 🟢 ready | 🚧 in progress | ✅ done | ❌ dropped

## Bugs
- 📋 MODB-6 Search crashes on empty query

## Minor
- ✅ MODB-2 Adaptar layout para android box TV

## Major
- ❓ MODB-3 Search for vidsrc alternatives ([item](items/MODB-3-vidsrc-alternatives.md))
```
- Sections: `Bugs` (something wrong to fix), `Minor` (simple idea), `Major` (complex idea).
- One line per item: `- <status> <PREFIX>-<n> <title>`, optionally followed by ` ([item](items/<ID>-<slug>.md))`.
- IDs are sequential per project and never reused. A new item takes the highest existing number + 1.
- The backlog is an index. Detail lives in `items/<ID>-<slug>.md` next to it (`backlog/items/`), never under the line.
- The status emoji is the only status of the item. Task files track task status; neither mirrors the other.

## Rules
- Read-only on the codebase: read, search, read-only shell commands. No edits, no builds that write, no tests that write.
- Writes only: item files in `items/`, and the status emoji and link of the processed lines in `$i`. Never change an item's title or the user's text in its `## Idea`.
- The run is unattended. Never stop to ask in chat; every question goes to the item file. The only exception is normalize, which needs one confirmation.
- Facts come from the codebase; decisions are the user's. Never ask what `$c` can answer, never answer your own question.
- Status transitions owned by refine: 📋 -> ❓ or 🟢, ❓ -> ❓ or 🟢, and ❓ -> ❌ only when the user answered yes to a drop question. 🚧 and ✅ belong to the user (or to `orchestrate` / `graduate`).
- Paths in item file headers are relative to the item file's own folder, never absolute.

## Procedure (refine)

### 1. Select
Read `$i`. If it does not follow the canonical format (no `Prefix:`, items without IDs), stop and tell the user to run `m=normalize` first.

Eligible items: 📋, and ❓ whose item file has at least one `Answer:` filled since the last round. With `$id`, process only the named items; a named item in another state is reported and skipped.

### 2. Refine each item
More than one item: process each in a fresh subagent when the host supports it, passing the item line, the item file path, `$c` and this skill's path. Run them in parallel, at most 3 at a time; items are independent and each subagent writes only its own item file. The subagent returns the new status; only the main run edits `$i`, after all subagents finish. Without subagent support, process the items one at a time in this context.

For each item:
1. **Read** the line and `items/<ID>-<slug>.md` if it exists. Create the file from `template.md` if missing, with the line's title as `## Idea`.
2. **Fold answers.** Move every answered question, with its answer, to `## Decisions`. `Answer: rec` accepts the recommended option. An answer that delegates without choosing ("whatever", "you decide") is not an answer: re-ask it with two concrete options. Unanswered questions stay open.
3. **Explore** `$c` for what the item touches. Write `## Findings` as facts with `file:line`. For a bug: the path from symptom to cause, and the root cause or ranked hypotheses with the evidence for each.
4. **Size** with the tier table in `orchestrate/SKILL.md` step 0 (trivial, small, standard). Write it to `Tier:` with the signal that set it.
5. **Verdict.** Worth doing, not worth it, or trivial (make the change directly, skip `orchestrate`). One paragraph, with the reason. If not worth it, add a drop question with that as the recommended answer.
6. **Questions.** Write the decisions the item still needs, most decisive first, at most 5 per round. Only questions that are independent of every open question; one whose answer depends on another waits for the next round. Each question has context (why it matters), 2-4 options with exactly one marked `(Recommended: <reason>)`, and an empty `Answer:` line. When options do not fit, ask open and still give a recommended answer.
7. **Stop test.** Ready when there are no open questions and you can predict the user's reaction to the next three questions you would ask. Then write `## Understanding` (Outcome, User, Why now, Success, Constraint, Out of scope; Out of scope is mandatory) from the Idea and Decisions only.
8. **Header.** Update `Status:`, `Round:` (+1), `Confidence:` (0-100%; below 70% add one line naming what is unresolved), `Updated:` (today).

### 3. Update the backlog
For each processed item set the status emoji (🟢 ready, ❓ open questions, ❌ drop confirmed) and add the `([item](items/<ID>-<slug>.md))` link if missing.

### 4. Report
One line per processed item: ID, new status, tier, number of open questions. Then the skipped items and why (waiting answers, not eligible, not found). Next step for 🟢 items: `/orchestrate i=<item file> o=features/<slug>/ p=<prefix>`.

## Normalize (`m=normalize`)
Rewrite `$i` into the canonical format without losing text.
1. **Prefix.** Use `Prefix:` if present; otherwise propose the project folder name, uppercased, letters and digits only (`MoDb` -> `MODB`).
2. **Map.** Map headings at any level to `Bugs`, `Minor`, `Major`; a heading that fits none, or an item that sits under the wrong one, is listed for the user. Give every item an ID in file order, done items included. Items without a status become 📋.
3. **Move detail.** Text under an item (continuation lines, a `### <item>` section, anchor-link lists) moves verbatim to `items/<ID>-<slug>.md` under `## Idea` (header only: `Backlog`, `Kind`, `Status: 📋 Todo`, `Round: 0`, `Updated`), and the line gets its link.
4. **Leftovers.** Every original line must end up in the backlog or an item file. Lines that are none of these (stray legends, notes) are listed; propose where each goes.
5. **Confirm.** Show the new backlog, the item files to create, and the leftovers with their proposed place. Write only after an explicit yes; fold in corrections and show again.

Normalize never refines. Report the files written.

## Output
- `items/<ID>-<slug>.md` per processed item, following `template.md`
- `$i` with updated status emojis and links (normalize: rewritten)
