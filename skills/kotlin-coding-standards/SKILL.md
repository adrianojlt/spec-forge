---
name: kotlin-coding-standards
description: "Kotlin coding standards: null safety, coroutines, data classes, and project structure."
---

# Kotlin Coding Standards

Standards for writing idiomatic, concise, and safe Kotlin code.

**Prerequisites**: Load `/coding-principles` first for language-agnostic guidelines.

## When to Activate

- Writing or reviewing Kotlin code
- Designing Kotlin modules and APIs
- Working with null safety, coroutines, or sealed classes
- Building Android apps, backend services, or multiplatform projects

## Core Principles

- Null safety is enforced by the type system
- Prefer immutable data and expressions
- Use coroutines for asynchronous programming
- Leverage Kotlin's concise syntax (data classes, extension functions)
- Write expressive code with minimal boilerplate

## Naming

```kotlin
// Classes/Objects: PascalCase
class UserService
object AppConfig

// Functions/properties: camelCase
fun getUserById(id: String): User?
val userCount = users.size

// Constants: SCREAMING_SNAKE_CASE (top-level or companion object)
const val MAX_RETRIES = 3
const val DEFAULT_TIMEOUT = 30L

// Packages: lowercase, no underscores
package com.example.user
```

## Null Safety

```kotlin
// Use nullable types explicitly
var user: User? = findUser("123")

// Safe calls with ?.
val name = user?.name

// Elvis operator for defaults
val displayName = user?.name ?: "Unknown"

// Safe casts with as?
val string: String? = obj as? String

// Use let for null checks
user?.let { 
    processUser(it)
}

// Use require/check for validation
fun createUser(name: String) {
    require(name.isNotBlank()) { "Name cannot be blank" }
    // ...
}

// Avoid !! (non-null assertion) in production code
val definitelyNotNull = nullable!! // Use only when absolutely certain
```

## Data Classes and Sealed Classes

```kotlin
// Use data classes for immutable data
data class User(
    val id: String,
    val name: String,
    val email: String
)

// Use sealed classes for restricted hierarchies
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val message: String) : Result<Nothing>()
    object Loading : Result<Nothing>()
}

// Use when expressions with sealed classes
fun handleResult(result: Result<User>) = when (result) {
    is Result.Success -> processUser(result.data)
    is Result.Error -> showError(result.message)
    Result.Loading -> showLoading()
}

// Use enums for simple constants
enum class Status { PENDING, ACTIVE, COMPLETED }
```

## Functions and Extension Functions

```kotlin
// Use expression bodies for simple functions
fun double(x: Int) = x * 2

// Use default parameters instead overloading
fun connect(timeout: Int = 30, retries: Int = 3) {
    // ...
}

// Use named arguments for clarity
connect(timeout = 60, retries = 5)

// Extension functions for adding behavior
fun String.isValidEmail(): Boolean = 
    matches(Regex("^[A-Za-z0-9+_.-]+@(.+)$"))

fun User.displayName(): String = 
    "$name ($email)"

// Use scope functions appropriately
user?.let { processUser(it) }           // Execute if not null
user?.apply { name = "New Name" }       // Configure and return
user?.run { validate() }                // Execute and return result
user?.also { logger.info("User: $it") } // Side effects

// Use inline functions for performance (with lambdas)
inline fun <T> measureTime(block: () -> T): Pair<T, Long> {
    val start = System.currentTimeMillis()
    val result = block()
    val elapsed = System.currentTimeMillis() - start
    return result to elapsed
}
```

## Error Handling

```kotlin
// Use Result type for explicit error handling
sealed class AppResult<out T> {
    data class Success<T>(val data: T) : AppResult<T>()
    data class Failure(val error: Throwable) : AppResult<Nothing>()
}

// Use runCatching for safe execution
val result = runCatching { riskyOperation() }
result.onSuccess { process(it) }
      .onFailure { logger.error("Failed", it) }

// Throw exceptions for unrecoverable errors
class NotFoundException(resource: String, id: String) : 
    RuntimeException("$resource not found: $id")

fun getUser(id: String): User = 
    repository.find(id) ?: throw NotFoundException("User", id)

// Use try-catch for specific exceptions
try {
    val user = getUser("123")
    processUser(user)
} catch (e: NotFoundException) {
    logger.warn("User not found: ${e.message}")
} catch (e: Exception) {
    logger.error("Unexpected error", e)
    throw e
}
```

## Coroutines

```kotlin
import kotlinx.coroutines.*

// Use suspend functions for async operations
suspend fun fetchUser(id: String): User {
    return apiClient.getUser(id)
}

// Use coroutineScope for structured concurrency
suspend fun fetchUserAndOrders(userId: String) = coroutineScope {
    val user = async { fetchUser(userId) }
    val orders = async { fetchOrders(userId) }
    Pair(user.await(), orders.await())
}

// Use withContext for context switching
suspend fun readFile(path: String): String = withContext(Dispatchers.IO) {
    File(path).readText()
}

// Use Flow for streams of data
fun observeUsers(): Flow<User> = flow {
    while (true) {
        emit(fetchLatestUsers())
        delay(1000)
    }
}

// Handle errors in coroutines
suspend fun safeFetchUser(id: String): User? = try {
    fetchUser(id)
} catch (e: Exception) {
    logger.error("Failed to fetch user", e)
    null
}
```

## Project Structure

```
myapp/
  build.gradle.kts
  src/
    main/
      kotlin/
        com/example/myapp/
          Main.kt
          user/
            UserService.kt
            UserRepository.kt
            User.kt
          http/
            ApiClient.kt
    test/
      kotlin/
        com/example/myapp/
          UserServiceTest.kt
```

## Common Patterns

```kotlin
// Builder pattern with DSL
class RequestBuilder {
    var url: String = ""
    var method: String = "GET"
    private val headers = mutableMapOf<String, String>()
    
    fun header(key: String, value: String) {
        headers[key] = value
    }
    
    fun build() = Request(url, method, headers.toMap())
}

fun request(block: RequestBuilder.() -> Unit): Request {
    return RequestBuilder().apply(block).build()
}

// Usage
val req = request {
    url = "https://api.example.com"
    method = "POST"
    header("Authorization", "Bearer token")
}

// Dependency injection
class UserService(
    private val repository: UserRepository,
    private val logger: Logger
) {
    suspend fun getUser(id: String): User {
        logger.info("Fetching user $id")
        return repository.find(id) ?: throw NotFoundException("User", id)
    }
}
```

## Code Smells to Avoid

- Using !! (non-null assertion) unnecessarily
- Ignoring coroutine cancellation
- Using var when val suffices
- Deep nesting (use early returns or when expressions)
- Overusing inheritance (prefer composition)
- Mutable shared state (use coroutines or synchronization)
- Large data classes (split into smaller ones)

## Testing

```kotlin
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.assertThrows
import io.mockk.*

class UserServiceTest {
    @Test
    fun `should return user when found`() {
        val repository = mockk<UserRepository>()
        every { repository.find("123") } returns User("123", "Alice", "alice@example.com")
        val service = UserService(repository, mockk())
        
        val user = service.getUser("123")
        
        assert(user.name == "Alice")
    }
    
    @Test
    fun `should throw NotFoundException when user not found`() {
        val repository = mockk<UserRepository>()
        every { repository.find("999") } returns null
        val service = UserService(repository, mockk())
        
        assertThrows<NotFoundException> {
            service.getUser("999")
        }
    }
}
```

## Remember

- Leverage Kotlin's null safety to prevent NPEs
- Prefer immutable data and expressions
- Use coroutines for asynchronous programming
- Write concise, expressive Kotlin code
