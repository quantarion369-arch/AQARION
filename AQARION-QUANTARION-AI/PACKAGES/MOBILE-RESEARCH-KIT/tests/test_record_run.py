import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


RECORDER = (
    Path(__file__).resolve().parents[1]
    / "tools"
    / "record_run.py"
)


class RecorderTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.output_root = Path(self.temporary.name) / "runs"

    def invoke(self, command, timeout=5):
        return subprocess.run(
            [
                sys.executable,
                str(RECORDER),
                "--timeout",
                str(timeout),
                "--output-root",
                str(self.output_root),
                "--",
                *command,
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )

    def receipt(self):
        paths = list(self.output_root.glob("run-*/receipt.json"))
        self.assertEqual(len(paths), 1)
        return paths[0].parent, json.loads(paths[0].read_text())

    def test_success_and_output(self):
        result = self.invoke([
            sys.executable,
            "-c",
            "import sys; print('hello'); print('note', file=sys.stderr)",
        ])
        self.assertEqual(result.returncode, 0)

        directory, record = self.receipt()
        self.assertEqual(record["status"], "completed")
        self.assertEqual(record["child_returncode"], 0)
        self.assertEqual(record["recorder_exit"], 0)
        self.assertEqual(
            (directory / "stdout.txt").read_text().strip(),
            "hello",
        )
        self.assertEqual(
            (directory / "stderr.txt").read_text().strip(),
            "note",
        )

    def test_child_failure(self):
        result = self.invoke([
            sys.executable,
            "-c",
            "import sys; sys.exit(7)",
        ])
        self.assertEqual(result.returncode, 7)

        _, record = self.receipt()
        self.assertEqual(record["status"], "completed")
        self.assertEqual(record["child_returncode"], 7)
        self.assertEqual(record["recorder_exit"], 7)

    def test_timeout(self):
        result = self.invoke(
            [
                sys.executable,
                "-c",
                "import time; time.sleep(10)",
            ],
            timeout=0.5,
        )
        self.assertEqual(result.returncode, 124)

        _, record = self.receipt()
        self.assertEqual(record["status"], "timed_out")
        self.assertEqual(record["recorder_exit"], 124)
        self.assertIsNotNone(record["child_returncode"])
        self.assertNotEqual(record["child_returncode"], 0)

    def test_missing_executable(self):
        missing = Path(self.temporary.name) / "missing_executable"
        result = self.invoke([str(missing)])
        self.assertEqual(result.returncode, 127)

        _, record = self.receipt()
        self.assertEqual(record["status"], "launch_failed")
        self.assertIsNone(record["child_returncode"])
        self.assertIn("error", record)

    def test_invalid_timeout(self):
        result = self.invoke(
            [
                sys.executable,
                "-c",
                "print('must not run')",
            ],
            timeout=0,
        )
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.output_root.exists())


if __name__ == "__main__":
    unittest.main()
