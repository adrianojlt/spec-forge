---
name: kotlin-coding-standards
description: "Kotlin coding standards: null safety, coroutines, data classes, and project structure."
disable-model-invocation: true
---

**Activation:** If invoked with no code target or explicit request, reply that these standards are loaded and ask what to apply them to. Do not start reviewing or refactoring the project on your own. Apply the standards below only when writing or reviewing code at the user's request.

# Kotlin Coding Standards

Builds on `coding-principles`. The Kotlin coding conventions are the baseline; these are the points to enforce.

## Null safety and immutability
- No `!!` in production code. Use `?.`, `?:`, `let`, or an early `return` / `throw` instead.
- `val` over `var`; read-only collection types (`List`, `Map`) in signatures, mutable ones kept local.
- `data class` for value carriers; `sealed` classes or interfaces for closed sets of states, with exhaustive `when` and no `else` branch.

## Errors
- Throw specific exceptions for unrecoverable cases (`repository.find(id) ?: throw NotFoundException("User", id)`).
- Return a sealed result type when failure is an expected outcome the caller must handle.
- `runCatching` must not swallow `CancellationException`; rethrow it, or avoid `runCatching` around suspend calls.

## Coroutines
- Structured concurrency only: `coroutineScope` / `supervisorScope`, never `GlobalScope`.
- Blocking I/O inside `withContext(Dispatchers.IO)`; inject dispatchers so tests can replace them.
- `Flow` for streams; respect cancellation in long loops.

## Style
- Extension functions for behavior that reads naturally on a type you do not own; not as a substitute for a method on your own class.
- Expression bodies for single-expression functions.
- No mutable shared state outside a coroutine-safe holder (`Mutex`, `StateFlow`, confinement).

## Tests
- JUnit 5 with MockK; backtick test names describing the scenario; `runTest` for suspend code, no `delay`-based waiting.
