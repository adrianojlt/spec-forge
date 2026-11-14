from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import pytest

from sf_scheduler.arm import ARMED, PAST, arm_tasks, disarm, job_command, job_name
from sf_scheduler.cli import main
from sf_scheduler.runner import default_command
from sf_scheduler.selection import decide
from sf_scheduler.state import TaskState, load_state, save_state
from sf_scheduler.taskfile import TaskFileError, parse_task_file

NOW = datetime(2026, 11, 14, 12, 0)
BASE = "title: t\ntask-type: prompt\npath: {path}\n"


def write(folder: Path, name: str, extra: str = "", body: str = "/refine i=x", fm_path=None) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    fm = BASE.format(path=fm_path or folder) + extra
    f = folder / f"{name}.md"
    f.write_text(f"---\n{fm}---\n\n{body}\n", encoding="utf-8")
    return f


def test_prompt_needs_no_max_tokens(tmp_path):
    spec = parse_task_file(write(tmp_path, "t"))
    assert spec.task_type == "prompt"
    assert spec.max_tokens is None


def test_other_types_still_require_max_tokens(tmp_path):
    f = tmp_path / "t.md"
    f.write_text("---\ntitle: t\ntask-type: analysis\npath: x\n---\n\nbody\n", encoding="utf-8")
    with pytest.raises(TaskFileError, match="max-tokens"):
        parse_task_file(f)


@pytest.mark.parametrize("value", ['"2026-11-14 18:05"', "2026-11-14 18:05"])
def test_run_at_parsed(tmp_path, value):
    spec = parse_task_file(write(tmp_path, "t", f"run-at: {value}\n"))
    assert spec.run_at == datetime(2026, 11, 14, 18, 5)


def test_run_at_invalid(tmp_path):
    with pytest.raises(TaskFileError, match="run-at"):
        parse_task_file(write(tmp_path, "t", 'run-at: "tomorrow"\n'))


def test_permission_mode_rejected_for_opencode(tmp_path):
    with pytest.raises(TaskFileError, match="permission-mode"):
        parse_task_file(write(tmp_path, "t", "provider: opencode\npermission-mode: acceptEdits\n"))


def test_opencode_auto_adds_flag(tmp_path):
    f = write(tmp_path, "t", "provider: opencode\nauto: true\n", body="/refine i=x")
    cmd = default_command(parse_task_file(f), f, tmp_path / "run-001")
    assert cmd == ["opencode", "run", "--auto", "/refine i=x"]


def test_run_task_resolves_command_through_path(tmp_path, monkeypatch):
    from sf_scheduler.runner import run_task

    f = write(tmp_path, "t")
    seen = []
    monkeypatch.setattr("sf_scheduler.runner.shutil.which", lambda name: sys.executable)
    monkeypatch.setattr(
        "sf_scheduler.runner.subprocess.Popen",
        lambda cmd, **kw: seen.append(cmd) or _FakeProc(),
    )
    run_task(parse_task_file(f), now=NOW, command_builder=lambda s, t, r: ["opencode", "run", "x"])
    assert seen[0][0] == sys.executable


class _FakeProc:
    pid = 0
    returncode = 0

    def wait(self, timeout=None):
        return 0


def test_opencode_without_auto_has_no_flag(tmp_path):
    f = write(tmp_path, "t", "provider: opencode\n", body="/refine i=x")
    cmd = default_command(parse_task_file(f), f, tmp_path / "run-001")
    assert cmd == ["opencode", "run", "/refine i=x"]


@pytest.mark.parametrize("extra", ["auto: true\n", "auto: yes please\n"])
def test_auto_rejected_for_claude_or_non_bool(tmp_path, extra):
    with pytest.raises(TaskFileError, match="auto"):
        parse_task_file(write(tmp_path, "t", extra))


def test_prompt_command_sends_body_verbatim(tmp_path):
    f = write(tmp_path, "t", "permission-mode: acceptEdits\n", body="/refine i=x id=all")
    cmd = default_command(parse_task_file(f), f, tmp_path / "run-001")
    assert cmd == ["claude", "-p", "/refine i=x id=all", "--permission-mode", "acceptEdits"]


def test_not_eligible_before_run_at(tmp_path):
    f = write(tmp_path, "t", 'run-at: "2026-11-14 18:05"\n')
    assert decide(f, NOW).reason == "before run-at"
    assert decide(f, datetime(2026, 11, 14, 18, 5)).eligible


def test_arm_registers_future_task_once(tmp_path):
    f = write(tmp_path / "app" / "scheduled-tasks", "t", 'run-at: "2026-11-14 18:05"\n')
    calls = []
    backend = lambda task, at: calls.append((task, at))

    assert arm_tasks(tmp_path, now=NOW, backend=backend) == [(f, ARMED)]
    assert calls == [(f, datetime(2026, 11, 14, 18, 5))]
    assert load_state(f).armed == "2026-11-14T18:05:00"

    assert arm_tasks(tmp_path, now=NOW, backend=backend) == []  # already armed
    assert len(calls) == 1


def test_arm_again_when_run_at_changes(tmp_path):
    folder = tmp_path / "app" / "scheduled-tasks"
    f = write(folder, "t", 'run-at: "2026-11-14 18:05"\n')
    calls = []
    arm_tasks(tmp_path, now=NOW, backend=lambda *a: calls.append(a))
    write(folder, "t", 'run-at: "2026-11-14 19:00"\n')
    arm_tasks(tmp_path, now=NOW, backend=lambda *a: calls.append(a))
    assert [c[1].hour for c in calls] == [18, 19]
    assert load_state(f).armed == "2026-11-14T19:00:00"


def test_arm_skips_past_inactive_done_and_no_run_at(tmp_path):
    folder = tmp_path / "app" / "scheduled-tasks"
    past = write(folder, "past", 'run-at: "2026-11-14 08:00"\n')
    write(folder, "off", 'run-at: "2026-11-14 18:05"\nactive: false\n')
    write(folder, "plain")
    done = write(folder, "done", 'run-at: "2026-11-14 18:05"\n')
    save_state(done, TaskState(1, NOW.isoformat(), "done"))
    calls = []
    assert arm_tasks(tmp_path, now=NOW, backend=lambda *a: calls.append(a)) == [(past, PAST)]
    assert calls == []


def test_job_command_runs_run_task_with_absolute_path(tmp_path):
    f = write(tmp_path, "t")
    cmd = job_command(f)
    assert cmd[:3] == [sys.executable, "-m", "sf_scheduler.cli"]
    assert cmd[3:] == ["run-task", str(f.resolve())]
    assert job_name(f).startswith("sf-scheduler-t-")


def test_run_one_runs_due_task_and_skips_future(tmp_path):
    from sf_scheduler.dispatch import run_one

    builder = lambda s, tf, rd: [sys.executable, "-c", "pass"]
    due = write(tmp_path, "due", 'run-at: "2000-01-01 00:00"\n')
    future = write(tmp_path, "future", 'run-at: "2999-01-01 00:00"\n')

    assert run_one(due, now=NOW, command_builder=builder).status == "done"
    assert run_one(future, now=NOW, command_builder=builder) is None
    assert load_state(future).run_count == 0


def test_disarm_calls_unregister_with_task_file(tmp_path):
    calls = []
    f = write(tmp_path, "t")
    disarm(f, unregister=calls.append)
    assert calls == [f]


@pytest.mark.parametrize("builder_code", ["pass", "raise SystemExit(1)"])
def test_run_task_cli_disarms_after_any_attempted_run(tmp_path, monkeypatch, builder_code):
    import sf_scheduler.cli as cli
    from sf_scheduler import dispatch

    due = write(tmp_path, "due", 'run-at: "2000-01-01 00:00"\n')
    builder = lambda s, tf, rd: [sys.executable, "-c", builder_code]
    real_run_one = dispatch.run_one
    monkeypatch.setattr(cli, "run_one", lambda *a, **k: real_run_one(*a, command_builder=builder, **k))
    calls = []
    monkeypatch.setattr(cli, "disarm", calls.append)

    assert main(["run-task", str(due)]) == 0
    assert calls == [due]


def test_run_task_cli_not_eligible_does_not_disarm(tmp_path, monkeypatch):
    import sf_scheduler.cli as cli

    future = write(tmp_path, "future", 'run-at: "2999-01-01 00:00"\n')
    calls = []
    monkeypatch.setattr(cli, "disarm", calls.append)
    assert main(["run-task", str(future)]) == 0
    assert calls == []


def test_run_task_cli_future_task_is_not_run(tmp_path, capsys):
    future = write(tmp_path, "future", 'run-at: "2999-01-01 00:00"\n')
    assert main(["run-task", str(future)]) == 0
    assert "not eligible" in capsys.readouterr().out
    assert load_state(future).run_count == 0
