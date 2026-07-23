---
name: conversation
description: "Q&A-only exploration session. Answer questions about the codebase, explore files, and save the full conversation as structured Markdown artifacts, with optional HTML."
argument-hint: "[o=<path>] [i=<existing-path>]"
disable-model-invocation: true
---

# conversation

## Purpose
Hold a read-only Q&A session about the codebase or a design problem. No implementation during the session. On explicit user request, save the conversation as two Markdown files: a structured summary (for AI agent reuse) and a separate Q&A file with all rounds. An HTML version, self-contained and including the Q&A rounds, is written only when the user asks for it.

## Inputs
- `$o` - output path without extension (optional at start, required on save). May be provided at invocation time or when the user says "save". The skill writes `<o>.md` and `<o>-qa.md` on save, plus `<o>.html` when HTML is requested.
- `$i` - path to an existing conversation file to load and continue (optional). Provide the `.md` path. If the file does not exist, the skill treats this as a new conversation and does not error.

## Hard rules
- Do not write, edit, or delete any project files during the session.
- Do not implement code, suggest implementations, or run tests.
- Do not save output until the user explicitly says "save" (or equivalent: "write it", "save this", "done").
- Read-only tools permitted during session: Read, Grep, Glob, Bash (read-only commands only, e.g. `ls`, `find`, `cat`). No Edit, Write, or shell commands that modify files.
- On save: write `<o>.md` and `<o>-qa.md`. Write `<o>.html` only if the user asked for HTML. Confirm which files were written.
- Write the `Output:` header as a path relative to the output file's own folder (usually just `./<basename>` without extension), never absolute - keeps links valid if the specs folder is moved.
- If user saves multiple times in one session: overwrite in place. Do not append again.

## Procedure

### Step 1 - Load or start
If `$i` is provided and the file exists: read `<i>` in full. Inform the user how many prior rounds are loaded. Proceed in continuation mode.

If `$i` is not provided, or the file does not exist: start a new conversation. Inform the user: "New conversation started. Ask anything."

### Step 2 - Q&A loop
Answer the user's questions. For each question:
- Read any project files needed to give an accurate answer.
- Cite specific files and line numbers when referencing code.
- Stay in Q&A mode. Do not propose implementations or write any files.
- Keep answers focused and precise.

Continue until the user says to save or stop.

### Step 3 - Save
When the user says "save" (or equivalent):

1. If `$o` was not provided at invocation time, ask: "Where should I save the conversation?" Use the provided response as the output path.
2. Detect whether HTML was requested: if the user said "save html" (or equivalent: "save with html", "also html", "save html too"), enable HTML output. Otherwise, write Markdown only.
3. Compile the full conversation: prior rounds (if continuation) plus all new rounds from this session.
4. Write `<o>.md` following `md-template.md`, and `<o>-qa.md` following `qa-template.md`. If updating existing files, overwrite them with the full updated content.
5. If HTML was requested: write `<o>.html` following `html-template.html`. The HTML is standalone - it carries the summary sections **and** every Q&A round, so it never depends on the Markdown files. Overwrite if it exists.
6. Confirm written files:
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
