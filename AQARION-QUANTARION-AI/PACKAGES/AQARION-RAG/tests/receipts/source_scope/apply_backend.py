import contextlib
import importlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
from http.server import ThreadingHTTPServer
from unittest import mock
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen

sys.dont_write_bytecode = True
HOME = Path.home()
REPO = HOME / "AQARION"
PKG = REPO / "AQARION-QUANTARION-AI/PACKAGES/AQARION-RAG"
WORK = Path(__file__).resolve().parent
TARGETS = ("retrieve.py", "context.py", "api.py")


def edit(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"Patch anchor mismatch: {label}; expected 1, found {count}"
        )
    return text.replace(old, new, 1)


def patch_sources(original):
    r, c, a = [original[name].decode("utf-8") for name in TARGETS]

    helpers = r'''
def source_id(entry):
    return f'{entry["path"]}@{entry["sha"]}'


def validate_manifest(entries=None):
    if entries is None:
        entries = load_manifest()
    if not isinstance(entries, list):
        raise ValueError("Manifest must contain a list")
    seen = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Invalid manifest entry")
        path = entry.get("path")
        sha = entry.get("sha")
        doc = entry.get("doc")
        if (
            not isinstance(path, str) or not path
            or path != path.strip()
            or "\\" in path
            or any(ord(ch) < 32 for ch in path)
            or any(part in ("", ".", "..") for part in path.split("/"))
        ):
            raise ValueError("Invalid repository-relative path")
        if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-fA-F]{40}", sha):
            raise ValueError("Invalid full pinned SHA")
        if not isinstance(doc, str) or not doc.strip():
            raise ValueError("Invalid document label")
        identity = (path, sha.lower())
        if identity in seen:
            raise ValueError("Duplicate manifest path/revision")
        seen.add(identity)
    return entries


def resolve_source_id(value, entries=None):
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError("Invalid source selector")
    matches = [
        entry for entry in validate_manifest(entries)
        if source_id(entry) == value
    ]
    if len(matches) != 1:
        raise KeyError("Unknown source selector")
    return matches[0]


'''
    r = edit(r, "def stem(w):\n",
             helpers + "def stem(w):\n", "identity helpers")
    r = edit(r, "def retrieve_cited(query, top_k=3):",
             "def retrieve_cited(query, top_k=3, source_id=None):",
             "cited signature")
    r = edit(
        r,
        "    for entry in load_manifest():\n",
        "    entries = load_manifest()\n"
        "    if source_id is not None:\n"
        "        entries = [resolve_source_id(source_id, entries)]\n"
        "    for entry in entries:\n",
        "restriction before ranking",
    )
    r = edit(r, "def retrieve(query, top_k=3):",
             "def retrieve(query, top_k=3, source_id=None):",
             "legacy signature")
    r = edit(
        r,
        "for item in retrieve_cited(query, top_k=top_k)",
        "for item in (\n"
        "            retrieve_cited(query, top_k=top_k)\n"
        "            if source_id is None else\n"
        "            retrieve_cited(query, top_k=top_k, source_id=source_id)\n"
        "        )",
        "legacy scoped forwarding",
    )

    c = edit(
        c,
        '        if source not in entries:\n'
        '            raise ValueError("Seed source is not in the pinned manifest")\n',
        '        if source not in entries:\n'
        '            raise ValueError("Seed source is not in the pinned manifest")\n'
        '        if seed.get("doc") != entries[source]["doc"]:\n'
        '            raise ValueError("Seed document label does not match manifest")\n',
        "seed label validation",
    )
    c = edit(c, "def retrieve_with_context(query):",
             "def retrieve_with_context(query, source_id=None):",
             "context signature")
    c = edit(
        c,
        "    return _expand_context(retrieve.retrieve_cited(query, top_k=3))",
        "    if source_id is None:\n"
        "        return _expand_context(retrieve.retrieve_cited(query, top_k=3))\n"
        "    entry = retrieve.resolve_source_id(source_id)\n"
        "    seeds = retrieve.retrieve_cited(query, top_k=3, source_id=source_id)\n"
        '    expected = (entry["path"], entry["sha"])\n'
        '    if any((s["path"], s["commit_sha"]) != expected for s in seeds):\n'
        '        raise ValueError("Scoped seed crossed source boundary")\n'
        "    return _expand_context(seeds)",
        "context scoped forwarding",
    )

    a = edit(
        a, "import json\n",
        "import json\nimport subprocess\nimport retrieve as retrieval_module\n",
        "explicit retrieval module alias",
    )
    a = edit(
        a, "from urllib.parse import urlparse, parse_qs\n",
        "from urllib.parse import urlparse, parse_qs, parse_qsl\n",
        "raw query parser",
    )

    routes = '''        source_scope = None
        selected_entry = None
        scoped_routes = {
            "/api/search", "/api/search/cited", "/api/search/context",
            "/api/search/evidence", "/api/sources/view",
        }
        if url.path in scoped_routes:
            values = [
                value for key, value in
                parse_qsl(url.query, keep_blank_values=True)
                if key == "source_id"
            ]
            if len(values) > 1 or (
                values and (
                    not values[0] or values[0] != values[0].strip()
                )
            ):
                self._send({"error": "invalid source_id parameter"}, 400)
                return
            if values:
                source_scope = values[0]
                try:
                    selected_entry = retrieval_module.resolve_source_id(
                        source_scope
                    )
                except KeyError:
                    self._send({"error": "unknown source_id"}, 404)
                    return
                except Exception:
                    self._send({"error": "manifest validation failed"}, 500)
                    return

        if url.path == "/api/sources":
            try:
                entries = retrieval_module.validate_manifest()
                self._send({"sources": [
                    {
                        "source_id": retrieval_module.source_id(entry),
                        "doc": entry["doc"],
                        "path": entry["path"],
                        "sha": entry["sha"],
                        "purpose": entry.get("purpose", ""),
                    }
                    for entry in entries
                ]})
            except Exception:
                self._send({"error": "manifest validation failed"}, 500)

        elif url.path == "/api/sources/view":
            if selected_entry is None:
                self._send({"error": "source_id is required"}, 400)
                return
            try:
                text = retrieval_module.load_at_sha(
                    selected_entry["path"], selected_entry["sha"]
                )
                self._send({
                    "source": {"source_id": source_scope, **selected_entry},
                    "text": text,
                })
            except subprocess.CalledProcessError:
                self._send({"error": "pinned Git object unavailable"}, 404)
            except Exception:
                self._send({"error": "pinned source loading failed"}, 500)

        elif url.path == "/":
'''
    a = edit(a, '        if url.path == "/":\n',
             routes, "scope validation and source routes")
    a = edit(
        a,
        "            retrieval_context = context.retrieve_with_context(q)\n",
        "            if source_scope is None:\n"
        "                retrieval_context = context.retrieve_with_context(q)\n"
        "            else:\n"
        "                retrieval_context = context.retrieve_with_context(\n"
        "                    q, source_id=source_scope)\n",
        "evidence route",
    )
    a = edit(
        a,
        "            self._send(context.retrieve_with_context(q))\n",
        "            if source_scope is None:\n"
        "                self._send(context.retrieve_with_context(q))\n"
        "            else:\n"
        "                self._send(context.retrieve_with_context(\n"
        "                    q, source_id=source_scope))\n",
        "context route",
    )
    for function in ("retrieve", "retrieve_cited"):
        a = edit(
            a,
            f"            results = {function}(q, top_k=3)\n",
            "            if source_scope is None:\n"
            f"                results = {function}(q, top_k=3)\n"
            "            else:\n"
            f"                results = {function}(\n"
            "                    q, top_k=3, source_id=source_scope)\n",
            function + " route",
        )

    proposed = dict(zip(TARGETS, (r, c, a)))
    for name, source in proposed.items():
        compile(source, name, "exec")
    return {
        name: source.encode("utf-8")
        for name, source in proposed.items()
    }


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


def snapshot(r, c, api):
    results = {}
    with http_server(api) as base:
        for query in (
            "quadratic stability",
            "observable closure",
            "zzzzqxxnomatch",
        ):
            results[query] = {
                "legacy": r.retrieve(query),
                "cited": r.retrieve_cited(query),
                "context": c.retrieve_with_context(query),
                "http": {
                    route: request(base, route, {"q": query})
                    for route in (
                        "/api/search", "/api/search/cited",
                        "/api/search/context", "/api/search/evidence",
                    )
                },
            }
    return json.loads(json.dumps(results))


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


def main():
    root = subprocess.check_output(
        ["git", "-C", str(REPO), "rev-parse", "--show-toplevel"],
        text=True,
    ).strip()
    if Path(root).resolve() != REPO.resolve():
        raise RuntimeError("Unexpected repository root")

    relative = [
        str((PKG / name).relative_to(REPO))
        for name in TARGETS
    ]
    for flags in (
        ["diff", "--quiet", "HEAD"],
        ["diff", "--cached", "--quiet", "HEAD"],
    ):
        result = subprocess.run(
            ["git", "-C", str(REPO), *flags, "--", *relative]
        )
        if result.returncode:
            raise RuntimeError(
                "Existing backend changes detected. Nothing patched."
            )

    if importlib.util.find_spec("pytest") is None:
        raise RuntimeError("pytest unavailable; no install or patch attempted")

    if any((PKG / name).is_symlink() for name in TARGETS):
        raise RuntimeError("Backend symlink detected; nothing patched")

    original = {
        name: (PKG / name).read_bytes()
        for name in TARGETS
    }
    proposed = patch_sources(original)

    backup = WORK / "original"
    backup.mkdir()
    for name in TARGETS:
        shutil.copy2(PKG / name, backup / name)

    sys.path.insert(0, str(PKG))
    changed = False

    try:
        import retrieve as r
        import context as c
        import api
        import relationships

        before = snapshot(r, c, api)
        (WORK / "global-before.json").write_text(
            json.dumps(before, indent=2), encoding="utf-8"
        )

        if any(
            (PKG / name).read_bytes() != original[name]
            for name in TARGETS
        ):
            raise RuntimeError("Backend changed during baseline capture")

        changed = True
        for name, data in proposed.items():
            (PKG / name).write_bytes(data)

        importlib.invalidate_caches()
        importlib.reload(r)
        importlib.reload(c)
        importlib.reload(api)

        after = snapshot(r, c, api)
        (WORK / "global-after.json").write_text(
            json.dumps(after, indent=2), encoding="utf-8"
        )

        if before != after:
            raise AssertionError(
                "Pre/post global retrieval or HTTP outputs changed"
            )
        print("GENUINE_GLOBAL_BEFORE_AFTER=PASS", flush=True)

        focused_tests(r, c, api, relationships)

        completed = subprocess.run(
            [
                sys.executable, "-B", "-m", "pytest",
                "-q", "-p", "no:cacheprovider", "tests",
            ],
            cwd=PKG,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
        )
        (WORK / "existing-suite.log").write_text(
            completed.stdout, encoding="utf-8"
        )
        print(completed.stdout, flush=True)
        if completed.returncode:
            raise RuntimeError("Existing package test suite failed")

        subprocess.run(
            ["git", "-C", str(REPO), "diff", "--check", "--", *relative],
            check=True,
        )
        subprocess.run(
            [
                "git", "-C", str(REPO), "--no-pager",
                "diff", "--stat", "--", *relative,
            ],
            check=True,
        )

        print("\nSOURCE_SCOPE_BACKEND=PASS")
        print("EXISTING_PACKAGE_TESTS=PASS")
        print("BACKUPS_SOURCE_AND_LOGS:", WORK)
        print("BROWSER_UNCHANGED")
        print("CORPUS_AND_NORMALIZATION_UNCHANGED")
        print("DEFECT_RESEARCH_UNCHANGED")
        print("NO_STAGE_COMMIT_PUSH_OR_INSTALL")
        print("HUGGING_FACE_UNCHANGED")

    except BaseException:
        if changed:
            for name, data in original.items():
                (PKG / name).write_bytes(data)
            if not all(
                (PKG / name).read_bytes() == original[name]
                for name in TARGETS
            ):
                raise RuntimeError("RESTORATION VERIFICATION FAILED")
            print("BACKEND_RESTORE=VERIFIED", flush=True)
        print("SOURCE_SCOPE_BACKEND=FAIL", flush=True)
        print("SOURCE_BACKUPS_AND_LOGS:", WORK, flush=True)
        raise


if __name__ == "__main__":
    main()
