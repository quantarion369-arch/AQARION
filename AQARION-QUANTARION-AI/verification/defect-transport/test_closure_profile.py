"""Exact regression tests for the iterated Koopman closure profile."""

import unittest

from closure_profile import closure_profile


def ones(n):
    return [1] * n


def indicator(n, state):
    return [int(state == x) for x in range(n)]


class ClosureProfileTests(unittest.TestCase):
    def test_four_state_chain_profile(self):
        T = [1, 2, 3, 3]
        initial_basis = [
            ones(4),
            indicator(4, 3),
        ]

        result = closure_profile(T, initial_basis)

        self.assertEqual(result["profile"], [1, 1, 0])
        self.assertEqual(result["defect_ranks"], [1, 1, 0])
        self.assertEqual(result["initial_dimension"], 2)
        self.assertEqual(result["final_dimension"], 4)
        self.assertEqual(
            result["total_linear_repair_cost"],
            2,
        )
        self.assertTrue(result["checks"]["increment_identity"])
        self.assertTrue(result["checks"]["monotonicity"])
        self.assertTrue(result["checks"]["telescoping_sum"])
        self.assertEqual(result["result"], "PASS")

    def test_invariant_observable_space_has_zero_profile(self):
        T = [1, 2, 3, 3]
        initial_basis = [ones(4)]

        result = closure_profile(T, initial_basis)

        self.assertEqual(result["profile"], [0])
        self.assertEqual(result["defect_ranks"], [0])
        self.assertEqual(result["initial_dimension"], 1)
        self.assertEqual(result["final_dimension"], 1)
        self.assertEqual(
            result["total_linear_repair_cost"],
            0,
        )
        self.assertEqual(result["result"], "PASS")

    def test_profile_monotonicity(self):
        T = [1, 2, 3, 3]
        initial_basis = [
            ones(4),
            indicator(4, 3),
        ]

        result = closure_profile(T, initial_basis)
        profile = result["profile"]

        self.assertTrue(
            all(
                profile[index + 1] <= profile[index]
                for index in range(len(profile) - 1)
            )
        )

    def test_telescoping_sum(self):
        T = [1, 2, 3, 3]
        initial_basis = [
            ones(4),
            indicator(4, 3),
        ]

        result = closure_profile(T, initial_basis)

        self.assertEqual(
            result["total_linear_repair_cost"],
            sum(result["profile"]),
        )

        self.assertEqual(
            result["final_dimension"] - result["initial_dimension"],
            sum(result["profile"]),
        )

    def test_different_dynamics_can_share_zero_profile(self):
        identity_T = [0, 1, 2]
        permutation_T = [1, 2, 0]

        full_basis = [
            indicator(3, 0),
            indicator(3, 1),
            indicator(3, 2),
        ]

        identity_result = closure_profile(
            identity_T,
            full_basis,
        )

        permutation_result = closure_profile(
            permutation_T,
            full_basis,
        )

        self.assertEqual(identity_result["profile"], [0])
        self.assertEqual(permutation_result["profile"], [0])
        self.assertEqual(
            identity_result["total_linear_repair_cost"],
            0,
        )
        self.assertEqual(
            permutation_result["total_linear_repair_cost"],
            0,
        )


if __name__ == "__main__":
    unittest.main()
