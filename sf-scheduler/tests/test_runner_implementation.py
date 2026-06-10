from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

from sf_scheduler.runner import run_task
from sf_scheduler.state import load_state
from sf_scheduler.taskfile import TaskSpec

NOW = datetime(2026, 6, 8, 3, 0)


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def init_repo(path: Path) -> str:
    path.mkdir(parents=True, exist_ok=True)
    _git(path, "init", "-q")
    _git(path, "config", "user.email", "test@example.com")
    _git(path, "config", "user.name", "Test")
    _git(path, "checkout", "-q", "-b", "main")
    (path / "file.txt").write_text("original\n")
    _git(path, "add", "file.txt")
    _git(path, "commit", "-q", "-m", "initial")
    return _git(path, "rev-parse", "HEAD")


def impl_spec(repo: Path, source: Path) -> TaskSpec:
    source.write_text("---\ntitle: t\ntask-type: implementation\npath: x\nmax-tokens: 1000\n---\n\nbody\n")
    return TaskSpec(
        title="t", task_type="implementation", path=str(repo), instructions="body",
        active=True, hours=None, max_runs=2, max_tokens=1000, provider="claude",
        source=source,
    )


# Stub agent: runs in the worktree (its cwd) and commits a change there.
_AGENT = (
    "import subprocess, pathlib;"
    "pathlib.Path('added.txt').write_text('done');"
    "subprocess.run(['git','add','added.txt'],check=True);"
    "subprocess.run(['git','commit','-q','-m','impl by agent'],check=True)"
)


def test_implementation_isolated_on_branch_main_untouched(tmp_path):
    repo = tmp_path / "repo"
    head_before = init_repo(repo)
    spec = impl_spec(repo, tmp_path / "task.md")

    def builder(s, task_file, run_dir):
        return [sys.executable, "-c", _AGENT]

    outcome = run_task(spec, now=NOW, command_builder=builder)

    assert outcome.status == "done"
    assert outcome.branch == "sf-sched/task-run-001"
    # main is physically untouched
    assert _git(repo, "rev-parse", "HEAD") == head_before
    assert not (repo / "added.txt").exists()
    # the dedicated branch carries the agent's commit
    branch_log = _git(repo, "log", "--oneline", outcome.branch)
    assert "impl by agent" in branch_log
    assert (outcome.run_dir / "branch.txt").read_text().strip() == outcome.branch
    assert load_state(spec.source).status == "done"


def test_implementation_non_git_path_fails(tmp_path):
    plain = tmp_path / "plaindir"
    plain.mkdir()
    spec = impl_spec(plain, tmp_path / "task.md")

    def boom(*_):
        raise AssertionError("agent must not launch for a non-git path")

    outcome = run_task(spec, now=NOW, command_builder=boom)
    assert outcome.status == "error"
    assert (outcome.run_dir / "FAILED").read_text().startswith("target path is not a git repository")
