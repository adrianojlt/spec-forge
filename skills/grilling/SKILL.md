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
- State a confidence number (0-100%) each turn. Below 70%, append a one-line reason naming what is still unresolved.
- Resolve dependencies between decisions one by one, walking each branch of the decision tree.
- If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up instead of asking. The *decisions* are the user's - put each one to them and wait.
- Do not act on the plan until the user confirms a shared understanding has been reached.
- "Sounds good", "whatever you think", and silence are not confirmation. See Step 4.
- If `$o` is set, write the `Source:` header as a path relative to the output file's own folder (e.g. `./auth-idea.md`), never absolute.

## Procedure

**Step 1 - Read**
Read `$i` in full (or capture the inline idea/plan/decision). Explore any referenced code or files before questioning.

**Step 2 - Interview**
Walk the decision tree one question at a time. Format each turn:

```
CONFIDENCE: ~<n>% [- <what is still unresolved, required below 70%>]
Q:          <one focused question>
RECOMMEND:  <your recommended answer, with the reasoning that produced it>
```

Wait for the user. Follow dependencies as answers surface them. Look up facts; never ask what the environment can tell you.

Watch for *should-want* answers: best-practice talk ("scalable", "clean architecture", "modern"), deference to convention ("the standard approach"), or "I should probably...". These are what a thoughtful answer sounds like, not what the user wants. When you hear one, ask:

> "If you didn't have to justify this to anyone, what would you actually want?"

**Step 3 - Stop test**
Stop interviewing when you can answer yes to: *can I predict the user's reaction to the next three questions I would ask?* If no, ask the next question.

Floor: if several rounds pass and confidence is not visibly rising, stop and say so. "I've asked N questions and still can't predict your reactions. Something foundational is missing. Want to step back?"

**Step 4 - Restate and confirm**
State the shared understanding back in the user's own words, then wait for an explicit yes:

```
- Outcome:      <one line>
- User:         <one line - who benefits>
- Why now:      <one line - what changed>
- Success:      <one line - how we know it worked>
- Constraint:   <one line - the binding limit>
- Out of scope: <one line - what we are explicitly not doing>

Yes / no / refine?
```

`Out of scope` is mandatory. Silent disagreement about non-goals is half of all misalignment.

Not a yes: "whatever you think is best" (delegation - re-ask with two concrete options), "sounds good" (ask "anything you'd refine?"), silence. Fold every correction in and restate. Loop until an explicit yes. Do not proceed or act until then.

**Step 5 - Write output (only if `$o` set)**
If `$o` was provided, write the confirmed shared understanding to it. Never write before the explicit yes; the file itself implies a confirmation the user did not give.

## Output contract
- No file by default - the shared understanding lives in the conversation.
- If `$o` is set: one artifact at `$o` capturing the confirmed understanding, with a relative `Source:` header.
