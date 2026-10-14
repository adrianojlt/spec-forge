---
name: typescript-coding-standards
description: "TypeScript coding standards: types, interfaces, error handling, async patterns, and project structure."
disable-model-invocation: true
---

**Activation:** If invoked with no code target or explicit request, reply that these standards are loaded and ask what to apply them to. Do not start reviewing or refactoring the project on your own. Apply the standards below only when writing or reviewing code at the user's request.

# TypeScript Coding Standards

Builds on `coding-principles`. Assumes `strict: true`; these are the points to enforce.

## Types
- No `any`. Use `unknown` and narrow it. No `as` casts or non-null `!` to silence the compiler; validate external data at the boundary (e.g. a schema parser) and let the types follow.
- `interface` for object shapes, `type` for unions, intersections, and function types.
- Discriminated unions for state (`{ status: 'loading' } | { status: 'success'; data: User }`), with exhaustive `switch` checked by a `never` default.
- String literal unions over `enum`.
- `readonly` fields and `ReadonlyArray` for data that should not change.
- Generics only when the function is used with more than one type; constrain them with `extends`.

## Errors and async
- Throw `Error` subclasses with a `name` and the data a caller needs; never throw strings.
- In `catch`, the error is `unknown`: narrow with `instanceof` before using it.
- No floating promises: every promise is awaited, returned, or explicitly handled. `Promise.all` for independent work.
- Do not turn an error into `null` unless absence is a real, documented outcome.

## Structure
- Group by feature (`user/user.service.ts`, `user/user.types.ts`), not by kind.
- Dependencies passed through constructors or function parameters; no module-level mutable state.
- Named exports over default exports.

## Tests
- Test the public behavior of a module; mock only at I/O boundaries.
