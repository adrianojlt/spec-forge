from __future__ import annotations

from datetime import datetime

from sf_scheduler.selection import eligible, in_window, select
from sf_scheduler.state import TaskState, save_state

# A fixed "now": Monday 2026-06-08, 03:00 local.
NOW = datetime(2026, 6, 8, 3, 0)


def _fm(**over) -> str:
    base = {
        "title": "t",
        "task-type": "analysis",
        "path": "~/c",
        "max-tokens": 5000,
    }
    base.update(over)
    lines = []
    for key, value in base.items():
        if isinstance(value, str) and ("-" in value or ":" in value):
            lines.append(f'{key}: "{value}"')
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines)


def test_in_window_normal():
    assert in_window("01:00-07:00", NOW) is True
    assert in_window("04:00-07:00", NOW) is False


def test_in_window_wraps_midnight():
    assert in_window("22:00-06:00", NOW) is True  # 03:00 is inside
    assert in_window("22:00-02:00", NOW) is False  # 03:00 is outside


def test_in_window_none_always_true():
    assert in_window(None, NOW) is True


def test_select_mixed_returns_only_eligible(tmp_path, make_task):
    # one of each skip reason + one eligible
    inactive = make_task("inactive", _fm(active=False))
    outside = make_task("outside", _fm(hours="04:00-05:00"))
    exhausted = make_task("exhausted", _fm(**{"max-runs": 2}))
    save_state(exhausted, TaskState(run_count=2, status="done"))
    good = make_task("good", _fm(hours="01:00-07:00"))

    decisions = {d.source.stem: d for d in select(tmp_path, NOW)}
    assert decisions["inactive"].reason == "inactive"
    assert decisions["outside"].reason == "outside hours"
    assert decisions["exhausted"].reason == "max-runs reached"
    assert decisions["good"].eligible is True

    elig = [d.source.stem for d in eligible(tmp_path, NOW)]
    assert elig == ["good"]


def test_double_run_guard(tmp_path, make_task):
    task = make_task("busy", _fm())
    save_state(task, TaskState(run_count=0, status="running"))
    [d] = select(tmp_path, NOW)
    assert d.eligible is False
    assert d.reason == "running"


def test_malformed_file_does_not_abort_scan(tmp_path, make_task):
    bad = tmp_path / "bad.md"
    bad.write_text("no frontmatter here\n", encoding="utf-8")
    make_task("good", _fm(hours="01:00-07:00"))

    decisions = {d.source.stem: d for d in select(tmp_path, NOW)}
    assert decisions["bad"].eligible is False
    assert decisions["bad"].reason.startswith("invalid:")
    assert decisions["good"].eligible is True
