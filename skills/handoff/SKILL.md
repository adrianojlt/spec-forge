---
name: handoff
description: Produce a resumable session handoff document for a future Claude Code session. References existing artifacts by path, does not duplicate content.
argument-hint: "o=<path> n=<description>"
disable-model-invocation: true
---

# handoff

## Purpose
Write a short document that lets a future session pick up exactly where this one ended, focused on what the next session (`$n`) needs.

## Inputs
- `$o` - path for the handoff document (e.g. `sessions/2026-05-23-auth.md`)
- `$n` - one sentence describing the focus of the next session

## Rules
- Under 500 words. Reference artifacts by path; never copy their content.
- Cover what was done, decisions made, what was deferred, open questions, and one concrete next action aligned with `$n`.
- No secrets, tokens, or credentials.

## Output
`$o`, following `template.md`.
