"""Source-scope boundary regressions using a disposable real Git repository.

HTTP evidence enrichment is mocked at its boundary.
Existing package tests separately cover relationship behavior.
"""
import contextlib
import json
from pathlib import Path
import subprocess
import tempfile
import threading
from http.server import ThreadingHTTPServer
from unittest import mock
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen

@contextlib.contextmanager
def http_server(api):
    server = ThreadingHTTPServer(("127.0.0.1", 0), api.Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def request(base, route, query=None):
    url = base + route
    if query:
        url += "?" + urlencode(query, doseq=True)
    try:
        with urlopen(url, timeout=15) as response:
            return response.status, json.loads(response.read())
    except HTTPError as error:
        return error.code, json.loads(error.read())


def focused_tests(r, c, api, relationships):
    passed = 0

    def ok(label):
        nonlocal passed
        passed += 1
        print("PASS:", label, flush=True)

    with tempfile.TemporaryDirectory(
        prefix="aqarion-scope-git-fixture-"
    ) as temporary:
        root = Path(temporary)

        def git(*args):
            return subprocess.check_output(
                [
                    "git",
                    "-c", "core.hooksPath=/dev/null",
                    "-c", "commit.gpgsign=false",
                    "-c", "user.name=AQARION Scope Test",
                    "-c", "user.email=scope-test@example.invalid",
                    "-C", str(root),
                    *args,
                ],
                text=True,
                stderr=subprocess.STDOUT,
            ).strip()

        git("init", "-q")
        texts = [
            "OLD_NEIGHBOR_ALPHA\n\nSHARED SEED NEEDLE\n\nOLD_NEIGHBOR_OMEGA",
            "NEW_NEIGHBOR_BETA\n\nSHARED SEED NEEDLE\n\nNEW_NEIGHBOR_SIGMA",
        ]
        shas = []

        for index, text in enumerate(texts):
            (root / "notes.md").write_text(text, encoding="utf-8")
            git("add", "--", "notes.md")
            git("commit", "-q", "-m", f"fixture revision {index+1}")
            shas.append(git("rev-parse", "HEAD"))

        (root / "notes.md").write_text(
            "WORKTREE_FALLBACK_CANARY", encoding="utf-8"
        )
        entries = [
            {
                "doc": f"Revision {index+1}",
                "path": "notes.md",
                "sha": sha,
                "purpose": "temporary test",
            }
            for index, sha in enumerate(shas)
        ]
        entries.append({
            "doc": "Missing object",
            "path": "notes.md",
            "sha": "f"*40,
            "purpose": "temporary test",
        })
        ids = [r.source_id(entry) for entry in entries]
        real_loader = r.load_at_sha

        with (
            mock.patch.object(r, "load_manifest", return_value=entries),
            mock.patch.object(r, "__file__", str(root / "retrieve.py")),
        ):
            for index in (0, 1):
                with mock.patch.object(
                    r, "load_at_sha", wraps=real_loader
                ) as loader:
                    result = c.retrieve_with_context(
                        "shared seed needle", source_id=ids[index]
                    )
                    assert result["seed_results"]
                    assert len(result["supplementary_context"]) == 2

                    for item in (
                        result["seed_results"]
                        + result["supplementary_context"]
                    ):
                        assert item["commit_sha"] == shas[index]
                        assert item["doc"] == entries[index]["doc"]
                        assert item["passage"] == texts[index][
                            item["char_start"]:item["char_end"]
                        ]

                    assert all(
                        call.args == ("notes.md", shas[index])
                        for call in loader.call_args_list
                    )
            ok("real Git revision isolation, selected-only loads, citations")

            seed = r.retrieve_cited(
                "shared seed needle", source_id=ids[0]
            )[0]
            seed["doc"] = "FORGED LABEL"
            try:
                c._expand_context([seed])
            except ValueError as error:
                assert "label" in str(error)
            else:
                raise AssertionError("Forged label accepted")
            ok("forged label rejected")

            wrong = r.retrieve_cited(
                "shared seed needle", source_id=ids[1]
            )
            with mock.patch.object(r, "retrieve_cited", return_value=wrong):
                try:
                    c.retrieve_with_context("needle", source_id=ids[0])
                except ValueError:
                    pass
                else:
                    raise AssertionError("Wrong revision accepted")
            ok("context rejects wrong-revision seeds")

            empty = c.retrieve_with_context(
                "zzzzqxxnomatch", source_id=ids[0]
            )
            assert empty["seed_results"] == []
            assert empty["supplementary_context"] == []
            ok("no-match does not fall back globally")

            with http_server(api) as base:
                routes = (
                    "/api/search", "/api/search/cited",
                    "/api/search/context", "/api/search/evidence",
                )
                invalid = (
                    ([""], 400),
                    (["  "], 400),
                    ([" " + ids[0]], 400),
                    ([ids[0], ids[0]], 400),
                    (["unknown"], 404),
                )

                for route in routes:
                    for values, expected in invalid:
                        with contextlib.ExitStack() as stack:
                            spies = [
                                stack.enter_context(mock.patch.object(obj, name))
                                for obj, name in (
                                    (api, "retrieve"),
                                    (api, "retrieve_cited"),
                                    (c, "retrieve_with_context"),
                                    (relationships, "resolve_related"),
                                )
                            ]
                            status, _ = request(
                                base, route,
                                {"q": "needle", "source_id": values},
                            )
                            assert status == expected, (route, values, status)
                            assert all(spy.call_count == 0 for spy in spies)
                ok("invalid scopes stop all four routes before downstream calls")

                original_context = c.retrieve_with_context
                with mock.patch.object(
                    c, "retrieve_with_context", wraps=original_context
                ) as spy:
                    status, body = request(
                        base, "/api/search/context",
                        {"q": "shared seed needle", "source_id": ids[0]},
                    )
                    assert status == 200
                    assert spy.call_count == 1
                    assert spy.call_args.kwargs["source_id"] == ids[0]
                    assert body["seed_results"]
                ok("valid request positive control uses monitored namespace")

                with (
                    mock.patch.object(
                        c, "retrieve_with_context", wraps=original_context
                    ) as retrieval_spy,
                    mock.patch.object(
                        relationships, "resolve_related",
                        return_value={"relationships": []},
                    ) as enrichment,
                ):
                    status, body = request(
                        base, "/api/search/evidence",
                        {"q": "shared seed needle", "source_id": ids[0]},
                    )
                    assert status == 200
                    assert retrieval_spy.call_count == enrichment.call_count == 1
                    bundle = body["retrieval_context"]
                    assert all(
                        item["commit_sha"] == shas[0]
                        for item in (
                            bundle["seed_results"]
                            + bundle["supplementary_context"]
                        )
                    )
                ok("scoped evidence HTTP; enrichment mocked at its boundary")

                status, listing = request(base, "/api/sources")
                assert status == 200
                assert {
                    item["source_id"] for item in listing["sources"]
                } == set(ids)

                status, viewed = request(
                    base, "/api/sources/view", {"source_id": ids[1]}
                )
                assert status == 200
                assert viewed["text"] == texts[1]
                assert viewed["source"]["sha"] == shas[1]
                ok("source list and complete pinned-source JSON")

                assert request(base, "/api/sources/view")[0] == 400
                status, missing = request(
                    base, "/api/sources/view", {"source_id": ids[2]}
                )
                assert status == 404 and "text" not in missing
                assert "WORKTREE_FALLBACK_CANARY" not in json.dumps(missing)
                ok("real missing Git object fails without worktree fallback")

                malformed = (
                    entries + [dict(entries[0])],
                    [{**entries[0], "sha": "bad"}],
                    [{**entries[0], "path": "../notes.md"}],
                    [{**entries[0], "path": "a//notes.md"}],
                )
                for bad in malformed:
                    with (
                        mock.patch.object(r, "load_manifest", return_value=bad),
                        mock.patch.object(c, "retrieve_with_context") as blocked,
                    ):
                        status, _ = request(
                            base, "/api/search/context",
                            {"q": "needle", "source_id": ids[0]},
                        )
                        assert status == 500
                        blocked.assert_not_called()
                ok("duplicate and malformed manifests fail closed")

    print("FOCUSED_CHECKS_PASSED:", passed)
    print("TEMPORARY_TEST_GIT_COMMITS=2")
    print("PROJECT_GIT_COMMITS=0")


def test_source_scope_boundary_contract():
    import retrieve
    import context
    import api
    import relationships

    focused_tests(retrieve, context, api, relationships)
