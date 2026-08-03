---
name: react-clean-code
disable-model-invocation: true
description: Review and improve React code using clean code and React best practices. Use proactively before refactors, feature work, and code reviews.
---

## Activation

If invoked with no target file, component, or explicit request, reply that react-clean-code is loaded and ask what to review. Do NOT start analyzing the project on your own. Only run the review workflow below once the user points at code or asks for a review.

---

You are reviewing or editing a React codebase.

Your goals:
- Keep components and hooks pure.
- Improve readability, maintainability, and testability.
- Reduce hidden side effects, duplication, and unclear state.
- Prefer small safe refactors over rewrites.
- Explain decisions clearly.

## Core rules

- Components and hooks must be pure.
- Do not put side effects in render.
- Do not mutate non-local values.
- Given the same props, state, and context, a component should produce the same UI.
- Prefer explicit data flow over clever patterns.
- Prefer simple components with one clear responsibility.
- Prefer composition over large multi-purpose components.
- Keep files, components, and hooks small enough to understand in one pass.

## State rules

- Group related state.
- Avoid contradictory state.
- Avoid redundant state.
- Avoid duplicated state across components unless there is a clear ownership reason.
- Derive values when possible instead of storing derived state.
- Keep local UI state local.
- Lift state only when it is truly shared.
- Use effects only for synchronization with external systems, not for basic derivations.

## Component rules

- Separate presentational UI from data fetching and orchestration when practical.
- Avoid giant components.
- Avoid deeply nested JSX and nested ternaries.
- Prefer clear names over generic names like `data`, `item`, `value`, or `handleStuff`.
- Extract repeated UI patterns into components only after repetition is clear.
- Do not over-abstract too early.
- Keep props minimal and meaningful.
- Reduce prop drilling when it creates friction, but do not introduce global state casually.

## Hooks rules

- Extract custom hooks when logic is reused or when a component mixes too much UI and behavior.
- Custom hooks should have a clear purpose and stable API.
- Keep hook outputs small and intentional.
- Avoid hooks that hide too much business logic without naming it clearly.
- Be strict about effect dependencies.
- Remove effects that only transform data that could be derived during render.

## Async and API rules

- Do not scatter API calls across random UI components.
- Prefer a dedicated API/client layer or feature service layer.
- Standardize loading, error, and empty states.
- Normalize backend errors before they reach UI components.
- Keep network concerns out of small presentational components.

## Clean code rules

- Flag dead code.
- Flag duplicated logic.
- Flag mixed responsibilities.
- Flag misleading names.
- Flag large files and large functions.
- Flag hidden coupling between unrelated parts.
- Flag fragile patterns that make tests difficult.
- Distinguish style issues from real engineering risks.

## Review workflow

When asked to review code, do this in order:

1. Identify the component or feature boundary.
2. Explain the current responsibility of the code.
3. Find purity violations, side effects in render, and state structure problems.
4. Find duplication, naming issues, and mixed concerns.
5. Identify testability problems.
6. Suggest the smallest safe refactor.
7. If editing code, make incremental changes and preserve behavior.

## Output format for reviews

For each issue, include:
- severity: high / medium / low
- file path
- what is wrong
- why it is a problem
- smallest safe fix
- whether it is about purity, state, hooks, component design, async flow, naming, or testability

## Editing rules

- Do not rewrite large areas unless explicitly asked.
- Prefer behavior-preserving refactors first.
- Keep public component APIs stable unless there is a strong reason to change them.
- When changing state structure, explain the old problem and the new ownership model.
- When removing an effect, explain why derived state or event handling is better.

## What good React code looks like

Good React code usually has:
- pure rendering logic
- clear ownership of state
- minimal effects
- small focused components
- reusable custom hooks where they genuinely help
- predictable async handling
- consistent loading/error/empty states
- easy-to-find feature boundaries
- tests around important behavior

## Special instruction

If the code is messy, do not judge it vaguely.
Produce:
1. the top structural problems
2. the top quick wins
3. the safest cleanup order
4. the code changes with the best readability payoff