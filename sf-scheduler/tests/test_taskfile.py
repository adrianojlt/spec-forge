from __future__ import annotations

import pytest

from sf_scheduler.taskfile import TaskFileError, parse_task_file

VALID = """\
title: Test task
task-type: analysis
path: ~/code
max-tokens: 5000
"""


def test_parse_valid_full(make_task):
    path = make_task(
        "t",
        """\
title: Full task
task-type: implementation
path: ~/code/app
active: false
hours: "22:00-06:00"
max-runs: 3
max-tokens: 8000
provider: opencode
""",
        body="Implement the feature.",
    )
    spec = parse_task_file(path)
    assert spec.title == "Full task"
    assert spec.task_type == "implementation"
    assert spec.path == "~/code/app"
    assert spec.active is False
    assert spec.hours == "22:00-06:00"
    assert spec.max_runs == 3
    assert spec.max_tokens == 8000
    assert spec.provider == "opencode"
    assert spec.instructions == "Implement the feature."


def test_defaults_applied(make_task):
    spec = parse_task_file(make_task("t", VALID))
    assert spec.active is True
    assert spec.hours is None
    assert spec.max_runs == 1
    assert spec.provider == "claude"


def test_no_frontmatter(tmp_path):
    path = tmp_path / "t.md"
    path.write_text("just a body, no frontmatter\n", encoding="utf-8")
    with pytest.raises(TaskFileError, match="no YAML frontmatter"):
        parse_task_file(path)


@pytest.mark.parametrize(
    "frontmatter, match",
    [
        ("task-type: analysis\npath: ~/c\nmax-tokens: 10", "title"),
        ("title: x\npath: ~/c\nmax-tokens: 10", "task-type"),
        ("title: x\ntask-type: bogus\npath: ~/c\nmax-tokens: 10", "task-type must be one of"),
        ("title: x\ntask-type: analysis\nmax-tokens: 10", "path"),
        ("title: x\ntask-type: analysis\npath: ~/c", "max-tokens"),
        ("title: x\ntask-type: analysis\npath: ~/c\nmax-tokens: 0", "positive integer"),
        ("title: x\ntask-type: analysis\npath: ~/c\nmax-tokens: 10\nactive: maybe", "active must be a boolean"),
        ('title: x\ntask-type: analysis\npath: ~/c\nmax-tokens: 10\nhours: "9-5"', "hours must be"),
        ("title: x\ntask-type: analysis\npath: ~/c\nmax-tokens: 10\nprovider: gpt", "provider must be one of"),
    ],
)
def test_invalid_rejected(tmp_path, frontmatter, match):
    path = tmp_path / "t.md"
    path.write_text(f"---\n{frontmatter}\n---\n\nbody\n", encoding="utf-8")
    with pytest.raises(TaskFileError, match=match):
        parse_task_file(path)


def test_empty_body_rejected(tmp_path):
    path = tmp_path / "t.md"
    path.write_text(f"---\n{VALID}---\n\n", encoding="utf-8")
    with pytest.raises(TaskFileError, match="instructions body is empty"):
        parse_task_file(path)
