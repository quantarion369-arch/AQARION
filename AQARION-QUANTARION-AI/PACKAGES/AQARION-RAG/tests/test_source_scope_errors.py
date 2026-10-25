"""Scoped missing-object errors; real Git, HTTP, and positive controls."""
import subprocess
from pathlib import Path
from unittest import mock

import pytest

import api
import context
import relationships
import retrieve
from tests.test_source_scope import http_server, request

ROUTES = (
    "/api/search",
    "/api/search/cited",
    "/api/search/context",
    "/api/search/evidence",
)
ERROR = {"error": "pinned Git object unavailable"}


@pytest.fixture(scope="module")
def pinned_sources(tmp_path_factory):
    root = tmp_path_factory.mktemp("pinned-error-fixture")

    def git(*args):
        return subprocess.check_output(
            [
                "git",
                "-c", "core.hooksPath=/dev/null",
                "-c", "commit.gpgsign=false",
                "-c", "user.name=AQARION Error Test",
                "-c", "user.email=error-test@example.invalid",
                "-C", str(root), *args,
            ],
            text=True,
            stderr=subprocess.STDOUT,
        ).strip()

    git("init", "-q")
    (root / "notes.md").write_text(
        "needle valid pinned passage", encoding="utf-8"
    )
    git("add", "--", "notes.md")
    git("commit", "-q", "-m", "valid fixture snapshot")
    good_sha = git("rev-parse", "HEAD")

    (root / "notes.md").write_text(
        "WORKTREE_FALLBACK_CANARY", encoding="utf-8"
    )

    good = {
        "doc": "Valid fixture",
        "path": "notes.md",
        "sha": good_sha,
        "purpose": "positive control",
    }
    missing = {
        "doc": "Missing fixture",
        "path": "notes.md",
        "sha": "f"*40,
        "purpose": "negative control",
    }
    return root, good, missing


@pytest.mark.parametrize("route", ROUTES)
def test_missing_pinned_object_returns_json(route, pinned_sources):
    root, good, missing = pinned_sources
    loader = retrieve.load_at_sha

    with (
        mock.patch.object(
            retrieve, "load_manifest", return_value=[good, missing]
        ),
        mock.patch.object(
            retrieve, "__file__", str(root / "retrieve.py")
        ),
        mock.patch.object(
            retrieve, "load_at_sha", wraps=loader
        ) as loads,
        mock.patch.object(
            relationships, "resolve_related"
        ) as enrichment,
        http_server(api) as base,
    ):
        status, body = request(
            base, route,
            {"q": "needle", "source_id": retrieve.source_id(missing)},
        )
        assert status == 404
        assert body == ERROR
        assert loads.call_count >= 1
        assert all(
            call.args == ("notes.md", missing["sha"])
            for call in loads.call_args_list
        )
        enrichment.assert_not_called()


@pytest.mark.parametrize("route", ROUTES)
def test_valid_source_works_after_missing_object(route, pinned_sources):
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
        ),
        http_server(api) as base,
    ):
        status, body = request(
            base, route,
            {"q": "needle", "source_id": retrieve.source_id(missing)},
        )
        assert status == 404 and body == ERROR

        status, body = request(
            base, route,
            {"q": "needle", "source_id": retrieve.source_id(good)},
        )
        assert status == 200
        assert "needle valid pinned passage" in str(body)
        assert "WORKTREE_FALLBACK_CANARY" not in str(body)


def test_successful_none_is_not_an_error_sentinel():
    class Sink:
        def _send(self, *args):
            raise AssertionError("Unexpected error response")

    result = api.Handler._retrieve_pinned_or_error(Sink(), lambda: None)
    assert result == (True, None)


@pytest.mark.parametrize("error_type", (ValueError, KeyError))
def test_programming_errors_are_not_client_errors(error_type):
    class Sink:
        def _send(self, *args):
            raise AssertionError("Programming error was relabeled")

    def broken():
        raise error_type("intentional programming-error control")

    with pytest.raises(error_type):
        api.Handler._retrieve_pinned_or_error(Sink(), broken)


def test_enrichment_failure_is_not_relabelled_as_missing_source(pinned_sources):
    _, good, missing = pinned_sources

    class Probe:
        path = "/api/search/evidence?q=needle&source_id=" + retrieve.source_id(good)
        _send = mock.Mock()
        _retrieve_pinned_or_error = api.Handler._retrieve_pinned_or_error

    probe = Probe()
    failure = subprocess.CalledProcessError(128, ["enrichment-fixture"])

    with (
        mock.patch.object(
            retrieve, "load_manifest", return_value=[good, missing]
        ),
        mock.patch.object(
            context, "retrieve_with_context",
            return_value={"seed_results": [], "supplementary_context": []},
        ),
        mock.patch.object(
            relationships, "resolve_related", side_effect=failure
        ),
    ):
        with pytest.raises(subprocess.CalledProcessError):
            api.Handler.do_GET(probe)
        probe._send.assert_not_called()
