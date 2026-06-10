"""Parse and validate sf-scheduler task files.

A task file is markdown with a YAML frontmatter block followed by a free-text
instructions body. See docs/task-file-schema.md for the contract.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

TASK_TYPES = {"analysis", "review", "implementation"}
PROVIDERS = {"claude", "opencode"}
DEFAULT_PROVIDER = "claude"

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)
_HOURS_RE = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)-([01]\d|2[0-3]):([0-5]\d)$")


class TaskFileError(Exception):
    """Raised when a task file is missing, malformed, or fails validation."""


@dataclass(frozen=True)
class TaskSpec:
    title: str
    task_type: str
    path: str
    instructions: str
    active: bool
    hours: str | None
    max_runs: int
    max_tokens: int
    provider: str
    source: Path


def parse_task_file(path: Path) -> TaskSpec:
    """Parse and validate a task file into a TaskSpec.

    Raises:
        TaskFileError: if the file is missing, has no frontmatter, contains
            invalid YAML, or fails field validation.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise TaskFileError(f"cannot read task file {path}: {exc}") from exc

    frontmatter, body = _split_frontmatter(path, text)

    try:
        data = yaml.safe_load(frontmatter) or {}
    except yaml.YAMLError as exc:
        raise TaskFileError(f"invalid YAML frontmatter in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise TaskFileError(f"frontmatter in {path} must be a mapping")

    return _validate(path, data, body.strip())


def _split_frontmatter(path: Path, text: str) -> tuple[str, str]:
    match = _FRONTMATTER_RE.match(text)
    if match is None:
        raise TaskFileError(f"{path} has no YAML frontmatter block")
    return match.group(1), match.group(2)


def _validate(path: Path, data: dict, body: str) -> TaskSpec:
    title = _require_str(path, data, "title")
    task_type = _require_str(path, data, "task-type")
    if task_type not in TASK_TYPES:
        raise TaskFileError(
            f"{path}: task-type must be one of {sorted(TASK_TYPES)}, got {task_type!r}"
        )
    target_path = _require_str(path, data, "path")

    active = data.get("active", True)
    if not isinstance(active, bool):
        raise TaskFileError(f"{path}: active must be a boolean")

    hours = data.get("hours")
    if hours is not None:
        if not isinstance(hours, str) or _HOURS_RE.match(hours) is None:
            raise TaskFileError(
                f"{path}: hours must be 'HH:MM-HH:MM' 24h format, got {hours!r}"
            )

    max_runs = _opt_positive_int(path, data, "max-runs", default=1)
    max_tokens = _require_positive_int(path, data, "max-tokens")

    provider = data.get("provider", DEFAULT_PROVIDER)
    if provider not in PROVIDERS:
        raise TaskFileError(
            f"{path}: provider must be one of {sorted(PROVIDERS)}, got {provider!r}"
        )

    if not body:
        raise TaskFileError(f"{path}: instructions body is empty")

    return TaskSpec(
        title=title,
        task_type=task_type,
        path=target_path,
        instructions=body,
        active=active,
        hours=hours,
        max_runs=max_runs,
        max_tokens=max_tokens,
        provider=provider,
        source=path,
    )


def _require_str(path: Path, data: dict, key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise TaskFileError(f"{path}: missing or empty required field {key!r}")
    return value.strip()


def _require_positive_int(path: Path, data: dict, key: str) -> int:
    if key not in data:
        raise TaskFileError(f"{path}: missing required field {key!r}")
    return _as_positive_int(path, data[key], key)


def _opt_positive_int(path: Path, data: dict, key: str, *, default: int) -> int:
    if key not in data:
        return default
    return _as_positive_int(path, data[key], key)


def _as_positive_int(path: Path, value: object, key: str) -> int:
    # bool is a subclass of int; reject it explicitly.
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise TaskFileError(f"{path}: {key} must be a positive integer, got {value!r}")
    return value
