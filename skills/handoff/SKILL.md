---
name: handoff
description: Produce a resumable session handoff document for a future Claude Code session. References existing artifacts by path, does not duplicate content.
argument-hint: "o=<path> n=<description>"
disable-model-invocation: true
---

# handoff

## Purpose
Write a concise, resumable handoff document that allows a future Claude Code session to pick up exactly where this session ended. References existing artifact files by path rather than duplicating their content.

## Inputs
- `$o` - path where the handoff document should be written (e.g. `sessions/2026-05-23-auth.md`)
- `$n` - one sentence describing the focus of the next session

## Hard rules
- Do not copy large sections from existing artifacts. Reference by path only.
- Redact sensitive data (tokens, secrets, passwords, credentials).
- Tailor the handoff to `$n`.
- Keep the document under 500 words.

## Procedure

**Step 1 - Capture current state**
Identify what was accomplished in this session:
- Which skills were run
- Which files were written or modified
- What decisions were made
- What was deferred

**Step 2 - List open questions**
List questions that are unresolved and relevant to the next session.

**Step 3 - Identify next action**
State the single most important next action for the next session, aligned with `$n`.

**Step 4 - List relevant files**
List all artifact files relevant to the next session with their paths and a one-line description.

**Step 5 - Write output**
Write `$o` using the structure in `template.md`.
Confirm file written.

## Readiness gate
- No sensitive data in output
- No large artifact content duplicated
- Next session focus is clear and actionable
- Relevant file paths are listed and accurate

## Output contract
See `template.md` for required sections.

## Validation
Verify against `checklist.md` before writing.
