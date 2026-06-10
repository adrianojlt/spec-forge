"""Dispatch: scan intake folders and run every eligible task.

Two modes share one folder-runner:
- scheduled: scan every app's `scheduled-tasks/` under an apps root (cron/launchd).
- remote: scan one app's `remote-tasks/` on demand (remote control).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .runner import DEFAULT_TIMEOUT_SECONDS, CommandBuilder, RunOutcome, default_command
from .runner import run_task
from .selection import eligible

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
    """Run every eligible task in a single intake folder."""
    outcomes: list[RunOutcome] = []
    for decision in eligible(folder, now):
        assert decision.spec is not None  # eligible decisions always carry a spec
        outcomes.append(
            run_task(
                decision.spec,
                now=now,
                timeout_seconds=timeout_seconds,
                command_builder=command_builder,
            )
        )
    return outcomes


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
