#!/usr/bin/env python3
"""AQARION Track D: exact quotient-defect audit.

Independent implementation.
Exact rational arithmetic.
Uniform block-average projection.
No imports from earlier AQARION scripts.

Verifies:
  delta_TV <= delta_mean <= 2 delta_TV
  ||(I-R) P R||_infinity = delta_mean
  D=0 iff strong lumpability for tested fixtures.

Bounded experiment, not a universal Lean proof.
"""

from fractions import Fraction
from itertools import combinations
from time import perf_counter
import hashlib
import sys


def canonical(labels):
    mapping = {}
    out = []
    for x in labels:
        if x not in mapping:
            mapping[x] = len(mapping)
        out.append(mapping[x])
    return tuple(out)


def get_blocks(labels):
    labels = canonical(labels)
    return [
        tuple(i for i, x in enumerate(labels) if x == j)
        for j in range(max(labels, default=-1) + 1)
    ]


def adjacency(n, edges):
    A = [[0] * n for _ in range(n)]
    for x, y in edges:
        A[x][y] = 1
        A[y][x] = 1
    return A


def random_walk(A):
    n = len(A)
    P = []
    for x in range(n):
        d = sum(A[x])
        if d == 0:
            row = [Fraction(0) for _ in range(n)]
            row[x] = Fraction(1)
        else:
            row = [Fraction(A[x][y], d) for y in range(n)]
        P.append(row)
    return P


def block_transition_vectors(P, labels):
    bs = get_blocks(labels)
    vectors = []
    for x in range(len(P)):
        vectors.append(tuple(
            sum((P[x][z] for z in C), Fraction(0))
            for C in bs
        ))
    return bs, vectors


def l1(a, b):
    return sum((abs(x-y) for x, y in zip(a, b)), Fraction(0))


def total_variation_defect(P, labels):
    bs, vectors = block_transition_vectors(P, labels)
    result = Fraction(0)
    for C in bs:
        for x, y in combinations(C, 2):
            result = max(result, l1(vectors[x], vectors[y]) / 2)
    return result


def mean_defect(P, labels):
    bs, vectors = block_transition_vectors(P, labels)
    result = Fraction(0)

    for C in bs:
        k = len(bs)
        mean = tuple(
            sum((vectors[x][j] for x in C), Fraction(0)) / len(C)
            for j in range(k)
        )
        for x in C:
            result = max(result, l1(vectors[x], mean))
    return result


def identity(n):
    return [
        [Fraction(int(i == j)) for j in range(n)]
        for i in range(n)
    ]


def matmul(A, B):
    return [
        [
            sum(
                (A[i][k] * B[k][j] for k in range(len(B))),
                Fraction(0)
            )
            for j in range(len(B[0]))
        ]
        for i in range(len(A))
    ]


def subtract(A, B):
    return [
        [A[i][j] - B[i][j] for j in range(len(A[0]))]
        for i in range(len(A))
    ]


def projection(labels):
    n = len(labels)
    R = [[Fraction(0) for _ in range(n)] for _ in range(n)]

    for C in get_blocks(labels):
        for x in C:
            for z in C:
                R[x][z] = Fraction(1, len(C))
    return R


def infinity_norm(A):
    return max(
        (
            sum((abs(x) for x in row), Fraction(0))
            for row in A
        ),
        default=Fraction(0)
    )


def strong_lumpable(P, labels):
    bs, vectors = block_transition_vectors(P, labels)
    for C in bs:
        for x, y in combinations(C, 2):
            if vectors[x] != vectors[y]:
                return False
    return True


def defect_matrix(P, labels):
    n = len(P)
    R = projection(labels)
    IminusR = subtract(identity(n), R)
    return matmul(matmul(IminusR, P), R)


def analyse(name, P, labels, expected_lumpable):
    tv = total_variation_defect(P, labels)
    mean = mean_defect(P, labels)
    D = defect_matrix(P, labels)
    norm = infinity_norm(D)
    lumpable = strong_lumpable(P, labels)

    assert tv <= mean
    assert mean <= 2 * tv
    assert norm == mean
    assert lumpable == (mean == 0)
    assert lumpable == expected_lumpable

    print(name)
    print("  DELTA_TV=", tv)
    print("  DELTA_MEAN=", mean)
    print("  DEFECT_INFINITY_NORM=", norm)
    print("  LUMPABLE=", lumpable)
    print("  LOWER_BOUND_PASS=", tv <= mean)
    print("  UPPER_BOUND_PASS=", mean <= 2 * tv)
    print("  MATRIX_IDENTITY_PASS=", norm == mean)
    print("  FIXTURE=PASS")


def run_fixture(name, n, edges, E, F):
    A = adjacency(n, edges)
    P = random_walk(A)

    # Join and meet are encoded independently here.
    # Join via union-find.
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        x, y = find(x), find(y)
        if x != y:
            parent[y] = x

    for labels in (E, F):
        groups = {}
        for i, v in enumerate(labels):
            groups.setdefault(v, []).append(i)
        for group in groups.values():
            for x in group[1:]:
                union(group[0], x)

    J = canonical([find(i) for i in range(n)])
    H = canonical(tuple(zip(E, F)))

    print()
    print("FIXTURE_" + name)
    analyse(name + "_E", P, E, True)
    analyse(name + "_F", P, F, True)
    analyse(name + "_JOIN", P, J, True)
    analyse(name + "_MEET", P, H, False)


def main():
    start = perf_counter()

    print("AQARION TRACK D — QUANTITATIVE DEFECT AUDIT")
    print("ARITHMETIC=EXACT_FRACTION")
    print("PROJECTION=UNIFORM_BLOCK_AVERAGE")
    print("NORM=INDUCED_INFINITY")
    print("IMPLEMENTATION=STANDALONE")

    run_fixture(
        "A",
        6,
        [(0, 4), (0, 5), (1, 2), (1, 3)],
        (0, 0, 1, 2, 1, 2),
        (0, 0, 1, 2, 2, 1),
    )

    run_fixture(
        "B",
        6,
        [(0, 1), (0, 2), (0, 4), (3, 4), (4, 5)],
        (0, 1, 2, 1, 0, 2),
        (0, 1, 2, 2, 0, 1),
    )

    elapsed = perf_counter() - start

    print()
    print("THEORETICAL_BOUND=delta_TV <= delta_mean <= 2*delta_TV")
    print("MATRIX_IDENTITY=||((I-R)PR)||_infinity = delta_mean")
    print("EXACT_ARITHMETIC=PASS")
    print("BOTH_WITNESSES=PASS")
    print("UNIVERSAL_LEAN_PROOF=NOT_RUN")
    print("NOVELTY=NOT_CLAIMED")
    print("ELAPSED_SECONDS=%.6f" % elapsed)
    print("STATUS=COMPLETED_BOUNDED_DEFECT_AUDIT")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("STATUS=FAILED")
        print("ERROR=" + repr(exc))
        sys.exit(1)
