import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SOURCE = (
    Path(__file__).resolve().parents[1]
    / "examples"
    / "quadratic_contract_atlas.py"
)
SPEC = importlib.util.spec_from_file_location(
    "quadratic_atlas_under_test", SOURCE
)
ATLAS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ATLAS)


class QuadraticAtlasTests(unittest.TestCase):
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
            timeout=20,
        )

    def test_primary_routes_agree(self):
        report = ATLAS.build_report([2, 3, 4, 5, 6, 8, 9], 3)
        self.assertTrue(report["all_checks_passed"])
        self.assertEqual(
            sum(row["candidates"] for row in report["summaries"]),
            7 * 343,
        )
        for summary in report["summaries"]:
            self.assertEqual(summary["primary_disagreements"], 0)

    def test_known_equivalent_pair_has_different_coefficients(self):
        row = ATLAS.analyze_candidate(3, -1, 0, 4)
        self.assertTrue(row["complete_acceptance"])
        self.assertTrue(row["exact_acceptance"])
        self.assertTrue(row["three_point_acceptance"])
        self.assertFalse(row["strict_acceptance"])
        self.assertTrue(row["strict_false_rejection"])
        certificate = row["equivalence_certificate"]
        self.assertEqual(len(certificate), 4)
        for comparison in certificate:
            self.assertEqual(
                comparison["reference_residue"],
                comparison["candidate_residue"],
            )

    def test_strict_rule_matches_on_selected_odd_moduli(self):
        report = ATLAS.build_report([3, 5, 7, 9], 3)
        for summary in report["summaries"]:
            self.assertEqual(summary["strict_false_rejections"], 0)
            self.assertEqual(summary["strict_false_acceptances"], 0)

    def test_witness_replay_detects_tampering(self):
        row = ATLAS.analyze_candidate(1, 0, 0, 5)
        witness = row["first_counterexample"]
        self.assertTrue(row["witness_replayed"])
        self.assertTrue(
            ATLAS.replay_witness(1, 0, 0, 5, witness)
        )
        corrupted = dict(witness)
        corrupted["candidate_output"] += 1
        self.assertFalse(
            ATLAS.replay_witness(1, 0, 0, 5, corrupted)
        )
        self.assertFalse(
            ATLAS.replay_witness(1, 0, 0, 5, None)
        )

    def test_cli_outputs_and_success(self):
        result = self.invoke("--moduli", 2, 4, "--bound", 2)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(
            (self.output / "atlas.json").read_text()
        )
        self.assertTrue(report["all_checks_passed"])
        self.assertEqual(report["exit_code"], 0)
        self.assertTrue((self.output / "atlas.md").is_file())

    def test_existing_output_is_preserved(self):
        self.output.mkdir()
        marker = self.output / "keep.txt"
        marker.write_bytes(b"preserve")
        result = self.invoke("--bound", 1)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(marker.read_bytes(), b"preserve")
        self.assertFalse((self.output / "atlas.json").exists())

    def test_invalid_inputs_are_rejected(self):
        for arguments in (
            ["--moduli", "1"],
            ["--bound", "-1"],
        ):
            with self.subTest(arguments=arguments):
                result = self.invoke(*arguments)
                self.assertEqual(result.returncode, 2)
                self.assertFalse(self.output.exists())

    def test_faulty_exact_classifier_returns_one(self):
        argv = [
            str(SOURCE),
            "--moduli", "3",
            "--bound", "1",
            "--output-dir", str(self.output),
        ]
        with patch.object(sys, "argv", argv):
            with patch.object(
                ATLAS, "exact_classifier", return_value=True
            ):
                with contextlib.redirect_stdout(io.StringIO()):
                    code = ATLAS.main()
        self.assertEqual(code, 1)
        report = json.loads(
            (self.output / "atlas.json").read_text()
        )
        self.assertFalse(report["all_checks_passed"])
        self.assertGreater(
            report["summaries"][0]["primary_disagreements"], 0
        )


if __name__ == "__main__":
    unittest.main()
