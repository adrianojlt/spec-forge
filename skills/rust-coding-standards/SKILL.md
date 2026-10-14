---
name: rust-coding-standards
description: "Rust coding standards: ownership, error handling, traits, concurrency, and project structure."
disable-model-invocation: true
---

**Activation:** If invoked with no code target or explicit request, reply that these standards are loaded and ask what to apply them to. Do not start reviewing or refactoring the project on your own. Apply the standards below only when writing or reviewing code at the user's request.

# Rust Coding Standards

Builds on `coding-principles`. Idiomatic Rust (API Guidelines, `rustfmt`, `clippy`) is the baseline; these are the points to enforce.

## Errors
- No `unwrap` / `expect` in library code or request paths; return `Result`. In binaries and tests they are fine, with `expect("why this cannot fail")` over `unwrap`.
- Propagate with `?` and add context where the error crosses a module boundary.
- One error enum per crate or module boundary, with `Display`; `thiserror` for libraries, `anyhow` only in application entry points.

## Ownership and types
- Borrow by default: `&str` over `String`, `&[T]` over `Vec<T>` in parameters. Take ownership only when the function stores or consumes the value.
- A `clone()` needs a reason; it is not a fix for a borrow-checker error.
- Make invalid states unrepresentable: enums over boolean flags, newtypes for IDs and units, typestate when an order of operations matters.
- `Rc` / `Arc` / `RefCell` / `Mutex` are a design signal; reconsider ownership first.

## Traits and generics
- Generics with `where` clauses once bounds stop fitting on one line; `impl Trait` in return position to hide concrete types.
- Do not define a trait until there is a second implementation or a test double that needs it.

## Concurrency
- Prefer message passing (channels) or ownership transfer; `Arc<Mutex<_>>` only for genuinely shared state, and never hold a lock across `.await`.
- Do not mix blocking calls into async code; use the runtime's blocking escape hatch.

## Tooling
- `cargo fmt` output is final; `cargo clippy` clean, warnings treated as errors.
- Unit tests in a `#[cfg(test)] mod tests` beside the code; integration tests in `tests/`.
