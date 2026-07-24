---
name: go-coding-standards
description: "Go coding standards: idioms, error handling, interfaces, concurrency, and project structure."
disable-model-invocation: true
---

**Activation:** If invoked with no code target or explicit request, reply that these standards are loaded and ask what to apply them to. Do not start reviewing or refactoring the project on your own. Apply the standards below only when writing or reviewing code at the user's request.

# Go Coding Standards

Standards for writing idiomatic, maintainable Go code.

**Prerequisites**: Load `/coding-principles` first for language-agnostic guidelines.

## When to Activate

- Writing or reviewing Go code
- Designing Go packages and modules
- Implementing error handling or concurrency patterns

## Core Principles

- Simplicity over cleverness
- Explicitness in errors and behavior
- Composition over inheritance (interfaces and embedding)
- Accept interfaces, return structs
- Handle errors explicitly, never ignore them

## Naming

```go
// Packages: lowercase, single word
package user
package httpclient

// Functions/variables: camelCase (unexported), PascalCase (exported)
func getUserByID(id string) (*User, error)
func NewService() *Service

// Receivers: short, consistent, never self/this
func (u *User) Validate() error
func (c *Client) Do(req *Request) (*Response, error)

// Interfaces: -er suffix for single-method
type Reader interface {
    Read(p []byte) (n int, err error)
}

// Constants: PascalCase (exported), camelCase (unexported)
const MaxRetries = 3
const defaultTimeout = 30 * time.Second
```

## Error Handling

```go
// Return errors explicitly, wrap with context using %w
func (s *Service) GetUser(id string) (*User, error) {
    user, err := s.repo.FindByID(id)
    if err != nil {
        return nil, fmt.Errorf("get user %s: %w", id, err)
    }
    return user, nil
}

// Check errors immediately after the call
result, err := doSomething()
if err != nil {
    return fmt.Errorf("do something: %w", err)
}

// Define sentinel errors for known conditions
var ErrNotFound = errors.New("not found")

// Use custom error types for rich context
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation: %s - %s", e.Field, e.Message)
}

// Check with errors.Is and errors.As
if errors.Is(err, ErrNotFound) { }
var valErr *ValidationError
if errors.As(err, &valErr) { }
```

## Interfaces

```go
// Keep interfaces small and composable
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }
type ReadWriter interface { Reader; Writer }

// Define interfaces where they're used, not where they're implemented
package user
type Logger interface {
    Info(msg string, args ...any)
}
type Service struct { logger Logger }
```

## Concurrency

```go
// Use channels for communication
func processItems(items []Item) <-chan Result {
    results := make(chan Result)
    go func() {
        defer close(results)
        for _, item := range items {
            results <- process(item)
        }
    }()
    return results
}

// Use sync.WaitGroup for waiting on multiple goroutines
var wg sync.WaitGroup
for i, item := range items {
    wg.Add(1)
    go func(idx int, it Item) {
        defer wg.Done()
        results[idx] = process(it)
    }(i, item)
}
wg.Wait()

// Protect shared state with mutexes
type Counter struct {
    mu    sync.Mutex
    value int
}
func (c *Counter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.value++
}

// Use context for cancellation (first parameter)
func fetchData(ctx context.Context, url string) ([]byte, error) {
    req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
    return http.DefaultClient.Do(req)
}
```

## Project Structure

```
myapp/
  go.mod
  main.go              # or cmd/myapp/main.go
  internal/            # Private application code
    user/
      service.go
      repository.go
  pkg/                 # Public library code (optional)
  api/                 # API definitions
  configs/
```

Group by feature, not by type. One package per directory, package name matches directory.

## Common Patterns

```go
// Functional options for flexible configuration
type Option func(*Server)
func WithPort(port int) Option {
    return func(s *Server) { s.port = port }
}
func NewServer(opts ...Option) *Server {
    s := &Server{port: 8080}
    for _, opt := range opts { opt(s) }
    return s
}

// Table-driven tests
func TestCalculate(t *testing.T) {
    tests := []struct {
        name     string
        input    int
        expected int
    }{
        {"zero", 0, 0},
        {"positive", 5, 10},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if got := calculate(tt.input); got != tt.expected {
                t.Errorf("got %d, want %d", got, tt.expected)
            }
        })
    }
}
```

## Code Smells to Avoid

- Ignoring errors (always check returned errors)
- Naked returns (use explicit returns in longer functions)
- Init function abuse (prefer explicit initialization)
- Interface pollution (don't create interfaces until needed)
- Goroutine leaks (ensure goroutines can exit)
- Package-level variables (prefer dependency injection)
- Oversized interfaces (split into smaller ones)

## Formatting

- Run `gofmt` or `goimports` on all code
- Use 4 spaces for indentation
- Group related declarations
- Order imports: stdlib, external, local
