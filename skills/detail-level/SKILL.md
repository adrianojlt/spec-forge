---
name: detail-level
description: Shorten the agent's chat answers to a chosen detail level, from 01 minimal to 05 normal, while never cutting warnings, questions, or failures
argument-hint: "[d=<01-05>]"
disable-model-invocation: true
---

# detail-level

## Purpose
Reduce how much text the agent produces per turn in chat. Long, fully detailed answers are tiring to read on every iteration. This skill sets a length budget for answers, and lets you ask for more detail at any single point without leaving the reduced mode.

It controls **how much is said**, not **how it is written**. Style compression (dropping articles, filler, hedging) is a separate concern and is unaffected by this skill.

## Inputs
- `$d` - detail level (optional). Numeric, padded or unpadded: `d=1` and `d=01` mean the same thing. Valid values are `01` to `05`. Named values such as `d=minimal` are invalid. If the skill is invoked with no argument, start at `01 minimal`.

## Hard rules
- Apply the level to chat output only. Never apply it to files: code, comments, commits, docs, task files, memory files. Those are written in full regardless of the active level.
- Never compress the protected content listed in `## What never shrinks`. The level does not override it at any value, including `01`.
- Code blocks quoted inside an answer are never shortened or truncated to fit a budget.
- Announce every level change with exactly one line: `Detail level: 03 concise`.
- Only plain-language requests change the level mid-session. A bare `d=3` typed mid-session is not a level change.
- Invalid value: warn once, then continue at `05 normal`. Never abort. Message form: `Unknown detail level 'd=9'. Falling back to 05 normal.`

## Detail levels
The level sets a length budget for answers. It only compresses; there is no level above the default.

| d | name | length budget | content structure |
|---|---|---|---|
| 01 | minimal | 1-2 sentences, ~40 words | Direct answer only. No reasoning, no caveats, no lists. |
| 02 | very concise | ~80 words | Answer plus one supporting fact. Bullets allowed, no headings. |
| 03 | concise | ~150 words | Answer plus a short why. |
| 04 | balanced | ~350 words | Answer plus reasoning plus relevant caveats. |
| 05 | normal | unbounded | Current behavior, unchanged. |

- Word counts are targets, not hard cuts. If an answer cannot be correct within its budget, escalate one level at a time until it fits. Escalation is silent, applies to that answer only, and does not change the session level.
- `05` is the default, the off switch, and the exact equivalent of never having loaded the skill. All three are the same state.

## What never shrinks
Two categories. The split is the point of the skill: shortening an explanation is a gain, swallowing a warning is a bug.

**Never shrinks** - stated in full at every level, including `01`:
- Security warnings and irreversible-action confirmations.
- Clarifying questions, with every option intact.
- Reports of failure: work not done, a test that failed, a step that was skipped.
- Code blocks quoted in an answer.

**Shrinks with the level:**
- Reasoning, justification, supporting context.
- Summaries of work already done, including progress notes.
- Tradeoffs and alternatives. At `01` these become one line; they never disappear.

## Procedure

### Step 1 - Resolve the level
Resolve the level from `d=` if given, otherwise `01 minimal`. If `d=` was given but is not one of `01`-`05`, print the fallback warning once and use `05 normal`.

Confirm with one line: `Detail level: 01 minimal`.

### Step 2 - Answer at the level
Render every answer at the active level. Apply the budget to the answer's prose. Keep the protected content of `## What never shrinks` complete.

Escalate silently for a single answer when correctness requires it.

### Step 3 - Expand on request
When the user asks for more detail (`mais detalhe`, `more detail`, `explica melhor`, `expand`, or equivalent), expand **the previous answer only**. The session level does not change, and the answer after the expansion returns to the active level.

Do not announce a level change; none happened.

### Step 4 - Change the level
Recognize plain-language level changes: `nivel de detalhe 3`, `detail level 3`, `use level 4`.

Recognize plain-language returns to normal: `volta ao normal`, `para de encurtar`, `back to normal`, `stop shortening`. These mean `05`.

A bare `d=3` typed mid-session is not a level change, so that `d=3` appearing inside a sentence never changes the level by accident. Vague requests such as "be more concise" are not level changes either.

Acknowledge with one line. Apply from the next answer on.

## Deactivate
`d=5` is the off switch. There is no separate `off` command, because `05` already means "as if the skill were not loaded".

All of these reach the same state:
- `/detail-level d=5` at invocation
- `nivel de detalhe 5` mid-session
- `volta ao normal` or `para de encurtar` mid-session

## Scope notes
- The level is not persisted. It lasts for the session and is not carried to the next one.
- On a long session the rule may lose force, and it is lost on compaction. Restate the level in plain language to restore it.
- The level applies to the agent's own chat output. It does not change which tools are used, how much of a file is read, or what work is done.
