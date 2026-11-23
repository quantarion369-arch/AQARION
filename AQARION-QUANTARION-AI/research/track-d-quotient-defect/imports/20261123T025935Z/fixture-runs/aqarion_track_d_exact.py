
#!/usr/bin/env python3
"""
AQARION TRACK D — EXACT FINITE EXPERIMENT

Tracks:
 A. Strong lumpability of rational finite Markov chains.
 B. Equitable partitions of finite undirected graphs.
 C. Exact binomial tails versus Chernoff bounds.

This is an experiment, not a proof of a universal theorem.
No result is called PASS merely because the program completes.

Python standard library only.
"""

from fractions import Fraction
from itertools import product
from math import comb, exp, ceil
import hashlib
import json
import random
import sys
import time


SEED = 0xA7A7103
rng = random.Random(SEED)


def emit(label, value):
    print(f"{label}={value}")


def compositions(total, parts):
    """All ordered nonnegative integer compositions."""
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, parts - 1):
            yield (first,) + rest


def partitions(n):
    """All set partitions as restricted-growth tuples."""
    if n <= 0:
        return
    labels = [0] * n

    def rec(i, maximum):
        if i == n:
            yield tuple(labels)
            return
        for label in range(maximum + 2):
            labels[i] = label
            yield from rec(i + 1, max(maximum, label))

    labels[0] = 0
    yield from rec(1, 0)


def cells(labels):
    count = max(labels) + 1
    return [
        tuple(i for i, label in enumerate(labels) if label == j)
        for j in range(count)
    ]


def union_find_join(p, q):
    """Join = transitive closure of equivalence under p or q."""
    n = len(p)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for labels in (p, q):
        representatives = {}
        for i, label in enumerate(labels):
            if label in representatives:
                union(i, representatives[label])
            else:
                representatives[label] = i

    roots = {}
    out = []
    for i in range(n):
        root = find(i)
        if root not in roots:
            roots[root] = len(roots)
        out.append(roots[root])
    return tuple(out)


def canonical(labels):
    """Canonical restricted-growth encoding."""
    mapping = {}
    out = []
    for x in labels:
        if x not in mapping:
            mapping[x] = len(mapping)
        out.append(mapping[x])
    return tuple(out)


def stochastic_matrix(n, denominator, row_choices):
    return tuple(
        tuple(Fraction(v, denominator) for v in row)
        for row in row_choices
    )


def is_stochastic(P):
    n = len(P)
    return (
        all(len(row) == n for row in P)
        and all(x >= 0 for row in P for x in row)
        and all(sum(row) == 1 for row in P)
    )


def lumpable(P, labels):
    """Exact strong lumpability criterion."""
    blocks = cells(labels)
    for block in blocks:
        for x in block:
            for y in block:
                for target in blocks:
                    sx = sum(P[x][z] for z in target)
                    sy = sum(P[y][z] for z in target)
                    if sx != sy:
                        return False
    return True


def quotient_markov(P, labels):
    """Return exact quotient matrix, or None if not well-defined."""
    if not lumpable(P, labels):
        return None

    blocks = cells(labels)
    Q = []
    for source in blocks:
        representative = source[0]
        row = []
        for target in blocks:
            row.append(sum(P[representative][z] for z in target))
        Q.append(tuple(row))

    Q = tuple(Q)
    if not is_stochastic(Q):
        raise AssertionError("Internal error: quotient is not stochastic")
    return Q


def graph_from_mask(n, mask):
    """Undirected simple graph adjacency matrix."""
    A = [[0] * n for _ in range(n)]
    bit = 0
    for i in range(n):
        for j in range(i + 1, n):
            if (mask >> bit) & 1:
                A[i][j] = 1
                A[j][i] = 1
            bit += 1
    return tuple(tuple(row) for row in A)


def equitable(A, labels):
    """Exact equitable partition test."""
    blocks = cells(labels)
    for source in blocks:
        for x in source:
            for y in source:
                for target in blocks:
                    sx = sum(A[x][z] for z in target)
                    sy = sum(A[y][z] for z in target)
                    if sx != sy:
                        return False
    return True


def quotient_graph(A, labels):
    """Return exact quotient adjacency matrix, or None."""
    if not equitable(A, labels):
        return None

    blocks = cells(labels)
    B = tuple(
        tuple(sum(A[source[0]][z] for z in target)
              for target in blocks)
        for source in blocks
    )

    # Verify A S = S B directly, without relying on the
    # quotient construction as its own correctness check.
    n = len(A)
    k = len(blocks)
    S = tuple(
        tuple(1 if i in blocks[j] else 0 for j in range(k))
        for i in range(n)
    )

    for i in range(n):
        for j in range(k):
            left = sum(A[i][v] * S[v][j] for v in range(n))
            right = sum(S[i][r] * B[r][j] for r in range(k))
            if left != right:
                raise AssertionError("A S = S B failed")

    return B


def experiment_markov():
    print("\n=== TRACK A: RATIONAL MARKOV CHAINS ===")

    cases = [
        (2, 2),
        (3, 2),
        (3, 3),
    ]

    matrix_count = 0
    partition_count = 0
    lumpable_partition_count = 0
    join_pair_count = 0
    quotient_count = 0
    failures = []

    for n, denominator in cases:
        parts = list(partitions(n))
        rows = list(compositions(denominator, n))
        print(
            f"MARKOV_CASE n={n} denominator={denominator} "
            f"partitions={len(parts)} row_types={len(rows)}"
        )

        for row_choices in product(rows, repeat=n):
            P = stochastic_matrix(n, denominator, row_choices)
            if not is_stochastic(P):
                raise AssertionError("Generated matrix is not stochastic")
            matrix_count += 1

            good = []
            for pi in parts:
                partition_count += 1
                if lumpable(P, pi):
                    good.append(pi)
                    lumpable_partition_count += 1
                    Q = quotient_markov(P, pi)
                    if Q is None:
                        failures.append(("quotient_missing", n, P, pi))
                    else:
                        quotient_count += 1

            # Check every pair of lumpable partitions.
            for i in range(len(good)):
                for j in range(i, len(good)):
                    join_pair_count += 1
                    joined = union_find_join(good[i], good[j])
                    if not lumpable(P, joined):
                        failures.append(
                            ("join_closure", n, P, good[i], good[j], joined)
                        )

    emit("MARKOV_MATRICES_CHECKED", matrix_count)
    emit("MARKOV_PARTITION_TESTS", partition_count)
    emit("MARKOV_LUMPABLE_PARTITIONS", lumpable_partition_count)
    emit("MARKOV_QUOTIENTS_CONSTRUCTED", quotient_count)
    emit("MARKOV_JOIN_PAIRS_CHECKED", join_pair_count)
    emit("MARKOV_COUNTEREXAMPLES", len(failures))

    if failures:
        print("MARKOV_FIRST_COUNTEREXAMPLE=", repr(failures[0]))
    else:
        print("MARKOV_OBSERVATION=No counterexample in tested finite cases")


def experiment_graphs():
    print("\n=== TRACK B: EQUITABLE GRAPH PARTITIONS ===")

    exhaustive_graphs = 0
    sampled_graphs = 0
    partition_tests = 0
    equitable_count = 0
    join_pair_count = 0
    failures = []
    meet_counterexample = None

    # Exhaust all simple graphs through n=4.
    for n in range(2, 5):
        parts = list(partitions(n))
        edge_count = n * (n - 1) // 2

        for mask in range(1 << edge_count):
            A = graph_from_mask(n, mask)
            exhaustive_graphs += 1
            good = []

            for pi in parts:
                partition_tests += 1
                if equitable(A, pi):
                    good.append(pi)
                    equitable_count += 1
                    B = quotient_graph(A, pi)
                    if B is None:
                        failures.append(("quotient_missing", n, mask, pi))

            for i in range(len(good)):
                for j in range(i, len(good)):
                    join_pair_count += 1
                    joined = union_find_join(good[i], good[j])
                    if not equitable(A, joined):
                        failures.append(
                            ("join_closure", n, mask, good[i], good[j], joined)
                        )

            # Search for a meet counterexample. The meet is the
            # common refinement, represented by pairs of labels.
            if meet_counterexample is None:
                for i in range(len(good)):
                    for j in range(i + 1, len(good)):
                        p, q = good[i], good[j]
                        meet = canonical(tuple((p[x], q[x]) for x in range(n)))
                        if not equitable(A, meet):
                            meet_counterexample = (n, mask, p, q, meet)
                            break
                    if meet_counterexample is not None:
                        break

    # Deterministic additional sample at n=5.
    n = 5
    parts = list(partitions(n))
    edge_count = n * (n - 1) // 2
    for _ in range(200):
        mask = rng.randrange(1 << edge_count)
        A = graph_from_mask(n, mask)
        sampled_graphs += 1
        good = []

        for pi in parts:
            partition_tests += 1
            if equitable(A, pi):
                good.append(pi)
                equitable_count += 1
                if quotient_graph(A, pi) is None:
                    failures.append(("sampled_quotient_missing", mask, pi))

        for i in range(len(good)):
            for j in range(i, len(good)):
                join_pair_count += 1
                joined = union_find_join(good[i], good[j])
                if not equitable(A, joined):
                    failures.append(
                        ("sampled_join_closure", mask, good[i], good[j], joined)
                    )

    emit("GRAPH_EXHAUSTIVE_GRAPHS", exhaustive_graphs)
    emit("GRAPH_SAMPLED_N5_GRAPHS", sampled_graphs)
    emit("GRAPH_PARTITION_TESTS", partition_tests)
    emit("GRAPH_EQUITABLE_PARTITIONS", equitable_count)
    emit("GRAPH_JOIN_PAIRS_CHECKED", join_pair_count)
    emit("GRAPH_COUNTEREXAMPLES", len(failures))

    if failures:
        print("GRAPH_FIRST_COUNTEREXAMPLE=", repr(failures[0]))
    else:
        print("GRAPH_OBSERVATION=No join-closure counterexample in tested cases")

    if meet_counterexample is None:
        print("MEET_CONTROL=No meet counterexample found in this search")
    else:
        print("MEET_CONTROL_COUNTEREXAMPLE=", repr(meet_counterexample))


def binomial_probability(n, p, k):
    return Fraction(comb(n, k)) * p**k * (1-p)**(n-k)


def exact_binomial_tail(n, p, predicate):
    return sum(
        (binomial_probability(n, p, k)
         for k in range(n + 1) if predicate(k)),
        Fraction(0, 1)
    )


def experiment_concentration():
    print("\n=== TRACK C: EXACT BINOMIAL / CHERNOFF TESTS ===")

    cases = 0
    upper_checked = 0
    lower_checked = 0
    violations = []

    probabilities = [
        Fraction(1, 4),
        Fraction(1, 2),
        Fraction(3, 4),
    ]
    deltas = [
        Fraction(1, 4),
        Fraction(1, 2),
        Fraction(1, 1),
    ]

    for n in range(1, 21):
        for p in probabilities:
            mu = n * p
            for delta in deltas:
                cases += 1
                threshold_upper = (1 + delta) * mu
                threshold_lower = (1 - delta) * mu

                # Strict event X > (1+delta)mu.
                upper = exact_binomial_tail(
                    n, p, lambda k: Fraction(k, 1) > threshold_upper
                )
                upper_bound = exp(
                    -(float(delta) ** 2) * float(mu)
                    / (2.0 + float(delta))
                )
                upper_checked += 1
                if float(upper) > upper_bound + 1e-12:
                    violations.append(
                        ("upper", n, str(p), str(delta),
                         str(upper), upper_bound)
                    )

                # Lower-tail bound applies for 0 < delta < 1.
                if delta < 1:
                    lower = exact_binomial_tail(
                        n, p, lambda k: Fraction(k, 1) < threshold_lower
                    )
                    lower_bound = exp(
                        -(float(delta) ** 2) * float(mu) / 2.0
                    )
                    lower_checked += 1
                    if float(lower) > lower_bound + 1e-12:
                        violations.append(
                            ("lower", n, str(p), str(delta),
                             str(lower), lower_bound)
                        )

    emit("BINOMIAL_PARAMETER_CASES", cases)
    emit("CHERNOFF_UPPER_TESTS", upper_checked)
    emit("CHERNOFF_LOWER_TESTS", lower_checked)
    emit("CHERNOFF_NUMERICAL_VIOLATIONS", len(violations))

    if violations:
        print("CHERNOFF_FIRST_VIOLATION=", repr(violations[0]))
    else:
        print("CHERNOFF_OBSERVATION=No violation in tested cases")

    print(
        "CHERNOFF_CAVEAT=Exact rational tails; floating-point "
        "exponential-bound comparison"
    )


def main():
    start = time.time()
    print("AQARION TRACK D — EXACT FINITE EXPERIMENT")
    print("UTC_OR_LOCAL_TIME=", time.strftime("%Y-%m-%dT%H:%M:%S"))
    print("PYTHON=", sys.version.replace("\n", " "))
    print("SEED=", SEED)
    print("ARITHMETIC=Fraction exact except displayed exponential bounds")

    experiment_markov()
    experiment_graphs()
    experiment_concentration()

    elapsed = time.time() - start
    emit("ELAPSED_SECONDS", f"{elapsed:.3f}")
    print("EXPERIMENT_STATUS=COMPLETED; NOT A UNIVERSAL PROOF")
    print("RESEARCH_STATUS=NO NOVELTY CLAIM; RESULTS REQUIRE REVIEW")


if __name__ == "__main__":
    main()

