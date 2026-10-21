"""Synthetic contract tests only: no Lean, network, or project Git writes."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import formal_binding as fb

CASES = (
    "wrong_declaration wrong_revision source_changed dependency_changed "
    "dirty_checkout wrong_repo bad_hash sorry allowance "
    "other_receipt_declaration wrong_kind no_axioms axioms_string "
    "failed_exit string_exit bool_exit untrusted_receipt "
    "wrong_receipt_digest source_not_manifest bad_pin pending_proved "
    "stale_review untrusted_review symlink traversal duplicate_keys"
).split()


class BindingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.lean = self.root / "lean"
        self.lean.mkdir()
        self.rev = "a" * 40
        self.origin = fb.REPO + ".git"
        self.dirty = b""
        self.blobs = {
            "Module.lean": b"-- synthetic fixture only",
            "Dependency.lean": b"-- synthetic dependency",
            "lean-toolchain": b"leanprover/lean4:v4.35.0-rc4",
        }
        for name, data in self.blobs.items():
            (self.lean / name).write_bytes(data)

        self.record = {
            "id": "TEST-FORMAL-001",
            "record_type": "formal",
            "title": "Synthetic contract test",
            "claim_text": "Synthetic statement; not a proof",
            "status": "open",
            "governance": "blocked",
            "evidence": "Synthetic fixture",
            "note": "No mathematics certified",
            "formal_evidence": {
                "repo": fb.REPO,
                "revision": self.rev,
                "source_path": "Module.lean",
                "source_file_sha256": fb.digest(self.blobs["Module.lean"]),
                "declaration": "Fixture.theorem",
                "statement_sha256": fb.digest(b"fixture type"),
                "receipt_path": "receipt.json",
                "receipt_sha256": "",
                "correspondence_review": {
                    "state": "pending",
                    "reviewer": None,
                },
            },
        }
        self.receipt = {
            "kind": "lean_build",
            "repo": fb.REPO,
            "revision": self.rev,
            "declaration": "Fixture.theorem",
            "declaration_type": "fixture type",
            "type_format": "lean-pp-explicit-v1",
            "exit_code": 0,
            "axioms": sorted(fb.OK_AXIOMS),
            "source_files": {
                name: fb.digest(data)
                for name, data in self.blobs.items()
            },
            "toolchain_path": "lean-toolchain",
            "lean_toolchain": self.blobs["lean-toolchain"].decode(),
            "compiler_commit": "c" * 40,
        }
        self.enroll = True
        self.review_enroll = True
        self.raw_duplicate = False

        def fake_git(root, *args):
            if args == ("remote", "get-url", "origin"):
                return self.origin.encode()
            if args == ("rev-parse", "HEAD"):
                return self.rev.encode()
            if args[0] == "status":
                return self.dirty
            if args[0] == "show":
                return self.blobs[args[1].split(":", 1)[1]]
            raise AssertionError(args)

        self.addCleanup(patch.stopall)
        patch("formal_binding.git", side_effect=fake_git).start()

    def approve_review(self):
        f = self.record["formal_evidence"]
        f["correspondence_review"] = {
            "state": "approved",
            "reviewer": "SYNTHETIC TEST REVIEWER",
            "reviewed_at": "2026-10-21T00:00:00Z",
            "claim_sha256": fb.digest(self.record["claim_text"].encode()),
            "revision": f["revision"],
            "declaration": f["declaration"],
            "statement_sha256": f["statement_sha256"],
        }

    def run_check(self):
        f = self.record["formal_evidence"]
        raw = fb.canonical(self.receipt)
        if self.raw_duplicate:
            raw = b'{"kind":"lean_build",' + raw[1:]

        (self.root / "receipt.json").write_bytes(raw)
        f["receipt_sha256"] = fb.digest(raw)

        if getattr(self, "wrong_digest", False):
            f["receipt_sha256"] = "0" * 64

        if getattr(self, "use_symlink", False):
            (self.root / "link.json").symlink_to("receipt.json")
            f["receipt_path"] = "link.json"

        allowed = {fb.digest(raw)} if self.enroll else set()
        reviews = (
            {fb.digest(fb.canonical(f["correspondence_review"]))}
            if self.review_enroll else set()
        )
        return fb.check_binding(
            self.record,
            self.root,
            self.lean,
            approved_receipts=allowed,
            approved_reviews=reviews,
        )

    def test_valid_pending_does_not_promote(self):
        before = copy.deepcopy(self.record)
        self.assertEqual(
            self.run_check(),
            {
                "technical": "pass",
                "correspondence": "pending",
                "promotion": "unchanged",
            },
        )
        self.assertEqual(self.record["status"], before["status"])
        self.assertEqual(self.record["governance"], before["governance"])

    def test_valid_reviewed_proved(self):
        self.approve_review()
        self.record["status"] = "proved"
        self.assertEqual(self.run_check()["correspondence"], "approved")

    def test_valid_empty_axiom_list(self):
        self.receipt["axioms"] = []
        self.assertEqual(self.run_check()["technical"], "pass")

    def schema_validator(self):
        path = Path(__file__).resolve().parents[1] / "schemas/registry.schema.json"
        return Draft202012Validator(json.loads(path.read_text()))

    def test_schema_accepts_formal_without_counts(self):
        self.run_check()
        self.schema_validator().validate([self.record])

    def test_schema_rejects_formal_fake_counts(self):
        self.run_check()
        self.record["cases"] = 0
        self.assertFalse(self.schema_validator().is_valid([self.record]))

    def test_schema_preserves_legacy_null_restriction(self):
        legacy = {
            "id": "TEST-LEGACY-001",
            "title": "Fixture",
            "status": "verified",
            "governance": "active",
            "evidence": "Fixture",
            "note": "Fixture",
            "cases": None,
            "violations": None,
            "count_provenance": "not established",
        }
        self.assertFalse(self.schema_validator().is_valid([legacy]))
        legacy["cases"] = 1
        legacy["violations"] = 0
        self.schema_validator().validate([legacy])

    def reject(self, case):
        f = self.record["formal_evidence"]
        r = self.receipt

        if case == "wrong_declaration":
            f["declaration"] = "Fixture.other"
        elif case == "wrong_revision":
            f["revision"] = "b" * 40
        elif case == "source_changed":
            (self.lean / "Module.lean").write_text("changed")
        elif case == "dependency_changed":
            (self.lean / "Dependency.lean").write_text("changed")
        elif case == "dirty_checkout":
            self.dirty = b" M Module.lean"
        elif case == "wrong_repo":
            self.origin = "https://github.com/other/repo"
        elif case == "bad_hash":
            f["source_file_sha256"] = None
        elif case == "sorry":
            r["axioms"].append("sorryAx")
        elif case == "allowance":
            f["allowed_axioms"] = list(fb.OK_AXIOMS) + ["sorryAx"]
        elif case == "other_receipt_declaration":
            r["declaration"] = "Fixture.other"
        elif case == "wrong_kind":
            r["kind"] = "python_census"
        elif case == "no_axioms":
            del r["axioms"]
        elif case == "axioms_string":
            r["axioms"] = "[]"
        elif case == "failed_exit":
            r["exit_code"] = 1
        elif case == "string_exit":
            r["exit_code"] = "0"
        elif case == "bool_exit":
            r["exit_code"] = False
        elif case == "untrusted_receipt":
            self.enroll = False
        elif case == "wrong_receipt_digest":
            self.wrong_digest = True
        elif case == "source_not_manifest":
            del r["source_files"]["Module.lean"]
        elif case == "bad_pin":
            r["lean_toolchain"] = "wrong"
        elif case == "pending_proved":
            self.record["status"] = "proved"
        elif case == "stale_review":
            self.approve_review()
            f["correspondence_review"]["claim_sha256"] = "b" * 64
        elif case == "untrusted_review":
            self.approve_review()
            self.review_enroll = False
        elif case == "symlink":
            self.use_symlink = True
        elif case == "traversal":
            f["source_path"] = "../escape.lean"
        elif case == "duplicate_keys":
            self.raw_duplicate = True
        else:
            raise AssertionError(case)

        with self.assertRaises((ValueError, KeyError, TypeError)):
            self.run_check()


for case in CASES:
    def test(self, case=case):
        self.reject(case)
    setattr(BindingTests, "test_reject_" + case, test)

if __name__ == "__main__":
    unittest.main(verbosity=2)
