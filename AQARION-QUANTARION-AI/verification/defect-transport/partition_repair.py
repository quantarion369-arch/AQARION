#!/usr/bin/env python3
"""Exact stable-partition refinement and partition-repair cost.

For a finite deterministic map T and an initial partition Pi, this module
computes the coarsest stable refinement Pi_* satisfying

    x ~ y  implies  T(x) ~ T(y).

It also computes the partition-repair cost

    c_part = |Pi_*| - |Pi|.

Together with closure_profile.py, this supports the comparison

    c_lin <= c_part,

where c_lin is the unrestricted linear closure cost.
"""

from closure_profile import closure_profile


def validate_inputs(T, partition):
    T = list(T)
    n = len(T)

    if n == 0:
        raise ValueError("state space must be nonempty")

    for target in T:
        if not isinstance(target, int) or target < 0 or target >= n:
            raise ValueError(
                "T must map {0,...,n-1} into itself"
            )

    if not partition:
        raise ValueError("partition must be nonempty")

    seen = set()

    for block in partition:
        if not block:
            raise ValueError("partition blocks must be nonempty")

        for state in block:
            if not isinstance(state, int) or state < 0 or state >= n:
                raise ValueError(
                    "partition contains an invalid state"
                )

            if state in seen:
                raise ValueError(
                    "partition contains a repeated state"
                )

            seen.add(state)

    if seen != set(range(n)):
        raise ValueError(
            "partition does not cover the state space exactly"
        )

    return T, [list(block) for block in partition]


def labels_from_partition(partition):
    labels = {}

    for block_index, block in enumerate(partition):
        for state in block:
            labels[state] = block_index

    return labels


def partition_from_labels(labels, n):
    blocks = {}

    for state in range(n):
        blocks.setdefault(labels[state], []).append(state)

    return [
        blocks[key]
        for key in sorted(blocks)
    ]


def coarsest_stable_partition(T, partition):
    """Return the coarsest stable refinement of partition under T."""
    T, partition = validate_inputs(T, partition)
    n = len(T)

    labels = labels_from_partition(partition)

    while True:
        signatures = {}
        new_labels = {}

        for state in range(n):
            signature = (
                labels[state],
                labels[T[state]],
            )

            if signature not in signatures:
                signatures[signature] = len(signatures)

            new_labels[state] = signatures[signature]

        if len(signatures) == len(set(labels.values())):
            labels = new_labels
            break

        labels = new_labels

    return partition_from_labels(labels, n)


def partition_repair_cost(T, partition):
    """Compute c_part = |coarsest stable refinement| - |initial partition|."""
    T, partition = validate_inputs(T, partition)

    stable_partition = coarsest_stable_partition(T, partition)

    return {
        "schema": "AQ-PARTITION-REPAIR/1",
        "initial_partition": partition,
        "stable_partition": stable_partition,
        "initial_block_count": len(partition),
        "stable_block_count": len(stable_partition),
        "partition_repair_cost": (
            len(stable_partition) - len(partition)
        ),
        "is_initial_partition_stable": (
            len(stable_partition) == len(partition)
        ),
    }


def block_constant_basis(T, partition):
    """Return indicator columns for the blocks of partition."""
    T, partition = validate_inputs(T, partition)
    n = len(T)

    basis = []

    for block in partition:
        block_set = set(block)

        basis.append(
            [
                int(state in block_set)
                for state in range(n)
            ]
        )

    return basis


def shift_register_map(word_length):
    """Return T for the shift-and-append-zero map on binary words.

    A word (b0, b1, ..., b_{d-1}) maps to
    (b1, ..., b_{d-1}, 0).
    """
    if word_length < 1:
        raise ValueError("word_length must be positive")

    state_count = 2 ** word_length
    transition = []

    for state in range(state_count):
        remaining = state & ((1 << (word_length - 1)) - 1)
        transition.append(remaining << 1)

    return transition


def first_bit_partition(word_length):
    """Return the partition of binary words by their first bit."""
    if word_length < 1:
        raise ValueError("word_length must be positive")

    state_count = 2 ** word_length
    half = state_count // 2

    return [
        list(range(half)),
        list(range(half, state_count)),
    ]


def closure_gap(T, partition):
    """Compute c_lin, c_part, and their gap for one finite system."""
    T, partition = validate_inputs(T, partition)

    linear_result = closure_profile(
        T,
        block_constant_basis(T, partition),
    )

    repair_result = partition_repair_cost(T, partition)

    linear_cost = linear_result[
        "total_linear_repair_cost"
    ]

    partition_cost = repair_result[
        "partition_repair_cost"
    ]

    gap = partition_cost - linear_cost

    checks = {
        "linear_profile_valid": (
            linear_result["result"] == "PASS"
        ),
        "gap_nonnegative": gap >= 0,
    }

    return {
        "schema": "AQ-CLOSURE-GAP/1",
        "transition": T,
        "initial_partition": partition,
        "stable_partition": repair_result[
            "stable_partition"
        ],
        "linear_profile": linear_result["profile"],
        "linear_repair_cost": linear_cost,
        "partition_repair_cost": partition_cost,
        "closure_gap": gap,
        "checks": checks,
        "result": (
            "PASS"
            if all(checks.values())
            else "FAIL"
        ),
    }


def main():
    import json

    T = [1, 2, 3, 3]
    partition = [
        [0, 1, 2],
        [3],
    ]

    result = closure_gap(T, partition)

    print(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
        )
    )

    if result["result"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
