# Scheduled trigger (cron / launchd)

The scheduled trigger fires the launcher on a cadence. On each fire it scans
every app's `scheduled-tasks/` under the apps root and runs the tasks that are
eligible (`active`, inside `hours`, under `max-runs`). The `hours` field in each
task gates the execution window, so the cron cadence can be coarse (e.g. every
15 minutes) while a task still only runs inside its window.

The command it runs:

```
<path-to>/sf-scheduler scheduled --root ~/ai-specs
```

`sf-scheduler` is the console script installed by the package (in your venv,
`.venv/bin/sf-scheduler`). Use its absolute path in cron/launchd.

## Option A - launchd (recommended on macOS)

launchd runs even when no shell is open and restarts the job on schedule.

1. Edit `deploy/com.sf-scheduler.scheduled.plist`:
   - set the absolute path to `sf-scheduler` in `ProgramArguments`,
   - set `--root` to your apps root,
   - set `StartInterval` (seconds) or replace it with a `StartCalendarInterval`.
2. Install:

   ```sh
   cp deploy/com.sf-scheduler.scheduled.plist ~/Library/LaunchAgents/
   launchctl load ~/Library/LaunchAgents/com.sf-scheduler.scheduled.plist
   ```

3. Check / inspect:

   ```sh
   launchctl list | grep sf-scheduler
   tail -f /tmp/sf-scheduler.out /tmp/sf-scheduler.err
   ```

4. Uninstall:

   ```sh
   launchctl unload ~/Library/LaunchAgents/com.sf-scheduler.scheduled.plist
   rm ~/Library/LaunchAgents/com.sf-scheduler.scheduled.plist
   ```

## Option B - cron

```sh
crontab -e
```

Add a line to run every 15 minutes (each task's `hours` still gates it):

```
*/15 * * * * /Users/you/src/mine/spec-forge/sf-scheduler/.venv/bin/sf-scheduler scheduled --root /Users/you/ai-specs >> /tmp/sf-scheduler.log 2>&1
```

## Exact time per task (`run-at`)

Instead of polling, give a task a `run-at` and register a one-time OS job for it.
No recurring trigger is needed.

```markdown
---
title: Refine backlog B
task-type: prompt
path: C:\Users\you\src\mine\gymlog
run-at: "2026-11-14 18:05"
permission-mode: acceptEdits
---
/refine i=C:\...\backlog-b.md id=all c=C:\Users\you\src\mine\gymlog
```

### Workflow

1. Create the task file in `<root>/<app>/scheduled-tasks/` with a `run-at`.
2. Run `arm` once to register it with the OS:

   ```
   sf-scheduler arm --root <root>
   ```

   If `sf-scheduler` is not on PATH, run the module instead:

   ```
   python -m sf_scheduler.cli arm --root <root>
   ```

Step 2 is required. A `run-at` alone registers nothing: the task only fires
once `arm` has created the OS job. There is nothing to enable or activate
beyond that, and no recurring trigger to set up.

`arm` prints `armed` for each task it registered. Repeat steps 1 and 2 for every
new task. Running `arm` again is safe: a task is armed once per `run-at` value.
To change the time, edit `run-at` and run `arm` again. A `run-at` already in the
past is reported and not armed.

### What `arm` creates

A one-time OS job that runs `sf-scheduler run-task <file>` at `run-at`:

- **Windows:** a Task Scheduler task named `sf-scheduler-<task>-<hash>`, created
  through PowerShell, set to "run as soon as possible after a missed start".
- **Linux and macOS:** an `at` job. On macOS `atd` is disabled by default.

After a run is attempted, whatever its outcome, `run-task` deletes the Windows task
(`at` jobs consume themselves): the job is one-shot and never fires again. A failure
is recorded in `<task>.results/run-NNN/` (`FAILED` or `STOPPED`) and in the task's
state file, not by keeping the job. To retry, delete the state file and the results
folder, then run `arm` again. A `run-task` call that finds the task not eligible
(for example before its `run-at`) leaves the job in place.

### Checking that a task is armed

On Windows:

```powershell
Get-ScheduledTask -TaskName 'sf-scheduler-*' | Get-ScheduledTaskInfo | Format-List TaskName,NextRunTime
```

`NextRunTime` should show the `run-at` time. The task is also visible in the Task
Scheduler UI (`taskschd.msc`), in the task library. On Linux and macOS use `atq`.

### Requirements

- `sf_scheduler` must be importable by the Python that ran `arm`
  (`pip install -e sf-scheduler`): the job calls that same Python.
- When the job fires, the usual guards still apply (`active`, `max-runs`,
  `hours`, lock), and the time cap kills a run that exceeds `--timeout`.
- The machine must be on and the user logged in (Windows), or `atd` running
  (Linux and macOS).
- A `prompt` task runs headless. If it edits files, set `permission-mode`
  (for example `acceptEdits`) or, with `provider: opencode`, `auto: true`, and test the command once by hand first: a prompt
  that asks for interactive confirmation cannot be answered.
- Output is `agent.log` in `<task>.results/run-NNN/`.

## Verifying

Use a short window and a small `max-runs` to test:

1. Create a `scheduled-tasks/` task with `hours` covering now and `max-runs: 1`.
2. Wait for one fire (or run the command manually once).
3. Confirm `<task>.results/run-001/` exists and `<task>.state.json` shows
   `run_count: 1`.
4. Wait for another fire and confirm the task is NOT re-run (run_count stays 1,
   `max-runs` reached).

## Operational notes

- The Mac must be awake for launchd/cron to fire. A sleeping machine will not run jobs.
- The launcher only runs eligible tasks; an empty or all-ineligible scan is a no-op.
- Fires may overlap: a fire that starts while an earlier one is still working skips the task that is running and never repeats one the earlier fire already ran.
- Each run records its outcome on disk (`report.md`/`summary.md`, or a `STOPPED`/`FAILED` marker). There are no notifications in v1.
