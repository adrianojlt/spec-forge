---
name: improve-codebase-architecture
description: Identify shallow modules and structural weaknesses in the current codebase; propose deeper agent-friendly module designs
disable-model-invocation: true
---

# improve-codebase-architecture

## Purpose
Analyze the codebase in the current directory for structural patterns that hurt agent-driven coding: scattered concepts, over-extracted pure functions, tightly coupled modules. Propose candidates for "deepening" - fewer, larger, well-named modules with clear invariants.

No code changes. Analysis and proposals only.

## Inputs
None. Operates on the current working directory.

## Hard rules
- No code changes at this stage.
- Every candidate must be backed by concrete evidence (file paths, line counts, coupling metrics) - not opinion.
- Proposals must be specific: name what to merge, rename, or encapsulate.
- Do not flag style issues (formatting, naming conventions) unless they create structural coupling.
- Do not propose extracting code for testability alone - that is not an architectural improvement.

## Procedure

**Step 1 - Map the codebase**
Explore the current directory:
- List all modules/packages and their file counts and approximate line counts
- Identify the top-level organizational structure (by feature, by layer, by type, etc.)
- Note any obvious inconsistencies in how concepts are organized

**Step 2 - Find structural weaknesses**
Scan for these anti-patterns with evidence:

1. **Scattered concepts** - A single domain concept implemented across many small files (e.g., "user" logic split across `user.js`, `user-helpers.js`, `user-utils.js`, `user-validators.js`). Evidence: file name clusters, import graph.

2. **Testability extractions** - Pure functions pulled into separate files solely to make them unit-testable, not because they represent a real abstraction. Evidence: tiny files with no imports, called from exactly one place.

3. **Tight coupling** - Modules with high fan-out (many imports from siblings) or fan-in (imported by many unrelated modules). Evidence: import count, call graph breadth.

4. **Shallow modules** - Files that expose many small functions with no encapsulation of invariants. Evidence: many exports, thin function bodies, callers must know too much.

**Step 3 - Prioritize candidates**
Select the top 3-5 candidates by:
- How often agents need to edit across multiple files to make one logical change (high = bad)
- Coupling radius (how many files break if this one changes)
- Concept coherence (does this file/module own one thing clearly)

**Step 4 - Propose improvements**
For each candidate, write a specific proposal:
- Current state (what exists, with evidence)
- Proposed design (what to merge, rename, encapsulate, or delete)
- Expected benefit (fewer files touched per logical change, clearer ownership)
- Estimated effort (small / medium / large)

**Step 5 - Write report**
Write `architecture-report.md` in the current directory using `template.md`.

## Readiness gate
All must pass before writing:
- Every candidate has file path evidence (not just opinion)
- Every proposal is specific enough to act on
- No candidate is a style issue disguised as a structural one

## Output contract
One artifact:
- `architecture-report.md` in the current directory. See `template.md` for required sections.

## Validation
Before writing, verify each candidate section has: current state with evidence, a concrete proposal, and an effort estimate. Vague proposals ("refactor this module") must be made specific or removed.
