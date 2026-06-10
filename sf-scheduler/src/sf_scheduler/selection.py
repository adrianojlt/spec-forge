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
        return Decision(spec.source, spec, False, "running")
    if state.run_count >= spec.max_runs:
        return Decision(spec.source, spec, False, "max-runs reached")
    if not in_window(spec.hours, now):
        return Decision(spec.source, spec, False, "outside hours")
    return Decision(spec.source, spec, True, "eligible")


def select(folder: Path, now: datetime) -> list[Decision]:
    """Evaluate every task file in `folder`, returning a Decision per file.

    Malformed task files become a non-eligible Decision with the parse error as
    the reason; they never abort the scan.
    """
    decisions: list[Decision] = []
    for task_file in sorted(folder.glob("*.md")):
        try:
            spec = parse_task_file(task_file)
        except TaskFileError as exc:
            decisions.append(Decision(task_file, None, False, f"invalid: {exc}"))
            continue
        state = load_state(task_file)
        decisions.append(evaluate(spec, state, now))
    return decisions


def eligible(folder: Path, now: datetime) -> list[Decision]:
    """Just the eligible decisions from `select`."""
    return [d for d in select(folder, now) if d.eligible]


def _parse_hhmm(value: str) -> time:
    hour, minute = value.split(":")
    return time(int(hour), int(minute))
