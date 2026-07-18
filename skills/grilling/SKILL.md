---
name: grilling
description: Relentless one-at-a-time interview to stress-test a plan, decision, or idea until you reach a shared understanding
argument-hint: "[i=<idea-or-file>] [o=<understanding.md>]"
disable-model-invocation: true
---

# grilling

## Purpose
Interview the user relentlessly about a plan, decision, or idea, walking down each branch of the decision tree one at a time until a shared understanding is reached. Unlike `/grill-me` (which batches questions and always writes a file), grilling is a conversational stress-test: one question at a time, a recommended answer for each, and a written summary only when asked.

## Inputs
- `$i` - idea, plan, or file to interrogate (optional; describe it inline at invocation if no file exists)
- `$o` - where to write the shared understanding (optional; if omitted, the understanding stays in the conversation and nothing is written)

## Hard rules
- Ask one question at a time. Wait for the answer before the next. Asking multiple questions at once is bewildering.
- For each question, provide your recommended answer.
- Resolve dependencies between decisions one by one, walking each branch of the decision tree.
- If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up instead of asking. The *decisions* are the user's - put each one to them and wait.
- Do not act on the plan until the user confirms a shared understanding has been reached.
- If `$o` is set, write the `Source:` header as a path relative to the output file's own folder (e.g. `./auth-idea.md`), never absolute.

## Procedure

**Step 1 - Read**
Read `$i` in full (or capture the inline idea/plan/decision). Explore any referenced code or files before questioning.

**Step 2 - Interview**
Walk the decision tree one question at a time. For each: state the question, give your recommended answer, wait for the user. Follow dependencies as answers surface them. Look up facts; never ask what the environment can tell you.

**Step 3 - Confirm**
When every branch is resolved, state the shared understanding and ask the user to confirm. Do not proceed or act until they do.

**Step 4 - Write output (only if `$o` set)**
If `$o` was provided, write the confirmed shared understanding to it.

## Output contract
- No file by default - the shared understanding lives in the conversation.
- If `$o` is set: one artifact at `$o` capturing the confirmed understanding, with a relative `Source:` header.
