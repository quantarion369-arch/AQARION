"""Object integrity controls using disposable Git repositories only."""

import hashlib
import subprocess
import zlib
from unittest import mock

import pytest

import api
import relationships
import retrieve

from tests.test_source_scope import http_server, request


CASES = (
    "valid",
    "corrupt_commit",
    "missing_referenced_blob",
    "wrong_hash_blob",
    "wrong_hash_commit",
    "wrong_hash_tree",
)

ROUTES = (
    "/api/search",
    "/api/search/cited",
    "/api/search/context",
    "/api/search/evidence",
    "/api/sources/view",
)


@pytest.fixture(params=CASES)
def object_case(request, tmp_path, monkeypatch):
    root = tmp_path / "isolated_git"
    root.mkdir()

    # Prevent inherited Git overrides from redirecting fixture operations.
    for name in (
        "GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR",
        "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
        "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    ):
        monkeypatch.delenv(name, raising=False)

    def git(*args, data=None):
        return subprocess.check_output(
            [
                "git",
                "-c", "core.hooksPath=/dev/null",
                "-c", "commit.gpgsign=false",
                "-c", "gc.auto=0",
                "-c", "user.name=Object Integrity Test",
                "-c", "user.email=test@example.invalid",
                "-C", str(root),
                *args,
            ],
            input=data,
        )

    git("init", "-q", "--object-format=sha1")
    notes = root / "notes.md"
    notes.write_bytes(b"needle valid pinned passage\n")
    git("add", "--", "notes.md")
    git("commit", "-q", "-m", "isolated object fixture")

    pin = git("rev-parse", "HEAD").decode().strip()
    tree = git("rev-parse", "HEAD^{tree}").decode().strip()
    blob = git("rev-parse", "HEAD:notes.md").decode().strip()

    def loose_path(oid):
        path = root / ".git" / "objects" / oid[:2] / oid[2:]
        assert path.is_file()
        return path

    def replace_payload(oid, kind, payload):
        header = (
            kind.encode("ascii")
            + b" "
            + str(len(payload)).encode("ascii")
            + b"\0"
        )
        raw = header + payload

        # This fixture deliberately stores bytes under the wrong identity.
        assert hashlib.sha1(raw).hexdigest() != oid

        path = loose_path(oid)
        path.chmod(0o600)
        path.write_bytes(zlib.compress(raw))

    case = request.param

    if case == "corrupt_commit":
        path = loose_path(pin)
        path.chmod(0o600)
        path.write_bytes(b"not a valid compressed Git object")

    elif case == "missing_referenced_blob":
        loose_path(blob).unlink()

    elif case == "wrong_hash_blob":
        replace_payload(
            blob, "blob", b"needle ALTERED_CONTENT\n"
        )

    elif case == "wrong_hash_commit":
        payload = git("cat-file", "commit", pin)
        assert b"\n\n" in payload
        changed = payload.replace(
            b"\n\n", b"\n\nALTERED_MESSAGE\n", 1
        )
        replace_payload(pin, "commit", changed)

    elif case == "wrong_hash_tree":
        alternate = git(
            "hash-object", "-w", "--stdin",
            data=b"needle ALTERED_TREE_TARGET\n",
        ).decode().strip()

        payload = git("cat-file", "tree", tree)
        original_oid = bytes.fromhex(blob)
        assert payload.count(original_oid) == 1

        changed = payload.replace(
            original_oid, bytes.fromhex(alternate), 1
        )
        replace_payload(tree, "tree", changed)

    notes.write_text(
        "WORKTREE_FALLBACK_CANARY", encoding="utf-8"
    )

    monkeypatch.setattr(
        retrieve, "__file__", str(root / "retrieve.py")
    )

    entry = {
        "doc": "Isolated integrity fixture",
        "path": "notes.md",
        "sha": pin,
        "purpose": "Disposable object-integrity test",
    }
    return case, entry


def test_loader_object_integrity(object_case):
    case, entry = object_case

    if case == "valid":
        result = retrieve.load_at_sha(
            entry["path"], entry["sha"]
        )
        assert result == "needle valid pinned passage\n"
        assert "WORKTREE_FALLBACK_CANARY" not in result
        return

    with pytest.raises(retrieve.PinnedSourceLoadError):
        retrieve.load_at_sha(entry["path"], entry["sha"])


@pytest.mark.parametrize("route", ROUTES)
def test_http_object_integrity(object_case, route):
    case, entry = object_case

    with (
        mock.patch.object(
            retrieve, "load_manifest", return_value=[entry]
        ),
        mock.patch.object(
            relationships, "resolve_related",
            return_value={"relationships": []},
        ) as enrichment,
        http_server(api) as base,
    ):
        status, body = request(
            base, route,
            {
                "q": "needle",
                "source_id": retrieve.source_id(entry),
            },
        )

        if case == "valid":
            assert status == 200
            assert "needle valid pinned passage" in str(body)
        else:
            assert status == 500
            assert body == {"error": "pinned source loading failed"}
            enrichment.assert_not_called()

        assert "WORKTREE_FALLBACK_CANARY" not in str(body)
        assert "ALTERED_CONTENT" not in str(body)
        assert "ALTERED_TREE_TARGET" not in str(body)


@pytest.mark.parametrize(
    "payload",
    (
        b"",
        b"first\r\nsecond\rthird\n",
        b"\xcf\x80 and \xce\xbb\n",
        b"\xff\xfe",
    ),
    ids=("empty", "mixed_newlines", "unicode", "undecodable"),
)
def test_verified_blob_preserves_text_behavior(
    payload, tmp_path, monkeypatch
):
    def git(*args, text=False):
        return subprocess.check_output(
            [
                "git",
                "-c", "core.hooksPath=/dev/null",
                "-c", "commit.gpgsign=false",
                "-c", "user.name=Blob Compatibility Test",
                "-c", "user.email=test@example.invalid",
                "-C", str(tmp_path),
                *args,
            ],
            text=text,
        )

    git("init", "-q", "--object-format=sha1")
    (tmp_path / "notes.md").write_bytes(payload)
    git("add", "--", "notes.md")
    git("commit", "-q", "-m", "blob compatibility fixture")
    pin = git("rev-parse", "HEAD", text=True).strip()

    monkeypatch.setattr(
        retrieve, "__file__", str(tmp_path / "retrieve.py")
    )

    try:
        reference = git("show", pin + ":notes.md", text=True)
    except UnicodeError:
        with pytest.raises(retrieve.PinnedSourceLoadError):
            retrieve.load_at_sha("notes.md", pin)
    else:
        assert retrieve.load_at_sha("notes.md", pin) == reference
