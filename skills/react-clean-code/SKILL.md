---
name: react-clean-code
disable-model-invocation: true
description: Review and improve React code using clean code and React best practices.
---

## Activation

If invoked with no target file, component, or explicit request, reply that react-clean-code is loaded and ask what to review. Do not start analyzing the project on your own. Only review once the user points at code or asks for a review.

---

You are reviewing or editing a React codebase. Builds on `coding-principles` and `typescript-coding-standards`; where they conflict, this skill wins.

## Detect the setup first

Check `package.json` for the React version and whether React Compiler is enabled, and match the codebase's existing idiom. With the compiler on, do not add manual `useMemo`, `useCallback`, or `memo`.

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

## Reviewing

Look for purity violations and side effects in render, state structure problems, effect misuse, hidden coupling between unrelated parts, and patterns that make tests difficult. Distinguish style issues from real engineering risks, and suggest the smallest safe refactor.

## Output format for reviews

For a messy area, lead with the top structural problems, the top quick wins, and the safest cleanup order. Then, for each issue, include:
- severity: high / medium / low
- file path
- what is wrong
- why it is a problem
- smallest safe fix
- category: purity, state, hooks, component design, async flow, naming, or testability

## Editing rules

- Do not rewrite large areas unless explicitly asked.
- Prefer incremental, behavior-preserving refactors.
- Keep public component APIs stable unless there is a strong reason to change them.
- When changing state structure, explain the old problem and the new ownership model.
- When removing an effect, explain why derived state or event handling is better.
