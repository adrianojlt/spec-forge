---
name: typescript-coding-standards
description: "TypeScript coding standards: types, interfaces, error handling, async patterns, and project structure."
---

# TypeScript Coding Standards

Standards for writing type-safe, maintainable TypeScript code.

**Prerequisites**: Load `/coding-principles` first for language-agnostic guidelines.

## When to Activate

- Writing or reviewing TypeScript code
- Designing TypeScript modules and APIs
- Working with complex types or generics
- Building Node.js applications or frontend frameworks

## Core Principles

- Leverage the type system to catch errors at compile time
- Prefer explicit types over `any`
- Use interfaces for object shapes, types for unions/intersections
- Handle errors explicitly, don't ignore promises
- Write expressive code with clear intent

## Naming

```typescript
// Types/Interfaces: PascalCase
interface User { id: string; name: string }
type OrderStatus = 'pending' | 'shipped' | 'delivered'

// Functions/variables: camelCase
function getUserById(id: string): Promise<User>
const userCount = users.length

// Constants: SCREAMING_SNAKE_CASE or camelCase
const MAX_RETRIES = 3
const defaultTimeout = 30000

// Classes: PascalCase
class UserService { }

// Enums: PascalCase for name, PascalCase for members
enum Color { Red, Green, Blue }
```

## Types and Interfaces

```typescript
// Use interfaces for object shapes
interface User {
  id: string
  name: string
  email: string
}

// Use types for unions, intersections, primitives
type ID = string | number
type UserWithOrders = User & { orders: Order[] }
type Status = 'active' | 'inactive' | 'pending'

// Prefer interfaces for extensibility
interface Logger {
  info(message: string): void
  error(message: string): void
}

// Use type aliases for complex types
type Handler<T> = (data: T) => Promise<void>

// Avoid any, use unknown for truly unknown values
function process(data: unknown): void {
  if (typeof data === 'string') {
    console.log(data.toUpperCase())
  }
}

// Use readonly for immutable properties
interface Config {
  readonly apiKey: string
  readonly timeout: number
}

// Use optional properties for optional fields
interface CreateUserRequest {
  name: string
  email: string
  age?: number
}
```

## Generics

```typescript
// Use generics for reusable functions
function identity<T>(value: T): T {
  return value
}

// Constrain generics with extends
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key]
}

// Use generics for collections
interface Repository<T> {
  findById(id: string): Promise<T | null>
  findAll(): Promise<T[]>
  save(entity: T): Promise<T>
}

// Use generic constraints for complex types
function merge<T extends object, U extends object>(a: T, b: U): T & U {
  return { ...a, ...b }
}
```

## Error Handling

```typescript
// Define custom error classes
class NotFoundError extends Error {
  constructor(public readonly id: string) {
    super(`Not found: ${id}`)
    this.name = 'NotFoundError'
  }
}

class ValidationError extends Error {
  constructor(
    public readonly field: string,
    public readonly message: string
  ) {
    super(`Validation failed: ${field} - ${message}`)
    this.name = 'ValidationError'
  }
}

// Throw errors explicitly
async function getUser(id: string): Promise<User> {
  const user = await repository.findById(id)
  if (!user) {
    throw new NotFoundError(id)
  }
  return user
}

// Handle errors with try-catch
try {
  const user = await getUser('123')
  processUser(user)
} catch (error) {
  if (error instanceof NotFoundError) {
    console.log(`User ${error.id} not found`)
  } else {
    console.error('Unexpected error:', error)
  }
}

// Use Result types for explicit error handling
type Result<T, E = Error> = 
  | { success: true; value: T }
  | { success: false; error: E }

function divide(a: number, b: number): Result<number, string> {
  if (b === 0) {
    return { success: false, error: 'Division by zero' }
  }
  return { success: true, value: a / b }
}
```

## Async/Await

```typescript
// Use async/await for asynchronous operations
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`)
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`)
  }
  return response.json()
}

// Use Promise.all for parallel execution
async function fetchUserAndOrders(userId: string) {
  const [user, orders] = await Promise.all([
    fetchUser(userId),
    fetchOrders(userId)
  ])
  return { user, orders }
}

// Handle errors in async functions
async function safeFetchUser(id: string): Promise<User | null> {
  try {
    return await fetchUser(id)
  } catch (error) {
    console.error('Failed to fetch user:', error)
    return null
  }
}

// Always handle promise rejections
fetchUser('123')
  .then(user => processUser(user))
  .catch(error => console.error('Error:', error))
```

## Project Structure

```
myapp/
  package.json
  tsconfig.json
  src/
    index.ts
    user/
      user.service.ts
      user.repository.ts
      user.types.ts
      index.ts
    http/
      client.ts
      middleware.ts
  tests/
    user.service.test.ts
  dist/                 # Compiled output
```

## Common Patterns

```typescript
// Discriminated unions for state
type State =
  | { status: 'loading' }
  | { status: 'success'; data: User }
  | { status: 'error'; error: Error }

function handleState(state: State) {
  switch (state.status) {
    case 'loading':
      console.log('Loading...')
      break
    case 'success':
      console.log('User:', state.data.name)
      break
    case 'error':
      console.error('Error:', state.error.message)
      break
  }
}

// Builder pattern
class RequestBuilder {
  private url: string = ''
  private method: string = 'GET'
  private headers: Record<string, string> = {}

  setUrl(url: string): this {
    this.url = url
    return this
  }

  setMethod(method: string): this {
    this.method = method
    return this
  }

  addHeader(key: string, value: string): this {
    this.headers[key] = value
    return this
  }

  build(): Request {
    return new Request(this.url, {
      method: this.method,
      headers: this.headers
    })
  }
}

// Dependency injection
class UserService {
  constructor(
    private readonly repository: UserRepository,
    private readonly logger: Logger
  ) {}

  async getUser(id: string): Promise<User> {
    this.logger.info(`Fetching user ${id}`)
    return this.repository.findById(id)
  }
}
```

## Code Smells to Avoid

- Using `any` (use `unknown` or proper types)
- Non-null assertions (`!`) without validation
- Ignoring promise rejections
- Type assertions (`as`) to bypass type checking
- Mutable shared state
- Large interfaces (split into smaller ones)
- Deep nesting (use early returns)

## Testing

```typescript
import { describe, it, expect, vi } from 'vitest'

describe('UserService', () => {
  it('should return user when found', async () => {
    const repository = {
      findById: vi.fn().mockResolvedValue({ id: '123', name: 'Alice' })
    }
    const service = new UserService(repository, mockLogger)

    const user = await service.getUser('123')

    expect(user.name).toBe('Alice')
  })

  it('should throw NotFoundError when user not found', async () => {
    const repository = {
      findById: vi.fn().mockResolvedValue(null)
    }
    const service = new UserService(repository, mockLogger)

    await expect(service.getUser('999')).rejects.toThrow(NotFoundError)
  })
})
```

## Remember

- Leverage TypeScript's type system to catch errors early
- Prefer explicit types and avoid `any`
- Handle errors and promise rejections explicitly
- Write expressive code with clear intent
