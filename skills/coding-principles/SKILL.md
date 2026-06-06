---
name: coding-principles
description: "Language-agnostic coding principles: readability, simplicity, and maintainability for any programming language."
---

# Coding Principles

Universal principles for writing readable, maintainable code in any language.

## When to Activate

- Writing or reviewing code in any programming language
- Establishing team coding standards
- Refactoring existing code
- Onboarding developers to code quality expectations
- Making architectural decisions about code organization

## Core Principles

### 1. Readability First

**Code is read far more than it is written.**

- Choose clear, descriptive names for variables, functions, and types
- Prefer self-documenting code over comments
- Maintain consistent formatting throughout the codebase
- Optimize for human comprehension, not compiler cleverness
- When in doubt, choose the more readable option

### 2. KISS (Keep It Simple, Stupid)

**The simplest solution that works is usually the best.**

- Avoid over-engineering and premature abstraction
- No premature optimization without profiling data
- Easy to understand beats clever every time
- If a solution feels complex, question whether it needs to be
- Start simple, add complexity only when proven necessary

### 3. DRY (Don't Repeat Yourself)

**Every piece of knowledge should have a single, authoritative representation.**

- Extract common logic into reusable functions or modules
- Share utilities across components and services
- Avoid copy-paste programming
- When you see duplication, consolidate it
- Balance DRY with readability - don't over-abstract

### 4. YAGNI (You Aren't Gonna Need It)

**Don't build features before they're needed.**

- Avoid speculative generality and premature abstraction
- Add complexity only when requirements demand it
- Don't implement "just in case" functionality
- Start with the minimum viable solution
- Refactor when actual needs emerge, not imagined ones

## Code Quality Guidelines

### Naming Philosophy

- Names should reveal intent - a reader should understand purpose without reading implementation
- Longer, descriptive names beat short, cryptic ones
- Consistent naming patterns across the codebase
- Avoid abbreviations unless universally understood in the domain
- Boolean names should read as questions (isReady, hasPermission, canExecute)

### Function Design

- Functions should do one thing and do it well
- Keep functions short and focused
- Minimize side effects - be explicit about what a function changes
- Prefer pure functions when possible (same input, same output)
- Limit parameter count - use parameter objects for complex signatures

### Error Handling Philosophy

- Fail fast with meaningful error messages
- Handle errors at the appropriate level of abstraction
- Don't hide errors - log them or propagate them with context
- Distinguish between recoverable and unrecoverable errors
- Provide actionable information in error messages

### Immutability

- Prefer immutable data structures by default
- Minimize shared mutable state
- When mutation is necessary, make it explicit and localized
- Immutable code is easier to reason about and test
- Reduces bugs related to concurrent access

### Testing Principles

- Tests should be deterministic and repeatable
- Test behavior, not implementation details
- Each test should verify one concept
- Tests should be fast to run
- Test names should describe the scenario being tested
- Maintain test code with the same care as production code

## Code Smells to Avoid

### Structural Smells

- **Long parameter lists** - use parameter objects or builders
- **Deep nesting** - use early returns, extract helper functions
- **Large functions** - break into smaller, focused functions
- **God classes/modules** - split into cohesive, single-responsibility units
- **Feature envy** - move behavior closer to the data it operates on

### Implementation Smells

- **Magic numbers** - use named constants
- **Magic strings** - use enums, constants, or configuration
- **Commented-out code** - delete it, version control has history
- **Dead code** - remove unused code paths
- **Speculative generality** - remove unused abstractions

### Behavioral Smells

- **Silent failures** - always handle or log errors
- **Hidden side effects** - make state changes explicit
- **Inconsistent abstractions** - maintain consistent levels of abstraction
- **Premature optimization** - optimize only with profiling evidence
- **Clever code** - prioritize clarity over cleverness

## Architecture Principles

### Separation of Concerns

- Each module, class, or function should have one clear responsibility
- Separate business logic from infrastructure concerns
- Keep UI/presentation logic separate from domain logic
- Isolate external dependencies behind clear interfaces

### Dependency Management

- Depend on abstractions, not concretions
- Minimize coupling between components
- Make dependencies explicit and injectable
- Avoid circular dependencies
- Prefer composition over inheritance

### API Design

- Design APIs for the consumer, not the implementer
- Be consistent in naming, parameter order, and return types
- Make the right way easy and the wrong way hard
- Document contracts clearly (inputs, outputs, errors, side effects)
- Version APIs when breaking changes are necessary

## Maintenance Principles

### Refactoring

- Refactor when code becomes hard to change or understand
- Keep refactoring separate from feature work
- Ensure tests pass before and after refactoring
- Make small, incremental changes
- Don't refactor code that isn't broken or causing pain

### Documentation

- Code should be self-documenting through good naming
- Document "why" not "what" - explain decisions and trade-offs
- Keep documentation close to the code it describes
- Update documentation when code changes
- Avoid redundant documentation that restates the code

### Evolution

- Design for change, but don't over-design
- Make it easy to add new features without modifying existing code
- Prefer extension over modification
- Accept that requirements will change - design accordingly
- Leave the codebase better than you found it

## Decision Framework

When facing a coding decision, ask:

1. **Is it readable?** Can someone unfamiliar with the code understand it quickly?
2. **Is it simple?** Is this the simplest solution that works?
3. **Is it necessary?** Does this solve an actual, current requirement?
4. **Is it maintainable?** Will this be easy to change when requirements evolve?
5. **Is it testable?** Can I verify this works correctly and continues to work?

If any answer is "no", reconsider the approach.

## Remember

- **Intentional over accidental** - every line of code should have a clear purpose
- **Explicit over implicit** - make behavior and dependencies obvious
- **Consistent over clever** - follow established patterns in the codebase
- **Maintainable over optimal** - prioritize long-term sustainability over micro-optimizations
- **Working over perfect** - ship working code, iterate based on real feedback
