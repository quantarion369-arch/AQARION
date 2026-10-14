"""Exact tests for stable refinement and closure-gap bounds."""

import unittest

from closure_profile import closure_profile
from partition_repair import (
    block_constant_basis,
    closure_gap,
    coarsest_stable_partition,
    first_bit_partition,
    partition_repair_cost,
    shift_register_map,
)


class StableRefinementTests(unittest.TestCase):
    def test_four_state_chain_requires_discrete_refinement(self):
        T = [1, 2, 3, 3]
        partition = [
            [0, 1, 2],
            [3],
        ]

        stable = coarsest_stable_partition(T, partition)

        self.assertEqual(
            stable,
            [[0], [1], [2], [3]],
        )

        result = partition_repair_cost(T, partition)

        self.assertEqual(
            result["partition_repair_cost"],
            2,
        )
        self.assertFalse(
            result["is_initial_partition_stable"]
        )

    def test_invariant_partition_has_zero_cost(self):
        T = [1, 2, 3, 3]
        partition = [
            [0, 1, 2, 3],
        ]

        result = partition_repair_cost(T, partition)

        self.assertEqual(
            result["stable_partition"],
            [[0, 1, 2, 3]],
        )
        self.assertEqual(
            result["partition_repair_cost"],
            0,
        )
        self.assertTrue(
            result["is_initial_partition_stable"]
        )

    def test_shift_register_two_state_words(self):
        word_length = 2
        T = shift_register_map(word_length)
        partition = first_bit_partition(word_length)

        self.assertEqual(
            T,
            [0, 2, 0, 2],
        )

        result = partition_repair_cost(T, partition)

        self.assertEqual(
            result["partition_repair_cost"],
            2,
        )

    def test_shift_register_three_state_words(self):
        word_length = 3
        T = shift_register_map(word_length)
        partition = first_bit_partition(word_length)

        self.assertEqual(
            T,
            [0, 2, 4, 6, 0, 2, 4, 6],
        )

        result = partition_repair_cost(T, partition)

        self.assertEqual(
            result["partition_repair_cost"],
            6,
        )


class ClosureGapTests(unittest.TestCase):
    def test_four_state_chain_gap_is_zero(self):
        T = [1, 2, 3, 3]
        partition = [
            [0, 1, 2],
            [3],
        ]

        result = closure_gap(T, partition)

        self.assertEqual(
            result["linear_profile"],
            [1, 1, 0],
        )
        self.assertEqual(
            result["linear_repair_cost"],
            2,
        )
        self.assertEqual(
            result["partition_repair_cost"],
            2,
        )
        self.assertEqual(
            result["closure_gap"],
            0,
        )
        self.assertEqual(
            result["result"],
            "PASS",
        )

    def test_shift_register_two_state_words_gap(self):
        word_length = 2
        T = shift_register_map(word_length)
        partition = first_bit_partition(word_length)

        result = closure_gap(T, partition)

        self.assertEqual(
            result["linear_repair_cost"],
            1,
        )
        self.assertEqual(
            result["partition_repair_cost"],
            2,
        )
        self.assertEqual(
            result["closure_gap"],
            1,
        )
        self.assertEqual(
            result["result"],
            "PASS",
        )

    def test_shift_register_three_state_words_gap(self):
        word_length = 3
        T = shift_register_map(word_length)
        partition = first_bit_partition(word_length)

        result = closure_gap(T, partition)

        self.assertEqual(
            result["linear_repair_cost"],
            2,
        )
        self.assertEqual(
            result["partition_repair_cost"],
            6,
        )
        self.assertEqual(
            result["closure_gap"],
            4,
        )
        self.assertEqual(
            result["result"],
            "PASS",
        )

    def test_gap_is_nonnegative_for_small_census(self):
        for state_count in (1, 2, 3):
            for transition in self._all_maps(state_count):
                for partition in self._all_partitions(state_count):
                    result = closure_gap(
                        transition,
                        partition,
                    )

                    self.assertTrue(
                        result["checks"]["gap_nonnegative"],
                        msg=(
                            f"negative gap for T={transition}, "
                            f"partition={partition}"
                        ),
                    )

    def _all_maps(self, state_count):
        from itertools import product

        return product(
            range(state_count),
            repeat=state_count,
        )

    def _all_partitions(self, state_count):
        from itertools import combinations

        states = list(range(state_count))

        def generate(remaining):
            if not remaining:
                yield []
                return

            first = remaining[0]

            for size in range(1, len(remaining) + 1):
                for chosen in combinations(remaining, size):
                    chosen_set = set(chosen)
                    rest = [
                        state
                        for state in remaining
                        if state not in chosen_set
                    ]

                    for tail in generate(rest):
                        yield [list(chosen)] + tail

        yield from generate(states)


if __name__ == "__main__":
    unittest.main()
