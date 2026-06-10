---
title: Security review of the auth module
task-type: review
path: ~/src/mine/my-app/src/auth
active: true
hours: "02:00-06:00"
max-runs: 5
max-tokens: 60000
provider: claude
---

Review the authentication module for correctness and security issues, with
particular attention to token expiry checks, session invalidation, and password
handling. Produce a findings report listing each issue, its severity, and a
suggested fix, so the findings can be turned into implementation tasks later.
Do not modify any code.
