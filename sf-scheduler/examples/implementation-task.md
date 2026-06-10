---
title: Add a health-check endpoint
task-type: implementation
path: ~/src/mine/my-app
active: true
hours: "22:00-06:00"
max-runs: 1
max-tokens: 80000
provider: claude
---

Add a simple `GET /healthz` endpoint that returns HTTP 200 with body `{"status":
"ok"}`. Follow the existing routing and handler conventions in the project. Add a
test for it. Do the work on a dedicated branch only - do not touch `main`. When
done, record the branch name and a short summary of the changes.
