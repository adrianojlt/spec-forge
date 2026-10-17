# Spec: [Title]

Source: [relative path to the input from this file's folder, e.g. ./auth-idea.md - never absolute; "conversation" if the idea was given in chat]
Date: [date]
Status: [Draft | Approved]

---

## Problem

[What is broken or missing, for whom, and why now.]

## Goals

- [Goal, and how success is observed]

## Non-goals

- [What is explicitly out of scope]

## Decisions

- [Decision]: [why; alternatives rejected]

## Codebase Findings

[Brownfield only, omit otherwise: relevant files and modules, current behavior, constraints already in place.]

**Patterns:** [one canonical example per convention the change touches; "none found" when the codebase has none, never invented]
- [Convention, e.g. error handling]: `[path/File#symbol]` - [what to mirror or avoid]

**Validation commands:**
- `[command]` - [what it proves, e.g. unit tests of the affected module]

## Slices

### Slice 1: [Name]
[What it delivers, observable by a user.]
- Depends on: [nothing | Slice N]
- Acceptance:
  - Given [state] When [action] Then [outcome]
  - Given [failure state] When [action] Then [outcome]

### Slice 2: [Name]
[...]

## Risks

- [Risk and how the plan handles it]

## Open Questions

- [ ] [Question] - [deferred because ...]
