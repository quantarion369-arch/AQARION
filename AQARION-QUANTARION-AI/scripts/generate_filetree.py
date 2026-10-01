#!/usr/bin/env python3
"""
Generate a minimal Git-derived FILETREE.md.

FILETREE.md records only tracked paths at one Git commit.
It is not an architecture document, claim registry, proof record,
verification receipt, or implementation-status report.
"""

from __future__ import annotations

import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import PurePosixPath

def run_bytes(*args: str) -> bytes:
    return subprocess.run(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
    ).stdout

def run_text(*args: str) -> str:
    return run_bytes(*args).decode("utf-8", errors="surrogateescape").strip()

def git_text(*args: str) -> str:
    return run_text("git", *args)

def git_bytes(*args: str) -> bytes:
    return run_bytes("git", *args)

def normalize_scope(scope: str | None) -> str | None:
    if scope is None or scope in ("", "."):
        return None
    normalized = PurePosixPath(scope).as_posix().strip("/")
    if normalized in ("", ".") or normalized == ".." or normalized.startswith("../"):
        raise ValueError("scope must be repository-relative")
    return normalized

def tracked_paths(commit: str) -> list[str]:
    raw = git_bytes("ls-tree", "-r", "-z", "--name-only", commit)
    return sorted(
        item.decode("utf-8", errors="surrogateescape")
        for item in raw.split(b"\0")
        if item
    )

def paths_in_scope(
    paths: list[str], scope: str | None
) -> list[str]:
    if scope is None:
        return paths
    prefix = scope + "/"
    selected = [
        path for path in paths if path.startswith(prefix)
    ]
    if not selected:
        raise ValueError(
            f"scope `{scope}` has no tracked files "
            "in the selected commit"
        )
    return selected

def render(
    repository_root: str,
    commit: str,
    tree: str,
    scope: str | None,
    paths: list[str],
) -> str:
    generated_utc = (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
    )

    lines = [
        "# FILETREE",
        "",
        f"Repository root: `{repository_root}`",
        f"Snapshot commit: `{commit}`",
        f"Snapshot tree: `{tree}`",
        f"Scope: `{scope or '/'}`",
        f"Generated UTC: `{generated_utc}`",
        f"Tracked file count: `{len(paths)}`",
        "",
        "This file is generated from the recorded Git commit.",
        "It lists tracked filesystem paths only.",
        "It does not state architecture, claim status, proof status,",
        "verification status, implementation readiness, or file semantics.",
        "",
        "## Paths",
        "",
    ]

    lines.extend(f"`{path}`" for path in paths)
    lines.append("")

    return "\n".join(lines)

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a minimal Git-derived FILETREE.md"
    )
    parser.add_argument(
        "--commit",
        default="HEAD",
        help="Commit-ish to snapshot. Default: HEAD",
    )
    parser.add_argument(
        "--scope",
        default=None,
        help="Optional repository-relative subtree.",
    )
    parser.add_argument(
        "--output",
        default="FILETREE.md",
        help="Output Markdown path. Default: FILETREE.md",
    )
    args = parser.parse_args()

    scope = normalize_scope(args.scope)

    repository_root = git_text(
        "rev-parse",
        "--show-toplevel",
    )

    commit = git_text(
        "rev-parse",
        args.commit,
    )

    tree = git_text(
        "rev-parse",
        f"{commit}^{{tree}}",
    )

    paths = paths_in_scope(
        tracked_paths(commit),
        scope,
    )

    with open(
        args.output,
        "w",
        encoding="utf-8",
        newline="\n",
    ) as handle:
        handle.write(
            render(
                repository_root=repository_root,
                commit=commit,
                tree=tree,
                scope=scope,
                paths=paths,
            )
        )

    print(f"WROTE: {args.output}")
    print(f"COMMIT: {commit}")
    print(f"TREE: {tree}")
    print(f"FILES: {len(paths)}")

if __name__ == "__main__":
    main()

