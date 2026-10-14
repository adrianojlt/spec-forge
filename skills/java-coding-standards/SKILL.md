---
name: java-coding-standards
description: "Java coding standards for Spring Boot services: naming, immutability, Optional usage, streams, exceptions, generics, and project layout."
origin: ECC
---

# Java Coding Standards

Java 17+ in Spring Boot services. Builds on `coding-principles`; only what is specific to Java or to this codebase's taste is listed here.

## Layout for human readers
- Always use braces, even for one-line `if` bodies.
- Inside a method, separate logical steps (guard, branch, transform, persist) with a blank line.
- Order injected `private final` fields by line length, shortest first.
- A constructor or method call with more than three arguments, or one that would not fit on a line, puts one argument per line.

```java
@Override
public void handle(CdcEvent event) {

    if (!"partners".equals(event.collection())) {
        return;
    }

    if (event.after() == null) {
        return;
    }

    Document resolved = resolveFields(Document.parse(event.after()));

    mongoTemplate.save(resolved, COLLECTION);
}
```

## No magic strings
- A string that names a fixed domain concept (table or collection name, operation type, FK field) or appears more than once is a `private static final` constant.
- When the same set of values is used across classes, or is switched on, it is an enum:

```java
public enum AggregateTable {
    BOOKINGS("bookings"),
    PAYMENTS("payments");

    private final String name;

    AggregateTable(String name) { this.name = name; }

    public String collectionName() { return name; }
}
```

## Types and nulls
- Records for DTOs and value objects; `final` fields and no setters on other classes.
- `Optional` only as a return type (`find*` methods). Never as a field or parameter; never `get()` without a check, prefer `map` / `orElseThrow`.
- Bean Validation (`@NotNull`, `@NotBlank`) on inbound DTOs.
- Streams for short transformations; a loop when the pipeline needs nesting or side effects.

## Errors and logging
- Unchecked, domain-specific exceptions (`MarketNotFoundException`). Wrap technical exceptions with context; no `catch (Exception e)` outside a central handler.
- SLF4J with snake_case event names and key=value pairs: `log.info("fetch_market slug={}", slug)`; pass the exception as the last argument.

## Spring
- Constructor injection only; no field injection, no static mutable state.

## Tests
- JUnit 5, AssertJ, Mockito. No partial mocks, no `Thread.sleep`.
