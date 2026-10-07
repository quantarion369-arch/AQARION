#!/usr/bin/env python3

import tempfile
import unittest
from pathlib import Path

import replay_controller as replay


class ReplayControllerTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

        fixture_dir = (
            self.root
            / "tests"
            / "fixtures"
        )

        fixture_dir.mkdir(parents=True)

        (self.root / "tests" / "test_sample.py").write_text(
            """
def test_alpha():
    pass


class TestBeta:
    def test_gamma(self):
        pass

    def helper(self):
        pass
""",
            encoding="utf-8",
        )

        (
            fixture_dir / "sample.json"
        ).write_text(
            '{"ok":true}\n',
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_rejects_parent_traversal(self):
        with self.assertRaises(ValueError):
            replay.safe_rel("../escape")

    def test_rejects_absolute_path(self):
        with self.assertRaises(ValueError):
            replay.safe_rel("/escape")

    def test_rejects_dot_and_empty(self):
        with self.assertRaises(ValueError):
            replay.safe_rel(".")
        with self.assertRaises(ValueError):
            replay.safe_rel("")

    def test_missing_manifest_file_fails(self):
        status, findings = replay.manifest_check(
            [
                {
                    "path": "present.txt",
                    "bytes": 1,
                    "sha256": "abc",
                }
            ],
            [
                {
                    "path": "missing.txt",
                    "sha256": None,
                }
            ],
            "report",
        )

        self.assertEqual(status, replay.FAIL)

        self.assertIn(
            "EXPECTED_FILE_ABSENT:missing.txt",
            findings,
        )

    def test_wrong_manifest_hash_fails(self):
        status, findings = replay.manifest_check(
            [
                {
                    "path": "present.txt",
                    "bytes": 1,
                    "sha256": "abc",
                }
            ],
            [
                {
                    "path": "present.txt",
                    "sha256": "different",
                }
            ],
            "report",
        )

        self.assertEqual(status, replay.FAIL)

        self.assertIn(
            "EXPECTED_FILE_HASH_WRONG:present.txt",
            findings,
        )

    def test_strict_unexpected_file_fails(self):
        status, findings = replay.manifest_check(
            [
                {
                    "path": "expected.txt",
                    "bytes": 1,
                    "sha256": "abc",
                },
                {
                    "path": "unexpected.py",
                    "bytes": 1,
                    "sha256": "def",
                },
            ],
            [
                {
                    "path": "expected.txt",
                    "sha256": None,
                }
            ],
            "reject",
        )

        self.assertEqual(status, replay.FAIL)

        self.assertIn(
            "UNEXPECTED_FILE_PRESENT:unexpected.py",
            findings,
        )

    def test_fixture_hash_passes(self):
        fixture = (
            self.root
            / "tests"
            / "fixtures"
            / "sample.json"
        )

        digest = replay.sha256_file(fixture)

        status, findings = replay.fixture_check(
            self.root,
            [
                {
                    "path": "tests/fixtures/sample.json",
                    "sha256": digest,
                }
            ],
        )

        self.assertEqual(status, replay.PASS)
        self.assertEqual(findings, [])

    def test_static_test_discovery(self):
        status, identifiers, digest = (
            replay.discover_tests(
                self.root,
                ["tests/test_sample.py"],
            )
        )

        self.assertEqual(status, replay.PASS)

        self.assertIn(
            "tests/test_sample.py::test_alpha",
            identifiers,
        )

        self.assertIn(
            "tests/test_sample.py::TestBeta",
            identifiers,
        )

        self.assertIn(
            "tests/test_sample.py::TestBeta::test_gamma",
            identifiers,
        )

        self.assertNotIn(
            "tests/test_sample.py::TestBeta::helper",
            identifiers,
        )

        self.assertEqual(len(digest), 64)

    def test_execution_requires_authorization(self):
        status, reason, code = replay.execute_tests(
            self.root,
            [
                "python",
                "-c",
                "raise SystemExit(0)",
            ],
            5,
            False,
        )

        self.assertEqual(
            status,
            replay.INCOMPLETE,
        )

        self.assertEqual(
            reason,
            "EXECUTION_NOT_AUTHORIZED",
        )

        self.assertIsNone(code)

    def test_mutation_changes_hash(self):
        status, reason = replay.mutation_check(
            self.root,
            "tests/fixtures/sample.json",
            "byte-flip-hash-must-change",
        )

        self.assertEqual(status, replay.PASS)

        self.assertEqual(
            reason,
            "BYTE_FLIP_CHANGED_SHA256",
        )

    def test_mutation_unsupported_mode_fails(self):
        status, reason = replay.mutation_check(
            self.root,
            "tests/fixtures/sample.json",
            "delete-and-pray",
        )

        self.assertEqual(status, replay.FAIL)
        self.assertTrue(
            reason.startswith("MUTATION_MODE_UNSUPPORTED:")
        )

    def test_policy_rejects_empty_required_files(self):
        path = self.root / "policy.json"
        path.write_text(
            '{"repository":"r","commit":"0"*40,"package_path":"p",'
            '"archive":{"max_bytes":1,"max_files":1,"max_file_bytes":1},'
            '"required_files":[],'
            '"required_tests":[],'
            '"execution":{"allow_exec":false,"command":[],"timeout_seconds":1},'
            '"mutations":{"required":true,"fixture":"x","mode":"byte-flip-hash-must-change"},'
            '"unexpected_files":"report",'
            '"limits":{"extracted_bytes":1,"receipt_bytes":1}}',
            encoding="utf-8",
        )
        with self.assertRaises(ValueError):
            replay.load_policy(path)

    def test_policy_rejects_unknown_mutation_mode(self):
        path = self.root / "policy.json"
        path.write_text(
            '{"repository":"r","commit":"0"*40,"package_path":"p",'
            '"archive":{"max_bytes":1,"max_files":1,"max_file_bytes":1},'
            '"required_files":[{"path":"a","sha256":null}],'
            '"required_tests":[],'
            '"execution":{"allow_exec":false,"command":[],"timeout_seconds":1},'
            '"mutations":{"required":true,"fixture":"x","mode":"unknown"},'
            '"unexpected_files":"report",'
            '"limits":{"extracted_bytes":1,"receipt_bytes":1}}',
            encoding="utf-8",
        )
        with self.assertRaises(ValueError):
            replay.load_policy(path)

    def test_incomplete_blocks_overall_pass(self):
        stages = {
            "archive": {"status": replay.PASS},
            "inventory": {"status": replay.PASS},
            "manifest": {"status": replay.PASS},
            "fixtures": {"status": replay.PASS},
            "tests": {"status": replay.INCOMPLETE},
            "mutations": {"status": replay.PASS},
        }

        self.assertEqual(
            replay.overall_status(stages),
            replay.INCOMPLETE,
        )

    def test_failure_blocks_overall_pass(self):
        stages = {
            "archive": {"status": replay.PASS},
            "inventory": {"status": replay.PASS},
            "manifest": {"status": replay.FAIL},
            "fixtures": {"status": replay.PASS},
            "tests": {"status": replay.PASS},
            "mutations": {"status": replay.PASS},
        }

        self.assertEqual(
            replay.overall_status(stages),
            replay.FAIL,
        )


if __name__ == "__main__":
    unittest.main()
