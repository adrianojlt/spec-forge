"""Decide which task files in an intake folder are eligible to run now.

Pure read logic: parsing + eligibility only. It never mutates state; the
launcher (run step) is responsible for status transitions.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time
from pathlib import Path

from .state import TaskState, load_state
from .taskfile import TaskFileError, TaskSpec, parse_task_file


REASON_RUNNING = "running"


@dataclass
class Decision:
    """Outcome of evaluating one task: eligible to run, or skipped with reason."""

    source: Path
    spec: TaskSpec | None
    eligible: bool
    reason: str


def in_window(hours: str | None, now: datetime) -> bool:
    """Whether `now` falls inside an 'HH:MM-HH:MM' window. Wraps midnight."""
    if hours is None:
        return True
    start_s, end_s = hours.split("-")
    start = _parse_hhmm(start_s)
    end = _parse_hhmm(end_s)
    current = now.time()
    if start <= end:
        return start <= current <= end
    # Window wraps midnight, e.g. 22:00-06:00.
    return current >= start or current <= end


def evaluate(spec: TaskSpec, state: TaskState, now: datetime) -> Decision:
    """Apply eligibility rules to a parsed task and its state."""
    if not spec.active:
        return Decision(spec.source, spec, False, "inactive")
    if state.status == "running":
        # Running, or left that way by a launcher that died: the task's lock
        # tells the two apart (see dispatch.run_folder).
        return Decision(spec.source, spec, False, REASON_RUNNING)
    if state.run_count >= spec.max_runs:
        return Decision(spec.source, spec, False, "max-runs reached")
    if not in_window(spec.hours, now):
        return Decision(spec.source, spec, False, "outside hours")
    return Decision(spec.source, spec, True, "eligible")


def decide(task_file: Path, now: datetime) -> Decision:
    """Parse one task file and evaluate it against its state as it is now.

    A malformed task file becomes a non-eligible Decision with the parse error
    as the reason.
    """
    try:
        spec = parse_task_file(task_file)
    except TaskFileError as exc:
        return Decision(task_file, None, False, f"invalid: {exc}")
    return evaluate(spec, load_state(task_file), now)


def select(folder: Path, now: datetime) -> list[Decision]:
    """Evaluate every task file in `folder`, returning a Decision per file.

    Malformed task files never abort the scan (see `decide`).
    """
    return [decide(task_file, now) for task_file in sorted(folder.glob("*.md"))]


def _parse_hhmm(value: str) -> time:
    hour, minute = value.split(":")
    return time(int(hour), int(minute))
