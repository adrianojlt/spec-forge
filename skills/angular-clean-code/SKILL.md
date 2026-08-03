---
name: angular-clean-code
disable-model-invocation: true
description: Review and improve Angular code using clean code and modern Angular best practices (standalone, signals, OnPush, RxJS hygiene, DI). Use proactively before refactors, feature work, and code reviews.
---

## Activation

If invoked with no target file, component, or explicit request, reply that angular-clean-code is loaded and ask what to review. Do NOT start analyzing the project on your own. Only run the review workflow below once the user points at code or asks for a review.

---

You are reviewing or editing an Angular codebase.

Your goals:
- Keep templates declarative and components thin.
- Improve readability, maintainability, and testability.
- Reduce hidden side effects, duplication, and unclear state ownership.
- Prefer small safe refactors over rewrites.
- Explain decisions clearly.

## Detect the Angular version first

Rules below differ by version. Before proposing changes, check `package.json` for the `@angular/core` version and match the codebase's existing idiom.

- Signals, `input()`/`output()`, `@if`/`@for`/`@switch` control flow, `@let`, zoneless change detection: modern Angular only.
- If the project is on an older version or is consistently RxJS-and-decorator based, do not propose a signals migration as a "cleanup". Note it as a separate, explicit decision.
- Never mix idioms inside one component just because the newer one is available.

## Core rules

- Templates must be side-effect free. No method calls that mutate, fetch, or log during change detection.
- Do not call expensive functions from a template binding. Bind to a signal, a field, or a pure pipe instead.
- A component should have one clear responsibility: render state and emit intent.
- Prefer explicit data flow over clever patterns and over ambient shared services.
- Prefer composition over large multi-purpose components.
- Keep files, components, and services small enough to understand in one pass.
- Prefer standalone components over `NgModule` in projects that already use them.

## State and change detection rules

- Default to `ChangeDetectionStrategy.OnPush` for components. Flag components that rely on default change detection to see updates.
- Do not call `ChangeDetectorRef.detectChanges()` or `markForCheck()` to paper over a state ownership problem. Find why the reference did not change.
- Avoid `setTimeout` used to defer past a change detection cycle. It hides the real bug.
- Derive values instead of storing derived state. Prefer `computed()` (or a pure getter/pipe in older code) over a field kept in sync by hand.
- Avoid contradictory state (`loading` plus `error` plus `data` as three independent booleans). Model one state instead.
- Keep local UI state inside the component. Lift into a service only when genuinely shared.
- In signal code: `computed()` for derivation, `effect()` only for synchronizing with something outside Angular. An `effect()` that only sets another signal is almost always a `computed()`.
- Do not mutate objects or arrays held in a signal or an `OnPush` input. Replace the reference.

## Component and template rules

- Separate presentational components from container/orchestration components when practical.
- Keep templates shallow. Flag deep nesting and nested ternaries. Extract a child component or use `@if`/`@switch`.
- Avoid logic in templates beyond simple presentation. Move conditions into named signals, fields, or `@let`.
- Prefer clear names over generic names like `data`, `item`, `value`, or `handleStuff`.
- Keep inputs minimal and meaningful. A component taking eight inputs usually wants to be split or take one object.
- Do not reach into children with `ViewChild` to drive behavior that belongs in inputs and outputs.
- Extract repeated UI patterns into components only after repetition is clear. Do not over-abstract too early.
- `@for` must have a stable, meaningful `track` expression. Flag `track $index` over identified data.
- Prefer the `async` pipe (or `toSignal`) over subscribing in the component and assigning to a field.

## DI and service rules

- Services hold logic and state. Components hold rendering and intent. Flag business rules living in components.
- Prefer `inject()` in modern codebases. Follow the existing convention if the project uses constructor injection.
- Be deliberate about provider scope. `providedIn: 'root'` means shared global state. Component-level providers mean per-instance. Flag a "singleton" that should have been per-feature, and per-instance state that callers assume is shared.
- Do not inject a service just to reach another service. Flag chains that exist only to pass through.
- Keep services free of `document`, `window`, and other platform globals. Inject them so they can be faked in tests.

## RxJS and async rules

- Every long-lived subscription must be cleaned up: `async` pipe, `takeUntilDestroyed()`, or an explicit teardown in `ngOnDestroy`. Flag any subscription without one.
- Flag nested `subscribe` inside `subscribe`. Use `switchMap`, `concatMap`, `mergeMap`, or `exhaustMap`, and say which one and why.
- Pick the flattening operator on purpose: `switchMap` to cancel stale work, `concatMap` to preserve order, `exhaustMap` to ignore while busy, `mergeMap` only when concurrency is genuinely fine.
- Do not put side effects in `map`. Use `tap` if a side effect is really needed, and question whether it is.
- Share expensive or multicast sources deliberately (`shareReplay` with a defined `refCount`/buffer). Flag accidental duplicate HTTP calls from multiple subscribers.
- Handle errors at a defined boundary. A `catchError` that swallows into `of(null)` and leaves the UI in a silent broken state is a bug.
- Do not scatter `HttpClient` calls across UI components. Prefer a dedicated API/client layer or feature service.
- Standardize loading, error, and empty states across the feature. Normalize backend errors before they reach components.

## Forms rules

- Prefer reactive forms for anything with validation, cross-field rules, or dynamic controls.
- Do not mix template-driven and reactive forms in one form.
- Keep validators pure and named. Flag inline anonymous validators with real logic in them.
- Do not subscribe to `valueChanges` to hand-sync a second field when a `computed()`, a derived control, or a validator would do it.
- Type forms where the version supports it. Flag `any`-typed form values crossing into business logic.

## Routing and structure rules

- Organize by feature, not by type. Flag `components/`, `services/`, `models/` folders that force every feature change to touch four directories.
- Lazy load feature routes. Flag a large feature eagerly pulled into the initial bundle.
- Keep route guards and resolvers small and testable. Business decisions belong in a service the guard calls.

## Clean code rules

- Flag dead code.
- Flag duplicated logic.
- Flag mixed responsibilities.
- Flag misleading names.
- Flag large files and large functions.
- Flag hidden coupling between unrelated parts.
- Flag fragile patterns that make tests difficult.
- Flag `any`, non-null assertions (`!`), and casts that hide a real modeling problem.
- Distinguish style issues from real engineering risks.

## Review workflow

When asked to review code, do this in order:

1. Check the Angular version and the codebase's dominant idiom.
2. Identify the component, service, or feature boundary.
3. Explain the current responsibility of the code.
4. Find template side effects, change detection workarounds, and state ownership problems.
5. Find subscription leaks, nested subscribes, and wrong flattening operators.
6. Find duplication, naming issues, and mixed concerns.
7. Identify testability problems (hard-wired globals, unmockable dependencies, logic only reachable through the DOM).
8. Suggest the smallest safe refactor.
9. If editing code, make incremental changes and preserve behavior.

## Output format for reviews

For each issue, include:
- severity: high / medium / low
- file path
- what is wrong
- why it is a problem
- smallest safe fix
- category: template, change detection, state, DI, RxJS, forms, routing, structure, naming, or testability

## Editing rules

- Do not rewrite large areas unless explicitly asked.
- Prefer behavior-preserving refactors first.
- Keep component inputs and outputs stable unless there is a strong reason to change them.
- Do not migrate to signals, standalone, or new control flow as a side effect of an unrelated fix. Propose it separately.
- When changing state structure, explain the old problem and the new ownership model.
- When removing an `effect()` or a `valueChanges` subscription, explain why derivation or event handling is better.
- When changing a flattening operator, state the behavior change (cancellation, ordering, concurrency) explicitly.

## What good Angular code looks like

Good Angular code usually has:
- side-effect-free templates
- `OnPush` components with clear input contracts
- derived state instead of hand-synced fields
- no leaked subscriptions
- thin components and meaningful services
- a single API layer with consistent loading/error/empty handling
- feature-shaped folders and lazy-loaded routes
- deliberate provider scope
- tests that exercise behavior through services, not only through the DOM

## Special instruction

If the code is messy, do not judge it vaguely.
Produce:
1. the top structural problems
2. the top quick wins
3. the safest cleanup order
4. the code changes with the best readability payoff
