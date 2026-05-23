# BACKLOG: User Authentication via Email + Password

Source: features/auth/plan.md
Date: 2026-05-23
Total tasks: 6

---

## AUTH-001 Create users table migration

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

---

## AUTH-002 Implement POST /api/auth/register endpoint

**Purpose:** Allows users to create accounts. Unlocks login and middleware testing.

**Depends on:** AUTH-001

**Scope notes:**
- In: validate email + password, hash password with bcrypt, insert user row, return 201
- Not in: email verification, rate limiting, invite-only logic (separate tasks if needed)

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
- Independent: yes (after AUTH-001)
- Negotiable: yes
- Valuable: yes
- Estimable: yes
- Small: yes
- Testable: yes

**Done:** Endpoint implemented, integration tests pass against test database, no password_hash appears in any response body.

---

## AUTH-003 Implement POST /api/auth/login endpoint

**Purpose:** Allows registered users to obtain a JWT token for authenticated requests.

**Depends on:** AUTH-002

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
- Independent: yes (after AUTH-002)
- Negotiable: yes
- Valuable: yes
- Estimable: yes
- Small: yes
- Testable: yes

**Done:** Endpoint implemented, integration tests pass, login response body contains only token field, JWT verified with correct secret and expiry in tests.

---

## AUTH-004 Implement JWT validation middleware

**Purpose:** Validates JWT on incoming requests. Enables route protection in AUTH-005.

**Depends on:** AUTH-003

**Scope notes:**
- In: parse Authorization header, verify JWT signature and expiry, attach user to request object
- Not in: applying middleware to routes (that is AUTH-005), role-based access control

**Acceptance criteria:**

Given a valid unexpired JWT in Authorization header
When the middleware runs
Then request passes through with user object attached to req.user

Given an expired JWT
When the middleware runs
Then HTTP 401 is returned with message indicating token expired

Given no Authorization header
When the middleware runs
Then HTTP 401 is returned

**INVEST check:**
- Independent: yes (after AUTH-003)
- Negotiable: yes
- Valuable: yes
- Estimable: yes
- Small: yes
- Testable: yes

**Done:** Middleware unit tested with valid, expired, and missing tokens. Does not depend on database (stateless JWT validation only).

---

## AUTH-005 Apply middleware to all protected routes

**Purpose:** Protects all non-public routes. Completes the authentication feature.

**Depends on:** AUTH-004

**Scope notes:**
- In: apply middleware to all routes listed in protected-routes.md, regression test public routes
- Not in: modifying route handlers, adding new routes

**Acceptance criteria:**

Given a request to a protected route with no token
When the request is made
Then HTTP 401 is returned

Given a request to a protected route with a valid token
When the request is made
Then the route handles the request normally

Given a request to a public route (health check, register, login)
When the request is made without a token
Then the route handles the request normally (no 401)

**INVEST check:**
- Independent: yes (after AUTH-004)
- Negotiable: yes
- Valuable: yes - completes feature
- Estimable: yes
- Small: yes
- Testable: yes

**Done:** All protected routes return 401 without token, all public routes pass without token, full regression suite passes.

---

## AUTH-006 Set JWT_SECRET in production environment

**Purpose:** Ops prerequisite for AUTH-005 to function in production.

**Depends on:** AUTH-003 (to know variable name and format)

**Scope notes:**
- In: generate secret, set JWT_SECRET in production environment config
- Not in: code changes, deployment automation changes

**Acceptance criteria:**

Given JWT_SECRET is set in the production environment
When the auth service starts
Then no "missing JWT_SECRET" error appears in startup logs

Given JWT_SECRET is set
When a token is generated via login and then used on a protected route
Then the request succeeds with HTTP 200

**INVEST check:**
- Independent: yes (can run in parallel with AUTH-004 and AUTH-005)
- Negotiable: yes
- Valuable: yes - production blocker
- Estimable: yes
- Small: yes
- Testable: yes

**Done:** JWT_SECRET confirmed set in production environment. Login + protected-route flow verified end-to-end in staging.
