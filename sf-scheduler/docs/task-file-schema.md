# sf-scheduler task-file schema

A task is a single markdown file with a YAML frontmatter block followed by a
free-text instructions body. One file = one task.

```markdown
---
title: Nightly auth module review
task-type: review
path: ~/src/mine/my-app
active: true
hours: "02:00-06:00"
max-runs: 5
max-tokens: 60000
max-budget-usd: 2
provider: claude
---

Review the authentication module for correctness and security issues.
Focus on token expiry and session handling. Produce a findings report.
```

## Frontmatter fields

| Field        | Type    | Required | Default            | Meaning |
|--------------|---------|----------|--------------------|---------|
| `title`      | string  | yes      | -                  | Human-readable name of the task. |
| `task-type`  | enum    | yes      | -                  | One of `analysis`, `review`, `implementation`. |
| `path`       | string  | yes      | -                  | Target code location. Absolute, or `~`-expanded. |
| `instructions` | -     | -        | -                  | Not a frontmatter key: the markdown **body** after the frontmatter is the instructions. |
| `active`     | bool    | no       | `true`             | If `false`, the launcher skips the task. |
| `hours`      | string  | no       | any time           | Allowed execution window, `"HH:MM-HH:MM"` 24h local time. Wraps midnight if start > end (e.g. `"22:00-06:00"`). Omit for no window. |
| `max-runs`   | int     | no       | `1`                | Total times the task may be started. A run that fails, is stopped or crashes counts. |
| `max-tokens` | int     | yes      | -                  | Per-run token budget, passed to the agent in its prompt. Advisory: nothing measures or enforces it. |
| `max-budget-usd` | number | no    | no cap             | Hard per-run spend cap in US dollars, enforced by the `claude` CLI (`--max-budget-usd`). Rejected with `provider: opencode`, which has no such cap. |
| `provider`   | enum    | no       | by task-type       | `claude` or `opencode`. Default: `claude` for all task-types in v1. |

### `task-type` semantics

- `analysis` - read-only. Produce a report describing part of the code at `path`.
- `review` - read-only. Produce a task-review report of findings to implement later.
- `implementation` - mutating. Carry out the instruction on a **dedicated git branch only** (never `main`). The result records the branch name and a summary.

## Folder layout

Each app under `~/ai-specs` gets two intake folders. The launcher scans them.

```
<app>/
  remote-tasks/                 <- triggered on demand (remote control)
    <task>.md
    <task>.state.json           <- sidecar run state (launcher-owned)
    <task>.lock                 <- sidecar run lock (launcher-owned, empty, left in place)
    <task>.results/
      run-001/
        report.md               <- analysis/review output
        summary.md              <- implementation summary (branch + changes)
        STOPPED                  <- present if the run hit the time cap
        FAILED                   <- present if the run errored
  scheduled-tasks/              <- triggered by time (cron/launchd)
    <task>.md
    <task>.state.json
    <task>.results/run-NNN/...
```

- Sidecar state for `foo.md` is `foo.state.json` in the same folder.
- Results for run N of `foo.md` are written under `foo.results/run-NNN/` (zero-padded run count).
- A run writes exactly one of: a result artifact (success), `STOPPED` (time cap), or `FAILED` (error, including a run whose launcher died).
- The lock for `foo.md` is `foo.lock` in the same folder. A launcher holds it for the length of a run, and the OS releases it when that launcher exits, however it exits. The file is never deleted; keep it out of version control (ignore `*.lock` in the intake folders).

## Sidecar state file (`<task>.state.json`)

Launcher-owned. Written atomically (temp file + rename). Never edited by hand.

```json
{
  "run_count": 0,
  "last_run": null,
  "status": "pending"
}
```

| Field       | Type            | Meaning |
|-------------|-----------------|---------|
| `run_count` | int             | Runs started so far, counted when a run starts. Compared against `max-runs`. |
| `last_run`  | string \| null  | ISO-8601 timestamp of the last run start, or `null`. |
| `status`    | enum            | `pending`, `running`, `done`, `stopped`, `error`, `exhausted`. |

### Status meanings

- `pending` - never run, or ready to run again.
- `running` - a run is in progress, or its launcher died before recording an outcome. The lock tells the two apart: the next scan that gets the lock closes a dead run as `error` with a `FAILED` marker.
- `done` - last run completed successfully within the time cap.
- `stopped` - last run hit the time cap and was killed.
- `error` - last run failed (bad path, agent non-zero exit, launcher interrupted or died, etc.). A run cut short by `max-budget-usd` ends however the `claude` CLI ends it; the launcher records that exit code like any other.
- `exhausted` - `run_count` reached `max-runs`; will not run again.

## Eligibility (launcher decision)

A task is eligible to run now when ALL hold:

1. `active` is `true`.
2. Current local time is inside `hours` (or `hours` is absent).
3. `run_count` < `max-runs` (else `exhausted`).
4. No other launcher holds the task's lock (double-run guard).

Rules 1 to 3 are checked again once the lock is held, right before the run: the folder scan can be many minutes old by then.
