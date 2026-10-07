"""Regression tests for the package regression runner."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


PACKAGE = Path(__file__).resolve().parents[1]


class RunRegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        self.root = Path(self.temp.name) / "package"
        self.tools = self.root / "tools"
        self.tests = self.root / "tests"
        self.tools.mkdir(parents=True)
        self.tests.mkdir()

        for name in ("run_regression.py", "verify_package.py"):
            shutil.copyfile(PACKAGE / "tools" / name, self.tools / name)

        content = b"original"
        (self.root / "sample.txt").write_bytes(content)
        manifest = {
            "algorithm": "sha256",
            "files": [
                {
                    "path": "sample.txt",
                    "bytes": len(content),
                    "sha256": hashlib.sha256(content).hexdigest(),
                }
            ],
        }
        (self.root / "manifest.json").write_text(
            json.dumps(manifest), encoding="utf-8"
        )

    def write_test(self, body):
        source = (
            "import unittest"
            + chr(10)
            + "class Example(unittest.TestCase):"
            + chr(10)
            + "    def test_example(self):"
            + chr(10)
            + "        "
            + body
            + chr(10)
        )
        (self.tests / "test_example.py").write_text(
            source, encoding="utf-8"
        )

    def run_runner(self):
        result = subprocess.run(
            [sys.executable, str(self.tools / "run_regression.py")],
            cwd=self.temp.name,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        return result.returncode, result.stdout + result.stderr

    def test_passing_suite_returns_zero(self):
        self.write_test("self.assertTrue(True)")
        code, output = self.run_runner()
        self.assertEqual(code, 0, output)
        self.assertIn("DISCOVERED_TESTS: 1", output)
        self.assertIn("REGRESSION_OK", output)
        self.assertIn("SKIPPED_TESTS: 0", output)

    def test_manifest_mismatch_stops_before_tests(self):
        self.write_test(
            "open('TEST_EXECUTED', 'w').close()"
        )
        (self.root / "sample.txt").write_bytes(b"modified")
        code, output = self.run_runner()
        self.assertEqual(code, 1, output)
        self.assertIn("REGRESSION_STOPPED", output)
        self.assertNotIn("DISCOVERED_TESTS:", output)
        self.assertFalse((self.root / "TEST_EXECUTED").exists())
        self.assertFalse((Path(self.temp.name) / "TEST_EXECUTED").exists())

    def test_failing_suite_returns_one(self):
        self.write_test("self.fail('intentional failure')")
        code, output = self.run_runner()
        self.assertEqual(code, 1, output)
        self.assertIn("REGRESSION_FAILED", output)
        self.assertNotIn("REGRESSION_OK", output)

    def test_zero_tests_returns_two(self):
        code, output = self.run_runner()
        self.assertEqual(code, 2, output)
        self.assertIn("No tests discovered", output)

    def test_missing_verifier_returns_two(self):
        (self.tools / "verify_package.py").unlink()
        code, output = self.run_runner()
        self.assertEqual(code, 2, output)
        self.assertIn("Required verifier or tests directory missing", output)

    def test_missing_tests_directory_returns_two(self):
        self.tests.rmdir()
        code, output = self.run_runner()
        self.assertEqual(code, 2, output)
        self.assertIn("Required verifier or tests directory missing", output)

    def test_broken_test_import_returns_two(self):
        (self.tests / "test_example.py").write_text(
            "raise RuntimeError('intentional import failure')",
            encoding="utf-8",
        )
        code, output = self.run_runner()
        self.assertEqual(code, 2, output)
        self.assertIn("Test discovery reported errors", output)

    def test_malformed_manifest_stops_runner(self):
        (self.root / "manifest.json").write_text(
            "{", encoding="utf-8"
        )
        code, output = self.run_runner()
        self.assertEqual(code, 1, output)
        self.assertIn("MANIFEST_ERROR", output)
        self.assertIn("REGRESSION_STOPPED", output)

    def test_skipped_test_is_reported(self):
        self.write_test("self.skipTest('intentional skip')")
        code, output = self.run_runner()
        self.assertEqual(code, 0, output)
        self.assertIn("REGRESSION_OK", output)
        self.assertIn("SKIPPED_TESTS: 1", output)


if __name__ == "__main__":
    unittest.main()
