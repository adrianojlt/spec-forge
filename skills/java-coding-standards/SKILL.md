---
name: java-coding-standards
description: "Java coding standards for Spring Boot services: naming, immutability, Optional usage, streams, exceptions, generics, and project layout."
origin: ECC
---

# Java Coding Standards

Standards for readable, maintainable Java (17+) code in Spring Boot services.

**Prerequisites**: Load `/coding-principles` first for language-agnostic guidelines.

## When to Activate

- Writing or reviewing Java code in Spring Boot projects
- Enforcing naming, immutability, or exception handling conventions
- Working with records, sealed classes, or pattern matching (Java 17+)
- Reviewing use of Optional, streams, or generics
- Structuring packages and project layout

## Code Quality Principles

### 1. Readability First
- Code is read more than written
- Clear variable and function names
- Self-documenting code preferred over comments
- Consistent formatting

### 2. KISS (Keep It Simple, Stupid)
- Simplest solution that works
- Avoid over-engineering
- No premature optimization
- Easy to understand > clever code

### 3. DRY (Don't Repeat Yourself)
- Extract common logic into functions
- Create reusable components
- Share utilities across modules
- Avoid copy-paste programming

### 4. YAGNI (You Aren't Gonna Need It)
- Don't build features before they're needed
- Avoid speculative generality
- Add complexity only when required
- Start simple, refactor when needed

## Core Principles

- Prefer clarity over cleverness
- Immutable by default; minimize shared mutable state
- Fail fast with meaningful exceptions
- Consistent naming and package structure

## Code Format
```Java
// ✅ Prefer this
if (doSomething()) {
    return true;
}

// ❌ Over this
if (doSomething()) return true; 
```
```Java
// ✅ Prefer this (a Human can read this better)
@Override
public void handle(CdcEvent event) {

    if (!"partners".equals(event.collection())) {
        return;
    }

    if ("DELETE".equals(event.operation())) {
        mongoTemplate.remove(
                Query.query(Criteria.where("_id").is(HandlerUtils.parseId(event.documentId()))),
                Document.class, COLLECTION);
        return;
    }

    if (event.after() == null) {
        return;
    }

    Document data = Document.parse(event.after());
    Document resolved = resolveFields(data);

    resolved.put("_id", HandlerUtils.parseId(event.documentId()));

    mongoTemplate.save(resolved, COLLECTION);
}

// ❌ Over this
@Override
public void handle(CdcEvent event) {
    if (!"partners".equals(event.collection())) {
        return;
    }
    if ("DELETE".equals(event.operation())) {
        mongoTemplate.remove(
                Query.query(Criteria.where("_id").is(HandlerUtils.parseId(event.documentId()))),
                Document.class, COLLECTION);
        return;
    }
    if (event.after() == null) {
        return;
    }
    Document data = Document.parse(event.after());
    Document resolved = resolveFields(data);
    resolved.put("_id", HandlerUtils.parseId(event.documentId()));
    mongoTemplate.save(resolved, COLLECTION);
}
```
```Java
// ✅ Prefer this (a Human can read this better)
private final DataSourceManager dataSourceManager;
private final LLMProviderService llmProviderService;
private final DatabaseMetadataService metadataService;
private final NaturalLanguageService naturalLanguageService;
private final DatabaseConfigRepository databaseConfigRepository;
private final LLMProviderConfigRepository llmProviderConfigRepository;
```
```Java
// ❌ Over this
private final DatabaseConfigRepository databaseConfigRepository;
private final LLMProviderConfigRepository llmProviderConfigRepository;
private final DataSourceManager dataSourceManager;
private final NaturalLanguageService naturalLanguageService;
private final LLMProviderService llmProviderService;
private final DatabaseMetadataService metadataService;
```
### Magic Strings → Enums or Constants

Never use raw string literals for values that:
- Represent a fixed domain concept (table names, collection names, operation types, FK field names)
- Appear in more than one place
- Could cause a typo that the compiler cannot catch

### Table / Collection Names
Always use an enum when switching or comparing against a fixed set of string-based domain values.
```Java
public enum AggregateTable {
    BOOKINGS("bookings"),
    PRODUCTS("products"),
    PAYMENTS("payments");
    // ...

    private final String name;

    AggregateTable(String name) { this.name = name; }

    public String collectionName() { return name; }

    public String rawCollectionName() { return "raw_" + name; }
}
```

### String literals
Never use the string literal inline if the same string is used in more than one place, always reference the constant. ex:
```Java
private static final String FK_PRODUCT    = "fk_product";
private static final String FK_BOOKING    = "fk_booking";
private static final String FK_BOOKING_ID = "fk_booking_id";
private static final String FK_PAYMENT_ID = "fk_payment_id";
```
If the same string is used in more than one Class, use a enum.



## Naming

```java
// ✅ Classes/Records: PascalCase
public class MarketService {}
public record Money(BigDecimal amount, Currency currency) {}

// ✅ Methods/fields: camelCase
private final MarketRepository marketRepository;
public Market findBySlug(String slug) {}

// ✅ Constants: UPPER_SNAKE_CASE
private static final int MAX_PAGE_SIZE = 100;
```

## Immutability

```java
// ✅ Favor records and final fields
public record MarketDto(Long id, String name, MarketStatus status) {}

public class Market {
  private final Long id;
  private final String name;
  // getters only, no setters
}
```

## Optional Usage

```java
// ✅ Return Optional from find* methods
Optional<Market> market = marketRepository.findBySlug(slug);

// ✅ Map/flatMap instead of get()
return market
    .map(MarketResponse::from)
    .orElseThrow(() -> new EntityNotFoundException("Market not found"));
```

## Streams Best Practices

```java
// ✅ Use streams for transformations, keep pipelines short
List<String> names = markets.stream()
    .map(Market::name)
    .filter(Objects::nonNull)
    .toList();

// ❌ Avoid complex nested streams; prefer loops for clarity
```

## Exceptions

- Use unchecked exceptions for domain errors; wrap technical exceptions with context
- Create domain-specific exceptions (e.g., `MarketNotFoundException`)
- Avoid broad `catch (Exception ex)` unless rethrowing/logging centrally

```java
throw new MarketNotFoundException(slug);
```

## Generics and Type Safety

- Avoid raw types; declare generic parameters
- Prefer bounded generics for reusable utilities

```java
public <T extends Identifiable> Map<Long, T> indexById(Collection<T> items) { ... }
```

## Project Structure (Maven/Gradle)

```
src/main/java/com/example/app/
  config/
  controller/
  service/
  repository/
  domain/
  dto/
  util/
src/main/resources/
  application.yml
src/test/java/... (mirrors main)
```

## Formatting and Style

- Use 2 or 4 spaces consistently (project standard)
- One public top-level type per file
- Keep methods short and focused; extract helpers
- Order members: constants, fields, constructors, public methods, protected, private

## Code Smells to Avoid

- Long parameter lists → use DTO/builders
- Deep nesting → early returns
- Magic numbers → named constants
- Static mutable state → prefer dependency injection
- Silent catch blocks → log and act or rethrow

## Logging

```java
private static final Logger log = LoggerFactory.getLogger(MarketService.class);
log.info("fetch_market slug={}", slug);
log.error("failed_fetch_market slug={}", slug, ex);
```

## Null Handling

- Accept `@Nullable` only when unavoidable; otherwise use `@NonNull`
- Use Bean Validation (`@NotNull`, `@NotBlank`) on inputs

## Testing Expectations

- JUnit 5 + AssertJ for fluent assertions
- Mockito for mocking; avoid partial mocks where possible
- Favor deterministic tests; no hidden sleeps

**Remember**: Keep code intentional, typed, and observable. Optimize for maintainability over micro-optimizations unless proven necessary.