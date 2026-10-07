import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


WORKFLOW = (
    Path(__file__).resolve().parents[1]
    / "tools"
    / "run_workflow.py"
)


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.output_root = Path(self.temporary.name) / "output"

    def invoke(self, code, timeout=5):
        return subprocess.run(
            [
                sys.executable,
                str(WORKFLOW),
                "--timeout",
                str(timeout),
                "--output-root",
                str(self.output_root),
                "--",
                sys.executable,
                "-c",
                code,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

    def artifacts(self):
        directories = list(self.output_root.glob("workflow-*"))
        self.assertEqual(len(directories), 1)
        directory = directories[0]

        inventory = directory / "inventory.json"
        self.assertTrue(inventory.is_file())
        self.assertEqual(
            json.loads(inventory.read_text())["kind"],
            "environment_snapshot",
        )

        receipts = list(directory.glob("runs/run-*/receipt.json"))
        self.assertEqual(len(receipts), 1)

        viewer = directory / "viewer.html"
        self.assertTrue(viewer.is_file())
        self.assertIn("Recorded execution", viewer.read_text())

        return receipts[0].parent, json.loads(receipts[0].read_text())

    def test_success_and_artifacts(self):
        result = self.invoke("print('workflow hello')")
        self.assertEqual(result.returncode, 0, result.stderr)

        run, receipt = self.artifacts()
        self.assertEqual(receipt["status"], "completed")
        self.assertEqual(receipt["child_returncode"], 0)
        self.assertEqual(
            (run / "stdout.txt").read_text().strip(),
            "workflow hello",
        )
        self.assertIn(
            "WORKFLOW_STATUS=reports_created",
            result.stdout,
        )
        self.assertIn("WORKFLOW_EXIT=0", result.stdout)

    def test_child_failure_still_creates_viewer(self):
        result = self.invoke("import sys; sys.exit(7)")
        self.assertEqual(result.returncode, 7, result.stderr)

        _, receipt = self.artifacts()
        self.assertEqual(receipt["status"], "completed")
        self.assertEqual(receipt["child_returncode"], 7)
        self.assertIn("WORKFLOW_RECORDER_EXIT=7", result.stdout)
        self.assertIn(
            "WORKFLOW_STATUS=reports_created",
            result.stdout,
        )

    def test_timeout_still_creates_viewer(self):
        result = self.invoke(
            "import time; time.sleep(10)",
            timeout=0.5,
        )
        self.assertEqual(result.returncode, 124, result.stderr)

        _, receipt = self.artifacts()
        self.assertEqual(receipt["status"], "timed_out")
        self.assertIn("WORKFLOW_EXIT=124", result.stdout)

    def test_invalid_timeout_creates_no_artifacts(self):
        result = self.invoke("print('must not run')", timeout=0)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.output_root.exists())


if __name__ == "__main__":
    unittest.main()
