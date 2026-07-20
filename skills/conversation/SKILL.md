---
name: conversation
description: "Q&A-only exploration session. Answer questions about the codebase, explore files, and save the full conversation as structured Markdown and HTML artifacts."
argument-hint: "[o=<path>] [i=<existing-path>]"
disable-model-invocation: true
---

# conversation

## Purpose
Hold a read-only Q&A session about the codebase or a design problem. No implementation during the session. On explicit user request, save the conversation as three files: a structured Markdown summary (for AI agent reuse), an HTML summary (for human reading), and a separate Q&A Markdown file with all rounds.

## Inputs
- `$o` - output path without extension (optional at start, required on save). May be provided at invocation time or when the user says "save". The skill writes `<o>.md`, `<o>.html`, and `<o>-qa.md` on save.
- `$i` - path to an existing conversation file to load and continue (optional). Provide the `.md` path. If the file does not exist, the skill treats this as a new conversation and does not error.

## Hard rules
- Do not write, edit, or delete any project files during the session.
- Do not implement code, suggest implementations, or run tests.
- Do not save output until the user explicitly says "save" (or equivalent: "write it", "save this", "done").
- Read-only tools permitted during session: Read, Grep, Glob, Bash (read-only commands only, e.g. `ls`, `find`, `cat`). No Edit, Write, or shell commands that modify files.
- On save: write files per save mode (full: all three; markdown-only: `.md` only). Confirm which files were written.
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
2. Detect save mode: if the user said "save markdown only" (or equivalent: "save md only", "only markdown", "just the markdown"), set mode to **markdown-only**. Otherwise, use **full** mode.
3. Compile the full conversation: prior rounds (if continuation) plus all new rounds from this session.
4. Write `<o>.md` following `md-template.md`. If updating an existing file, overwrite it with the full updated content.
5. If mode is **full**: write `<o>.html` following `html-template.html`, and write `<o>-qa.md` following `qa-template.md`. Overwrite if they exist.
6. Confirm written files:
   - Full mode: "Saved: `<o>.md`, `<o>.html`, and `<o>-qa.md`."
   - Markdown-only mode: "Saved: `<o>.md`."

Do not end the session after saving. The user may continue asking questions and save again.

## Output contract
Default (full mode) - three files written on save:
- `<o>.md` - structured Markdown summary (overview, files explored, key findings, open questions). See `md-template.md`.
- `<o>.html` - styled HTML summary with inline CSS. See `html-template.html`.
- `<o>-qa.md` - Q&A rounds in Markdown. See `qa-template.md`.

Markdown-only mode - one file written on save:
- `<o>.md` - same structured Markdown summary as above.

All files are complete and self-contained. Each save overwrites existing files entirely.
