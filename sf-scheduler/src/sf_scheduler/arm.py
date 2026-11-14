"""Arm tasks that have a `run-at`: register one OS job per task, for that time.

The job runs `sf-scheduler run-task <file>` once. Whether the task still runs
is decided then by the usual guards (active, max-runs, hours, lock), so a stale
job (task edited or deactivated after arming) is harmless.
"""

from __future__ import annotations

import hashlib
import os
import shlex
import subprocess
import sys
from collections.abc import Callable
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from .dispatch import SCHEDULED_DIR
from .state import load_state, save_state
from .taskfile import TaskFileError, parse_task_file

Backend = Callable[[Path, datetime], None]

ARMED = "armed"
PAST = "run-at already passed"


def job_name(task_file: Path) -> str:
    digest = hashlib.sha1(str(task_file.resolve()).encode("utf-8")).hexdigest()[:12]
    return f"sf-scheduler-{task_file.stem}-{digest}"


def job_command(task_file: Path) -> list[str]:
    return [sys.executable, "-m", "sf_scheduler.cli", "run-task", str(task_file.resolve())]


def register_windows(task_file: Path, run_at: datetime) -> None:
    """Register a one-time Task Scheduler job (locale independent, via PowerShell)."""
    cmd = job_command(task_file)
    arguments = subprocess.list2cmdline(cmd[1:])
    script = (
        f"$a = New-ScheduledTaskAction -Execute {_ps(cmd[0])} -Argument {_ps(arguments)}; "
        f"$t = New-ScheduledTaskTrigger -Once -At ([datetime]{_ps(run_at.strftime('%Y-%m-%dT%H:%M:%S'))}); "
        "$s = New-ScheduledTaskSettingsSet -StartWhenAvailable; "
        f"Register-ScheduledTask -TaskName {_ps(job_name(task_file))} "
        "-Action $a -Trigger $t -Settings $s -Force | Out-Null"
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
        check=True, capture_output=True, text=True,
    )


def register_posix(task_file: Path, run_at: datetime) -> None:
    """Queue a one-time job with `at`."""
    subprocess.run(
        ["at", "-t", run_at.strftime("%Y%m%d%H%M")],
        input=shlex.join(job_command(task_file)) + "\n",
        check=True, capture_output=True, text=True,
    )


def default_backend() -> Backend:
    return register_windows if os.name == "nt" else register_posix


def unregister_windows(task_file: Path) -> None:
    """Delete the task's one-time Task Scheduler job. Missing job is not an error."""
    script = (
        f"Unregister-ScheduledTask -TaskName {_ps(job_name(task_file))} "
        "-Confirm:$false -ErrorAction SilentlyContinue"
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
        check=False, capture_output=True, text=True,
    )


def disarm(task_file: Path, *, unregister: Callable[[Path], None] | None = None) -> None:
    """Remove the OS job of a task that ran. `at` jobs consume themselves, so POSIX is a no-op."""
    if unregister is None:
        if os.name != "nt":
            return
        unregister = unregister_windows
    unregister(task_file)


def arm_tasks(
    root: Path, *, now: datetime, backend: Backend | None = None
) -> list[tuple[Path, str]]:
    """Register an OS job for every not-yet-armed task with a future `run-at`.

    Returns (task file, ARMED | PAST) for each task acted on or worth reporting.
    Re-running is safe: a task is armed once per `run-at` value, and changing
    `run-at` arms it again.
    """
    backend = backend or default_backend()
    results: list[tuple[Path, str]] = []
    for app in sorted(p for p in root.iterdir() if p.is_dir()):
        folder = app / SCHEDULED_DIR
        if not folder.is_dir():
            continue
        for task_file in sorted(folder.glob("*.md")):
            try:
                spec = parse_task_file(task_file)
            except TaskFileError:
                continue
            state = load_state(task_file)
            if spec.run_at is None or not spec.active or state.run_count >= spec.max_runs:
                continue
            if spec.run_at <= now:
                results.append((task_file, PAST))
                continue
            stamp = spec.run_at.isoformat()
            if state.armed == stamp:
                continue
            backend(task_file, spec.run_at)
            save_state(task_file, replace(state, armed=stamp))
            results.append((task_file, ARMED))
    return results


def _ps(value: str) -> str:
    """Quote a value as a PowerShell single-quoted string."""
    return "'" + value.replace("'", "''") + "'"
