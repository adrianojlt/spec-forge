---
name: go-coding-standards
description: "Go coding standards: idioms, error handling, interfaces, concurrency, and project structure."
disable-model-invocation: true
---

**Activation:** If invoked with no code target or explicit request, reply that these standards are loaded and ask what to apply them to. Do not start reviewing or refactoring the project on your own. Apply the standards below only when writing or reviewing code at the user's request.

# Go Coding Standards

Builds on `coding-principles`. Idiomatic Go (Effective Go, Go Code Review Comments) is the baseline; these are the points to enforce.

## Errors
- Check every error immediately; never discard one with `_` unless a comment says why.
- Wrap with context using `%w`, lowercase and without "failed to": `fmt.Errorf("get user %s: %w", id, err)`.
- Sentinel errors (`var ErrNotFound = errors.New(...)`) for conditions callers branch on; custom error types when they need fields. Compare with `errors.Is` / `errors.As`, never by string.

## Interfaces and packages
- Accept interfaces, return structs. Define an interface in the package that consumes it, only when there is a second implementation or a test double that needs it.
- Small interfaces; single-method ones take the `-er` suffix.
- Group packages by feature, not by type. Application code under `internal/`. No package named `util`, `common`, or `helpers`.
- No package-level mutable state and no `init()` for wiring; pass dependencies explicitly.
- Functional options only when a constructor has several optional settings.

## Concurrency
- `context.Context` is the first parameter of anything that does I/O or may block; never store it in a struct.
- Every goroutine has a clear exit path (context cancellation or a closed channel). No goroutine leaks.
- Protect shared state with a mutex next to the data it guards, or confine it to one goroutine; `go test -race` must pass.

## Style
- `gofmt` / `goimports` output is final. Imports grouped stdlib, external, local.
- Receivers are short and consistent, never `self` or `this`.
- No naked returns in functions longer than a few lines.

## Tests
- Table-driven tests with `t.Run` and a descriptive `name` per case.
- `got %v, want %v` failure messages.
