"""SM003 regression tests and manifest-to-recomputation checks."""
import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST_PATH = HERE / "manifest.json"

spec = importlib.util.spec_from_file_location(
    "sm003_mutations", HERE / "mutations.py"
)
sm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sm)


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
        for t, blocks in cases:
            with self.subTest(t=t, blocks=blocks):
                values = sm.case_values(t, blocks)
                self.assertEqual(
                    values["baseline_rank"],
                    values["graph_prediction"],
                )

    def test_manifest_witness_ids_are_unique(self):
        manifest = load_manifest()
        witnesses = manifest["witness_suite"]["instances"]
        ids = [w["w"] for w in witnesses]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(ids)

    def test_manifest_detection_sets_match_recomputation(self):
        manifest = load_manifest()
        actual = sm.witness_detection_sets(manifest)
        declared_ids = set(manifest["mutant_ids_explicit"])
        invalid_ids = set(sm.INVALID_MUTANTS)

        for witness in manifest["witness_suite"]["instances"]:
            wid = witness["w"]
            declared = set(witness["detects"])
            with self.subTest(witness=wid):
                self.assertTrue(
                    declared <= declared_ids,
                    f"{wid}: unknown IDs {sorted(declared - declared_ids)}",
                )
                self.assertFalse(
                    declared & invalid_ids,
                    f"{wid}: invalid mutants cannot count as coverage",
                )
                self.assertEqual(
                    declared,
                    set(actual[wid]),
                    f"{wid}: false positives="
                    f"{sorted(declared - set(actual[wid]))}; "
                    f"missing detections="
                    f"{sorted(set(actual[wid]) - declared)}",
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
            t, blocks = sm.witness_instance(witness)
            with self.subTest(witness=witness["w"]):
                sm.validate_instance(t, blocks)
                self.assertLess(len(set(t)), len(t))
                self.assertGreater(len(set(t)), 1)
                self.assertTrue(any(len(b) > 1 for b in blocks))

    def test_unreached_block_requirement_is_suite_level(self):
        manifest = load_manifest()
        touched_counts = {}

        for witness in manifest["witness_suite"]["instances"]:
            t, blocks = sm.witness_instance(witness)
            block_of = {
                x: i for i, block in enumerate(blocks) for x in block
            }
            touched = {block_of[t[x]] for x in range(len(t))}
            touched_counts[witness["w"]] = len(touched)

        # W1 has an unreached target block. W2 reaches both blocks.
        self.assertLess(touched_counts["W1"], 2)
        self.assertEqual(touched_counts["W2"], 2)

        requirements = manifest["witness_suite"]["requires"]
        self.assertTrue(requirements["at_least_one_witness_has_unreached_block"])

    def test_partition_label_permutation_invariance(self):
        t = [1, 1, 2]
        a = sm.case_values(t, [[0], [1], [2]])
        b = sm.case_values(t, [[2], [0], [1]])
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
