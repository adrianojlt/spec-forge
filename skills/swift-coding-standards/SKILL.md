---
name: swift-coding-standards
description: "Swift coding standards: optionals, error handling, protocols, concurrency, and project structure."
disable-model-invocation: true
---

**Activation:** If invoked with no code target or explicit request, reply that these standards are loaded and ask what to apply them to. Do not start reviewing or refactoring the project on your own. Apply the standards below only when writing or reviewing code at the user's request.

# Swift Coding Standards

Standards for writing idiomatic, safe, and expressive Swift code.

**Prerequisites**: Load `/coding-principles` first for language-agnostic guidelines.

## When to Activate

- Writing or reviewing Swift code
- Designing Swift modules and frameworks
- Working with optionals, protocols, or concurrency
- Building iOS/macOS applications or server-side Swift

## Core Principles

- Safety first: leverage the type system to prevent bugs
- Prefer value types (structs) over reference types (classes)
- Use optionals to represent absence explicitly
- Handle errors with do-catch or Result types
- Write expressive, readable code with clear intent

## Naming

```swift
// Types: PascalCase
struct UserService { }
enum OrderStatus { case pending, shipped, delivered }

// Functions/variables: camelCase
func getUser(byID id: String) throws -> User
let userCount = users.count

// Constants: camelCase (not SCREAMING_SNAKE_CASE)
let maxRetries = 3
let defaultTimeout: TimeInterval = 30

// Protocols: PascalCase, descriptive
protocol Serializable {
    func serialize() -> Data
}
```

## Optionals

```swift
// Use optionals to represent absence
var user: User? = findUser(id: "123")

// Unwrap safely with if let or guard let
if let user = user {
    print(user.name)
}

// Use guard for early exit
guard let user = user else {
    throw UserError.notFound
}

// Use optional chaining for concise access
let street = user?.address?.street

// Provide defaults with nil-coalescing
let name = user?.name ?? "Unknown"

// Force unwrap only when you're certain (avoid in production)
let definitelyExists = optional!
```

## Error Handling

```swift
// Define custom error types
enum UserError: Error {
    case notFound(id: String)
    case validationFailed(field: String, message: String)
    case networkError(underlying: Error)
}

// Throw errors explicitly
func getUser(id: String) throws -> User {
    guard let user = repository.find(id: id) else {
        throw UserError.notFound(id: id)
    }
    return user
}

// Handle errors with do-catch
do {
    let user = try getUser(id: "123")
    process(user)
} catch UserError.notFound(let id) {
    print("User \(id) not found")
} catch {
    print("Unexpected error: \(error)")
}

// Use Result for asynchronous operations
func fetchData(completion: @escaping (Result<Data, Error>) -> Void) {
    // implementation
}

// Convert throwing functions to Result
let result = Result { try riskyOperation() }
```

## Protocols and Extensions

```swift
// Define small, focused protocols
protocol Logger {
    func info(_ message: String)
    func error(_ message: String)
}

// Use protocol extensions for default implementations
extension Logger {
    func info(_ message: String) {
        print("[INFO] \(message)")
    }
}

// Use protocol-oriented programming
protocol Identifiable {
    var id: String { get }
}

extension Array where Element: Identifiable {
    func find(byID id: String) -> Element? {
        first { $0.id == id }
    }
}

// Prefer composition over inheritance
protocol Nameable { var name: String { get } }
protocol Ageable { var age: Int { get } }

struct Person: Nameable, Ageable {
    let name: String
    let age: Int
}
```

## Value Types vs Reference Types

```swift
// Prefer structs for data models
struct User {
    let id: String
    var name: String
    var email: String
}

// Use classes when you need reference semantics
class UserService {
    private let repository: UserRepository
    
    init(repository: UserRepository) {
        self.repository = repository
    }
    
    func getUser(id: String) throws -> User {
        try repository.find(id: id)
    }
}

// Use structs with mutating methods
struct Counter {
    private var count = 0
    
    mutating func increment() {
        count += 1
    }
}
```

## Concurrency (Swift 5.5+)

```swift
// Use async/await for asynchronous operations
func fetchUser(id: String) async throws -> User {
    let data = try await apiClient.get("/users/\(id)")
    return try JSONDecoder().decode(User.self, from: data)
}

// Use async let for parallel execution
async func fetchUserAndOrders(userID: String) async throws -> (User, [Order]) {
    async let user = fetchUser(id: userID)
    async let orders = fetchOrders(userID: userID)
    return try await (user, orders)
}

// Use Task for detached work
Task {
    let result = await expensiveComputation()
    await MainActor.run {
        updateUI(with: result)
    }
}

// Use actors for shared mutable state
actor Counter {
    private var count = 0
    
    func increment() {
        count += 1
    }
    
    func value() -> Int {
        count
    }
}

// Access actor properties safely
let counter = Counter()
await counter.increment()
let value = await counter.value()
```

## Project Structure

```
MyApp/
  Package.swift           # Swift Package Manager
  Sources/
    MyApp/
      main.swift
      User/
        UserService.swift
        UserRepository.swift
        User.swift
      HTTP/
        APIClient.swift
  Tests/
    MyAppTests/
      UserServiceTests.swift
```

## Common Patterns

```swift
// Result builders for DSLs
@resultBuilder
struct HTMLBuilder {
    static func buildBlock(_ components: String...) -> String {
        components.joined()
    }
}

func html(@HTMLBuilder content: () -> String) -> String {
    "<html>\(content())</html>"
}

// Property wrappers for reusable logic
@propertyWrapper
struct UserDefault<T> {
    let key: String
    let defaultValue: T
    
    var wrappedValue: T {
        get { UserDefaults.standard.object(forKey: key) as? T ?? defaultValue }
        set { UserDefaults.standard.set(newValue, forKey: key) }
    }
}

struct Settings {
    @UserDefault(key: "username", defaultValue: "Guest")
    var username: String
}
```

## Code Smells to Avoid

- Force unwrapping optionals (use if let, guard let, or ??)
- Implicitly unwrapped optionals in production code
- Using classes when structs suffice
- Ignoring errors (always handle or propagate)
- Retain cycles with closures (use [weak self] or [unowned self])
- Overusing inheritance (prefer protocols and composition)
- Large switch statements (consider strategy pattern or enums with associated values)

## Testing

```swift
import XCTest

final class UserServiceTests: XCTestCase {
    func testGetUser_Success() throws {
        let repository = MockUserRepository()
        repository.users = [User(id: "123", name: "Alice")]
        let service = UserService(repository: repository)
        
        let user = try service.getUser(id: "123")
        
        XCTAssertEqual(user.name, "Alice")
    }
    
    func testGetUser_NotFound() {
        let repository = MockUserRepository()
        let service = UserService(repository: repository)
        
        XCTAssertThrowsError(try service.getUser(id: "999")) { error in
            XCTAssertTrue(error is UserError)
        }
    }
}
```

## Remember

- Leverage Swift's type system to make invalid states unrepresentable
- Prefer value types and protocols over class hierarchies
- Handle optionals and errors explicitly
- Write expressive code that reads like natural language
