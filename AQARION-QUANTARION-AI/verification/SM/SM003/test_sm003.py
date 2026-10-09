import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "sm003_mutations", HERE / "mutations.py"
)
sm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sm)


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
        for transition, blocks in cases:
            with self.subTest(transition=transition, blocks=blocks):
                values = sm.case_values(transition, blocks)
                self.assertEqual(
                    values["baseline_rank"], values["graph_prediction"]
                )

    def test_all_declared_alternatives_have_outcomes(self):
        report = sm.run(2)
        expected = {
            "D:K^T", "D:[K,P]", "D:(I-P)K", "D:PKP", "D:(I-P)K^T",
            "D:KP(I-P)", "R:ignore-isolated", "R:preimage",
            "R:ignore+preimage_cluster", "R:c", "R:k-c-1", "R:first",
            "R:c-only-variant",
        }
        self.assertEqual(set(report["mutation_outcomes"]), expected)
        self.assertEqual(
            report["mutation_outcomes"]["R:c-only-variant"],
            "INVALID_MUTANT",
        )

    def test_partition_label_permutation_invariance(self):
        t = [1, 1, 2]
        a = sm.case_values(t, [[0], [1], [2]])
        b = sm.case_values(t, [[2], [0], [1]])
        self.assertEqual(a["baseline_rank"], b["baseline_rank"])
        self.assertEqual(a["graph_prediction"], b["graph_prediction"])

    def test_census_completion_counts(self):
        expected = {1: 1, 2: 8, 3: 135, 4: 3840}
        for n, count in expected.items():
            self.assertEqual(n ** n * len(list(sm.parts(n))), count)


if __name__ == "__main__":
    unittest.main()
