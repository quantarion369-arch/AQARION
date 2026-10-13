
"""SM003 regression tests and manifest-to-recomputation checks."""
import importlib.util
import itertools
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST_PATH = HERE / "manifest.json"
SIGNATURES_PATH = HERE / "detection_signatures.py"

def load_module(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sm = load_module("sm003_mutations", HERE / "mutations.py")
signatures = load_module("sm003_detection_signatures", SIGNATURES_PATH)


def load_manifest():
    with MANIFEST_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


class SM003RegressionTests(unittest.TestCase):
    def test_partition_counts(self):
        self.assertEqual(
            [len(list(sm.parts(n))) for n in range(1, 5)],
            [1, 2, 5, 15],
        )

    def test_rank_identity_edge_cases(self):
        cases = [
            ([0, 1], [[0], [1]]),
            ([0, 0], [[0], [1]]),
            ([1, 2, 0], [[0], [1], [2]]),
            ([1, 1, 2], [[0], [1], [2]]),
            ([0, 2, 2, 0], [[0, 1], [2, 3]]),
        ]
        for transition, partition in cases:
            with self.subTest(transition=transition, partition=partition):
                values = sm.case_values(transition, partition)
                self.assertEqual(
                    values["baseline_rank"],
                    values["graph_prediction"],
                )

    def test_manifest_witness_ids_are_unique(self):
        manifest = load_manifest()
        witnesses = manifest["witness_suite"]["instances"]
        ids = [witness["w"] for witness in witnesses]
        self.assertTrue(ids)
        self.assertEqual(len(ids), len(set(ids)))

    def test_manifest_detection_sets_match_recomputation(self):
        manifest = load_manifest()
        actual = sm.witness_detection_sets(manifest)
        declared_ids = set(manifest["mutant_ids_explicit"])
        invalid_ids = set(sm.INVALID_MUTANTS)

        for witness in manifest["witness_suite"]["instances"]:
            witness_id = witness["w"]
            declared = set(witness["detects"])
            with self.subTest(witness=witness_id):
                self.assertTrue(
                    declared <= declared_ids,
                    f"{witness_id}: unknown IDs "
                    f"{sorted(declared - declared_ids)}",
                )
                self.assertFalse(
                    declared & invalid_ids,
                    f"{witness_id}: invalid mutants cannot count as coverage",
                )
                self.assertEqual(
                    declared,
                    set(actual[witness_id]),
                    f"{witness_id}: false positives="
                    f"{sorted(declared - set(actual[witness_id]))}; "
                    f"missing detections="
                    f"{sorted(set(actual[witness_id]) - declared)}",
                )

    def test_witness_detection_matrix(self):
        manifest = load_manifest()
        actual = sm.witness_detection_sets(manifest)
        expected = {
            "W1": {
                "D:K^T",
                "D:[K,P]",
                "D:(I-P)K",
                "D:PKP",
                "D:(I-P)K^T",
                "R:ignore-isolated",
                "R:preimage",
                "R:c",
                "R:k-c-1",
            },
            "W2": {
                "D:KP(I-P)",
                "R:k-c-1",
                "R:first",
            },
        }
        self.assertEqual(
            actual,
            {key: sorted(value) for key, value in expected.items()},
        )

    def test_cluster_is_not_a_canonical_mutant(self):
        manifest = load_manifest()
        ids = set(manifest["mutant_ids_explicit"])
        self.assertNotIn("R:ignore+preimage_cluster", ids)
        self.assertIn("R:ignore-isolated", ids)
        self.assertIn("R:preimage", ids)

    def test_duplicate_mutant_is_invalid(self):
        manifest = load_manifest()
        self.assertIn("R:c", manifest["mutant_ids_explicit"])
        self.assertIn("R:c-only-variant", sm.INVALID_MUTANTS)
        self.assertEqual(
            sm.run(2)["mutation_outcomes"]["R:c-only-variant"],
            "INVALID_MUTANT",
        )

    def test_witnesses_are_noninjective_and_nonconstant(self):
        manifest = load_manifest()
        for witness in manifest["witness_suite"]["instances"]:
            transition, partition = sm.witness_instance(witness)
            with self.subTest(witness=witness["w"]):
                sm.validate_instance(transition, partition)
                self.assertLess(len(set(transition)), len(transition))
                self.assertGreater(len(set(transition)), 1)
                self.assertTrue(any(len(block) > 1 for block in partition))

    def test_unreached_block_requirement_is_suite_level(self):
        manifest = load_manifest()
        touched_counts = {}

        for witness in manifest["witness_suite"]["instances"]:
            transition, partition = sm.witness_instance(witness)
            block_of = {
                state: index
                for index, block in enumerate(partition)
                for state in block
            }
            touched = {
                block_of[transition[state]]
                for state in range(len(transition))
            }
            touched_counts[witness["w"]] = len(touched)

        self.assertLess(touched_counts["W1"], 2)
        self.assertEqual(touched_counts["W2"], 2)

        requirements = manifest["witness_suite"]["requires"]
        self.assertTrue(
            requirements["at_least_one_witness_has_unreached_block"]
        )

    def test_partition_label_permutation_invariance(self):
        transition = [1, 1, 2]
        a = sm.case_values(transition, [[0], [1], [2]])
        b = sm.case_values(transition, [[2], [0], [1]])
        self.assertEqual(a["baseline_rank"], b["baseline_rank"])
        self.assertEqual(a["graph_prediction"], b["graph_prediction"])
        self.assertEqual(a["closure_truth"], b["closure_truth"])

    def test_census_completion_counts(self):
        expected = {1: 1, 2: 8, 3: 135, 4: 3840}
        for n, count in expected.items():
            with self.subTest(n=n):
                self.assertEqual(
                    n ** n * len(list(sm.parts(n))),
                    count,
                )

    def test_all_declared_mutants_have_outcomes(self):
        manifest = load_manifest()
        report = sm.run(2)
        self.assertEqual(
            set(report["mutation_outcomes"]),
            set(manifest["mutant_ids_explicit"]),
        )

    def test_r_first_and_degenerate_d_mutant_have_same_detection_set(self):
        """Exhaustively check the implementation-level equivalence for n<=4."""
        degenerate = "D:KP(I-P)"
        first = "R:first"

        for n in range(1, 5):
            partitions = list(sm.parts(n))
            for transition in itertools.product(range(n), repeat=n):
                for partition in partitions:
                    values = sm.case_values(transition, partition)
                    detected = set(values["detected"])

                    with self.subTest(
                        n=n,
                        transition=transition,
                        partition=partition,
                    ):
                        self.assertTrue(
                            values["d_test_verdicts"][degenerate]
                        )
                        self.assertEqual(
                            values["graph_rank_predictions"][first], 0
                        )
                        self.assertEqual(
                            degenerate in detected,
                            first in detected,
                        )

    def test_r_first_manifest_warning(self):
        manifest = load_manifest()
        warning = manifest["mutant_semantics"]["R:first"].get("warning", "")
        self.assertIn("prediction is always zero", warning)
        self.assertIn("D:KP(I-P)", warning)
        self.assertIn("partition is not invariant", warning)

    def test_detection_signature_script_builds_small_report(self):
        report = signatures.build_report(1, include_case_ids=False)
        self.assertEqual(report["schema"], "AQ-SM003-DETECTION-SIGNATURES/1")
        self.assertEqual(report["status"], "COMPUTED")
        self.assertEqual(report["scope"]["cases"], 1)
        self.assertEqual(
            report["canonical_mutant_count"],
            len((*sm.D_MUTANTS, *sm.R_MUTANTS)),
        )
        self.assertGreaterEqual(report["signature_count"], 1)
        for signature in report["signatures"]:
            self.assertNotIn("detected_case_ids", signature)

    def test_invalid_partitions_are_rejected(self):
        with self.assertRaises(ValueError):
            sm.case_values([0, 1], [[0], [0, 1]])
        with self.assertRaises(ValueError):
            sm.case_values([0, 1], [[0], []])

    def test_invalid_transitions_are_rejected(self):
        with self.assertRaises(ValueError):
            sm.case_values([0, 2], [[0], [1]])


if __name__ == "__main__":
    unittest.main(verbosity=2)
