from __future__ import annotations

import json

import pytest

from sf_scheduler.state import TaskState, load_state, save_state, state_path


def test_load_missing_returns_default(tmp_path):
    task = tmp_path / "foo.md"
    state = load_state(task)
    assert state == TaskState(run_count=0, last_run=None, status="pending")


def test_state_path_sidecar(tmp_path):
    assert state_path(tmp_path / "foo.md").name == "foo.state.json"


def test_save_then_load_roundtrip(tmp_path):
    task = tmp_path / "foo.md"
    save_state(task, TaskState(run_count=2, last_run="2026-06-08T03:00:00", status="done"))
    loaded = load_state(task)
    assert loaded == TaskState(run_count=2, last_run="2026-06-08T03:00:00", status="done")


def test_save_is_atomic_no_partial(tmp_path, monkeypatch):
    task = tmp_path / "foo.md"
    save_state(task, TaskState(run_count=1, status="done"))

    # Force os.replace to fail; the prior good state must remain intact and no
    # temp file should be left behind.
    import sf_scheduler.state as state_mod

    def boom(*_args, **_kwargs):
        raise OSError("disk full")

    monkeypatch.setattr(state_mod.os, "replace", boom)
    with pytest.raises(OSError):
        save_state(task, TaskState(run_count=99, status="error"))

    assert load_state(task) == TaskState(run_count=1, last_run=None, status="done")
    leftover = [p for p in tmp_path.iterdir() if p.name.endswith(".tmp")]
    assert leftover == []


def test_invalid_status_rejected(tmp_path):
    with pytest.raises(ValueError, match="invalid status"):
        save_state(tmp_path / "foo.md", TaskState(status="bogus"))


def test_unknown_status_on_disk_coerced(tmp_path):
    task = tmp_path / "foo.md"
    state_path(task).write_text(json.dumps({"run_count": 1, "status": "weird"}), encoding="utf-8")
    assert load_state(task).status == "pending"
