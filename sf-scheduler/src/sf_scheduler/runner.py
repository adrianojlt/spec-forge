"""Run a single eligible task against a headless agent.

The launcher owns the deterministic guards here:
- a hard wall-clock timeout that kills a runaway run,
- an optional spend cap (`max-budget-usd`), handed to the agent CLI to enforce,
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
        cmd = ["claude", "-p", prompt]
        if spec.max_budget_usd is not None:
            cmd += ["--max-budget-usd", str(spec.max_budget_usd)]
        return cmd
    return ["opencode", "run", prompt]


def run_task(
    spec: TaskSpec,
    *,
    now: datetime,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    command_builder: CommandBuilder = default_command,
) -> RunOutcome:
    """Execute one task, enforce the guards, and record the outcome.

    run_count is incremented when the run starts, before anything can fail, so
    a run that errors, is stopped, or dies with its launcher still counts: a
    repeatedly failing task cannot retry forever and burn tokens.
    """
    task_file = spec.source
    run_number = load_state(task_file).run_count + 1
    run_dir = run_dir_for(task_file, run_number)
    run_dir.mkdir(parents=True, exist_ok=True)
    save_state(task_file, TaskState(run_number, now.isoformat(), "running"))

    target = Path(os.path.expanduser(spec.path))
    if not target.exists():
        return _finish(task_file, run_number, run_dir, now, "error", marker="FAILED",
                       message=f"target path does not exist: {spec.path}\n")

    # Set up the working directory. Implementation tasks run in an isolated git
    # worktree on a dedicated branch so the default branch is never touched.
    branch: str | None = None
    default_head: str | None = None
    if spec.task_type == "implementation":
        repo = _repo_root(target)
        if repo is None:
            return _finish(task_file, run_number, run_dir, now, "error", marker="FAILED",
                           message=f"target path is not a git repository: {spec.path}\n")
        default_head = _git(repo, "rev-parse", "HEAD").stdout.strip()
        branch = f"sf-sched/{task_file.stem}-{run_dir.name}"
        try:
            cwd = _add_worktree(repo, run_dir, branch)
        except subprocess.CalledProcessError as exc:
            return _finish(task_file, run_number, run_dir, now, "error", marker="FAILED",
                           message=f"could not create isolated worktree: {exc.stderr or exc}\n")
        (run_dir / "branch.txt").write_text(branch + "\n", encoding="utf-8")
    else:
        cwd = target if target.is_dir() else target.parent

    cmd = command_builder(spec, task_file, run_dir)
    log_path = run_dir / "agent.log"
    try:
        with open(log_path, "wb") as log:
            proc = subprocess.Popen(
                cmd, stdout=log, stderr=subprocess.STDOUT,
                cwd=str(cwd), start_new_session=True,
            )
    except OSError as exc:
        return _finish(task_file, run_number, run_dir, now, "error", marker="FAILED",
                       message=f"could not launch agent: {exc}\n", branch=branch)

    try:
        returncode = proc.wait(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        _kill_tree(proc)
        return _finish(task_file, run_number, run_dir, now, "stopped", marker="STOPPED",
                       message=f"killed after {timeout_seconds}s (time cap)\n",
                       branch=branch)
    except BaseException:
        # The launcher itself is going down (Ctrl+C, shutdown). Never leave the
        # agent running unsupervised, and record what happened to this run.
        _kill_tree(proc)
        _finish(task_file, run_number, run_dir, now, "error", marker="FAILED",
                message="launcher interrupted; agent killed\n", branch=branch)
        raise

    if returncode != 0:
        return _finish(task_file, run_number, run_dir, now, "error", marker="FAILED",
                       message=f"agent exited with code {returncode}\n",
                       returncode=returncode, branch=branch)

    # Defensive: even with worktree isolation, confirm the default branch did not move.
    if default_head is not None:
        repo = _repo_root(target)
        moved = repo is not None and _git(repo, "rev-parse", "HEAD").stdout.strip() != default_head
        if moved:
            return _finish(task_file, run_number, run_dir, now, "error", marker="FAILED",
                           message="default branch HEAD moved during the run; aborting\n",
                           branch=branch)

    return _finish(task_file, run_number, run_dir, now, "done",
                   returncode=returncode, branch=branch)


def recover_interrupted(task_file: Path) -> bool:
    """Close out a run whose launcher died before recording an outcome.

    Call only while holding the task's lock: the lock proves no launcher is
    running the task, so a state still saying `running` is a dead run. It was
    already counted when it started. Returns True if such a run was closed.
    """
    state = load_state(task_file)
    if state.status != "running":
        return False
    run_dir = run_dir_for(task_file, state.run_count)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "FAILED").write_text("launcher died during this run\n", encoding="utf-8")
    save_state(task_file, TaskState(state.run_count, state.last_run, "error"))
    return True


def _finish(
    task_file: Path, run_number: int, run_dir: Path, now: datetime, status: str,
    *, marker: str | None = None, message: str = "",
    returncode: int | None = None, branch: str | None = None,
) -> RunOutcome:
    if marker is not None:
        (run_dir / marker).write_text(message, encoding="utf-8")
    save_state(task_file, TaskState(run_number, now.isoformat(), status))
    return RunOutcome(status, run_dir, returncode, branch)


def _kill_tree(proc: subprocess.Popen) -> None:
    """Kill the agent and every process it started, then reap it."""
    if os.name == "nt":
        # Windows has no process group to signal: taskkill /T walks the tree.
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
            capture_output=True, check=False,
        )
        proc.kill()  # in case taskkill could not reach the agent itself
    else:
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
