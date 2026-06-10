"""Per-task run state, stored as a JSON sidecar next to the task file.

State is launcher-owned and written atomically (temp file + os.replace) so an
interrupted write never leaves a partial/corrupt record.
"""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path

STATUSES = {"pending", "running", "done", "stopped", "error", "exhausted"}


@dataclass
class TaskState:
    run_count: int = 0
    last_run: str | None = None
    status: str = "pending"


def state_path(task_file: Path) -> Path:
    """Sidecar path for a task file: foo.md -> foo.state.json."""
    return task_file.with_suffix(".state.json")


def load_state(task_file: Path) -> TaskState:
    """Load state for a task, returning a default pending state if absent."""
    path = state_path(task_file)
    if not path.exists():
        return TaskState()
    data = json.loads(path.read_text(encoding="utf-8"))
    status = data.get("status", "pending")
    if status not in STATUSES:
        status = "pending"
    return TaskState(
        run_count=int(data.get("run_count", 0)),
        last_run=data.get("last_run"),
        status=status,
    )


def save_state(task_file: Path, state: TaskState) -> None:
    """Atomically persist state for a task."""
    if state.status not in STATUSES:
        raise ValueError(f"invalid status {state.status!r}")
    path = state_path(task_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=path.name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(asdict(state), fh, indent=2)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_name, path)
    except BaseException:
        # Leave the prior state file intact; remove the temp file.
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
        raise
