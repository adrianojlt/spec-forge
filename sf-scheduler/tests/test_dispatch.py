from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

from sf_scheduler.dispatch import remote_run, run_folder, scheduled_run
from sf_scheduler.state import TaskState, load_state, save_state

NOW = datetime(2026, 6, 8, 3, 0)

OK_BUILDER = lambda s, tf, rd: [sys.executable, "-c", f"open(r'{rd}/report.md','w').write('ok')"]


def write_task(folder: Path, name: str, *, active=True, hours=None, max_runs=1) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    fm = [f"title: {name}", "task-type: analysis", "path: x", "max-tokens: 1000",
          f"active: {str(active).lower()}", f"max-runs: {max_runs}"]
    if hours:
        fm.append(f'hours: "{hours}"')
    # point path at an existing dir so the run proceeds
    fm[2] = f"path: {folder}"
    (folder / f"{name}.md").write_text("---\n" + "\n".join(fm) + "\n---\n\nbody\n")
    return folder / f"{name}.md"


def test_run_folder_runs_only_eligible(tmp_path):
    write_task(tmp_path, "good")
    write_task(tmp_path, "off", active=False)
    outcomes = run_folder(tmp_path, now=NOW, command_builder=OK_BUILDER)
    assert len(outcomes) == 1
    assert outcomes[0].status == "done"


def test_scheduled_scans_each_app(tmp_path):
    root = tmp_path
    write_task(root / "app1" / "scheduled-tasks", "a")
    write_task(root / "app2" / "scheduled-tasks", "b")
    # a remote-tasks folder must be ignored by scheduled mode
    write_task(root / "app1" / "remote-tasks", "r")

    results = scheduled_run(root, now=NOW, command_builder=OK_BUILDER)
    ran = {o.status for fr in results for o in fr.outcomes}
    folders = {fr.folder.parent.name for fr in results}
    assert folders == {"app1", "app2"}
    assert ran == {"done"}
    assert sum(len(fr.outcomes) for fr in results) == 2  # remote task not run


def test_remote_processes_named_app(tmp_path):
    root = tmp_path
    write_task(root / "myapp" / "remote-tasks", "task")
    result = remote_run(root, "myapp", now=NOW, command_builder=OK_BUILDER)
    assert [o.status for o in result.outcomes] == ["done"]


def test_remote_missing_folder_raises(tmp_path):
    import pytest

    with pytest.raises(FileNotFoundError):
        remote_run(tmp_path, "nope", now=NOW, command_builder=OK_BUILDER)


def test_max_runs_respected_across_calls(tmp_path):
    task = write_task(tmp_path, "once", max_runs=1)
    run_folder(tmp_path, now=NOW, command_builder=OK_BUILDER)
    assert load_state(task).run_count == 1
    # second pass: already at max-runs, not eligible
    outcomes = run_folder(tmp_path, now=NOW, command_builder=OK_BUILDER)
    assert outcomes == []
    assert load_state(task).run_count == 1
