import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


VIEWER = (
    Path(__file__).resolve().parents[1]
    / "tools"
    / "view_report.py"
)


class ViewerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)

        root = Path(self.temporary.name)
        self.receipt_path = root / "receipt.json"
        self.inventory_path = root / "inventory.json"
        self.output = root / "viewer.html"

        self.receipt = {
            "kind": "command_execution",
            "status": "completed",
            "child_returncode": 0,
            "recorder_exit": 0,
            "elapsed_seconds": 0.25,
            "timeout_seconds": 5,
            "started_at_utc": "synthetic-test-time",
            "command": ["python3", "synthetic-example"],
        }
        self.inventory = {
            "kind": "environment_snapshot",
            "environment": "synthetic-test",
            "architecture": "test-architecture",
            "python_version": "test-version",
            "termux_version": None,
            "android": {},
            "recorded_at_utc": "synthetic-test-time",
        }

    def invoke(self):
        self.receipt_path.write_text(json.dumps(self.receipt))
        self.inventory_path.write_text(json.dumps(self.inventory))

        return subprocess.run(
            [
                sys.executable,
                str(VIEWER),
                "--receipt",
                str(self.receipt_path),
                "--inventory",
                str(self.inventory_path),
                "--output",
                str(self.output),
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

    def test_page_generation(self):
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)

        page = self.output.read_text()
        self.assertIn("<!doctype html>", page)
        self.assertIn("Recorded execution", page)
        self.assertIn("Environment snapshot", page)
        self.assertIn("completed", page)
        self.assertIn("does not authenticate", page)

    def test_report_text_is_escaped(self):
        self.receipt["command"] = ["<script>alert(1)</script>"]
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)

        page = self.output.read_text()
        self.assertIn("&lt;script&gt;", page)
        self.assertNotIn("<script>", page)

    def test_wrong_receipt_kind(self):
        self.receipt["kind"] = "wrong-kind"
        result = self.invoke()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())

    def test_wrong_inventory_kind(self):
        self.inventory["kind"] = "wrong-kind"
        result = self.invoke()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())

    def test_existing_page_is_preserved(self):
        original = b"existing page must remain unchanged"
        self.output.write_bytes(original)

        result = self.invoke()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.output.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
