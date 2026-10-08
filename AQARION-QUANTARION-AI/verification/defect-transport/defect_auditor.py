#!/usr/bin/env python3
"""Exact-rational finite-map defect auditor.

Input JSON:
{
  "T": [1, 2, 0],
  "partition": [[0, 2], [1]]
}
States are 0,...,n-1. Blocks must be nonempty and partition
the state space exactly. Verdicts use exact rational arithmetic.
"""
from fractions import Fraction
import argparse
import json
from pathlib import Path

def matmul(A, B):
    return [
        [
            sum(A[i][r] * B[r][j] for r in range(len(B)))
            for j in range(len(B[0]))
        ]
        for i in range(len(A))
    ]

def rank_q(A):
    A = [[Fraction(x) for x in row] for row in A]
    if not A:
        return 0
    rows, cols = len(A), len(A[0])
    pivot_row = 0

    for col in range(cols):
        pivot = next(
            (i for i in range(pivot_row, rows) if A[i][col]),
            None,
        )
        if pivot is None:
            continue

        A[pivot_row], A[pivot] = A[pivot], A[pivot_row]
        p = A[pivot_row][col]
        A[pivot_row] = [x / p for x in A[pivot_row]]

        for i in range(rows):
            if i != pivot_row and A[i][col]:
                q = A[i][col]
                A[i] = [
                    x - q * y
                    for x, y in zip(A[i], A[pivot_row])
                ]

        pivot_row += 1
        if pivot_row == rows:
            break

    return pivot_row

def connected_components(k, edges):
    adj = [set() for _ in range(k)]
    for a, b in edges:
        if a != b:
            adj[a].add(b)
            adj[b].add(a)

    seen, out = set(), []
    for start in range(k):
        if start in seen:
            continue

        stack, component = [start], []
        seen.add(start)

        while stack:
            x = stack.pop()
            component.append(x)
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)

        out.append(sorted(component))

    return out

def canonical_partition(T, partition):
    n = len(T)
    if n == 0:
        raise ValueError("state space must be nonempty")

    if any(
        not isinstance(y, int) or y < 0 or y >= n
        for y in T
    ):
        raise ValueError(
            "T must map {0,...,n-1} into itself"
        )

    if not partition or any(not block for block in partition):
        raise ValueError("partition must have nonempty blocks")

    label = {}
    for i, block in enumerate(partition):
        for x in block:
            if not isinstance(x, int) or x < 0 or x >= n:
                raise ValueError(
                    f"invalid state in block {i}: {x}"
                )
            if x in label:
                raise ValueError(f"state {x} occurs more than once")
            label[x] = i

    if set(label) != set(range(n)):
        raise ValueError("partition does not cover the state space")

    return label

def audit(T, partition):
    T = list(T)
    partition = [list(B) for B in partition]
    label = canonical_partition(T, partition)

    n, k = len(T), len(partition)
    sizes = [len(B) for B in partition]

    # M[i][j] = number of x in B_i with T(x) in B_j.
    M = [[0] * k for _ in range(k)]
    for i, block in enumerate(partition):
        for x in block:
            M[i][label[T[x]]] += 1

    # Orthogonal block-averaging projection.
    P = [
        [Fraction(0) for _ in range(n)]
        for _ in range(n)
    ]
    for block in partition:
        for x in block:
            for y in block:
                P[x][y] = Fraction(1, len(block))

    # Pullback convention: (Kf)(x)=f(T(x)), K[x,T[x]]=1.
    K = [
        [Fraction(int(T[x] == y)) for y in range(n)]
        for x in range(n)
    ]

    I_minus_P = [
        [
            Fraction(int(x == y)) - P[x][y]
            for y in range(n)
        ]
        for x in range(n)
    ]
    D = matmul(I_minus_P, matmul(K, P))

    # Support graph on target-block indices.
    support = [
        {j for j, count in enumerate(row) if count > 0}
        for row in M
    ]
    edges = sorted({
        (a, b)
        for S in support
        for a in S
        for b in S
        if a < b
    })
    components = connected_components(k, edges)
    c = len(components)

    # Column j of A is D applied to the indicator of block j.
    A = [
        [
            sum(D[x][y] for y in block)
            for block in partition
        ]
        for x in range(n)
    ]

    rank_D = rank_q(D)
    rank_restricted = rank_q(A)

    # One indicator vector per connected component.
    component_basis = [
        [Fraction(int(j in C)) for C in components]
        for j in range(k)
    ]
    basis_rank = rank_q(component_basis)

    basis_annihilated = all(
        sum(
            A[x][j] * component_basis[j][q]
            for j in range(k)
        ) == 0
        for x in range(n)
        for q in range(c)
    )

    kernel_dim = k - rank_restricted

    # Direct exact Frobenius energy.
    energy_direct = sum(
        x * x for row in D for x in row
    )

    # Exact transport identity:
    # sum_ij M_ij (|B_i|-M_ij)/(|B_i||B_j|).
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

    checks = {
        "rank_identity": rank_D == k - c,
        "restricted_rank_identity": rank_restricted == k - c,
        "component_kernel_basis_annihilated": basis_annihilated,
        "component_kernel_basis_independent": basis_rank == c,
        "kernel_dimension": kernel_dim == c,
        "energy_identity": energy_direct == energy_transport,
    }

    return {
        "state_count": n,
        "block_count": k,
        "T": T,
        "partition": partition,
        "block_sizes": sizes,
        "transport_matrix": M,
        "support_sets": [sorted(s) for s in support],
        "support_graph_edges": [list(e) for e in edges],
        "support_graph_components": components,
        "component_count": c,
        "actual_rank_D": rank_D,
        "predicted_rank": k - c,
        "restricted_rank": rank_restricted,
        "kernel_dimension": kernel_dim,
        "component_kernel_basis_rank": basis_rank,
        "frobenius_squared_direct": str(energy_direct),
        "frobenius_squared_transport": str(energy_transport),
        "checks": checks,
        "result": "PASS" if all(checks.values()) else "FAIL",
    }

def self_test():
    fixtures = [
        (
            "identity_singletons",
            [0, 1, 2, 3],
            [[0], [1], [2], [3]],
        ),
        (
            "cycle_pair_merge",
            [1, 2, 3, 0],
            [[0, 2], [1], [3]],
        ),
        (
            "constant_map",
            [0, 0, 0, 0],
            [[0, 1], [2], [3]],
        ),
        (
            "mixed_transport",
            [1, 1, 3, 2, 4, 4],
            [[0, 1], [2], [3, 4], [5]],
        ),
    ]

    results = []
    for name, T, partition in fixtures:
        result = audit(T, partition)
        result["fixture"] = name
        results.append(result)

    # Same support, different positive multiplicities.
    blocks = [[0, 1, 2, 3], [4, 5, 6, 7]]
    T1 = [0, 4, 5, 6, 0, 1, 2, 4]
    T2 = [0, 1, 4, 5, 0, 1, 4, 5]

    a, b = audit(T1, blocks), audit(T2, blocks)
    support_same = a["support_sets"] == b["support_sets"]
    rank_same = a["actual_rank_D"] == b["actual_rank_D"]
    energy_different = (
        a["frobenius_squared_direct"]
        != b["frobenius_squared_direct"]
    )

    support_weight = {
        "same_support": support_same,
        "M1": a["transport_matrix"],
        "M2": b["transport_matrix"],
        "rank1": a["actual_rank_D"],
        "rank2": b["actual_rank_D"],
        "energy1": a["frobenius_squared_direct"],
        "energy2": b["frobenius_squared_direct"],
        "support_rank_invariant": support_same and rank_same,
        "energy_distinguishes_pair": energy_different,
        "result": (
            "PASS"
            if support_same and rank_same and energy_different
            else "FAIL"
        ),
    }

    all_fixture_checks = all(
        r["result"] == "PASS" for r in results
    )

    # Mutation control: deliberately halve the transport formula.
    wrong_half_normalization = sum(
        (
            Fraction(1, 2)
            * Fraction(
                a["transport_matrix"][i][j]
                * (
                    a["block_sizes"][i]
                    - a["transport_matrix"][i][j]
                ),
                a["block_sizes"][i] * a["block_sizes"][j],
            )
            for i in range(a["block_count"])
            for j in range(a["block_count"])
        ),
        Fraction(0),
    )
    normalization_mutation_detected = (
        Fraction(a["frobenius_squared_direct"])
        != wrong_half_normalization
    )

    # Orientation control: cycle versus inverse cycle.
    cycle_T = [1, 2, 3, 0]
    inverse_cycle_T = [3, 0, 1, 2]
    orientation_partition = [[0, 1], [2], [3]]

    forward_a = audit(cycle_T, orientation_partition)
    inverse_a = audit(inverse_cycle_T, orientation_partition)
    orientation_control_detected = (
        forward_a["transport_matrix"]
        != inverse_a["transport_matrix"]
    )

    all_pass = (
        all_fixture_checks
        and support_weight["result"] == "PASS"
        and normalization_mutation_detected
        and orientation_control_detected
    )

    return {
        "fixtures": results,
        "fixture_count": len(results),
        "fixture_rank_passes": sum(
            r["checks"]["rank_identity"] for r in results
        ),
        "fixture_kernel_passes": sum(
            all(
                r["checks"][key]
                for key in (
                    "component_kernel_basis_annihilated",
                    "component_kernel_basis_independent",
                    "kernel_dimension",
                )
            )
            for r in results
        ),
        "fixture_energy_passes": sum(
            r["checks"]["energy_identity"] for r in results
        ),
        "support_weight_experiment": support_weight,
        "mutation_controls": {
            "wrong_energy_normalization_detected":
                normalization_mutation_detected,
            "reversed_map_changes_transport_matrix":
                orientation_control_detected,
        },
        "all_pass": all_pass,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_json",
        nargs="?",
        help="JSON file with T and partition",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run built-in exact fixtures and mutation controls",
    )
    parser.add_argument(
        "--output",
        help="optional path for JSON output",
    )
    args = parser.parse_args()

    if args.self_test:
        result = self_test()
    elif args.input_json:
        data = json.loads(
            Path(args.input_json).read_text(encoding="utf-8")
        )
        result = audit(data["T"], data["partition"])
    else:
        parser.error("provide input_json or --self-test")

    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(
            rendered + "\n",
            encoding="utf-8",
        )
    print(rendered)

    if args.self_test and not result["all_pass"]:
        raise SystemExit(1)
    if not args.self_test and result.get("result") == "FAIL":
        raise SystemExit(1)

if __name__ == "__main__":
    main()
