#!/usr/bin/env python3

from fractions import Fraction as Q
from itertools import combinations
from datetime import datetime, timezone
from time import perf_counter
import sys
import traceback

ZERO = Q(0)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical(labels):
    mapping = {}
    result = []
    for label in labels:
        if label not in mapping:
            mapping[label] = len(mapping)
        result.append(mapping[label])
    return tuple(result)


def blocks(labels):
    labels = canonical(labels)
    return [
        tuple(i for i, label in enumerate(labels) if label == j)
        for j in range(max(labels, default=-1) + 1)
    ]


def random_walk(n, edges):
    A = [[0] * n for _ in range(n)]
    for x, y in edges:
        require(0 <= x < n and 0 <= y < n, "Invalid edge")
        require(x != y, "Fixtures must be loop-free")
        require(A[x][y] == 0, "Duplicate edge")
        A[x][y] = A[y][x] = 1

    P = []
    for x in range(n):
        degree = sum(A[x])
        if degree:
            P.append([Q(A[x][y], degree) for y in range(n)])
        else:
            P.append([Q(int(x == y)) for y in range(n)])

    require(
        all(sum(row, ZERO) == 1 for row in P),
        "Transition matrix is not row-stochastic",
    )
    require(
        all(value >= 0 for row in P for value in row),
        "Negative transition probability",
    )
    return P


def matmul(A, B):
    require(bool(A) and bool(B), "Empty matrix")
    require(len(A[0]) == len(B), "Matrix dimension mismatch")
    return [
        [
            sum(
                (A[i][k] * B[k][j] for k in range(len(B))),
                ZERO,
            )
            for j in range(len(B[0]))
        ]
        for i in range(len(A))
    ]


def subtract(A, B):
    require(len(A) == len(B), "Matrix row mismatch")
    require(
        all(len(a) == len(b) for a, b in zip(A, B)),
        "Matrix column mismatch",
    )
    return [
        [x - y for x, y in zip(a, b)]
        for a, b in zip(A, B)
    ]


def infinity_norm(A):
    return max(
        (sum((abs(x) for x in row), ZERO) for row in A),
        default=ZERO,
    )


def l1(a, b):
    require(len(a) == len(b), "Vector dimension mismatch")
    return sum((abs(x - y) for x, y in zip(a, b)), ZERO)


def projection(labels):
    n = len(labels)
    R = [[ZERO for _ in range(n)] for _ in range(n)]
    for C in blocks(labels):
        for x in C:
            for y in C:
                R[x][y] = Q(1, len(C))
    return R


def join_partition(E, F):
    require(len(E) == len(F), "Partition size mismatch")
    parent = list(range(len(E)))

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
        for C in blocks(labels):
            for x in C[1:]:
                union(C[0], x)

    return canonical([find(x) for x in range(len(E))])


def analyse(name, P, labels, expected):
    n = len(P)
    require(len(labels) == n, name + ": label count mismatch")
    require(all(len(row) == n for row in P), "Nonsquare matrix")

    C = blocks(labels)
    vectors = [
        tuple(
            sum((P[x][z] for z in target), ZERO)
            for target in C
        )
        for x in range(n)
    ]

    tv = max(
        (
            l1(vectors[x], vectors[y]) / 2
            for source in C
            for x, y in combinations(source, 2)
        ),
        default=ZERO,
    )

    mean_defect = ZERO
    for source in C:
        mean = tuple(
            sum((vectors[x][j] for x in source), ZERO) / len(source)
            for j in range(len(C))
        )
        for x in source:
            mean_defect = max(mean_defect, l1(vectors[x], mean))

    lumpable = all(
        vectors[x] == vectors[source[0]]
        for source in C
        for x in source
    )

    R = projection(labels)
    require(matmul(R, R) == R, name + ": R^2 != R")
    require(
        all(sum(row, ZERO) == 1 for row in R),
        name + ": projection row sum failure",
    )

    I = [[Q(int(i == j)) for j in range(n)] for i in range(n)]
    D = matmul(matmul(subtract(I, R), P), R)
    norm = infinity_norm(D)
    zero_matrix = [[ZERO for _ in range(n)] for _ in range(n)]

    require(tv <= mean_defect, name + ": lower bound failure")
    require(mean_defect <= 2 * tv, name + ": upper bound failure")
    require(norm == mean_defect, name + ": norm identity failure")
    require(lumpable == (tv == 0), name + ": TV equivalence failure")
    require(
        lumpable == (mean_defect == 0),
        name + ": mean equivalence failure",
    )
    require(
        lumpable == (D == zero_matrix),
        name + ": matrix equivalence failure",
    )
    require(
        (tv, mean_defect, norm) == expected,
        name + ": unexpected exact fixture values: "
        + repr((tv, mean_defect, norm)),
    )

    print(name)
    print("  PARTITION=" + repr(canonical(labels)))
    print("  DELTA_TV=" + str(tv))
    print("  DELTA_MEAN=" + str(mean_defect))
    print("  DEFECT_INFINITY_NORM=" + str(norm))
    print("  LUMPABLE=" + str(lumpable))
    print("  PROJECTION_IDEMPOTENT=PASS")
    print("  DEFECT_BOUNDS=PASS")
    print("  MATRIX_NORM_IDENTITY=PASS")
    print("  ZERO_EQUIVALENCES=PASS")
    print("  EXPECTED_EXACT_VALUES=PASS")
    print("  FIXTURE=PASS")
    return 1


def fixture(name, edges, E, F, expected_meet):
    P = random_walk(6, edges)
    J = join_partition(E, F)
    H = canonical(tuple(zip(E, F)))

    zero = (ZERO, ZERO, ZERO)
    print("\nFIXTURE_" + name)

    tested = 0
    tested += analyse(name + "_E", P, E, zero)
    tested += analyse(name + "_F", P, F, zero)
    tested += analyse(name + "_JOIN", P, J, zero)
    tested += analyse(
        name + "_MEET", P, H,
        (expected_meet, expected_meet, expected_meet),
    )
    return tested


def main():
    start = perf_counter()

    print("AQARION TRACK D - QUANTITATIVE DEFECT AUDIT")
    print("UTC_START=" + datetime.now(timezone.utc).isoformat())
    print("PYTHON=" + sys.version.replace("\n", " "))
    print("ARITHMETIC=EXACT_FRACTION")
    print("PROJECTION=UNIFORM_BLOCK_AVERAGE")
    print("MATRIX_ACTION=COLUMN_OBSERVABLES")
    print("TRANSITION_CONVENTION=ROW_STOCHASTIC")
    print("NORM=MAXIMUM_ABSOLUTE_ROW_SUM")
    print("IMPLEMENTATION=STANDALONE")

    tested = fixture(
        "A",
        [(0, 4), (0, 5), (1, 2), (1, 3)],
        (0, 0, 1, 2, 1, 2),
        (0, 0, 1, 2, 2, 1),
        Q(1),
    )

    tested += fixture(
        "B",
        [(0, 1), (0, 2), (0, 4), (3, 4), (4, 5)],
        (0, 1, 2, 1, 0, 2),
        (0, 1, 2, 2, 0, 1),
        Q(2, 3),
    )

    require(tested == 8, "Incorrect number of analysed partitions")

    print("\nPARTITION_CASES_CHECKED=" + str(tested))
    print("BOTH_WITNESSES=PASS")
    print("UNIVERSAL_LEAN_PROOF=NOT_RUN")
    print("EXHAUSTIVE_SEARCH=NOT_RUN")
    print("NOVELTY=NOT_CLAIMED")
    print("ELAPSED_SECONDS=%.6f" % (perf_counter() - start))
    print("UTC_END=" + datetime.now(timezone.utc).isoformat())
    print("STATUS=COMPLETED_BOUNDED_DEFECT_AUDIT")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
        print("STATUS=FAILED")
        sys.exit(1)
