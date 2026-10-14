---
name: python-coding-standards
description: "Python coding standards: type hints, error handling, async patterns, and project structure."
disable-model-invocation: true
---

**Activation:** If invoked with no code target or explicit request, reply that these standards are loaded and ask what to apply them to. Do not start reviewing or refactoring the project on your own. Apply the standards below only when writing or reviewing code at the user's request.

# Python Coding Standards

Builds on `coding-principles`. PEP 8 and the project's formatter/linter are the baseline; these are the points to enforce.

## Types
- Type hints on every function signature, with modern syntax: `list[str]`, `X | None`.
- `Protocol` for structural interfaces, only when there is a second implementation or a test double that needs it.
- `@dataclass` (frozen when possible) or the project's model library for structured data; no bare dicts passed between layers.

## Errors and resources
- Catch specific exceptions; never a bare `except:` or a silent `except Exception: pass`.
- Domain exceptions subclass a project base exception; re-raise with `raise ... from err` to keep the cause.
- Resources (files, connections, locks) are managed with `with` / context managers.
- No mutable default arguments.

## Async
- `async` only for I/O-bound work. Never call blocking I/O inside a coroutine; use the async client or `asyncio.to_thread`.
- `asyncio.gather` or task groups for independent work; every created task is awaited or tracked.

## Structure
- `src/` layout with `pyproject.toml`; group modules by feature.
- No module-level mutable state; pass dependencies explicitly.
- Logging through `logging.getLogger(__name__)` with lazy `%s` arguments, never `print`.
- Docstrings on public functions and classes only where the name and types do not already say it.

## Tests
- pytest, with fixtures for shared setup and `parametrize` for input tables. No `time.sleep` in tests.
