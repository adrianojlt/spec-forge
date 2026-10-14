---
name: swift-coding-standards
description: "Swift coding standards: optionals, error handling, protocols, concurrency, and project structure."
disable-model-invocation: true
---

**Activation:** If invoked with no code target or explicit request, reply that these standards are loaded and ask what to apply them to. Do not start reviewing or refactoring the project on your own. Apply the standards below only when writing or reviewing code at the user's request.

# Swift Coding Standards

Builds on `coding-principles`. The Swift API Design Guidelines are the baseline; these are the points to enforce.

## Optionals and errors
- No force unwrap (`!`) and no implicitly unwrapped optionals in production code, except `@IBOutlet`. Use `guard let` for early exit, `if let` for local branches, `??` for real defaults.
- Throw typed domain errors (enums conforming to `Error`); never `try?` away an error that a caller or the user should see.

## Types
- Structs and enums by default; a class only for identity, shared mutable state, or framework requirements. Mark classes `final` unless designed for inheritance.
- Enums with associated values over flag combinations; make invalid states unrepresentable.
- Protocols for real abstraction points (a second implementation or a test double), with default behavior in extensions. Composition over class hierarchies.
- Access control as narrow as possible: `private` first, `public` only for module API.

## Concurrency
- `async` / `await` and structured concurrency (`async let`, task groups) over completion handlers and detached tasks.
- Shared mutable state lives in an `actor`; UI updates on `@MainActor`.
- Closures that capture `self` and outlive the call use `[weak self]`.
- Strict concurrency checking warnings are fixed, not suppressed.

## Tests
- XCTest or Swift Testing, one scenario per test; async tests use `async` test functions, not expectations with sleeps.
