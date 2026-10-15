"""Failure-path acceptance tests for Mobile Research Kit orchestration."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
TOOLS = PACKAGE_ROOT / "tools"
RUN_WORKFLOW = TOOLS / "run_workflow.py"


class RunWorkflowFailurePathTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)

    def tearDown(self):
        self.tempdir.cleanup()

    def _run(self, *arguments):
        return subprocess.run(
            [sys.executable, str(RUN_WORKFLOW), *map(str, arguments)],
            capture_output=True,
            text=True,
            timeout=30,
        )

    def test_timeout_is_classified_and_evidence_is_preserved(self):
        output_root = self.root / "evidence"
        result = self._run(
            "--timeout", "0.5",
            "--output-root", output_root,
            "--", sys.executable, "-c", "import time; time.sleep(3)",
        )

        self.assertIn(
            "WORKFLOW_STATUS=reports_created",
            result.stdout,
        )

        receipts = list(output_root.glob("workflow-*/runs/run-*/receipt.json"))
        self.assertEqual(len(receipts), 1)

        receipt = json.loads(
            receipts[0].read_text(encoding="utf-8")
        )
        self.assertEqual(receipt["status"], "timed_out")
        self.assertTrue(
            (receipts[0].parent.parent.parent / "viewer.html").is_file()
        )
        self.assertTrue(
            (receipts[0].parent.parent.parent / "inventory.json").is_file()
        )

    def test_orchestration_failure_returns_125(self):
        blocker = self.root / "not-a-directory"
        blocker.write_text("block output root", encoding="utf-8")

        result = self._run(
            "--timeout", "5",
            "--output-root", blocker,
            "--", sys.executable, "-c", "print('never runs')",
        )

        self.assertEqual(result.returncode, 125)
        self.assertIn(
            "WORKFLOW_STATUS=orchestration_failed",
            result.stdout,
        )
        self.assertIn(
            "WORKFLOW_EXIT=125",
            result.stdout,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
