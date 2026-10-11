#!/usr/bin/env python3
"""Exact exhaustive audit of the finite-map support-rank and energy identities."""
from fractions import Fraction
from itertools import product
import json
import platform
import sys


def partitions(n):
    """Restricted-growth-string enumeration of set partitions of [n]."""
    if n < 1:
        raise ValueError("n must be positive")
    labels = [0] * n

    def rec(pos, max_label):
        if pos == n:
            blocks = [[] for _ in range(max_label + 1)]
            for x, label in enumerate(labels):
                blocks[label].append(x)
            yield tuple(tuple(block) for block in blocks)
            return
        for label in range(max_label + 2):
            labels[pos] = label
            yield from rec(pos + 1, max(max_label, label))

    labels[0] = 0
    yield from rec(1, 0)


def rank_q(matrix):
    """Exact Gaussian-elimination rank over Q."""
    A = [[Fraction(x) for x in row] for row in matrix]
    if not A:
        return 0
    rows, cols = len(A), len(A[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next(
            (r for r in range(pivot_row, rows) if A[r][col]),
            None,
        )
        if pivot is None:
            continue
        A[pivot_row], A[pivot] = A[pivot], A[pivot_row]
        p = A[pivot_row][col]
        A[pivot_row] = [x / p for x in A[pivot_row]]
        for r in range(rows):
            if r != pivot_row and A[r][col]:
                q = A[r][col]
                A[r] = [
                    x - q * y
                    for x, y in zip(A[r], A[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def matmul(A, B):
    return [
        [
            sum(A[i][r] * B[r][j] for r in range(len(B)))
            for j in range(len(B[0]))
        ]
        for i in range(len(A))
    ]


def audit(T, blocks):
    n, k = len(T), len(blocks)
    label = [None] * n
    for i, block in enumerate(blocks):
        for x in block:
            label[x] = i
    sizes = [len(block) for block in blocks]

    M = [[0] * k for _ in range(k)]
    for i, block in enumerate(blocks):
        for x in block:
            M[i][label[T[x]]] += 1

    P = [
        [Fraction(0) for _ in range(n)]
        for _ in range(n)
    ]
    for block in blocks:
        for x in block:
            for y in block:
                P[x][y] = Fraction(1, len(block))

    # Pullback convention: K[x,T(x)] = 1.
    K = [
        [Fraction(int(T[x] == y)) for y in range(n)]
        for x in range(n)
    ]
    IminusP = [
        [
            Fraction(int(x == y)) - P[x][y]
            for y in range(n)
        ]
        for x in range(n)
    ]
    D = matmul(IminusP, matmul(K, P))

    # Support graph: all vertices in each support set are connected.
    support = [
        {j for j, value in enumerate(row) if value > 0}
        for row in M
    ]
    adjacency = [set() for _ in range(k)]
    for S in support:
        for j in S:
            adjacency[j].update(S)

    seen, components = set(), []
    for v in range(k):
        if v in seen:
            continue
        stack, component = [v], []
        seen.add(v)
        while stack:
            u = stack.pop()
            component.append(u)
            for w in adjacency[u]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        components.append(sorted(component))
    c = len(components)

    # D restricted to V_Pi: columns are D applied to block indicators.
    restricted = [
        [sum(D[x][y] for y in block) for block in blocks]
        for x in range(n)
    ]
    component_indicators = [
        [Fraction(int(j in C)) for C in components]
        for j in range(k)
    ]
    kernel_basis_annihilated = all(
        sum(
            restricted[x][j] * component_indicators[j][q]
            for j in range(k)
        ) == 0
        for x in range(n)
        for q in range(c)
    )

    rank_full = rank_q(D)
    rank_restricted = rank_q(restricted)
    energy_direct = sum(
        (x * x for row in D for x in row),
        Fraction(0),
    )
    energy_transport = sum(
        (
            Fraction(
                M[i][j] * (sizes[i] - M[i][j]),
                sizes[i] * sizes[j],
            )
            for i in range(k)
            for j in range(k)
        ),
        Fraction(0),
    )

    return {
        "rank_full": rank_full,
        "rank_restricted": rank_restricted,
        "predicted_rank": k - c,
        "component_count": c,
        "component_basis_annihilated": kernel_basis_annihilated,
        "component_basis_independent": rank_q(component_indicators) == c,
        "energy_direct": energy_direct,
        "energy_transport": energy_transport,
        "transport_matrix": M,
    }


def main():
    per_n = []
    total = 0

    for n in range(1, 5):
        parts = list(partitions(n))
        checks = 0
        for T in product(range(n), repeat=n):
            for blocks in parts:
                result = audit(T, blocks)
                assert result["rank_full"] == result["predicted_rank"], (
                    n, T, blocks, result
                )
                assert result["rank_restricted"] == result["predicted_rank"], (
                    n, T, blocks, result
                )
                assert result["component_basis_annihilated"], (
                    n, T, blocks, result
                )
                assert result["component_basis_independent"], (
                    n, T, blocks, result
                )
                assert result["energy_direct"] == result["energy_transport"], (
                    n, T, blocks, result
                )
                checks += 1

        total += checks
        per_n.append({
            "n": n,
            "maps": n**n,
            "partitions": len(parts),
            "map_partition_pairs": checks,
            "all_checks_pass": True,
        })

    blocks = [[0, 1, 2, 3], [4, 5, 6, 7]]
    pair = []
    for T in (
        [0, 4, 5, 6, 0, 1, 2, 4],
        [0, 1, 4, 5, 0, 1, 4, 5],
    ):
        pair.append(audit(T, blocks))

    assert pair[0]["transport_matrix"] == [[1, 3], [3, 1]]
    assert pair[1]["transport_matrix"] == [[2, 2], [2, 2]]
    assert pair[0]["predicted_rank"] == pair[1]["predicted_rank"] == 1
    assert pair[0]["energy_direct"] == Fraction(3, 4)
    assert pair[1]["energy_direct"] == Fraction(1, 1)

    output = {
        "suite": "finite-map support-rank and energy exhaustive audit",
        "domain": "all maps T:[n]->[n] and all set partitions, n=1..4",
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "per_n": per_n,
        "total_map_partition_pairs": total,
        "rank_identity_passes": total,
        "restricted_rank_identity_passes": total,
        "component_kernel_basis_checks_pass": total,
        "component_basis_independence_passes": total,
        "energy_identity_passes": total,
        "same_support_weight_pair": {
            "M1": pair[0]["transport_matrix"],
            "M2": pair[1]["transport_matrix"],
            "rank1": pair[0]["rank_full"],
            "rank2": pair[1]["rank_full"],
            "energy1": str(pair[0]["energy_direct"]),
            "energy2": str(pair[1]["energy_direct"]),
            "pass": True,
        },
        "verdict": (
            "PASS on declared finite domain; "
            "not a universal proof or Lean certificate"
        ),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
