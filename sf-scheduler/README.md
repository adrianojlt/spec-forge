# sf-scheduler

Run simple, well-scoped AI tasks against a codebase while you are away from the
computer. Drop a task file in a watched folder (or schedule it), and a headless
AI agent picks it up, does the work, and leaves the result behind for you to
review later.

## How it works

sf-scheduler is a **thin launcher plus a skill**, not a standalone app.

- The **launcher** (`src/sf_scheduler/`, Python) does only the parts that must be
  deterministic: decide which task files are due (`active` / `hours` /
  `max-runs`), keep an atomic per-task run-count state, and enforce a hard
  token/time cap that kills a runaway run.
- The **`sf-scheduler-run` skill** (`skills/sf-scheduler-run/` in this repo) tells
  the headless agent what to actually do per task type.
- **cron / launchd** fires the launcher on a schedule. **Claude Code remote
  control** triggers it on demand.

```
cron/launchd ─┐
remote control ┼─> launcher ──(eligible task)──> headless agent + sf-scheduler-run skill ──> results in task folder
              ─┘   (guards: hours, max-runs,
                    atomic state, hard token cap)
```

## Folders

Each app under `~/ai-specs` has two intake folders the launcher scans:

- `remote-tasks/` - tasks picked up on demand (remote trigger).
- `scheduled-tasks/` - tasks picked up by time (scheduled trigger).

## Task types

- `analysis` - report on part of the code.
- `review` - task-review report of findings to implement later.
- `implementation` - carry out an instruction, on a dedicated git branch only (never `main`).

## Where to start

- Task-file format and folder/state/marker layout: [`docs/task-file-schema.md`](docs/task-file-schema.md).
- Example tasks: [`examples/`](examples/).

## Remote session setup

To trigger tasks from a phone via Claude Code remote control without typing long
commands, add this to `~/.claude/CLAUDE.md`:

```markdown
## Remote Sessions
When asked about remote tasks or to run them, check `~/src/mine/ai-mine-specs/apps/`.
Each app subfolder may have a `remote-tasks/` directory with `.md` task files.
To run tasks for an app: `sf-scheduler remote --root ~/src/mine/ai-mine-specs/apps --app <app-name>`
```

Then from the remote session just say: "run remote tasks for `<app>`" and Claude
runs the command. No manual typing of the full path required.

## Planned enhancements

- **Per-task model selection** - add a `model` frontmatter field (e.g. `model: claude-opus-4-8`) and pass `--model` to the headless agent command. Currently the default Claude Code model is used for all runs.

## Safety

- Per-task `max-tokens` is a hard cap; the launcher kills a run that exceeds it.
- `implementation` tasks never touch `main`; work lands on a dedicated branch.
- Every run leaves a result, a `STOPPED` marker, or a `FAILED` marker on disk
  (there are no notifications in v1).
