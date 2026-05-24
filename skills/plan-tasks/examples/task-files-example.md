# Example: Per-File Task Output

Command run:
```
/plan-tasks i=features/user-auth/plan.md o=features/user-auth/tasks/todo/ p=user-auth
```

Result: 6 files written to `features/user-auth/tasks/todo/`:

```
features/user-auth/tasks/todo/
  user-auth-task-01.md
  user-auth-task-02.md
  user-auth-task-03.md
  user-auth-task-04.md
  user-auth-task-05.md
  user-auth-task-06.md
```

---

## user-auth-task-01.md

```markdown
# user-auth-task-01 Create users table migration

Source: features/user-auth/plan.md
Date: 2026-05-23

---

**Purpose:** Establishes the database foundation required before any auth code can run.

**Depends on:** none

**Scope notes:**
- In: write migration file, create users table with id, email, password_hash, created_at
- Not in: seeding data, modifying existing tables, application code

**Acceptance criteria:**

Given the migration has not been run
When the migration is applied to a clean test database
Then the users table exists with columns: id UUID, email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, created_at TIMESTAMPTZ NOT NULL

Given the migration has already been run
When the migration is applied again
Then no error is thrown (idempotent)

Given the migration is applied
When a duplicate email is inserted
Then the database rejects the insert with a unique constraint error

**INVEST check:**
- Independent: yes
- Negotiable: yes
- Valuable: yes - unlocks all auth development
- Estimable: yes
- Small: yes
- Testable: yes

**Done:** Migration file committed, runs clean on local and staging databases, reviewed by one engineer.
```

---

## user-auth-task-02.md

```markdown
# user-auth-task-02 Implement POST /api/auth/register endpoint

Source: features/user-auth/plan.md
Date: 2026-05-23

---

**Purpose:** Allows users to create accounts. Unlocks login and middleware testing.

**Depends on:** user-auth-task-01

**Scope notes:**
- In: validate email + password, hash password with bcrypt, insert user row, return 201
- Not in: email verification, rate limiting, invite-only logic

**Acceptance criteria:**

Given a valid email and password in request body
When POST /api/auth/register is called
Then a new user row is created and HTTP 201 is returned with no password_hash in response body

Given an email already registered
When POST /api/auth/register is called
Then HTTP 409 is returned and no new user row is created

Given an empty or missing email or password
When POST /api/auth/register is called
Then HTTP 400 is returned with a validation error message

**INVEST check:**
- Independent: yes (after user-auth-task-01)
- Negotiable: yes
- Valuable: yes
- Estimable: yes
- Small: yes
- Testable: yes

**Done:** Endpoint implemented, integration tests pass against test database, no password_hash appears in any response body.
```

---

## user-auth-task-03.md

```markdown
# user-auth-task-03 Implement POST /api/auth/login endpoint

Source: features/user-auth/plan.md
Date: 2026-05-23

---

**Purpose:** Allows registered users to obtain a JWT token for authenticated requests.

**Depends on:** user-auth-task-02

**Scope notes:**
- In: lookup user by email, verify password with bcrypt, generate 24h JWT, return token
- Not in: refresh tokens, remember-me, account lockout

**Acceptance criteria:**

Given a registered user with correct password
When POST /api/auth/login is called
Then HTTP 200 is returned with a signed JWT token that expires in 24 hours

Given a registered user with wrong password
When POST /api/auth/login is called
Then HTTP 401 is returned and the error message does not reveal whether the email exists

Given an unregistered email
When POST /api/auth/login is called
Then HTTP 401 is returned (same response as wrong password - prevents email enumeration)

**INVEST check:**
- Independent: yes (after user-auth-task-02)
- Negotiable: yes
- Valuable: yes
- Estimable: yes
- Small: yes
- Testable: yes

**Done:** Endpoint implemented, integration tests pass, login response contains only token field, JWT verified with correct secret and expiry.
```

---

## user-auth-task-04.md through user-auth-task-06.md

Follow the same format. Task 04: JWT middleware. Task 05: apply middleware to protected routes. Task 06: set JWT_SECRET in production environment.
