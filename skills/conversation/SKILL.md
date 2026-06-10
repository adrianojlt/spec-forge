---
name: conversation
description: "Q&A-only exploration session. Answer questions about the codebase, explore files, and save the full conversation as a structured Markdown and HTML artifact."
argument-hint: "o=<path> [i=<existing-path>]"
disable-model-invocation: true
---

# conversation

## Purpose
Hold a read-only Q&A session about the codebase or a design problem. No implementation during the session. On explicit user request, save the full conversation as two files: a structured Markdown file (for AI agent reuse) and an HTML file (for human reading).

## Inputs
- `$o` - output path without extension (required). The skill writes `<o>.md` and `<o>.html` on save.
- `$i` - path to an existing conversation file to load and continue (optional). Provide the `.md` path. If the file does not exist, the skill treats this as a new conversation and does not error.

## Hard rules
- Do not write, edit, or delete any project files during the session.
- Do not implement code, suggest implementations, or run tests.
- Do not save output until the user explicitly says "save" (or equivalent: "write it", "save this", "done").
- Read-only tools permitted during session: Read, Grep, Glob, Bash (read-only commands only, e.g. `ls`, `find`, `cat`). No Edit, Write, or shell commands that modify files.
- On save: write both `<o>.md` and `<o>.html`. Confirm both files were written.
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

1. Compile the full conversation: prior rounds (if continuation) plus all new rounds from this session.
2. Write `<o>.md` following `md-template.md`. If updating an existing file, overwrite it with the full updated content.
3. Write `<o>.html` following `html-template.html`. If updating an existing file, overwrite it.
4. Confirm: "Saved: `<o>.md` and `<o>.html`."

Do not end the session after saving. The user may continue asking questions and save again.

## Output contract
Two files written on save:
- `<o>.md` - structured Markdown. See `md-template.md`.
- `<o>.html` - styled HTML with inline CSS. See `html-template.html`.

Both files are complete and self-contained. Each save overwrites both files entirely.
