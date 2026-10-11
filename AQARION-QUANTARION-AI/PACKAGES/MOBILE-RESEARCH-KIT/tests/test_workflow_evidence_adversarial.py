"""Adversarial receipt-consistency tests.

These tests check schema and internal consistency.
They do not establish authenticated provenance or tamper-proof evidence.
"""

import importlib.util
import json
import unittest
from pathlib import Path

from tools.validate_workflow_evidence import validate_evidence


fixture_path = Path(__file__).with_name("test_workflow_evidence.py")
fixture_spec = importlib.util.spec_from_file_location(
    "_workflow_evidence_fixture_source",
    fixture_path,
)
fixture_module = importlib.util.module_from_spec(fixture_spec)
fixture_spec.loader.exec_module(fixture_module)


class WorkflowEvidenceAdversarialTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixture_module.WorkflowEvidenceAcceptanceTests()
        self.fixture.setUp()

    def tearDown(self):
        self.fixture.tearDown()

    def update_receipt(self, updates=None, remove=()):
        path = self.fixture.receipt_path
        record = json.loads(path.read_text(encoding="utf-8"))
        if updates:
            record.update(updates)
        for field in remove:
            record.pop(field, None)
        path.write_text(json.dumps(record), encoding="utf-8")

    def validate(self):
        return validate_evidence(
            self.fixture.root,
            dict(fixture_module.TEST_ENVIRONMENT),
        )

    def assert_rejected_with(self, metadata, fragment):
        self.assertFalse(metadata["acceptance_passed"])
        self.assertTrue(
            any(
                fragment in message
                for message in metadata["acceptance_failures"]
            ),
            metadata["acceptance_failures"],
        )
        saved = json.loads(
            (self.fixture.root / "run-metadata.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertFalse(saved["acceptance_passed"])

    def test_contradictory_exit_codes_are_rejected(self):
        self.update_receipt({
            "recorder_exit": 0,
            "child_returncode": 7,
        })
        metadata = self.validate()
        self.assert_rejected_with(metadata, "disagrees with child_returncode")
        self.assertFalse(metadata["child_command_succeeded"])

    def test_reversed_timestamps_are_rejected(self):
        self.update_receipt({
            "started_at_utc": "2026-10-11T12:00:02+00:00",
            "ended_at_utc": "2026-10-11T12:00:01+00:00",
        })
        self.assert_rejected_with(
            self.validate(), "ended before it started"
        )

    def test_non_string_statuses_are_rejected_without_exception(self):
        for status in (["completed"], {"state": "completed"}, 0, None):
            with self.subTest(status=status):
                self.update_receipt({"status": status})
                self.assert_rejected_with(
                    self.validate(), "receipt was not finalized"
                )

    def test_completed_receipt_requires_child_returncode(self):
        self.update_receipt(remove=("child_returncode",))
        self.assert_rejected_with(
            self.validate(), "child_returncode must be an integer"
        )

    def test_boolean_child_returncode_is_rejected(self):
        self.update_receipt({"child_returncode": False})
        self.assert_rejected_with(
            self.validate(), "child_returncode must be an integer"
        )

    def test_missing_start_timestamp_is_rejected(self):
        self.update_receipt(remove=("started_at_utc",))
        self.assert_rejected_with(
            self.validate(), "receipt has no started_at_utc"
        )

    def test_timezone_free_start_timestamp_is_rejected(self):
        self.update_receipt({
            "started_at_utc": "2026-10-11T12:00:00",
        })
        self.assert_rejected_with(
            self.validate(), "started_at_utc is invalid"
        )

    def test_signal_normalization_is_valid_failure_evidence(self):
        self.update_receipt({
            "recorder_exit": 143,
            "child_returncode": -15,
        })
        metadata = self.validate()
        self.assertTrue(
            metadata["acceptance_passed"],
            metadata["acceptance_failures"],
        )
        self.assertEqual(metadata["recorder_exit"], 143)
        self.assertFalse(metadata["child_command_succeeded"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
