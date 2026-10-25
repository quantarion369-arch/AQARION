"""Operational source failures must not masquerade as absence."""

import subprocess
from unittest import mock

import pytest

import api
import relationships
import retrieve

from tests.test_source_scope import http_server, request
from tests.test_source_scope_errors import pinned_sources


ROUTES = (
    "/api/search",
    "/api/search/cited",
    "/api/search/context",
    "/api/search/evidence",
    "/api/sources/view",
)

FAILURES = (
    "nonzero_exit",
    "executable_missing",
    "permission_denied",
)


def injected_failure(kind):
    if kind == "nonzero_exit":
        return subprocess.CalledProcessError(
            128,
            ["git", "injected-operation"],
            stderr="PRIVATE_DIAGNOSTIC_CANARY",
        )
    if kind == "executable_missing":
        return FileNotFoundError("PRIVATE_DIAGNOSTIC_CANARY")
    return PermissionError("PRIVATE_DIAGNOSTIC_CANARY")


@pytest.mark.parametrize("route", ROUTES)
@pytest.mark.parametrize("failure_kind", FAILURES)
def test_operational_failure_is_500_and_recovers(
    route, failure_kind, pinned_sources
):
    root, good, missing = pinned_sources

    with (
        mock.patch.object(
            retrieve, "load_manifest", return_value=[good, missing]
        ),
        mock.patch.object(
            retrieve, "__file__", str(root / "retrieve.py")
        ),
        mock.patch.object(
            relationships, "resolve_related",
            return_value={"relationships": []},
        ) as enrichment,
        http_server(api) as base,
    ):
        query = {
            "q": "needle",
            "source_id": retrieve.source_id(good),
        }

        # Fixture setup already completed using real Git.
        # Inject failure only during the source-loading request.
        with mock.patch.object(
            retrieve.subprocess,
            "run",
            side_effect=injected_failure(failure_kind),
        ):
            status, body = request(base, route, query)

        assert status == 500, (
            f"{route}: operational {failure_kind} returned "
            f"{status}, expected 500; body={body!r}"
        )
        assert body == {"error": "pinned source loading failed"}
        assert "PRIVATE_DIAGNOSTIC_CANARY" not in str(body)
        assert "WORKTREE_FALLBACK_CANARY" not in str(body)
        enrichment.assert_not_called()

        # Fault removed: the same server must serve the valid pin.
        status, body = request(base, route, query)
        assert status == 200
        assert "needle valid pinned passage" in str(body)
        assert "WORKTREE_FALLBACK_CANARY" not in str(body)


@pytest.mark.parametrize("route", ROUTES)
@pytest.mark.parametrize(
    "condition", ("missing_commit", "missing_path", "noncommit_object")
)
def test_classified_source_conditions(route, condition, pinned_sources):
    root, good, missing = pinned_sources
    selected = dict(good)

    if condition == "missing_commit":
        selected = dict(missing)
    elif condition == "missing_path":
        selected["path"] = "absent/pinned.md"
    else:
        selected["sha"] = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse",
             good["sha"] + ":notes.md"],
            text=True,
        ).strip()

    expected_status = 500 if condition == "noncommit_object" else 404
    expected_error = (
        "pinned source loading failed" if expected_status == 500
        else "pinned Git object unavailable"
    )

    with (
        mock.patch.object(
            retrieve, "load_manifest", return_value=[selected]
        ),
        mock.patch.object(
            retrieve, "__file__", str(root / "retrieve.py")
        ),
        mock.patch.object(
            relationships, "resolve_related",
            return_value={"relationships": []},
        ) as enrichment,
        http_server(api) as base,
    ):
        status, body = request(
            base, route,
            {"q": "needle", "source_id": retrieve.source_id(selected)},
        )
        assert status == expected_status
        assert body == {"error": expected_error}
        assert "WORKTREE_FALLBACK_CANARY" not in str(body)
        enrichment.assert_not_called()


@pytest.mark.parametrize("route", ROUTES)
@pytest.mark.parametrize("stage", ("tree_read", "blob_read"))
def test_later_git_operation_failure_is_500(
    route, stage, pinned_sources
):
    root, good, missing = pinned_sources
    real_run = subprocess.run

    def failing_run(command, *args, **kwargs):
        is_tree = "ls-tree" in command
        is_blob = (
            "cat-file" in command
            and command[command.index("cat-file") + 1] == "blob"
        )
        if (
            (stage == "tree_read" and is_tree)
            or (stage == "blob_read" and is_blob)
        ):
            raise subprocess.CalledProcessError(
                128, command, stderr="PRIVATE_DIAGNOSTIC_CANARY"
            )
        return real_run(command, *args, **kwargs)

    with (
        mock.patch.object(
            retrieve, "load_manifest", return_value=[good, missing]
        ),
        mock.patch.object(
            retrieve, "__file__", str(root / "retrieve.py")
        ),
        mock.patch.object(
            relationships, "resolve_related"
        ) as enrichment,
        http_server(api) as base,
    ):
        with mock.patch.object(
            retrieve.subprocess, "run", side_effect=failing_run
        ):
            status, body = request(
                base, route,
                {"q": "needle", "source_id": retrieve.source_id(good)},
            )
        assert status == 500
        assert body == {"error": "pinned source loading failed"}
        assert "PRIVATE_DIAGNOSTIC_CANARY" not in str(body)
        enrichment.assert_not_called()


def test_exact_filename_and_nested_path_loading(tmp_path, monkeypatch):
    def git(*args):
        return subprocess.check_output(
            [
                "git", "-c", "core.hooksPath=/dev/null",
                "-c", "commit.gpgsign=false",
                "-c", "user.name=Classification Test",
                "-c", "user.email=test@example.invalid",
                "-C", str(tmp_path), *args,
            ],
            text=True,
        ).strip()

    git("init", "-q")
    names = (
        "literal[ab]*?.md",
        "literalabX.md",
        "nested/topic.md",
    )
    for name in names:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("PINNED:" + name, encoding="utf-8")

    git("add", "--", ".")
    git("commit", "-q", "-m", "literal path fixture")
    pin = git("rev-parse", "HEAD")

    monkeypatch.setattr(
        retrieve, "__file__", str(tmp_path / "retrieve.py")
    )

    for name in names:
        (tmp_path / name).write_text(
            "WORKTREE_FALLBACK_CANARY", encoding="utf-8"
        )
        assert retrieve.load_at_sha(name, pin) == "PINNED:" + name

    # Existing directory and existing noncommit identity are load errors.
    with pytest.raises(retrieve.PinnedSourceLoadError):
        retrieve.load_at_sha("nested", pin)

    with pytest.raises(retrieve.PinnedSourceUnavailable):
        retrieve.load_at_sha("absent.md", pin)
