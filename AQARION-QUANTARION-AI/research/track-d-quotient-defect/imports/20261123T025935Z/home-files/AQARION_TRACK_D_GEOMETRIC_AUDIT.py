#!/usr/bin/env python3

"""
AQARION TRACK D — GEOMETRIC AGGREGATION AUDIT

Exact Fraction arithmetic.
Standard library only.

Tests:
  1. Uniform aggregation identities.
  2. Rectangular and lifted defect identities.
  3. Block-size-sharp defect constant.
  4. Dobrushin contraction coefficient.
  5. Exact telescoping identity.
  6. Finite-horizon linear and geometric bounds.
  7. Multiple initial distributions.
  8. Deterministic and rational stochastic fixtures.

No Lean proof is claimed.
No novelty claim is made.
"""

from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import random
import sys
import traceback

ZERO = F(0)
ONE = F(1)

CHECKS = 0
HORIZON_CHECKS = 0
CASES = 0
MAX_T = 20

OUT = Path.home() / "AQARION_TRACK_D_GEOMETRIC_AUDIT_RECEIPT.txt"


def require(ok, message):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise AssertionError(message)


def matmul(A, B):
    return [
        [
            sum((x*y for x, y in zip(row, col)), ZERO)
            for col in zip(*B)
        ]
        for row in A
    ]


def add(A, B):
    return [
        [x+y for x, y in zip(a, b)]
        for a, b in zip(A, B)
    ]


def sub(A, B):
    return [
        [x-y for x, y in zip(a, b)]
        for a, b in zip(A, B)
    ]


def scale(c, A):
    return [[c*x for x in row] for row in A]


def identity(n):
    return [
        [F(i == j) for j in range(n)]
        for i in range(n)
    ]


def matpow(A, t):
    n = len(A)
    result = identity(n)
    base = A
    while t:
        if t & 1:
            result = matmul(result, base)
        base = matmul(base, base)
        t >>= 1
    return result


def vmat(v, A):
    return [
        sum((v[i]*A[i][j] for i in range(len(v))), ZERO)
        for j in range(len(A[0]))
    ]


def vadd(a, b):
    return [x+y for x, y in zip(a, b)]


def vsub(a, b):
    return [x-y for x, y in zip(a, b)]


def l1(v):
    return sum((abs(x) for x in v), ZERO)


def norm_inf(A):
    return max(
        (sum((abs(x) for x in row), ZERO) for row in A),
        default=ZERO
    )


def canon(labels):
    d = {}
    return tuple(d.setdefault(x, len(d)) for x in labels)


def partition_blocks(labels):
    labels = canon(labels)
    return [
        tuple(i for i, x in enumerate(labels) if x == j)
        for j in range(max(labels)+1)
    ]


def make_system(P, labels):
    n = len(P)
    blocks = partition_blocks(labels)
    k = len(blocks)

    # S: state-to-block membership.
    S = [
        [F(j == labels[i]) for j in range(k)]
        for i in range(n)
    ]

    # L: uniform block-to-state lifting.
    L = [
        [
            F(1, len(blocks[i])) if x in blocks[i] else ZERO
            for x in range(n)
        ]
        for i in range(k)
    ]

    R = matmul(S, L)
    Q = matmul(matmul(L, P), S)
    E = sub(matmul(P, S), matmul(S, Q))

    D = matmul(
        matmul(sub(identity(n), R), P),
        R
    )

    return blocks, S, L, R, Q, E, D


def dobrushin(Q):
    # Maximum total variation distance between rows.
    result = ZERO
    for a, b in combinations(Q, 2):
        result = max(result, l1(vsub(a, b))/2)
    return result


def geometric_sum(tau, t):
    total = ZERO
    power = ONE
    for _ in range(t):
        total += power
        power *= tau
    return total


def stochastic(P):
    return (
        all(len(row) == len(P) for row in P)
        and all(
            all(x >= ZERO for x in row)
            and sum(row, ZERO) == ONE
            for row in P
        )
    )


def initials(n):
    result = []
    for i in range(n):
        result.append([
            F(i == j) for j in range(n)
        ])
    result.append([F(1, n)]*n)
    return result


def exact_telescope(P, S, E, Q, t):
    n = len(P)
    k = len(Q)

    lhs = sub(matmul(matpow(P, t), S),
              matmul(S, matpow(Q, t)))

    rhs = [[ZERO]*k for _ in range(n)]

    for r in range(t):
        term = matmul(
            matmul(matmul(matpow(P, r), E),
                   matpow(Q, t-1-r)),
            identity(k)
        )
        rhs = add(rhs, term)

    return lhs == rhs


def audit(name, P, labels, sharp_m=None):
    global CASES, HORIZON_CHECKS

    CASES += 1
    n = len(P)

    require(stochastic(P), name + ": P stochastic")
    require(len(labels) == n, name + ": partition length")

    blocks, S, L, R, Q, E, D = make_system(P, labels)
    k = len(blocks)

    require(matmul(L, S) == identity(k),
            name + ": LS=I")

    require(matmul(S, L) == R,
            name + ": SL=R")

    require(matmul(R, R) == R,
            name + ": R^2=R")

    require(stochastic(Q),
            name + ": coarse matrix stochastic")

    require(matmul(E, L) == D,
            name + ": D=EL")

    eps = norm_inf(E)
    dnorm = norm_inf(D)

    require(eps == dnorm,
            name + ": norm identity")

    # Original pairwise and mean defects.
    vectors = matmul(P, S)
    tv = ZERO
    mean = ZERO

    for C in blocks:
        avg = [
            sum((vectors[x][j] for x in C), ZERO)
            / len(C)
            for j in range(k)
        ]

        for x in C:
            mean = max(mean, l1(vsub(vectors[x], avg)))

        for x, y in combinations(C, 2):
            tv = max(
                tv,
                l1(vsub(vectors[x], vectors[y]))/2
            )

    m = max(map(len, blocks))

    require(tv <= mean,
            name + ": lower defect bound")

    require(
        mean <= 2*F(m-1, m)*tv,
        name + ": sharp block-size upper bound"
    )

    require(mean == eps,
            name + ": mean equals residual norm")

    tau = dobrushin(Q)

    require(ZERO <= tau <= ONE,
            name + ": Dobrushin range")

    print("\nCASE=" + name, flush=True)
    print("  STATES=" + str(n))
    print("  BLOCKS=" + str(k))
    print("  MAX_BLOCK_SIZE=" + str(m))
    print("  DELTA_TV=" + str(tv))
    print("  EPSILON=" + str(eps))
    print("  DEFECT_NORM=" + str(dnorm))
    print("  DOBRUSHIN_TAU=" + str(tau))
    print("  FIXED_GEOMETRIC_FACTOR=" +
          str(ONE/(ONE-tau)) if tau < ONE
          else "  FIXED_GEOMETRIC_FACTOR=UNBOUNDED")

    # Sharpness verification.
    if sharp_m is not None:
        expected = 2*F(sharp_m-1, sharp_m)
        require(tv == ONE,
                name + ": sharp TV")
        require(mean == expected,
                name + ": sharp upper equality")
        print("  SHARPNESS=PASS", flush=True)

    # Initial distributions: every point mass and uniform.
    for mu in initials(n):
        for t in range(MAX_T+1):
            # True block distribution.
            true_micro = vmat(mu, matpow(P, t))
            true_block = vmat(true_micro, S)

            # Coarse prediction.
            coarse_initial = vmat(mu, S)
            coarse_block = vmat(
                coarse_initial,
                matpow(Q, t)
            )

            actual = l1(vsub(true_block, coarse_block))/2

            linear = min(ONE, F(t)*eps/2)

            geom = min(
                ONE,
                eps*geometric_sum(tau, t)/2
            )

            require(actual <= linear,
                    name + ": linear horizon bound")

            require(actual <= geom,
                    name + ": geometric horizon bound")

            HORIZON_CHECKS += 1

        # Exact matrix telescoping identity.
        for t in (0, 1, 2, 3, 5, 10, MAX_T):
            require(
                exact_telescope(P, S, E, Q, t),
                name + ": telescope t=" + str(t)
            )

    # Report selected actual errors for uniform initialization.
    mu = [F(1, n)]*n
    print("  HORIZON_RESULTS:", flush=True)

    for t in (0, 1, 2, 3, 5, 10, 20):
        true_block = vmat(vmat(mu, matpow(P, t)), S)
        coarse_block = vmat(vmat(mu, S), matpow(Q, t))
        actual = l1(vsub(true_block, coarse_block))/2

        linear = min(ONE, F(t)*eps/2)
        geom = min(ONE, eps*geometric_sum(tau, t)/2)

        print(
            "    t=" + str(t)
            + " ACTUAL=" + str(actual)
            + " LINEAR=" + str(linear)
            + " GEOMETRIC=" + str(geom),
            flush=True
        )

    print("  CASE=PASS", flush=True)


def sharp_fixture(m):
    # States a_1,...,a_m,b.
    # a_1 -> b
    # a_i -> a_2 for i >= 2
    # b -> b

    n = m+1
    P = [[ZERO]*n for _ in range(n)]

    P[0][m] = ONE

    for i in range(1, m):
        P[i][1] = ONE

    P[m][m] = ONE

    labels = [0]*m + [1]

    audit("SHARP_M_" + str(m), P, labels, m)


def random_fixture(seed, name, n, labels):
    rng = random.Random(seed)

    P = []
    for _ in range(n):
        weights = [rng.randint(1, 7) for _ in range(n)]
        total = sum(weights)
        P.append([F(x, total) for x in weights])

    audit(name, P, labels)


def main():
    start = datetime.now(timezone.utc)

    print("AQARION TRACK D GEOMETRIC AUDIT", flush=True)
    print("UTC_START=" + start.isoformat())
    print("PYTHON=" + sys.version.replace("\n", " "))
    print("ARITHMETIC=EXACT_FRACTION")
    print("DEPENDENCIES=STANDARD_LIBRARY_ONLY")
    print("MAX_HORIZON=" + str(MAX_T), flush=True)

    # Exact block-size sharpness tests.
    for m in (2, 3, 4, 5):
        sharp_fixture(m)

    # Existing six-state graph fixtures.
    graph_fixtures = [
        (
            "GRAPH_A",
            [(0,4),(0,5),(1,2),(1,3)],
            (0,0,1,2,1,2)
        ),
        (
            "GRAPH_B",
            [(0,1),(0,2),(0,4),(3,4),(4,5)],
            (0,1,2,1,0,2)
        ),
    ]

    for name, edges, labels in graph_fixtures:
        n = 6
        A = [[0]*n for _ in range(n)]

        for x, y in edges:
            A[x][y] = A[y][x] = 1

        P = [
            [
                F(A[x][y], sum(A[x]))
                if sum(A[x])
                else F(x == y)
                for y in range(n)
            ]
            for x in range(n)
        ]

        audit(name, P, labels)

    # Rational stochastic systems with varied partitions.
    random_fixture(
        0xA7A7103,
        "RATIONAL_1",
        5,
        (0,0,1,1,2)
    )

    random_fixture(
        0xA7A7104,
        "RATIONAL_2",
        6,
        (0,1,0,2,1,2)
    )

    random_fixture(
        0xA7A7105,
        "RATIONAL_3",
        7,
        (0,0,0,1,1,2,2)
    )

    end = datetime.now(timezone.utc)

    print("\n=== FINAL RECEIPT ===", flush=True)
    print("CASES_PASSED=" + str(CASES))
    print("CHECKS_PASSED=" + str(CHECKS))
    print("HORIZON_CHECKS=" + str(HORIZON_CHECKS))
    print("MAX_HORIZON=" + str(MAX_T))
    print("UNIVERSAL_LEAN_PROOF=NOT_RUN")
    print("INDEPENDENT_IMPLEMENTATION=NOT_CLAIMED")
    print("NOVELTY=NOT_CLAIMED")
    print("UTC_END=" + end.isoformat())
    print("STATUS=COMPLETED_EXACT_GEOMETRIC_AUDIT",
          flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("\nSTATUS=FAILED", flush=True)
        print("ERROR=" + repr(exc), flush=True)
        traceback.print_exc()
        sys.exit(1)
