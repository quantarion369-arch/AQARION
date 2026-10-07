import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


INVENTORY = (
    Path(__file__).resolve().parents[1]
    / "tools"
    / "inspect_environment.py"
)


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.destination = (
            Path(self.temporary.name) / "capability.json"
        )

    def invoke(self, *arguments):
        return subprocess.run(
            [sys.executable, str(INVENTORY), *map(str, arguments)],
            capture_output=True,
            text=True,
            timeout=20,
        )

    def test_report_creation(self):
        result = self.invoke(self.destination)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.destination.is_file())

        saved = json.loads(self.destination.read_text())
        printed = json.loads(result.stdout)

        self.assertEqual(saved, printed)
        self.assertEqual(saved["schema_version"], "0.1.0")
        self.assertEqual(saved["kind"], "environment_snapshot")
        self.assertIsInstance(saved["command_locations"], dict)
        self.assertIn("python3", saved["command_locations"])
        self.assertIn("not_established", saved)
        self.assertTrue(saved["not_established"])

    def test_existing_report_is_preserved(self):
        original = b"existing report must remain unchanged"
        self.destination.write_bytes(original)

        result = self.invoke(self.destination)

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.destination.read_bytes(), original)

    def test_missing_argument(self):
        result = self.invoke()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Usage:", result.stderr)
        self.assertFalse(self.destination.exists())


if __name__ == "__main__":
    unittest.main()
