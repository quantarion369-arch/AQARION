"""Regression tests pinning the profile-sufficiency separation result.

Two finite deterministic systems with initial partitions have identical
defect-rank profiles but different partition-repair costs. This pins the
negative result:

    profile(T, Pi) = profile(T', Pi')
    does not imply
    c_part(T, Pi) = c_part(T', Pi').

Witness A:
    T = (0, 0, 0, 1)
    Pi = {{0, 2, 3}, {1}}
    profile = (1, 0), c_lin = 1, c_part = 1

Witness B:
    T = (0, 0, 1, 1)
    Pi = {{0, 2}, {1, 3}}
    profile = (1, 0), c_lin = 1, c_part = 2
"""

import unittest

from partition_repair import closure_gap


WITNESS_A = {
    "transition": (0, 0, 0, 1),
    "partition": [
        [0, 2, 3],
        [1],
    ],
    "expected_profile": [1, 0],
    "expected_linear_cost": 1,
    "expected_partition_cost": 1,
}

WITNESS_B = {
    "transition": (0, 0, 1, 1),
    "partition": [
        [0, 2],
        [1, 3],
    ],
    "expected_profile": [1, 0],
    "expected_linear_cost": 1,
    "expected_partition_cost": 2,
}


class ProfileSeparationTests(unittest.TestCase):
    def test_witness_a_has_expected_costs(self):
        result = closure_gap(
            WITNESS_A["transition"],
            WITNESS_A["partition"],
        )

        self.assertEqual(
            result["linear_profile"],
            WITNESS_A["expected_profile"],
        )
        self.assertEqual(
            result["linear_repair_cost"],
            WITNESS_A["expected_linear_cost"],
        )
        self.assertEqual(
            result["partition_repair_cost"],
            WITNESS_A["expected_partition_cost"],
        )
        self.assertEqual(
            result["closure_gap"],
            0,
        )
        self.assertEqual(
            result["result"],
            "PASS",
        )

    def test_witness_b_has_expected_costs(self):
        result = closure_gap(
            WITNESS_B["transition"],
            WITNESS_B["partition"],
        )

        self.assertEqual(
            result["linear_profile"],
            WITNESS_B["expected_profile"],
        )
        self.assertEqual(
            result["linear_repair_cost"],
            WITNESS_B["expected_linear_cost"],
        )
        self.assertEqual(
            result["partition_repair_cost"],
            WITNESS_B["expected_partition_cost"],
        )
        self.assertEqual(
            result["closure_gap"],
            1,
        )
        self.assertEqual(
            result["result"],
            "PASS",
        )

    def test_witnesses_share_profile_but_differ_in_partition_cost(self):
        result_a = closure_gap(
            WITNESS_A["transition"],
            WITNESS_A["partition"],
        )
        result_b = closure_gap(
            WITNESS_B["transition"],
            WITNESS_B["partition"],
        )

        self.assertEqual(
            result_a["linear_profile"],
            result_b["linear_profile"],
        )
        self.assertEqual(
            result_a["linear_repair_cost"],
            result_b["linear_repair_cost"],
        )
        self.assertNotEqual(
            result_a["partition_repair_cost"],
            result_b["partition_repair_cost"],
        )

    def test_both_witnesses_respect_gap_nonnegativity(self):
        for witness in (WITNESS_A, WITNESS_B):
            result = closure_gap(
                witness["transition"],
                witness["partition"],
            )

            self.assertTrue(
                result["checks"]["gap_nonnegative"],
                msg=(
                    f"negative gap for T={witness['transition']}, "
                    f"partition={witness['partition']}"
                ),
            )


if __name__ == "__main__":
    unittest.main()
