from __future__ import annotations

from sf_scheduler.lock import lock_path, task_lock


def test_lock_path_sidecar(tmp_path):
    assert lock_path(tmp_path / "foo.md").name == "foo.lock"


def test_one_holder_at_a_time_and_free_after_release(tmp_path):
    task = tmp_path / "foo.md"
    with task_lock(task) as first:
        assert first is True
        with task_lock(task) as second:
            assert second is False
    with task_lock(task) as again:
        assert again is True
