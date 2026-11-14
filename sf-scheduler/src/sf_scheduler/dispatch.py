"""Dispatch: scan intake folders and run every eligible task.

Two modes share one folder-runner:
- scheduled: scan every app's `scheduled-tasks/` under an apps root (cron/launchd).
- remote: scan one app's `remote-tasks/` on demand (remote control).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .lock import task_lock
from .runner import DEFAULT_TIMEOUT_SECONDS, CommandBuilder, RunOutcome, default_command
from .runner import recover_interrupted, run_task
from .selection import REASON_RUNNING, decide, select

SCHEDULED_DIR = "scheduled-tasks"
REMOTE_DIR = "remote-tasks"


@dataclass
class FolderResult:
    folder: Path
    outcomes: list[RunOutcome]


def run_folder(
    folder: Path,
    *,
    now: datetime,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    command_builder: CommandBuilder = default_command,
) -> list[RunOutcome]:
    """Run every eligible task in a single intake folder.

    Each task runs under its lock, and whether it runs is decided again once
    the lock is held: the folder scan can be many minutes old by then, and
    another launcher may have run the task since.
    """
    outcomes: list[RunOutcome] = []
    for scanned in select(folder, now):
        if not (scanned.eligible or scanned.reason == REASON_RUNNING):
            continue
        outcome = run_one(scanned.source, now=now, timeout_seconds=timeout_seconds,
                          command_builder=command_builder)
        if outcome is not None:
            outcomes.append(outcome)
    return outcomes


def run_one(
    task_file: Path,
    *,
    now: datetime,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    command_builder: CommandBuilder = default_command,
) -> RunOutcome | None:
    """Run one task file if it is eligible once its lock is held, else None."""
    with task_lock(task_file) as held:
        if not held:
            return None  # another launcher is running this task right now
        recover_interrupted(task_file)
        decision = decide(task_file, now)
        if not decision.eligible:
            return None
        assert decision.spec is not None  # eligible decisions always carry a spec
        return run_task(
            decision.spec,
            now=now,
            timeout_seconds=timeout_seconds,
            command_builder=command_builder,
        )


def scheduled_run(
    root: Path,
    *,
    now: datetime,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    command_builder: CommandBuilder = default_command,
) -> list[FolderResult]:
    """Scan every app's scheduled-tasks/ under the apps root and run eligible tasks."""
    results: list[FolderResult] = []
    for app in sorted(p for p in root.iterdir() if p.is_dir()):
        folder = app / SCHEDULED_DIR
        if folder.is_dir():
            results.append(
                FolderResult(folder, run_folder(
                    folder, now=now, timeout_seconds=timeout_seconds,
                    command_builder=command_builder))
            )
    return results


def remote_run(
    root: Path,
    app: str,
    *,
    now: datetime,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    command_builder: CommandBuilder = default_command,
) -> FolderResult:
    """Process one app's remote-tasks/ on demand."""
    folder = root / app / REMOTE_DIR
    if not folder.is_dir():
        raise FileNotFoundError(f"no {REMOTE_DIR}/ folder for app {app!r} under {root}")
    return FolderResult(folder, run_folder(
        folder, now=now, timeout_seconds=timeout_seconds, command_builder=command_builder))
