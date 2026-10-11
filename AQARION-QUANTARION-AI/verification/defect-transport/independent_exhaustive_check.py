#!/usr/bin/env python3
"""
Independent exact exhaustive audit for finite deterministic defect operators.

This checker is implementation-independent at the Python module level: it does
not import defect_auditor.py. It is not an independent mathematical proof.

Declared finite domain:
    all maps T : [n] -> [n] and all set partitions of [n], n = 1, 2, 3, 4.

Validated identities on that finite domain:
    1. rank(D) equals rank(D restricted to the block-constant subspace);
    2. rank(D) <= min(k - 1, n - k), where k is the number of blocks;
    3. D = 0 if and only if the partition is forward congruent for T;
    4. ||D||_F^2 equals the exact block-transport energy formula.

The script also includes a permanent negative regression showing that the
retired support-component rank formula is false under its former
support-clique definition.

A PASS is exact bounded computational evidence on the declared finite domain.
It is not a universal proof, a Lean certificate, or a repository-bound replay
until output, command, revision, and source hash are preserved together.
"""

from fractions import Fraction
from itertools import product
import json
import platform
import sys


def partitions(n):
    """Yield all set partitions of [n] via restricted-growth strings."""
    if n < 1:
        raise ValueError("n must be positive")

    labels = [0] * n

    def rec(position, maximum_label):
        if position == n:
            blocks = [[] for _ in range(maximum_label + 1)]
            for state in range(n):
                blocks[labels[state]].append(state)
            yield tuple(tuple(block) for block in blocks)
            return

        for label in range(maximum_label + 2):
            labels[position] = label
            yield from rec(position + 1, max(maximum_label, label))

    yield from rec(1, 0)


def rank_q(matrix):
    """Return exact matrix rank over Q using Gauss-Jordan elimination."""
    if not matrix:
        return 0

    row_count = len(matrix)
    column_count = len(matrix[0])
    if any(len(row) != column_count for row in matrix):
        raise ValueError("matrix rows must have equal length")

    working = [[Fraction(entry) for entry in row] for row in matrix]
    pivot_row = 0

    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if working[row][column] != 0
            ),
            None,
        )

        if pivot is None:
            continue

        working[pivot_row], working[pivot] = (
            working[pivot],
            working[pivot_row],
        )

        pivot_value = working[pivot_row][column]
        working[pivot_row] = [
            entry / pivot_value
            for entry in working[pivot_row]
        ]

        for row in range(row_count):
            if row == pivot_row or working[row][column] == 0:
                continue

            multiplier = working[row][column]
            working[row] = [
                entry - multiplier * pivot_entry
                for entry, pivot_entry in zip(
                    working[row],
                    working[pivot_row],
                )
            ]

        pivot_row += 1
        if pivot_row == row_count:
            break

    return pivot_row


def matmul(left, right):
    """Multiply exact matrices."""
    if not left or not right:
        raise ValueError("matrices must be nonempty")

    shared_dimension = len(right)
    if any(len(row) != shared_dimension for row in left):
        raise ValueError("incompatible matrix dimensions")

    output_columns = len(right[0])
    if any(len(row) != output_columns for row in right):
        raise ValueError("right matrix rows must have equal length")

    return [
        [
            sum(
                left[row][inner] * right[inner][column]
                for inner in range(shared_dimension)
            )
            for column in range(output_columns)
        ]
        for row in range(len(left))
    ]


def labels_for_blocks(n, blocks):
    """Return the block label of every state and validate a partition."""
    label = [None] * n

    for block_index, block in enumerate(blocks):
        if not block:
            raise ValueError("partition blocks must be nonempty")

        for state in block:
            if not isinstance(state, int) or isinstance(state, bool):
                raise ValueError("states must be non-Boolean integers")
            if state < 0 or state >= n:
                raise ValueError("partition state outside [n]")
            if label[state] is not None:
                raise ValueError("partition blocks must be disjoint")
            label[state] = block_index

    if any(block_index is None for block_index in label):
        raise ValueError("partition blocks must cover [n]")

    return label


def transport_matrix(T, blocks, label):
    """Return M[beta][alpha] = |{x in B_beta : T(x) in B_alpha}|."""
    n = len(T)
    k = len(blocks)
    matrix = [[0] * k for _ in range(k)]

    for source_block, block in enumerate(blocks):
        for state in block:
            image = T[state]
            if not isinstance(image, int) or isinstance(image, bool):
                raise ValueError("map images must be non-Boolean integers")
            if image < 0 or image >= n:
                raise ValueError("map image outside [n]")
            matrix[source_block][label[image]] += 1

    return matrix


def averaging_projection(n, blocks):
    """Return the block-averaging projection P as an exact rational matrix."""
    projection = [
        [Fraction(0) for _ in range(n)]
        for _ in range(n)
    ]

    for block in blocks:
        weight = Fraction(1, len(block))
        for row in block:
            for column in block:
                projection[row][column] = weight

    return projection


def pullback_matrix(T):
    """
    Return K for the pullback convention (Kf)(x) = f(T(x)).

    Equivalently, K[x][T[x]] = 1.
    """
    n = len(T)
    return [
        [
            Fraction(int(T[row] == column))
            for column in range(n)
        ]
        for row in range(n)
    ]


def forward_congruent(T, blocks, label):
    """Return whether every source block maps into one target block."""
    return all(
        len({label[T[state]] for state in block}) <= 1
        for block in blocks
    )


def legacy_support_components(transport):
    """
    Return components under the retired support-clique construction.

    Kept only for the permanent negative regression. It does not determine
    rank(D) in general.
    """
    k = len(transport)
    adjacency = [set() for _ in range(k)]

    for row in transport:
        support = {
            target
            for target, count in enumerate(row)
            if count > 0
        }
        for target in support:
            adjacency[target].update(support)

    seen = set()
    components = []

    for vertex in range(k):
        if vertex in seen:
            continue

        stack = [vertex]
        component = []
        seen.add(vertex)

        while stack:
            current = stack.pop()
            component.append(current)

            for neighbor in adjacency[current]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)

        components.append(tuple(sorted(component)))

    return tuple(components)


def audit(T, blocks):
    """Compute exact defect, ranks, transport data, and energy identities."""
    n = len(T)
    if n < 1:
        raise ValueError("T must be nonempty")
    if not blocks:
        raise ValueError("partition must have at least one block")

    k = len(blocks)
    label = labels_for_blocks(n, blocks)
    sizes = [len(block) for block in blocks]
    transport = transport_matrix(T, blocks, label)

    projection = averaging_projection(n, blocks)
    pullback = pullback_matrix(T)

    complement = [
        [
            Fraction(int(row == column)) - projection[row][column]
            for column in range(n)
        ]
        for row in range(n)
    ]

    defect = matmul(complement, matmul(pullback, projection))

    restricted_defect = [
        [
            sum(defect[row][column] for column in block)
            for block in blocks
        ]
        for row in range(n)
    ]

    energy_direct = sum(
        (entry * entry for row in defect for entry in row),
        Fraction(0),
    )

    energy_transport = sum(
        (
            Fraction(
                transport[source][target]
                * (sizes[source] - transport[source][target]),
                sizes[source] * sizes[target],
            )
            for source in range(k)
            for target in range(k)
        ),
        Fraction(0),
    )

    components = legacy_support_components(transport)

    return {
        "n": n,
        "k": k,
        "blocks": tuple(tuple(block) for block in blocks),
        "transport_matrix": transport,
        "rank_full": rank_q(defect),
        "rank_restricted": rank_q(restricted_defect),
        "rank_ceiling": min(k - 1, n - k),
        "forward_congruent": forward_congruent(T, blocks, label),
        "energy_direct": energy_direct,
        "energy_transport": energy_transport,
        "legacy_support_components": components,
        "legacy_component_count": len(components),
        "legacy_predicted_rank": k - len(components),
    }


def assert_partition_generator():
    """Verify Bell-number counts for the declared domain."""
    expected = {1: 1, 2: 2, 3: 5, 4: 15}

    observed = {
        n: len(list(partitions(n)))
        for n in expected
    }

    assert observed == expected, (observed, expected)
    return observed


def assert_legacy_support_rank_counterexample():
    """
    Reject the false legacy support-component rank formula.

    T = (0, 1, 0), Pi = {{0,1}, {2}} gives:
        M = [[2, 0],
             [1, 0]]

    The legacy support-clique graph has two singleton components, predicting
    rank 0, while exact calculation gives rank(D) = 1.
    """
    T = (0, 1, 0)
    blocks = ((0, 1), (2,))
    result = audit(T, blocks)

    assert result["transport_matrix"] == [[2, 0], [1, 0]], result
    assert result["legacy_component_count"] == 2, result
    assert result["legacy_predicted_rank"] == 0, result
    assert result["rank_full"] == 1, result
    assert result["rank_restricted"] == 1, result
    assert result["rank_full"] != result["legacy_predicted_rank"], result

    return {
        "map": list(T),
        "partition": [list(block) for block in blocks],
        "transport_matrix": result["transport_matrix"],
        "legacy_component_count": result["legacy_component_count"],
        "legacy_predicted_rank": result["legacy_predicted_rank"],
        "exact_rank": result["rank_full"],
        "pass": True,
        "conclusion": (
            "The retired support-component rank formula is false: "
            "support connectivity alone does not determine rank(D)."
        ),
    }


def assert_same_support_weight_control():
    """
    Check that equal support patterns can have different exact energies.

    Both transport matrices have positive entries in every position and rank 1,
    but the weights and exact Frobenius defect energies differ.
    """
    blocks = ((0, 1, 2, 3), (4, 5, 6, 7))
    maps = (
        (0, 4, 5, 6, 0, 1, 2, 4),
        (0, 1, 4, 5, 0, 1, 4, 5),
    )

    first = audit(maps[0], blocks)
    second = audit(maps[1], blocks)

    assert first["transport_matrix"] == [[1, 3], [3, 1]], first
    assert second["transport_matrix"] == [[2, 2], [2, 2]], second
    assert first["rank_full"] == 1, first
    assert second["rank_full"] == 1, second
    assert first["energy_direct"] == Fraction(3, 4), first
    assert second["energy_direct"] == Fraction(1, 1), second
    assert first["energy_direct"] != second["energy_direct"], (
        first,
        second,
    )

    return {
        "M1": first["transport_matrix"],
        "M2": second["transport_matrix"],
        "rank1": first["rank_full"],
        "rank2": second["rank_full"],
        "energy1": str(first["energy_direct"]),
        "energy2": str(second["energy_direct"]),
        "pass": True,
        "conclusion": (
            "The examples have the same transport support and the same "
            "defect rank, but different exact defect energies."
        ),
    }


def main():
    bell_counts = assert_partition_generator()

    per_n = []
    total_pairs = 0
    rank_ceiling_passes = 0
    restricted_full_rank_agreement_passes = 0
    zero_defect_forward_congruence_passes = 0
    energy_identity_passes = 0

    for n in range(1, 5):
        all_partitions = list(partitions(n))
        map_partition_pairs = 0

        for T in product(range(n), repeat=n):
            for blocks in all_partitions:
                result = audit(T, blocks)

                assert result["rank_full"] == result["rank_restricted"], (
                    "full/restricted rank disagreement",
                    n,
                    T,
                    blocks,
                    result,
                )
                restricted_full_rank_agreement_passes += 1

                assert result["rank_full"] <= result["rank_ceiling"], (
                    "rank-ceiling violation",
                    n,
                    T,
                    blocks,
                    result,
                )
                rank_ceiling_passes += 1

                assert (
                    result["rank_full"] == 0
                ) == result["forward_congruent"], (
                    "zero-defect/forward-congruence disagreement",
                    n,
                    T,
                    blocks,
                    result,
                )
                zero_defect_forward_congruence_passes += 1

                assert result["energy_direct"] == result["energy_transport"], (
                    "energy-identity violation",
                    n,
                    T,
                    blocks,
                    result,
                )
                energy_identity_passes += 1
                map_partition_pairs += 1

        total_pairs += map_partition_pairs
        per_n.append(
            {
                "n": n,
                "maps": n**n,
                "partitions": len(all_partitions),
                "map_partition_pairs": map_partition_pairs,
                "all_checks_pass": True,
            }
        )

    assert total_pairs == 3984, total_pairs
    assert rank_ceiling_passes == total_pairs
    assert restricted_full_rank_agreement_passes == total_pairs
    assert zero_defect_forward_congruence_passes == total_pairs
    assert energy_identity_passes == total_pairs

    output = {
        "suite": (
            "finite-map defect rank-bound, exactness, and energy "
            "exhaustive audit"
        ),
        "domain": (
            "all deterministic maps T:[n]->[n] and all set partitions, "
            "n=1..4"
        ),
        "arithmetic": "exact rational arithmetic via fractions.Fraction",
        "implementation_independence": (
            "This checker does not import defect_auditor.py; it is not "
            "an independent mathematical proof."
        ),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "partition_counts": bell_counts,
        "per_n": per_n,
        "total_map_partition_pairs": total_pairs,
        "rank_ceiling_passes": rank_ceiling_passes,
        "restricted_full_rank_agreement_passes": (
            restricted_full_rank_agreement_passes
        ),
        "zero_defect_forward_congruence_passes": (
            zero_defect_forward_congruence_passes
        ),
        "energy_identity_passes": energy_identity_passes,
        "retired_support_rank_counterexample": (
            assert_legacy_support_rank_counterexample()
        ),
        "same_support_weight_control": assert_same_support_weight_control(),
        "verdict": (
            "PASS on the declared finite domain for the rank ceiling, "
            "full-versus-restricted rank agreement, "
            "zero-defect/forward-congruence equivalence, and the exact "
            "transport-energy identity; not a universal proof, Lean "
            "certificate, repository-bound replay, or external reproduction."
        ),
    }

    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
