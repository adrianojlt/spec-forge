from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

from sf_scheduler.runner import (
    default_command,
    results_dir,
    run_dir_for,
    run_task,
)
from sf_scheduler.state import load_state
from sf_scheduler.taskfile import TaskSpec

NOW = datetime(2026, 6, 8, 3, 0)


def make_spec(tmp_path: Path, *, task_type="analysis", provider="claude", path=None) -> TaskSpec:
    source = tmp_path / "task.md"
    source.write_text("---\ntitle: t\ntask-type: analysis\npath: x\nmax-tokens: 1000\n---\n\nbody\n")
    target = path if path is not None else str(tmp_path)
    return TaskSpec(
        title="t",
        task_type=task_type,
        path=target,
        instructions="body",
        active=True,
        hours=None,
        max_runs=3,
        max_tokens=1000,
        provider=provider,
        source=source,
    )


def _py(script: str) -> list:
    def builder(spec, task_file, run_dir):
        return [sys.executable, "-c", script.format(run_dir=str(run_dir))]

    return builder


def test_success_writes_results_and_increments(tmp_path):
    spec = make_spec(tmp_path)
    builder = _py("open(r'{run_dir}/report.md','w').write('ok')")
    outcome = run_task(spec, now=NOW, command_builder=builder)

    assert outcome.status == "done"
    assert (outcome.run_dir / "report.md").read_text() == "ok"
    state = load_state(spec.source)
    assert state.run_count == 1
    assert state.status == "done"


def test_timeout_kills_and_writes_stopped(tmp_path):
    spec = make_spec(tmp_path)
    builder = _py("import time; time.sleep(30)")
    outcome = run_task(spec, now=NOW, timeout_seconds=1, command_builder=builder)

    assert outcome.status == "stopped"
    assert (outcome.run_dir / "STOPPED").exists()
    assert load_state(spec.source).status == "stopped"


def test_error_exit_writes_failed(tmp_path):
    spec = make_spec(tmp_path)
    builder = _py("import sys; sys.exit(2)")
    outcome = run_task(spec, now=NOW, command_builder=builder)

    assert outcome.status == "error"
    assert outcome.returncode == 2
    assert (outcome.run_dir / "FAILED").exists()
    assert load_state(spec.source).status == "error"


def test_bad_path_fails_without_launching(tmp_path):
    spec = make_spec(tmp_path, path="/no/such/dir/xyz")

    def boom(*_):
        raise AssertionError("agent must not be launched for a bad path")

    outcome = run_task(spec, now=NOW, command_builder=boom)
    assert outcome.status == "error"
    assert (outcome.run_dir / "FAILED").read_text().startswith("target path does not exist")
    assert load_state(spec.source).status == "error"


def test_run_count_increments_across_attempts(tmp_path):
    spec = make_spec(tmp_path)
    ok = _py("open(r'{run_dir}/report.md','w').write('ok')")
    run_task(spec, now=NOW, command_builder=ok)
    second = run_task(spec, now=NOW, command_builder=ok)

    assert load_state(spec.source).run_count == 2
    assert second.run_dir == run_dir_for(spec.source, 2)


def test_default_command_provider_mapping(tmp_path):
    rdir = results_dir(tmp_path / "task.md") / "run-001"
    claude = make_spec(tmp_path, provider="claude")
    opencode = make_spec(tmp_path, provider="opencode")
    assert default_command(claude, claude.source, rdir)[0] == "claude"
    assert default_command(opencode, opencode.source, rdir)[:2] == ["opencode", "run"]
