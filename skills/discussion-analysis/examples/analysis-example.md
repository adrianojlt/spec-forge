# Analysis: User Authentication via Email + Password

Source: features/auth/discussion.md
Date: 2026-05-23
Status: Ready

---

## Problem Statement

The system currently has no authentication layer. Any request reaches any endpoint without credentials. Email and password authentication must be added before the beta launch. The solution must use the existing PostgreSQL database and Express.js API with no new infrastructure.

## Confirmed Facts

- No authentication exists today.
- PostgreSQL is the current database (confirmed in discussion).
- Express.js is the existing API framework.
- Session tokens must expire after 24 hours.
- No new infrastructure is permitted.
- No email verification is required at registration for beta.
- JWT is confirmed as the token format.
- bcrypt is confirmed for password hashing.
- Deadline is 2 weeks.

## Assumptions

- Email addresses are globally unique (not enforced yet in schema).
- The existing database schema can accommodate a new `users` table without migration conflicts.
- The Express.js version supports middleware-based auth without major refactor.
- 24-hour JWT expiry is acceptable to stakeholders without refresh tokens.

> Note: Every assumption here must be validated or explicitly accepted before planning begins.

## Goals

- Users can register with email and password.
- Users can log in and receive a session token.
- Protected endpoints reject unauthenticated requests.
- Passwords are stored securely (hashed).

## Non-Goals

- OAuth or social login.
- Password reset via email.
- Multi-factor authentication.
- Admin user management UI.

## Constraints

- Must use existing PostgreSQL database.
- Must integrate with existing Express.js API.
- Session tokens expire after 24 hours.
- No new infrastructure.
- Must ship in 2 weeks.

## Risks

- No email verification means disposable or invalid emails can register.
- No rate limiting on login allows brute-force attacks.
- JWT secret management not addressed in discussion (where is secret stored?).
- Schema migration could break existing data if not carefully applied.

## Dependencies

- PostgreSQL database must be accessible with write permissions (for `users` table creation).
- JWT_SECRET environment variable must be set in deployment before tokens can be validated.
- Existing route list needed to know which routes to protect.

## Edge Cases

- Registration with duplicate email.
- Login with wrong password (error message must not reveal whether email exists).
- Expired JWT presented to protected endpoint.
- Empty or malformed request body on registration or login.
- Very long email or password inputs.

## Open Questions

- [ ] Should registration be open or invite-only for beta?
- [ ] Is rate limiting on login required at launch?
- [ ] Where is the JWT secret stored in the current deployment? (new - surfaced during analysis)
- [ ] Is there a current database migration system in place? (new - surfaced during analysis)

## Readiness Assessment

Analysis is complete enough to begin planning. Two open questions from discussion remain, plus two new questions surfaced during analysis. Planning can begin, but "open vs. invite-only registration" must be answered before AUTH-002 can be fully scoped, and JWT secret storage must be resolved before Slice 3 ships.
