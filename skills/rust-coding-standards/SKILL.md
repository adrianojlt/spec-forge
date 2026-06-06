---
name: rust-coding-standards
description: "Rust coding standards: ownership, error handling, traits, concurrency, and project structure."
---

# Rust Coding Standards

Standards for writing idiomatic, safe, and efficient Rust code.

**Prerequisites**: Load `/coding-principles` first for language-agnostic guidelines.

## When to Activate

- Writing or reviewing Rust code
- Designing Rust crates and modules
- Working with ownership, borrowing, or lifetimes
- Implementing error handling or concurrency patterns

## Core Principles

- Ownership and borrowing ensure memory safety
- Prefer explicit error handling with Result/Option
- Use traits for abstraction and composition
- Leverage the type system to prevent bugs
- Zero-cost abstractions without runtime overhead

## Naming

```rust
// Types: PascalCase
struct UserService;
enum OrderStatus { Pending, Shipped, Delivered }

// Functions/variables: snake_case
fn get_user_by_id(id: &str) -> Result<User, Error>
let user_count = users.len();

// Constants: SCREAMING_SNAKE_CASE
const MAX_RETRIES: u32 = 3;
const DEFAULT_TIMEOUT: Duration = Duration::from_secs(30);

// Traits: PascalCase, descriptive
trait Serializable {
    fn serialize(&self) -> Vec<u8>;
}
```

## Ownership and Borrowing

```rust
// Prefer borrowing over ownership when possible
fn process_user(user: &User) -> String {
    format!("User: {}", user.name)
}

// Use ownership when you need to take responsibility
fn consume_data(data: Vec<u8>) -> Result<(), Error> {
    // data is moved and will be dropped here
}

// Use references for read-only access
fn calculate_total(items: &[Item]) -> f64 {
    items.iter().map(|i| i.price).sum()
}

// Use mutable references for in-place modification
fn update_status(user: &mut User, status: Status) {
    user.status = status;
}

// Clone explicitly when you need owned data
fn duplicate_user(user: &User) -> User {
    user.clone()
}
```

## Error Handling

```rust
// Use Result for recoverable errors
fn read_file(path: &str) -> Result<String, io::Error> {
    fs::read_to_string(path)
}

// Use ? operator for error propagation
fn process_file(path: &str) -> Result<Data, Error> {
    let content = fs::read_to_string(path)?;
    parse_data(&content)
}

// Add context with map_err
fn get_user(id: &str) -> Result<User, Error> {
    db.find_user(id)
        .map_err(|e| Error::Database(format!("find user {}: {}", id, e)))
}

// Define custom error types
#[derive(Debug)]
enum AppError {
    NotFound(String),
    ValidationError { field: String, message: String },
    Database(String),
}

impl std::fmt::Display for AppError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            AppError::NotFound(id) => write!(f, "not found: {}", id),
            AppError::ValidationError { field, message } => {
                write!(f, "validation: {} - {}", field, message)
            }
            AppError::Database(msg) => write!(f, "database: {}", msg),
        }
    }
}

// Use Option for absence, not null
fn find_user(id: &str) -> Option<User> {
    users.get(id).cloned()
}

// Unwrap Option safely
let user = find_user("123").ok_or(AppError::NotFound("123".into()))?;
let name = user.name.as_deref().unwrap_or("unknown");
```

## Traits and Generics

```rust
// Define small, focused traits
trait Logger {
    fn info(&self, msg: &str);
    fn error(&self, msg: &str);
}

// Use trait bounds for generic functions
fn process<T: Logger>(logger: &T, data: &[u8]) {
    logger.info("processing data");
}

// Use impl Trait for simpler syntax
fn create_logger() -> impl Logger {
    ConsoleLogger::new()
}

// Use where clauses for complex bounds
fn complex_function<T, U>(t: T, u: U) -> Result<(), Error>
where
    T: Logger + Send,
    U: Iterator<Item = String>,
{
    // implementation
}
```

## Concurrency

```rust
// Use threads for CPU-bound work
use std::thread;

let handle = thread::spawn(move || {
    expensive_computation(data)
});
let result = handle.join().unwrap();

// Use channels for message passing
use std::sync::mpsc;

let (tx, rx) = mpsc::channel();
thread::spawn(move || {
    tx.send(compute_result()).unwrap();
});
let result = rx.recv().unwrap();

// Use Arc<Mutex<T>> for shared mutable state
use std::sync::{Arc, Mutex};

let counter = Arc::new(Mutex::new(0));
let counter_clone = Arc::clone(&counter);
thread::spawn(move || {
    let mut num = counter_clone.lock().unwrap();
    *num += 1;
});

// Use async/await for IO-bound work
async fn fetch_data(url: &str) -> Result<String, reqwest::Error> {
    reqwest::get(url).await?.text().await
}
```

## Project Structure

```
myapp/
  Cargo.toml
  src/
    main.rs          # Binary entry point
    lib.rs           # Library entry point
    user/
      mod.rs         # Module declaration
      service.rs
      repository.rs
      model.rs
  tests/             # Integration tests
    integration_test.rs
  benches/           # Benchmarks
    benchmark.rs
  examples/          # Usage examples
    example.rs
```

## Common Patterns

```rust
// Builder pattern
struct RequestBuilder {
    url: String,
    timeout: Option<Duration>,
}

impl RequestBuilder {
    fn new(url: String) -> Self {
        Self { url, timeout: None }
    }
    
    fn timeout(mut self, timeout: Duration) -> Self {
        self.timeout = Some(timeout);
        self
    }
    
    fn build(self) -> Request {
        Request {
            url: self.url,
            timeout: self.timeout.unwrap_or(DEFAULT_TIMEOUT),
        }
    }
}

// Type state pattern
struct Unvalidated;
struct Validated;

struct Form<State> {
    data: FormData,
    _state: std::marker::PhantomData<State>,
}

impl Form<Unvalidated> {
    fn validate(self) -> Result<Form<Validated>, ValidationError> {
        // validation logic
        Ok(Form { data: self.data, _state: PhantomData })
    }
}

impl Form<Validated> {
    fn submit(&self) -> Result<(), Error> {
        // can only submit validated forms
    }
}
```

## Code Smells to Avoid

- Unwrap/expect in library code (return Result instead)
- Excessive cloning (prefer borrowing)
- Ignoring compiler warnings (fix them)
- Using String when &str suffices
- Manual memory management (trust the borrow checker)
- Overuse of Rc/Arc (reconsider design)
- Large enums (consider splitting or using structs)

## Testing

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_calculate_total() {
        let items = vec![Item { price: 10.0 }, Item { price: 20.0 }];
        assert_eq!(calculate_total(&items), 30.0);
    }

    #[test]
    fn test_error_handling() {
        let result = process_invalid_data();
        assert!(matches!(result, Err(AppError::ValidationError { .. })));
    }
}
```

## Remember

- Leverage the type system to make invalid states unrepresentable
- Prefer explicit error handling over panics
- Use ownership to express intent and prevent bugs
- Write idiomatic Rust, not Rust translated from other languages
