import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import contextlib
import io


SOURCE = (
    Path(__file__).resolve().parents[1]
    / "examples"
    / "modular_contract_atlas.py"
)
SPEC = importlib.util.spec_from_file_location(
    "modular_atlas_under_test", SOURCE
)
ATLAS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ATLAS)


class ModularAtlasTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.output = Path(self.temporary.name) / "atlas"

    def invoke(self, *extra):
        return subprocess.run(
            [
                sys.executable, str(SOURCE),
                "--output-dir", str(self.output),
                *map(str, extra),
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )

    def test_two_routes_agree_across_composite_and_prime_moduli(self):
        report = ATLAS.build_report([2, 3, 4, 5, 6, 8, 9], 5, 0)
        self.assertTrue(report["all_routes_agree"])
        self.assertEqual(len(report["results"]), 7 * 121)

        for row in report["results"]:
            self.assertTrue(
                row["complete_observation"]["complete_residue_coverage"]
            )

    def test_default_acceptance_counts(self):
        report = ATLAS.build_report([2, 3, 4, 5, 6], 5, 0)
        counts = {
            row["modulus"]: row["accepted"]
            for row in report["summaries"]
        }
        self.assertEqual(counts, {2: 30, 3: 12, 4: 9, 5: 6, 6: 2})

    def test_empty_domains_have_no_evidence(self):
        for domain in ([], iter(())):
            result = ATLAS.observe(0, 0, 5, domain)
            self.assertIsNone(result["accepted_on_checked_domain"])
            self.assertEqual(result["evidence_status"], "no_evidence")
            self.assertEqual(result["inputs_checked"], 0)
            self.assertEqual(result["residues_covered"], 0)
            self.assertIs(result["complete_residue_coverage"], False)
            self.assertIsNone(result["first_counterexample"])

    def test_nonempty_observations_preserve_boolean_outcomes(self):
        accepted = ATLAS.observe(0, 0, 5, [0])
        rejected = ATLAS.observe(0, 0, 5, [1])
        self.assertIs(accepted["accepted_on_checked_domain"], True)
        self.assertIs(rejected["accepted_on_checked_domain"], False)
        for result in (accepted, rejected):
            self.assertEqual(result["evidence_status"], "observed")
            self.assertEqual(result["inputs_checked"], 1)

    def test_zero_radius_report_has_observed_nonempty_samples(self):
        report = ATLAS.build_report([5], 1, 0)
        self.assertTrue(report["all_routes_agree"])
        for row in report["results"]:
            sample = row["sample_observation"]
            complete = row["complete_observation"]
            self.assertEqual(sample["inputs_checked"], 1)
            self.assertEqual(sample["evidence_status"], "observed")
            self.assertIs(type(sample["accepted_on_checked_domain"]), bool)
            self.assertEqual(complete["evidence_status"], "observed")
            self.assertIs(type(complete["accepted_on_checked_domain"]), bool)

    def test_sample_at_zero_can_miss_slope_error(self):
        sampled = ATLAS.observe(0, 0, 5, [0])
        complete = ATLAS.observe(0, 0, 5, range(5))

        self.assertTrue(sampled["accepted_on_checked_domain"])
        self.assertFalse(sampled["complete_residue_coverage"])
        self.assertFalse(complete["accepted_on_checked_domain"])
        self.assertEqual(
            complete["first_counterexample"]["input"], 1
        )

    def test_counterexample_witnesses_are_valid(self):
        report = ATLAS.build_report([2, 4, 6], 3, 0)
        for row in report["results"]:
            witness = row["complete_observation"]["first_counterexample"]
            if witness is not None:
                x = witness["input"]
                q = row["modulus"]
                reference = x*x + x
                candidate = x*x + row["a"]*x + row["b"]

                self.assertEqual(
                    witness["reference_output"], reference
                )
                self.assertEqual(
                    witness["candidate_output"], candidate
                )
                self.assertNotEqual(reference % q, candidate % q)

    def test_negative_controls_are_detected(self):
        for q in (2, 3, 4, 8, 9):
            with self.subTest(q=q):
                controls = ATLAS.negative_controls(q)
                self.assertEqual(len(controls), 3)
                self.assertTrue(
                    all(item["detected"] for item in controls)
                )

    def test_faulty_primary_classifier_creates_disagreements(self):
        with patch.object(ATLAS, "classify", return_value=True):
            report = ATLAS.build_report([3], 2, 0)

        self.assertFalse(report["all_routes_agree"])
        self.assertGreater(
            report["summaries"][0]["route_disagreements"], 0
        )

    def test_cli_saves_outputs_and_returns_zero(self):
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)

        report = json.loads(
            (self.output / "atlas.json").read_text()
        )
        self.assertTrue(report["all_routes_agree"])
        self.assertTrue(report["all_negative_controls_detected"])
        self.assertIn(
            "| 2 | 121 | 30 | 91 |",
            (self.output / "atlas.md").read_text(),
        )

    def test_existing_output_is_preserved(self):
        self.output.mkdir()
        marker = self.output / "keep.txt"
        marker.write_bytes(b"preserve")

        result = self.invoke()

        self.assertEqual(result.returncode, 2)
        self.assertEqual(marker.read_bytes(), b"preserve")
        self.assertFalse((self.output / "atlas.json").exists())

    def test_invalid_arguments_are_rejected(self):
        cases = [
            ["--moduli", "1"],
            ["--bound", "-1"],
            ["--sample-radius", "-1"],
        ]

        for extra in cases:
            with self.subTest(extra=extra):
                result = self.invoke(*extra)
                self.assertEqual(result.returncode, 2)
                self.assertFalse(self.output.exists())

    def test_cli_returns_one_when_classifier_is_faulty(self):
        argv = [
            str(SOURCE),
            "--moduli", "3",
            "--bound", "1",
            "--output-dir", str(self.output),
        ]

        with patch.object(sys, "argv", argv):
            with patch.object(ATLAS, "classify", return_value=True):
                with contextlib.redirect_stdout(io.StringIO()):
                    code = ATLAS.main()

        self.assertEqual(code, 1)

        report = json.loads(
            (self.output / "atlas.json").read_text()
        )
        self.assertEqual(report["exit_code"], 1)
        self.assertFalse(report["all_routes_agree"])


if __name__ == "__main__":
    unittest.main()
