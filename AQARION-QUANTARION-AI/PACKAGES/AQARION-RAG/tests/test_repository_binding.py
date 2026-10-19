"""Regression tests for explicit binding to the package's repository."""

import subprocess
from pathlib import Path

import retrieve as retrieval


def test_snapshot_loader_works_outside_checkout(tmp_path, monkeypatch):
    package = Path(retrieval.__file__).resolve().parent
    entry = retrieval.load_manifest()[0]

    expected = subprocess.check_output(
        [
            "git", "-C", str(package),
            "show", f"{entry['sha']}:{entry['path']}",
        ],
        text=True,
    )

    monkeypatch.chdir(tmp_path)

    actual = retrieval.load_at_sha(entry["path"], entry["sha"])
    assert actual == expected


def test_retrieval_ignores_unrelated_git_repository(tmp_path, monkeypatch):
    query = "evidence ledger"
    package = Path(retrieval.__file__).resolve().parent

    monkeypatch.chdir(package)
    expected = retrieval.retrieve(query)
    assert expected, "Control retrieval must return at least one passage"

    subprocess.run(
        ["git", "init", "--quiet", str(tmp_path)],
        check=True,
        capture_output=True,
        text=True,
    )

    monkeypatch.chdir(tmp_path)

    actual = retrieval.retrieve(query)
    assert actual == expected
