# Discussion: User Authentication via Email + Password

Source: inbox/auth-idea.md
Date: 2026-05-23
Status: Ready

---

## Problem Summary

The current system has no authentication. Any user can access any endpoint without credentials. We need basic email/password authentication before the beta launch.

## Goals

- Users can register with email and password.
- Users can log in and receive a session token.
- Protected endpoints reject unauthenticated requests.
- Passwords are stored securely (hashed, not plaintext).

## Non-Goals

- OAuth or social login (not this iteration).
- Password reset via email (post-beta).
- Multi-factor authentication (post-beta).
- Admin user management UI (separate feature).

## Constraints

- Must use existing PostgreSQL database (no new databases).
- Must integrate with existing Express.js API.
- Session tokens must expire after 24 hours.
- No new infrastructure allowed (use existing server).
- Must ship within 2 weeks.

## Users and Stakeholders

- Primary user: end users of the web app.
- Stakeholders: product lead (approval), security team (review).

## Assumptions

- Email addresses are unique per account.
- We are not required to verify email at registration (for beta).
- bcrypt is acceptable for password hashing.

## Decisions Made

- JWT for session tokens (confirmed in discussion).
- No email verification at registration for beta.
- 24-hour token expiry with no refresh tokens initially.

## Open Questions

- [ ] Should registration be open or invite-only for beta?
- [ ] Is rate limiting on login required at launch?

## Risks and Ambiguities

- No email verification means disposable emails can register.
- Rate limiting absence could allow brute-force attacks on login.

## Readiness Status

- [x] Problem clear
- [x] Goals bounded
- [x] Success criteria defined
- [x] Constraints named
- [x] Scope boundary explicit
- [ ] No blocking open questions (2 minor questions remain, non-blocking)
