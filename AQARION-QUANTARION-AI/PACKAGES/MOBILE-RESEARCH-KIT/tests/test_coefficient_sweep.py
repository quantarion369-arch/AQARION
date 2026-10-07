import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SOURCE = (
    Path(__file__).resolve().parents[1]
    / "examples"
    / "coefficient_sweep.py"
)
SPEC = importlib.util.spec_from_file_location(
    "coefficient_sweep_under_test", SOURCE
)
SWEEP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SWEEP)


class CoefficientSweepTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.output = Path(self.temporary.name) / "sweep"

    def invoke(self, radius=20, bound=2):
        return subprocess.run(
            [
                sys.executable, str(SOURCE),
                "--radius", str(radius),
                "--bound", str(bound),
                "--output-dir", str(self.output),
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

    def test_default_classification_counts(self):
        report = SWEEP.build_report(20, 2)
        self.assertEqual(report["candidate_count"], 25)
        self.assertEqual(report["classification_counts"], {
            "both": 1,
            "equality_only": 0,
            "parity_only": 5,
            "neither": 19,
        })

    def test_classifications_match_coefficient_rules(self):
        for radius in (1, 3, 20):
            report = SWEEP.build_report(radius, 3)
            for row in report["results"]:
                with self.subTest(
                    radius=radius, a=row["a"], b=row["b"]
                ):
                    self.assertEqual(
                        row["equality_accepted"],
                        row["a"] == 1 and row["b"] == 0,
                    )
                    self.assertEqual(
                        row["parity_accepted"],
                        row["a"] % 2 == 1 and row["b"] % 2 == 0,
                    )
                    self.assertEqual(
                        row["inputs_checked"], 2 * radius + 1
                    )

    def test_report_and_table_are_saved(self):
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(
            (self.output / "report.json").read_text()
        )
        table = (self.output / "table.md").read_text()
        self.assertEqual(report["candidate_count"], 25)
        self.assertIn(
            "| 1 | 0 | pass | pass | both |", table
        )
        self.assertIn(
            "| -1 | 0 | fail | pass | parity_only |", table
        )
        self.assertIn("CANDIDATE_COUNT=25", result.stdout)

    def test_existing_output_directory_is_preserved(self):
        self.output.mkdir()
        marker = self.output / "keep.txt"
        marker.write_bytes(b"preserve this")
        result = self.invoke()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(marker.read_bytes(), b"preserve this")
        self.assertFalse((self.output / "report.json").exists())
        self.assertFalse((self.output / "table.md").exists())

    def test_invalid_arguments_create_no_output(self):
        for radius, bound in ((0, 2), (20, -1)):
            with self.subTest(radius=radius, bound=bound):
                result = self.invoke(radius, bound)
                self.assertEqual(result.returncode, 2)
                self.assertFalse(self.output.exists())

    def test_zero_bound_has_one_candidate(self):
        report = SWEEP.build_report(1, 0)
        self.assertEqual(report["candidate_count"], 1)
        row = report["results"][0]
        self.assertEqual((row["a"], row["b"]), (0, 0))
        self.assertEqual(row["classification"], "neither")


if __name__ == "__main__":
    unittest.main()
