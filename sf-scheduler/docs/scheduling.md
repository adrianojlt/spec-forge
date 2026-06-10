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
- Each run records its outcome on disk (`report.md`/`summary.md`, or a `STOPPED`/`FAILED` marker). There are no notifications in v1.
