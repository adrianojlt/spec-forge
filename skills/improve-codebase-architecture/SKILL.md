---
name: improve-codebase-architecture
description: Identify shallow modules and structural weaknesses in the current codebase; propose deeper agent-friendly module designs
disable-model-invocation: true
---

# improve-codebase-architecture

## Purpose
Find structural patterns in the current directory that hurt agent-driven coding, and propose "deepening": fewer, larger, well-named modules with clear invariants, so one logical change touches fewer files. Analysis only, no code changes.

## Scope
- **YAGNI / hot spots**: if the user named a direction (module, subsystem, pain point), focus there. Otherwise, inspect recent commits (`git log --oneline`) to find areas that change often and prioritize those first; widen only if churn is scattered. Deepening untouched code rarely pays back.
- **Fresh exploration**: delegate the codebase scan to a subagent with a fresh context window when available, so exploration does not crowd the main session.
- **ADRs**: if ADRs exist (e.g. `docs/adr/`), read relevant ones first. Do not re-litigate an ADR unless the friction clearly justifies reopening it, and flag the conflict explicitly.

## What to look for
- **Scattered concepts**: one domain concept spread over many small files (`user.js`, `user-helpers.js`, `user-utils.js`, `user-validators.js`). Evidence: name clusters, import graph.
- **Testability extractions**: pure functions moved into their own files only to unit-test them, called from one place. Extracting for testability alone is not an architectural improvement.
- **Tight coupling**: high fan-out to siblings, or high fan-in from unrelated modules.
- **Shallow modules**: many exports with thin bodies and no invariant they protect; callers must know too much.

Style (formatting, naming conventions) is out of scope unless it creates structural coupling.

## Rules
- Apply the **deletion test** to suspected shallow modules: would removing or merging it concentrate complexity behind a smaller interface, or just move it elsewhere? Keep only candidates where complexity concentrates.
- Pick up to 5 candidates (fewer is fine; if nothing clears the bar, say so instead of padding), ranked by how many files a logical change touches, coupling radius, and how clearly a module owns one thing.
- Tag every candidate with a strength: `Strong` (clear friction, passes deletion test), `Worth exploring` (payoff depends on upcoming work), or `Speculative`.
- Every candidate cites evidence: file paths, line counts, import counts. Not opinion.
- Every proposal names exactly what to merge, rename, encapsulate, or delete, the expected benefit, and the effort (small / medium / large). Drop anything vaguer than that.

## Output
`architecture-report.md` in the current directory, following `template.md`.
