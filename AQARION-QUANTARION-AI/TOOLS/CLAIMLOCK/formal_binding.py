"""Formal binding contract checks. No network, builds, or status writes.
Approved digests are operator-reviewed policy, never registry-controlled.
The empty production catalogs intentionally authorize no new evidence.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess

APPROVED_RECEIPTS = frozenset()
APPROVED_REVIEWS = frozenset()
OK_AXIOMS = frozenset({"propext", "Classical.choice", "Quot.sound"})
REPO = "https://github.com/quantarion369-arch/AQARION-LEAN"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(data):
    return json.dumps(
        data, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()


def fields(data, names):
    require(isinstance(data, dict), "expected an object")
    require(
        set(names) <= set(data),
        "missing fields: " + str(sorted(set(names) - set(data))),
    )


def safe_file(root, relative):
    require(isinstance(relative, str) and bool(relative), "invalid relative path")
    path = Path(relative)
    require(not path.is_absolute() and ".." not in path.parts, "unsafe path")
    current = Path(root).resolve()
    for part in path.parts:
        current = current / part
        require(not current.is_symlink(), "symlinked input")
    require(current.is_file(), "missing file: " + relative)
    return current


def sha_value(value):
    return (
        isinstance(value, str)
        and re.fullmatch("[0-9a-f]{64}", value) is not None
    )


def git(root, *args):
    return subprocess.check_output(
        ["git", "-C", str(root), *args],
        stderr=subprocess.PIPE,
        timeout=15,
    )


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        require(key not in obj, "duplicate JSON key: " + key)
        obj[key] = value
    return obj


def check_binding(
    record, claim_root, lean_root,
    *, approved_receipts=None, approved_reviews=None
):
    receipts = APPROVED_RECEIPTS if approved_receipts is None else approved_receipts
    reviews = APPROVED_REVIEWS if approved_reviews is None else approved_reviews

    fields(record, ["id", "record_type", "claim_text", "status", "formal_evidence"])
    require(record["record_type"] == "formal", "not a formal record")
    require(
        isinstance(record["claim_text"], str) and bool(record["claim_text"].strip()),
        "empty claim text",
    )
    require(lean_root is not None, "AQARION_FORMAL_LEAN_ROOT is required")

    f = record["formal_evidence"]
    fields(f, [
        "repo", "revision", "source_path", "source_file_sha256",
        "declaration", "statement_sha256", "receipt_path",
        "receipt_sha256", "correspondence_review",
    ])
    require(f["repo"] == REPO, "unapproved formal repository")
    rev = f["revision"]
    require(
        isinstance(rev, str) and re.fullmatch("[0-9a-f]{40}", rev) is not None,
        "invalid revision",
    )
    require(
        all(sha_value(f[k]) for k in (
            "source_file_sha256", "statement_sha256", "receipt_sha256"
        )),
        "invalid or missing SHA256",
    )
    require(
        isinstance(f["declaration"], str)
        and re.fullmatch(
            "[A-Za-z_][A-Za-z0-9_'.]*(?:[.][A-Za-z_][A-Za-z0-9_']*)+",
            f["declaration"],
        ) is not None,
        "invalid qualified declaration",
    )

    origin = git(lean_root, "remote", "get-url", "origin").decode().strip()
    origin = origin.removesuffix(".git").replace(
        "git@github.com:", "https://github.com/"
    )
    require(origin == REPO, "wrong Lean checkout repository")
    require(
        git(lean_root, "rev-parse", "HEAD").decode().strip() == rev,
        "checkout revision mismatch",
    )
    require(
        not git(lean_root, "status", "--porcelain", "--untracked-files=all").strip(),
        "Lean checkout is dirty",
    )

    source = safe_file(lean_root, f["source_path"])
    require(
        digest(source.read_bytes()) == f["source_file_sha256"],
        "source hash mismatch",
    )

    receipt_bytes = safe_file(claim_root, f["receipt_path"]).read_bytes()
    require(
        digest(receipt_bytes) == f["receipt_sha256"],
        "receipt hash mismatch",
    )
    receipt = json.loads(receipt_bytes, object_pairs_hook=unique_object)
    fields(receipt, [
        "kind", "repo", "revision", "declaration", "declaration_type",
        "type_format", "exit_code", "axioms", "source_files",
        "toolchain_path", "lean_toolchain", "compiler_commit",
    ])
    require(receipt["kind"] == "lean_build", "not a Lean build receipt")
    for key in ("repo", "revision", "declaration"):
        require(receipt[key] == f[key], "receipt " + key + " mismatch")

    require(
        type(receipt["exit_code"]) is int and receipt["exit_code"] == 0,
        "build did not record integer exit zero",
    )
    require(
        receipt["type_format"] == "lean-pp-explicit-v1",
        "unsupported declaration type format",
    )
    require(
        isinstance(receipt["declaration_type"], str)
        and bool(receipt["declaration_type"].strip()),
        "empty declaration type",
    )
    require(
        digest(receipt["declaration_type"].encode()) == f["statement_sha256"],
        "statement digest mismatch",
    )

    axioms = receipt["axioms"]
    require(
        isinstance(axioms, list) and all(isinstance(x, str) for x in axioms),
        "malformed axiom dependencies",
    )
    require(
        len(axioms) == len(set(axioms)) and set(axioms) <= OK_AXIOMS,
        "unapproved or duplicated axiom",
    )
    if "allowed_axioms" in f:
        allowed = f["allowed_axioms"]
        require(
            isinstance(allowed, list)
            and all(isinstance(x, str) for x in allowed),
            "malformed per-record allowance",
        )
        require(
            set(allowed) <= OK_AXIOMS and set(axioms) <= set(allowed),
            "record axiom allowance violates policy",
        )

    inputs = receipt["source_files"]
    require(isinstance(inputs, dict) and bool(inputs), "missing build input manifest")
    require(
        inputs.get(f["source_path"]) == f["source_file_sha256"],
        "source not bound in input manifest",
    )
    require(
        receipt["toolchain_path"] in inputs,
        "toolchain not bound in manifest",
    )
    for relative, expected in inputs.items():
        require(sha_value(expected), "invalid input hash")
        data = safe_file(lean_root, relative).read_bytes()
        require(
            digest(data) == expected,
            "build input hash mismatch: " + relative,
        )
        require(
            git(lean_root, "show", rev + ":" + relative) == data,
            "input differs from pinned Git blob",
        )

    pin = safe_file(lean_root, receipt["toolchain_path"]).read_text().strip()
    require(pin == receipt["lean_toolchain"], "compiler pin mismatch")
    require(
        isinstance(receipt["compiler_commit"], str)
        and re.fullmatch("[0-9a-f]{40}", receipt["compiler_commit"]) is not None,
        "missing compiler revision",
    )
    require(
        f["receipt_sha256"] in receipts,
        "receipt provenance not enrolled in trusted policy",
    )

    review = f["correspondence_review"]
    fields(review, ["state", "reviewer"])
    require(review["state"] in {"pending", "approved"}, "invalid review state")
    if review["state"] == "approved":
        fields(review, [
            "claim_sha256", "revision", "declaration",
            "statement_sha256", "reviewed_at",
        ])
        require(
            isinstance(review["reviewer"], str) and bool(review["reviewer"].strip()),
            "missing reviewer",
        )
        require(
            isinstance(review["reviewed_at"], str)
            and bool(review["reviewed_at"].strip()),
            "missing review time",
        )
        require(
            review["claim_sha256"] == digest(record["claim_text"].encode()),
            "review targets stale claim",
        )
        for key in ("revision", "declaration", "statement_sha256"):
            require(review[key] == f[key], "review targets stale " + key)
        require(
            digest(canonical(review)) in reviews,
            "review approval not enrolled in trusted policy",
        )

    require(
        record["status"] != "proved" or review["state"] == "approved",
        "proved formal claim has pending correspondence review",
    )
    return {
        "technical": "pass",
        "correspondence": review["state"],
        "promotion": "unchanged",
    }


def validate_formal_bindings(records, claim_root, lean_root):
    errors = []
    for record in records:
        if record.get("record_type") != "formal":
            continue
        try:
            check_binding(record, claim_root, lean_root)
        except Exception as exc:
            errors.append(str(record.get("id", "<missing-id>")) + ": " + str(exc))
    return errors
