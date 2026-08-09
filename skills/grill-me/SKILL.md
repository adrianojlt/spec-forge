---
name: grill-me
description: Explore and flesh out an idea through relentless questioning before any document is written
argument-hint: "i=<idea-or-draft-file> [o=<grilled-notes.md>]"
disable-model-invocation: true
---

# grill-me

## Purpose
Read an idea or draft and ask relentless questions until every assumption, constraint, and design branch is resolved. No output until all branches are closed. Can explore the codebase to answer its own questions rather than always deferring to the user.

Feeds into `/draft-discussion`, which detects grilled notes and asks only the themes they leave unresolved.

## Inputs
- `$i` - idea or draft file to explore (or describe the idea inline at invocation if no file exists yet)
- `$o` - where to write grilled-notes.md (optional; defaults to `grilled-notes.md` in current dir)

## Hard rules
- Write the `Source:` header as a path relative to the output file's own folder (e.g. `./auth-idea.md`), never absolute - keeps links valid if the specs folder is moved.
- No code at this stage.
- No architecture decisions unless the user confirms them.
- If a question can be answered by exploring the codebase, explore the codebase - do not ask the user.
- Do not write output until the readiness gate passes.
- Always batch questions by theme. Never ask one question at a time.
- Do not summarize what you already know between rounds - only ask what remains unresolved.

## Procedure

**Step 1 - Read**
Read `$i` in full (or capture the inline idea). If the idea references existing code, explore the relevant files before asking any questions.

**Step 2 - Round 1 questions**
Ask 8-15 grouped questions across these themes (skip themes with obvious answers):
1. Goals - what outcome are we trying to achieve, how is success measured
2. Problem - what is broken or missing today, why now
3. Users - who uses this, who approves it, who is affected by it
4. Constraints - time, budget, tech stack, org, legal, existing dependencies
5. Scope boundary - what is explicitly out of scope
6. Technical unknowns - what is unclear about how this works or integrates
7. Risks - what could go wrong, what is the worst case
8. Definition of done - when is this considered complete

**Step 3 - Follow-up rounds**
After each answer set, identify remaining unresolved branches. Ask targeted follow-ups. Repeat until the readiness gate passes. Do not ask about things the codebase can answer - explore instead.

**Step 4 - Write output**
Write `$o` (or `grilled-notes.md`) using the structure in `template.md`.

## Readiness gate
All must pass before writing output:
- Problem is unambiguous
- Goals are bounded and measurable
- All major design decisions resolved or explicitly deferred with rationale
- No critical open question remains unacknowledged
- Scope boundary is explicit

## Output contract
One artifact:
- `$o` or `grilled-notes.md` - consolidated understanding. See `template.md` for required sections.

## Validation
Every section in `template.md` must be filled. Open Questions must be empty or contain only acknowledged deferrals with rationale.
