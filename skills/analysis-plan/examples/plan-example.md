# Plan: User Authentication via Email + Password

Source: features/auth/analysis.md
Date: 2026-05-23
Status: Ready

---

## Approach Summary

Add email/password authentication to the Express.js API using JWT tokens and bcrypt for password hashing. Work is split into three sequential slices: database foundation, auth endpoints, and middleware protection. Each slice is independently testable and mergeable.

## Scope Slices

### Slice 1: Database foundation
Create the `users` table and migration. Confirm schema compatibility with existing tables.
- Depends on: nothing
- Delivers: `users` table in PostgreSQL with email (unique), password_hash, created_at

### Slice 2: Auth endpoints
Implement `/register` and `/login` endpoints. No middleware yet.
- Depends on: Slice 1
- Delivers: POST /register returns 201, POST /login returns JWT token on valid credentials

### Slice 3: Middleware and protection
Implement JWT validation middleware. Apply to all protected routes.
- Depends on: Slice 2
- Delivers: Protected routes reject requests without valid JWT; existing unprotected routes unchanged

## Sequence

1. Slice 1 (Database) - must exist before any code can read or write users
2. Slice 2 (Auth endpoints) - can be developed and tested against real DB
3. Slice 3 (Middleware) - requires valid JWT generation from Slice 2

## Dependencies

- PostgreSQL write access required (Slice 1 blocker).
- JWT_SECRET environment variable must be set in deployment before Slice 3 ships.
- Existing route list needed to know which routes to protect (needed for Slice 3).

## Data Model Impact

- New table: `users` (id UUID, email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, created_at TIMESTAMPTZ)
- Migration required: yes, new table only, no changes to existing tables
- Rollback: drop table (safe, no existing data)

## API Impact

- New: POST /api/auth/register - creates user, returns 201
- New: POST /api/auth/login - validates credentials, returns { token }
- Changed: all protected routes - now require Authorization: Bearer <token> header
- Unchanged: public routes (health check, etc.)

## UI Impact

- None. UI is out of scope for this feature.

## Testing Strategy

- Slice 1: run migration on test DB, verify schema with describe command
- Slice 2: integration tests hitting real test DB (not mocks) - register, login, duplicate email, wrong password
- Slice 3: integration tests - request with valid token, expired token, no token, malformed token
- Manual: verify existing public endpoints still work after middleware is applied

## Risks

- JWT secret not in deployment environment yet (must be resolved before Slice 3 ships).
- Rate limiting absent - brute-force attack possible on /login (accepted for beta, post-launch task).
- Migration failure on production DB could block launch (mitigate: test migration on staging first).

## Rollout / Review Gates

- Gate 1 (before Slice 2): migration reviewed by one other engineer, run successfully on staging
- Gate 2 (before Slice 3): auth endpoints tested end-to-end, JWT_SECRET confirmed in prod env
- Gate 3 (before launch): full regression on existing routes to confirm no unintended protection applied

## Open Questions

- [ ] JWT_SECRET: where is it stored and who sets it in the deployment environment?
- [ ] Which routes are protected vs. public? (need list before Slice 3)
- [ ] Is registration open or invite-only? (affects register endpoint behavior)
