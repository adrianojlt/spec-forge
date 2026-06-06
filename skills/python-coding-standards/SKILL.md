---
name: python-coding-standards
description: "Python coding standards: type hints, error handling, async patterns, and project structure."
---

# Python Coding Standards

Standards for writing idiomatic, maintainable Python code.

**Prerequisites**: Load `/coding-principles` first for language-agnostic guidelines.

## When to Activate

- Writing or reviewing Python code
- Designing Python modules and packages
- Working with type hints, async/await, or decorators
- Building web applications, APIs, or data pipelines

## Core Principles

- Readability counts (PEP 20: "The Zen of Python")
- Explicit is better than implicit
- Use type hints for better code quality
- Handle errors explicitly with exceptions
- Prefer composition over inheritance

## Naming

```python
# Classes: PascalCase
class UserService:
    pass

# Functions/variables: snake_case
def get_user_by_id(user_id: str) -> User:
    pass

user_count = len(users)

# Constants: SCREAMING_SNAKE_CASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Private: leading underscore
def _internal_helper():
    pass

_private_attribute = "internal"

# Modules: short, lowercase
import user_service
```

## Type Hints

```python
from typing import Optional, Union

# Use type hints for function signatures
def get_user(user_id: str) -> Optional[User]:
    return repository.find(user_id)

# Use Union for multiple types
def process_id(id_value: Union[str, int]) -> None:
    pass

# Use built-in types in Python 3.9+
def get_users() -> list[User]:
    return repository.find_all()

def get_user_map() -> dict[str, User]:
    return {u.id: u for u in users}

# Use TypeAlias for complex types (Python 3.10+)
from typing import TypeAlias

UserID: TypeAlias = str | int

# Use Protocol for structural typing
from typing import Protocol

class Logger(Protocol):
    def info(self, message: str) -> None:
        ...
    
    def error(self, message: str) -> None:
        ...

def process(logger: Logger) -> None:
    logger.info("processing")
```

## Error Handling

```python
# Define custom exceptions
class NotFoundError(Exception):
    def __init__(self, resource: str, id: str):
        super().__init__(f"{resource} not found: {id}")
        self.resource = resource
        self.id = id

class ValidationError(Exception):
    def __init__(self, field: str, message: str):
        super().__init__(f"Validation failed: {field} - {message}")
        self.field = field
        self.message = message

# Raise exceptions explicitly
def get_user(user_id: str) -> User:
    user = repository.find(user_id)
    if user is None:
        raise NotFoundError("User", user_id)
    return user

# Handle exceptions with try-except
try:
    user = get_user("123")
    process_user(user)
except NotFoundError as e:
    logger.warning(f"User not found: {e.id}")
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    raise

# Use context managers for resource management
with open("file.txt") as f:
    content = f.read()

# Create custom context managers
from contextlib import contextmanager

@contextmanager
def database_transaction():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
```

## Functions and Classes

```python
# Use docstrings for public APIs
def calculate_total(items: list[Item]) -> float:
    """
    Calculate the total price of items.
    
    Args:
        items: List of items to sum
        
    Returns:
        Total price including tax
        
    Raises:
        ValueError: If items list is empty
    """
    if not items:
        raise ValueError("Items list cannot be empty")
    return sum(item.price for item in items) * 1.1

# Use dataclasses for data models
from dataclasses import dataclass

@dataclass
class User:
    id: str
    name: str
    email: str

# Use slots for memory efficiency
@dataclass(slots=True)
class Point:
    x: float
    y: float

# Prefer composition over inheritance
class UserService:
    def __init__(self, repository: UserRepository, logger: Logger):
        self._repository = repository
        self._logger = logger
    
    def get_user(self, user_id: str) -> User:
        self._logger.info(f"Fetching user {user_id}")
        return self._repository.find(user_id)
```

## Async/Await

```python
import asyncio

# Use async/await for I/O-bound operations
async def fetch_user(user_id: str) -> User:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"/api/users/{user_id}") as response:
            return await response.json()

# Use asyncio.gather for parallel execution
async def fetch_user_and_orders(user_id: str):
    user, orders = await asyncio.gather(
        fetch_user(user_id),
        fetch_orders(user_id)
    )
    return {"user": user, "orders": orders}

# Use asyncio.create_task for background work
async def process_with_logging(user_id: str):
    task = asyncio.create_task(fetch_user(user_id))
    logger.info("Started fetch task")
    user = await task
    return user
```

## Project Structure

```
myapp/
  pyproject.toml        # or setup.py
  src/
    myapp/
      __init__.py
      main.py
      user/
        __init__.py
        service.py
        repository.py
        models.py
      http/
        __init__.py
        client.py
  tests/
    __init__.py
    test_user_service.py
  README.md
```

## Common Patterns

```python
# Decorators for cross-cutting concerns
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        logger.info(f"{func.__name__} took {elapsed:.2f}s")
        return result
    return wrapper

@timer
def expensive_operation():
    time.sleep(1)

# Strategy pattern with functions
def process_data(data: list[dict], strategy: str = "default"):
    strategies = {
        "default": default_processor,
        "fast": fast_processor,
        "detailed": detailed_processor,
    }
    processor = strategies.get(strategy, default_processor)
    return processor(data)

# Generator for lazy evaluation
def read_large_file(filepath: str):
    with open(filepath) as f:
        for line in f:
            yield line.strip()
```

## Code Smells to Avoid

- Bare except clauses (catch specific exceptions)
- Mutable default arguments (`def f(items=[])`)
- Using `isinstance` checks instead of polymorphism
- Deep nesting (use early returns or extract functions)
- Global variables (use dependency injection)
- Ignoring return values
- Overusing inheritance

## Testing

```python
import pytest
from unittest.mock import Mock, patch

def test_get_user_success():
    repository = Mock()
    repository.find.return_value = User(id="123", name="Alice", email="alice@example.com")
    service = UserService(repository, Mock())
    
    user = service.get_user("123")
    
    assert user.name == "Alice"

def test_get_user_not_found():
    repository = Mock()
    repository.find.return_value = None
    service = UserService(repository, Mock())
    
    with pytest.raises(NotFoundError):
        service.get_user("999")

# Use fixtures for reusable setup
@pytest.fixture
def mock_repository():
    repo = Mock()
    repo.find.return_value = User(id="123", name="Alice", email="alice@example.com")
    return repo

def test_with_fixture(mock_repository):
    service = UserService(mock_repository, Mock())
    user = service.get_user("123")
    assert user.name == "Alice"
```

## Remember

- Follow PEP 8 style guide
- Use type hints to improve code quality
- Handle errors explicitly with exceptions
- Write readable, expressive Python code
