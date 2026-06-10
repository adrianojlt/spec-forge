"""Run a single eligible task against a headless agent.

The launcher owns the deterministic guards here:
- a hard wall-clock timeout that kills a runaway run,
- branch isolation for `implementation` tasks (the agent runs in a dedicated git
  worktree on its own branch, so the repo's default branch is physically
  untouched, enforced by code rather than trusted to the agent), and
- an outcome always recorded on disk (results, a STOPPED marker, or a FAILED
  marker).

The actual task work is delegated to the headless agent via the
`sf-scheduler-run` skill.
"""

from __future__ import annotations

import os
import signal
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .state import TaskState, load_state, save_state
from .taskfile import TaskSpec

SKILL_REF = "sf-scheduler-run"
DEFAULT_TIMEOUT_SECONDS = 1800

CommandBuilder = Callable[[TaskSpec, Path, Path], list[str]]


@dataclass
class RunOutcome:
    status: str  # "done" | "stopped" | "error"
    run_dir: Path
    returncode: int | None
    branch: str | None = None


def results_dir(task_file: Path) -> Path:
    return task_file.with_suffix(".results")


def run_dir_for(task_file: Path, run_number: int) -> Path:
    return results_dir(task_file) / f"run-{run_number:03d}"


def default_command(spec: TaskSpec, task_file: Path, run_dir: Path) -> list[str]:
    """Build the headless agent command for a task's provider."""
    # TODO: add spec.model and pass --model <model> here when per-task model selection is implemented
    prompt = (
        f"Use the {SKILL_REF} skill to perform this scheduled task.\n"
        f"Task file: {task_file}\n"
        f"Task type: {spec.task_type}\n"
        f"Target path: {spec.path}\n"
        f"Token budget: {spec.max_tokens}\n"
        f"Write all outputs into: {run_dir}\n"
    )
    if spec.provider == "claude":
        return ["claude", "-p", prompt]
    return ["opencode", "run", prompt]


def run_task(
    spec: TaskSpec,
    *,
    now: datetime,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    command_builder: CommandBuilder = default_command,
) -> RunOutcome:
    """Execute one task, enforce the guards, and record the outcome.

    run_count is incremented on every terminal attempt (success, stopped, or
    error) so a repeatedly failing task cannot retry forever and burn tokens.
    """
    task_file = spec.source
    state = load_state(task_file)
    run_number = state.run_count + 1
    run_dir = run_dir_for(task_file, run_number)
    run_dir.mkdir(parents=True, exist_ok=True)

    target = Path(os.path.expanduser(spec.path))
    if not target.exists():
        return _finish(task_file, state, run_dir, now, "error", marker="FAILED",
                       message=f"target path does not exist: {spec.path}\n")

    # Set up the working directory. Implementation tasks run in an isolated git
    # worktree on a dedicated branch so the default branch is never touched.
    branch: str | None = None
    default_head: str | None = None
    if spec.task_type == "implementation":
        repo = _repo_root(target)
        if repo is None:
            return _finish(task_file, state, run_dir, now, "error", marker="FAILED",
                           message=f"target path is not a git repository: {spec.path}\n")
        default_head = _git(repo, "rev-parse", "HEAD").stdout.strip()
        branch = f"sf-sched/{task_file.stem}-{run_dir.name}"
        try:
            cwd = _add_worktree(repo, run_dir, branch)
        except subprocess.CalledProcessError as exc:
            return _finish(task_file, state, run_dir, now, "error", marker="FAILED",
                           message=f"could not create isolated worktree: {exc.stderr or exc}\n")
        (run_dir / "branch.txt").write_text(branch + "\n", encoding="utf-8")
    else:
        cwd = target if target.is_dir() else target.parent

    # Mark running before launching so the double-run guard sees it.
    save_state(task_file, TaskState(state.run_count, now.isoformat(), "running"))

    cmd = command_builder(spec, task_file, run_dir)
    log_path = run_dir / "agent.log"
    try:
        with open(log_path, "wb") as log:
            proc = subprocess.Popen(
                cmd, stdout=log, stderr=subprocess.STDOUT,
                cwd=str(cwd), start_new_session=True,
            )
            try:
                returncode = proc.wait(timeout=timeout_seconds)
            except subprocess.TimeoutExpired:
                _kill_group(proc)
                return _finish(task_file, state, run_dir, now, "stopped", marker="STOPPED",
                               message=f"killed after {timeout_seconds}s (token/time cap)\n",
                               branch=branch)
    except (FileNotFoundError, OSError) as exc:
        return _finish(task_file, state, run_dir, now, "error", marker="FAILED",
                       message=f"could not launch agent: {exc}\n", branch=branch)

    if returncode != 0:
        return _finish(task_file, state, run_dir, now, "error", marker="FAILED",
                       message=f"agent exited with code {returncode}\n",
                       returncode=returncode, branch=branch)

    # Defensive: even with worktree isolation, confirm the default branch did not move.
    if default_head is not None:
        repo = _repo_root(target)
        moved = repo is not None and _git(repo, "rev-parse", "HEAD").stdout.strip() != default_head
        if moved:
            return _finish(task_file, state, run_dir, now, "error", marker="FAILED",
                           message="default branch HEAD moved during the run; aborting\n",
                           branch=branch)

    return _finish(task_file, state, run_dir, now, "done", returncode=returncode, branch=branch)


def _finish(
    task_file: Path, prior: TaskState, run_dir: Path, now: datetime, status: str,
    *, marker: str | None = None, message: str = "",
    returncode: int | None = None, branch: str | None = None,
) -> RunOutcome:
    if marker is not None:
        (run_dir / marker).write_text(message, encoding="utf-8")
    save_state(task_file, TaskState(prior.run_count + 1, now.isoformat(), status))
    return RunOutcome(status, run_dir, returncode, branch)


def _kill_group(proc: subprocess.Popen) -> None:
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    except ProcessLookupError:
        pass
    proc.wait()


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, check=True,
    )


def _repo_root(path: Path) -> Path | None:
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip())


def _add_worktree(repo: Path, run_dir: Path, branch: str) -> Path:
    worktree = run_dir / "work"
    _git(repo, "worktree", "add", "-b", branch, str(worktree), "HEAD")
    return worktree
