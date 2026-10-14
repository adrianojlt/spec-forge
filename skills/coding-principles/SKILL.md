---
name: coding-principles
description: "Language-agnostic coding principles: readability, simplicity, and maintainability for any programming language."
---

# Coding Principles

Rules for writing and reviewing code in any language. Language skills (`<language>-coding-standards`) add to these; where they conflict, the language skill wins, and the project's existing patterns win over both.

## Simplicity
- Write the smallest change that solves the current requirement. No "just in case" features, options, or configuration for values that never change.
- No abstraction without a second real use: no single-implementation interfaces, no base classes for one subclass, no helper extracted for one call site.
- Tolerate duplication until the third occurrence; then extract. A wrong abstraction costs more than two copies.
- Optimize only with a measurement that shows the problem.

## Readability
- Names reveal intent without reading the body. No abbreviations outside well-known domain terms. Booleans read as questions (`isReady`, `hasPermission`).
- Early returns over nesting. One level of abstraction per function.
- Comments explain *why* (a decision, a constraint, a workaround), never *what* the code already says.
- Named constants instead of magic numbers and strings.

## Errors
- Fail fast, with a message that says what went wrong and with which input.
- Never swallow an error. Handle it where you can act on it; otherwise propagate it with added context.
- Validate at trust boundaries (user input, network, files, external APIs). Do not defend against states your own code makes impossible.

## State and structure
- Immutable by default; keep mutation local and visible.
- Make dependencies explicit (passed in), not reached for (globals, service locators).
- Keep domain logic out of transport, persistence, and UI code.
- Composition over inheritance. No circular dependencies.

## Tests
- Test behavior through the public surface, not implementation details.
- Deterministic: no real clock, network, or shared mutable state without control.
- One scenario per test, named after the scenario.

## Changes
- Match the existing patterns of the codebase over personal preference.
- Keep refactoring separate from feature work. Remove code your change made dead; mention other dead code instead of deleting it.
