"""Per-task run lock: at most one launcher process runs a task at a time.

An OS-level lock on a sidecar file (`foo.md` -> `foo.lock`). The OS drops the
lock when its holder exits, however it exits, so a crashed or killed launcher
can never leave a task locked. The file itself is left in place: deleting it
while another launcher has it open would let two of them hold "the" lock.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

if os.name == "nt":
    import msvcrt

    def _try_lock(fd: int) -> bool:
        try:
            msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
        except OSError:
            return False
        return True

    def _unlock(fd: int) -> None:
        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)

else:
    import fcntl

    def _try_lock(fd: int) -> bool:
        try:
            # flock, not lockf: a lockf lock is dropped as soon as the process
            # closes any descriptor of the file, even an unrelated one.
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            return False
        return True

    def _unlock(fd: int) -> None:
        fcntl.flock(fd, fcntl.LOCK_UN)


def lock_path(task_file: Path) -> Path:
    """Sidecar lock path for a task file: foo.md -> foo.lock."""
    return task_file.with_suffix(".lock")


@contextmanager
def task_lock(task_file: Path) -> Iterator[bool]:
    """Try to take the task's lock without waiting.

    Yields True when this process now holds it, False when another process
    does. The lock is released on exit from the block.
    """
    fd = os.open(lock_path(task_file), os.O_RDWR | os.O_CREAT)
    held = False
    try:
        held = _try_lock(fd)
        yield held
    finally:
        if held:
            _unlock(fd)
        os.close(fd)
