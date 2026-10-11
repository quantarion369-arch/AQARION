"""Acceptance tests for Mobile Research Kit workflow evidence."""

import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_workflow_evidence import validate_evidence


TEST_ENVIRONMENT = {
    "GITHUB_REPOSITORY": "quantarion369-arch/AQARION",
    "GITHUB_SHA": "0123456789abcdef0123456789abcdef01234567",
    "GITHUB_REF": "refs/heads/main",
    "GITHUB_WORKFLOW": "AQARION Mobile Research Kit Validation",
    "GITHUB_EVENT_NAME": "workflow_dispatch",
    "GITHUB_RUN_ID": "123456789",
    "GITHUB_RUN_ATTEMPT": "1",
    "GITHUB_SERVER_URL": "https://github.com",
}


class WorkflowEvidenceAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)

        self.workflow_dir = self.root / "workflow-test"
        self.run_dir = (
            self.workflow_dir / "runs" / "run-test"
        )
        self.run_dir.mkdir(parents=True)

        self.receipt_path = self.run_dir / "receipt.json"
        self.viewer_path = self.workflow_dir / "viewer.html"
        self.inventory_path = self.workflow_dir / "inventory.json"

        self._write_valid_evidence()

    def tearDown(self):
        self.tempdir.cleanup()

    def _write_valid_evidence(self):
        (self.run_dir / "stdout.txt").write_text(
            "REGRESSION_OK\n", encoding="utf-8"
        )
        (self.run_dir / "stderr.txt").write_text(
            "", encoding="utf-8"
        )

        receipt = {
            "schema_version": "0.1.0",
            "kind": "command_execution",
            "status": "completed",
            "started_at_utc": "2026-10-11T12:00:00+00:00",
            "ended_at_utc": "2026-10-11T12:00:01+00:00",
            "command": ["python", "tools/run_regression.py"],
            "stdout_file": "stdout.txt",
            "stderr_file": "stderr.txt",
            "recorder_exit": 0,
            "child_returncode": 0,
        }

        self.receipt_path.write_text(
            json.dumps(receipt), encoding="utf-8"
        )
        self.viewer_path.write_text(
            "<!doctype html><title>Evidence</title>",
            encoding="utf-8",
        )
        self.inventory_path.write_text(
            json.dumps({"python": "3.x", "platform": "test"}),
            encoding="utf-8",
        )

    def _validate(self):
        return validate_evidence(self.root, TEST_ENVIRONMENT)

    def test_valid_evidence_passes_and_binds_run(self):
        metadata = self._validate()

        self.assertTrue(metadata["acceptance_passed"])
        self.assertEqual(metadata["acceptance_failures"], [])
        self.assertEqual(
            metadata["repository"],
            TEST_ENVIRONMENT["GITHUB_REPOSITORY"],
        )
        self.assertEqual(
            metadata["commit_sha"],
            TEST_ENVIRONMENT["GITHUB_SHA"],
        )
        self.assertEqual(metadata["run_id"], "123456789")
        self.assertEqual(metadata["run_attempt"], "1")
        self.assertEqual(
            metadata["run_url"],
            "https://github.com/quantarion369-arch/AQARION/"
            "actions/runs/123456789",
        )
        self.assertTrue(metadata["receipt_sha256"])
        self.assertTrue(metadata["viewer_sha256"])
        self.assertTrue(metadata["inventory_sha256"])

        metadata_path = self.root / "run-metadata.json"
        self.assertTrue(metadata_path.is_file())

        saved = json.loads(metadata_path.read_text(encoding="utf-8"))
        self.assertTrue(saved["acceptance_passed"])

    def test_missing_receipt_fails(self):
        self.receipt_path.unlink()

        metadata = self._validate()

        self.assertFalse(metadata["acceptance_passed"])
        self.assertTrue(any(
            "expected exactly one receipt" in failure
            for failure in metadata["acceptance_failures"]
        ))

    def test_missing_viewer_fails(self):
        self.viewer_path.unlink()

        metadata = self._validate()

        self.assertFalse(metadata["acceptance_passed"])
        self.assertTrue(any(
            "expected exactly one viewer" in failure
            for failure in metadata["acceptance_failures"]
        ))

    def test_missing_inventory_fails(self):
        self.inventory_path.unlink()

        metadata = self._validate()

        self.assertFalse(metadata["acceptance_passed"])
        self.assertTrue(any(
            "expected exactly one inventory" in failure
            for failure in metadata["acceptance_failures"]
        ))

    def test_malformed_receipt_fails(self):
        self.receipt_path.write_text("{bad json", encoding="utf-8")

        metadata = self._validate()

        self.assertFalse(metadata["acceptance_passed"])
        self.assertTrue(any(
            "execution receipt is not readable valid JSON" in failure
            for failure in metadata["acceptance_failures"]
        ))

    def test_started_receipt_fails(self):
        record = json.loads(
            self.receipt_path.read_text(encoding="utf-8")
        )
        record["status"] = "started"
        record.pop("ended_at_utc", None)

        self.receipt_path.write_text(
            json.dumps(record), encoding="utf-8"
        )

        metadata = self._validate()

        self.assertFalse(metadata["acceptance_passed"])
        self.assertTrue(any(
            "receipt was not finalized" in failure
            for failure in metadata["acceptance_failures"]
        ))
        self.assertTrue(any(
            "receipt has no ended_at_utc" in failure
            for failure in metadata["acceptance_failures"]
        ))

    def test_missing_output_file_fails(self):
        (self.run_dir / "stdout.txt").unlink()

        metadata = self._validate()

        self.assertFalse(metadata["acceptance_passed"])
        self.assertTrue(any(
            "missing or empty recorded output file: stdout_file" in failure
            for failure in metadata["acceptance_failures"]
        ))

    def test_malformed_inventory_fails(self):
        self.inventory_path.write_text("{bad json", encoding="utf-8")

        metadata = self._validate()

        self.assertFalse(metadata["acceptance_passed"])
        self.assertTrue(any(
            "environment inventory is not readable valid JSON" in failure
            for failure in metadata["acceptance_failures"]
        ))

    def test_missing_run_binding_fails(self):
        incomplete_environment = dict(TEST_ENVIRONMENT)
        incomplete_environment.pop("GITHUB_SHA")

        metadata = validate_evidence(self.root, incomplete_environment)

        self.assertFalse(metadata["acceptance_passed"])
        self.assertTrue(any(
            "missing GitHub run-binding field: GITHUB_SHA" in failure
            for failure in metadata["acceptance_failures"]
        ))

    def test_nonzero_child_is_valid_process_evidence(self):
        """A failed child can still have structurally valid evidence."""
        record = json.loads(
            self.receipt_path.read_text(encoding="utf-8")
        )
        record["recorder_exit"] = 1
        record["child_returncode"] = 1

        self.receipt_path.write_text(
            json.dumps(record), encoding="utf-8"
        )
        (self.run_dir / "stdout.txt").write_text(
            "REGRESSION_FAILED\n", encoding="utf-8"
        )

        metadata = self._validate()

        # Evidence integrity passes; the regression step's own exit code
        # is what keeps the GitHub job failed.
        self.assertTrue(metadata["acceptance_passed"])
        self.assertEqual(metadata["recorder_exit"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
