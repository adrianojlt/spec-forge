"""Command-line entrypoint for the sf-scheduler launcher.

    sf-scheduler scheduled --root ~/ai-specs
    sf-scheduler remote    --root ~/ai-specs --app my-app

cron/launchd invokes the `scheduled` subcommand; Claude Code remote control
invokes the `remote` subcommand.
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from .dispatch import DEFAULT_TIMEOUT_SECONDS, FolderResult, remote_run, scheduled_run


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sf-scheduler")
    sub = parser.add_subparsers(dest="mode", required=True)

    sched = sub.add_parser("scheduled", help="run due tasks in every app's scheduled-tasks/")
    sched.add_argument("--root", required=True, help="apps root, e.g. ~/ai-specs")
    sched.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)

    remote = sub.add_parser("remote", help="run tasks in one app's remote-tasks/")
    remote.add_argument("--root", required=True, help="apps root, e.g. ~/ai-specs")
    remote.add_argument("--app", required=True, help="app folder name under the root")
    remote.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)

    args = parser.parse_args(argv)
    root = Path(os.path.expanduser(args.root))
    now = datetime.now()

    if args.mode == "scheduled":
        results = scheduled_run(root, now=now, timeout_seconds=args.timeout)
    else:
        try:
            results = [remote_run(root, args.app, now=now, timeout_seconds=args.timeout)]
        except FileNotFoundError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1

    _report(results)
    return 0


def _report(results: list[FolderResult]) -> None:
    total = 0
    for result in results:
        for outcome in result.outcomes:
            total += 1
            print(f"{result.folder}: {outcome.run_dir.name} -> {outcome.status}")
    if total == 0:
        print("no eligible tasks")


if __name__ == "__main__":
    raise SystemExit(main())
