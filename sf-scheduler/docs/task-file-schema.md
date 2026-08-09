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
| `max-runs`   | int     | no       | `1`                | Total times the task may execute before it is `exhausted`. |
| `max-tokens` | int     | yes      | -                  | Hard per-run token cap. The launcher enforces this and kills a run that exceeds it. |
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
    <task>.results/
      run-001/
        report.md               <- analysis/review output
        summary.md              <- implementation summary (branch + changes)
        STOPPED                  <- present if the run hit the cap/timeout
        FAILED                   <- present if the run errored
  scheduled-tasks/              <- triggered by time (cron/launchd)
    <task>.md
    <task>.state.json
    <task>.results/run-NNN/...
```

- Sidecar state for `foo.md` is `foo.state.json` in the same folder.
- Results for run N of `foo.md` are written under `foo.results/run-NNN/` (zero-padded run count).
- A run writes exactly one of: a result artifact (success), `STOPPED` (cap/timeout), or `FAILED` (error).

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
| `run_count` | int             | Completed runs so far. Compared against `max-runs`. |
| `last_run`  | string \| null  | ISO-8601 timestamp of the last run start, or `null`. |
| `status`    | enum            | `pending`, `running`, `done`, `stopped`, `error`, `exhausted`. |

### Status meanings

- `pending` - never run, or ready to run again.
- `running` - a run is in progress (double-run guard skips these).
- `done` - last run completed successfully within the cap.
- `stopped` - last run hit the token/time cap and was killed.
- `error` - last run failed (bad path, agent non-zero exit, etc.).
- `exhausted` - `run_count` reached `max-runs`; will not run again.

## Eligibility (launcher decision)

A task is eligible to run now when ALL hold:

1. `active` is `true`.
2. Current local time is inside `hours` (or `hours` is absent).
3. `run_count` < `max-runs` (else `exhausted`).
4. `status` is not `running` (double-run guard).
