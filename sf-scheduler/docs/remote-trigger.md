# Remote trigger (on demand)

The remote trigger runs the launcher against one app's `remote-tasks/` folder on
demand, so you can kick off a task while away from the keyboard. v1 uses Claude
Code remote control as the native trigger; the launcher command is the same one
cron would run, just in `remote` mode.

The command:

```
<path-to>/sf-scheduler remote --root ~/ai-specs --app <app-name>
```

It scans `~/ai-specs/<app-name>/remote-tasks/`, runs every eligible task, and
writes results in-folder, exactly like the scheduled path.

## Triggering from Claude Code remote control (phone)

1. Drop a task file into the app's `remote-tasks/` folder (e.g. via a git pull on
   the Mac, or any synced path). It follows the same schema as scheduled tasks.
2. From the Claude Code mobile/remote-control session connected to your Mac, ask
   it to run:

   ```
   Run: <path-to>/sf-scheduler remote --root ~/ai-specs --app <app-name>
   ```

   (or invoke it through whatever shell access the remote session gives you).
3. The launcher processes the folder and writes results under
   `<task>.results/run-NNN/` in `remote-tasks/`.

## Verifying

1. Put a small `analysis` task in `~/ai-specs/<app>/remote-tasks/` with
   `max-tokens` low and a path to a real code dir.
2. Trigger the `remote` command (locally first, then from remote control).
3. Confirm `report.md` appears under the task's `results/run-001/` and
   `<task>.state.json` shows `run_count: 1`, `status: done`.

## Notes

- `remote` mode ignores `hours` only insofar as you choose when to trigger it; a
  task's `active` and `max-runs` are still honoured.
- A later, optional enhancement is auto-pickup: have the scheduled launcher also
  scan `remote-tasks/` on a short cadence so a dropped file runs without an
  explicit trigger. Deferred for v1.
