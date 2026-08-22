---
name: conversation
description: "Q&A-only exploration session. Answer questions about the codebase, explore files, and save the full conversation as structured Markdown artifacts, with optional HTML."
argument-hint: "[o=<path>] [i=<existing-path>] [d=<level>]"
disable-model-invocation: true
---

# conversation

## Purpose
Hold a read-only Q&A session about the codebase or a design problem. No implementation during the session. On explicit user request, save the conversation as two Markdown files: a structured summary (for AI agent reuse) and a separate Q&A file with all rounds. An HTML version, self-contained and including the Q&A rounds, is written only when the user asks for it.

## Inputs
- `$o` - output path without extension (optional at start, required on save). May be provided at invocation time or when the user says "save". The skill writes `<o>.md` and `<o>-qa.md` on save, plus `<o>.html` when HTML is requested.
- `$i` - path to an existing conversation file to load and continue (optional). Provide the `.md` path. If the file does not exist, the skill treats this as a new conversation and does not error.
- `$d` - detail level for answers (optional). Numeric, padded or unpadded: `d=1` and `d=01` mean the same thing. Valid values are `01` to `05`. Named values such as `d=minimal` are invalid. Defaults to `05 normal`, which is the current behavior. See `## Detail levels`.

## Hard rules
- Do not write, edit, or delete any project files during the session.
- Do not implement code, suggest implementations, or run tests.
- Do not save output until the user explicitly says "save" (or equivalent: "write it", "save this", "done").
- Read-only tools permitted during session: Read, Grep, Glob, Bash (read-only commands only, e.g. `ls`, `find`, `cat`). No Edit, Write, or shell commands that modify files.
- On save: first ask which Q&A rounds to save, then write `<o>.md` and `<o>-qa.md`. Write `<o>.html` only if the user asked for HTML. Confirm which files were written.
- Save only the rounds the user selected. Renumber the kept rounds sequentially (Round 1, Round 2, ...) in the written files.
- Write the `Output:` header as a path relative to the output file's own folder (usually just `./<basename>` without extension), never absolute - keeps links valid if the specs folder is moved.
- If user saves multiple times in one session: overwrite in place. Do not append again.

## Detail levels
`$d` controls how verbose answers are. It only compresses output; there is no level above the default.

| d | name | length budget | content structure |
|---|---|---|---|
| 01 | minimal | 1-2 sentences, ~40 words | Direct answer plus citations. No reasoning, no caveats, no lists. |
| 02 | very concise | ~80 words | Answer plus citations plus one supporting fact. Bullets allowed, no headings. |
| 03 | concise | ~150 words | Answer plus citations plus a short why. |
| 04 | balanced | ~350 words | Answer plus citations plus reasoning plus relevant caveats. |
| 05 | normal | unbounded | Current behavior, unchanged. |

- Word counts are targets, not hard cuts. If an answer cannot be correct within its budget, escalate one level at a time until it fits. Escalation is silent, applies to that answer only, and does not change the session level.
- `d=05` is identical to giving no `d=` at all.
- Invalid value: warn once, then continue at `05 normal`. Never abort the session. Message form: `Unknown detail level 'd=9'. Falling back to 05 normal.`
- The level applies to live answers, `<o>.md`, `<o>-qa.md`, `<o>.html`, and the skill's own procedural messages.
- Procedural messages are compressed in wording only. Never drop an option or any information the user needs to answer a prompt. The save-time round-selection list keeps every round and every choice at every level.
- file:line citations are mandatory at every level, including `01 minimal`. The level never overrides that hard rule.
- `Files Explored`, `Key findings` and `Open questions` stay complete at every level. They are indexes, not prose: shorten the wording, never drop entries.
- `Overview` length scales with the level: `01` -> 1 paragraph, `02` -> 1, `03` -> 1-2, `04` -> 2-3, `05` -> 2-5.

### Level tracking
- The level is tracked per round. Each round is rendered at the level active when its question was asked, so a saved file may legitimately contain mixed-level rounds.
- Mid-session change: only the plain-language form is recognized, e.g. `now use detail level 3`. Acknowledge it with one line: `Detail level: 03 concise`.
- A bare `d=3` typed mid-session is not a level change; argument syntax belongs to invocation only. Vague requests such as "be more concise" are not level changes either.
- A change affects only rounds asked after it. Earlier rounds keep the level they were answered at.
- Rounds loaded from `<i>` are written back verbatim. The current session's level never re-renders them.

### Persistence and precedence
- Saved files carry a `Detail:` line in the header block, next to `Status:`, with the value format `03 concise`. All three files carry it: `<o>.md`, `<o>-qa.md`, `<o>.html`.
- The persisted value is the level active at save time. It is the resume level, not a description of every round in the file.
- Precedence on load: explicit `d=` at invocation > `Detail:` in the loaded `<i>` file > `05 normal`.
- An existing file without a `Detail:` line loads at `05 normal`.

## Procedure

### Step 1 - Load or start
If `$i` is provided and the file exists: read `<i>` in full. Inform the user how many prior rounds are loaded. Proceed in continuation mode.

If `$i` is not provided, or the file does not exist: start a new conversation. Inform the user: "New conversation started. Ask anything."

Resolve the detail level for the session, in this order: explicit `d=` at invocation, then the `Detail:` line of the loaded `<i>` file, then `05 normal`. If `d=` was given but is not one of `01`-`05`, print the fallback warning once and use `05 normal`.

### Step 2 - Q&A loop
Answer the user's questions. For each question:
- Read any project files needed to give an accurate answer.
- Cite specific files and line numbers when referencing code.
- Stay in Q&A mode. Do not propose implementations or write any files.
- Keep answers focused and precise.
- Render the answer at the active detail level, and record which level that round was answered at.
- If the user asks for a different level in plain language, switch, acknowledge with one line, and apply the new level from the next round on.

Continue until the user says to save or stop.

### Step 3 - Save
When the user says "save" (or equivalent):

1. If `$o` was not provided at invocation time, ask: "Where should I save the conversation?" Use the provided response as the output path.
2. Detect whether HTML was requested: if the user said "save html" (or equivalent: "save with html", "also html", "save html too"), enable HTML output. Otherwise, write Markdown only.
3. Ask which Q&A rounds to save. List every round numbered, each with its verbatim question (truncate long questions to a short preview). Ask the user to pick the rounds to keep (e.g. "all", "1,3,4", "1-3,5"). Default is all rounds if the user replies "all" or gives no selection. Only the selected rounds are written to `<o>-qa.md` and to the HTML Q&A section; the summary in `<o>.md` is derived only from the selected rounds.
4. Compile the full conversation: prior rounds (if continuation) plus all new rounds from this session, keeping only the rounds the user selected.
5. Write `<o>.md` following `md-template.md`, and `<o>-qa.md` following `qa-template.md`. If updating existing files, overwrite them with the full updated content. Re-render each round's answer at the level that round was answered at; write rounds loaded from `<i>` back verbatim. Set the `Detail:` header of both files to the level active at save time.
6. If HTML was requested: write `<o>.html` following `html-template.html`. The HTML is standalone - it carries the summary sections **and** the selected Q&A rounds, so it never depends on the Markdown files. It carries the same `Detail:` value and the same content as the Markdown files. Overwrite if it exists.
7. Confirm written files:
   - Markdown only: "Saved: `<o>.md` and `<o>-qa.md`."
   - With HTML: "Saved: `<o>.md`, `<o>-qa.md`, and `<o>.html`."

Do not end the session after saving. The user may continue asking questions and save again.

## Output contract
Default - two files written on save:
- `<o>.md` - structured Markdown summary (overview, files explored, key findings, open questions). See `md-template.md`.
- `<o>-qa.md` - Q&A rounds in Markdown. See `qa-template.md`.

When HTML is requested - one extra file:
- `<o>.html` - styled HTML with inline CSS, containing the summary sections and all Q&A rounds. See `html-template.html`.

All files are complete and self-contained. Each save overwrites existing files entirely.
