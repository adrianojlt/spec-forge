from __future__ import annotations

from pathlib import Path

import pytest


def write_task(folder: Path, name: str, *, frontmatter: str, body: str = "Do the thing.") -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{name}.md"
    path.write_text(f"---\n{frontmatter}\n---\n\n{body}\n", encoding="utf-8")
    return path


@pytest.fixture
def make_task(tmp_path):
    def _make(name: str, frontmatter: str, body: str = "Do the thing.") -> Path:
        return write_task(tmp_path, name, frontmatter=frontmatter, body=body)

    return _make
