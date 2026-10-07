import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


SOURCE = (
    Path(__file__).resolve().parents[1]
    / "examples"
    / "contract_collision_lab.py"
)
SPEC = importlib.util.spec_from_file_location(
    "contract_collision_under_test", SOURCE
)
LAB = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LAB)


class ContractCollisionTests(unittest.TestCase):
    def invoke(self, *arguments):
        return subprocess.run(
            [sys.executable, str(SOURCE), *map(str, arguments)],
            capture_output=True,
            text=True,
            timeout=10,
        )

    def report(self, radius):
        result = self.invoke("--radius", radius)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_six_fixture_outcomes(self):
        report = self.report(20)
        expected = {
            ("reference", "equality"): True,
            ("reference", "parity"): True,
            ("subtract_mutation", "equality"): False,
            ("subtract_mutation", "parity"): True,
            ("offset_mutation", "equality"): False,
            ("offset_mutation", "parity"): False,
        }

        results = report["results"]
        self.assertEqual(len(results), 6)
        actual = {
            (row["candidate"], row["contract"]):
                row["accepted_on_tested_domain"]
            for row in results
        }
        self.assertEqual(actual, expected)

        for row in results:
            self.assertTrue(row["expectation_matched"])
            self.assertEqual(
                row["expected_acceptance"],
                expected[(row["candidate"], row["contract"])],
            )

        self.assertTrue(report["all_fixture_expectations_met"])

    def test_subtraction_counterexample(self):
        report = self.report(20)
        row = next(
            row for row in report["results"]
            if row["candidate"] == "subtract_mutation"
            and row["contract"] == "equality"
        )
        self.assertEqual(row["inputs_checked"], 1)
        self.assertEqual(row["first_counterexample"], {
            "input": -20,
            "reference_output": 380,
            "candidate_output": 420,
            "reference_parity": 0,
            "candidate_parity": 0,
        })

    def test_offset_counterexamples(self):
        report = self.report(20)
        rows = [
            row for row in report["results"]
            if row["candidate"] == "offset_mutation"
        ]
        self.assertEqual(len(rows), 2)
        for row in rows:
            self.assertEqual(row["inputs_checked"], 1)
            self.assertEqual(row["first_counterexample"], {
                "input": -20,
                "reference_output": 380,
                "candidate_output": 381,
                "reference_parity": 0,
                "candidate_parity": 1,
            })

    def test_accepted_contracts_check_entire_domain(self):
        report = self.report(20)
        self.assertEqual(report["domain"], {
            "minimum": -20,
            "maximum": 20,
            "size": 41,
        })

        accepted = [
            row for row in report["results"]
            if row["accepted_on_tested_domain"]
        ]
        self.assertEqual(len(accepted), 3)
        for row in accepted:
            self.assertEqual(row["inputs_checked"], 41)
            self.assertIsNone(row["first_counterexample"])

    def test_minimum_radius(self):
        report = self.report(1)
        self.assertEqual(report["domain"], {
            "minimum": -1,
            "maximum": 1,
            "size": 3,
        })
        self.assertTrue(report["all_fixture_expectations_met"])

    def test_nonpositive_radius_is_rejected(self):
        for radius in (0, -1):
            with self.subTest(radius=radius):
                result = self.invoke("--radius", radius)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn(
                    "--radius must be at least 1", result.stderr
                )

    def test_noninteger_radius_is_rejected(self):
        result = self.invoke("--radius", "not-an-integer")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("invalid int value", result.stderr)

    def test_failed_fixture_returns_exit_two(self):
        output = io.StringIO()
        argv = [str(SOURCE), "--radius", "1"]

        with patch.object(sys, "argv", argv):
            with patch.object(
                LAB, "subtract_mutation", new=LAB.reference
            ):
                with contextlib.redirect_stdout(output):
                    code = LAB.main()

        report = json.loads(output.getvalue())
        self.assertEqual(code, 2)
        self.assertFalse(report["all_fixture_expectations_met"])

        failures = [
            (row["candidate"], row["contract"])
            for row in report["results"]
            if not row["expectation_matched"]
        ]
        self.assertEqual(
            failures, [("subtract_mutation", "equality")]
        )


if __name__ == "__main__":
    unittest.main()
