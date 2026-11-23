#!/usr/bin/env python3

from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import sys
import traceback

Z = F(0)
O = F(1)

CHECKS = 0
HORIZON_CHECKS = 0
SWEEP_CASES = 0

HOME = Path.home()
RECEIPT = HOME / "AQARION_TRACK_D_MULTISTEP_RECEIPT.txt"
MAX_T = 30
MAX_POWER = 20


def check(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(message)


def mm(A, B):
    return [
        [
            sum((x*y for x, y in zip(row, col)), Z)
            for col in zip(*B)
        ]
        for row in A
    ]


def sub(A, B):
    return [[x-y for x, y in zip(a, b)]
            for a, b in zip(A, B)]


def eye(n):
    return [[F(i == j) for j in range(n)]
            for i in range(n)]


def power(A, t):
    result = eye(len(A))
    base = A
    while t:
        if t & 1:
            result = mm(result, base)
        base = mm(base, base)
        t >>= 1
    return result


def vm(v, A):
    return [
        sum((v[i]*A[i][j] for i in range(len(v))), Z)
        for j in range(len(A[0]))
    ]


def vsub(a, b):
    return [x-y for x, y in zip(a, b)]


def l1(v):
    return sum((abs(x) for x in v), Z)


def norm(A):
    return max(
        (sum(map(abs, row), Z) for row in A),
        default=Z
    )


def tau(A):
    return max(
        (l1(vsub(a, b))/2 for a, b in combinations(A, 2)),
        default=Z
    )


def blocks(labels):
    ids = {}
    labels = tuple(ids.setdefault(x, len(ids)) for x in labels)
    return [
        tuple(i for i, x in enumerate(labels) if x == j)
        for j in range(len(ids))
    ]


def system(P, labels):
    n = len(P)
    C = blocks(labels)
    k = len(C)

    S = [
        [F(labels[i] == j) for j in range(k)]
        for i in range(n)
    ]

    L = [
        [
            F(1, len(C[i])) if x in C[i] else Z
            for x in range(n)
        ]
        for i in range(k)
    ]

    R = mm(S, L)
    Q = mm(mm(L, P), S)
    E = sub(mm(P, S), mm(S, Q))
    D = mm(mm(sub(eye(n), R), P), R)

    return S, L, R, Q, E, D


def telescope(P, S, E, Q, t):
    lhs = sub(mm(power(P, t), S),
              mm(S, power(Q, t)))

    rhs = [[Z]*len(Q) for _ in P]

    for r in range(t):
        term = mm(
            mm(power(P, r), E),
            power(Q, t-1-r)
        )
        rhs = [
            [a+b for a, b in zip(x, y)]
            for x, y in zip(rhs, term)
        ]

    return lhs == rhs


def initial_vectors(n):
    result = [
        [F(i == j) for j in range(n)]
        for i in range(n)
    ]
    result.append([F(1, n)]*n)
    return result


def audit(name, P, labels, expected_eps=None):
    global HORIZON_CHECKS

    S, L, R, Q, E, D = system(P, labels)
    n = len(P)
    k = len(Q)

    check(all(
        all(x >= Z for x in row) and sum(row) == O
        for row in P
    ), name + ": P stochastic")

    check(mm(L, S) == eye(k), name + ": LS=I")
    check(mm(S, L) == R, name + ": SL=R")
    check(mm(R, R) == R, name + ": R2=R")
    check(mm(E, L) == D, name + ": D=EL")

    eps = norm(E)
    check(norm(D) == eps, name + ": norm identity")
    check(all(sum(row, Z) == Z for row in E),
          name + ": E row sums zero")

    if expected_eps is not None:
        check(eps == expected_eps, name + ": expected epsilon")

    taus = [tau(power(Q, s)) for s in range(MAX_POWER+1)]

    # Exact primary witness sequence.
    if name == "PRIMARY_WITNESS":
        expected = [
            O, O, F(1,2), F(1,4), F(1,8),
            F(1,16), F(1,32)
        ]
        check(taus[:7] == expected,
              "primary exact contraction sequence")

        check(tau(Q) == O,
              "one-step coefficient equals one")

        check(taus[2] < O,
              "two-step contraction")

    print("\nCASE=" + name, flush=True)
    print("  STATES=" + str(n))
    print("  COARSE_STATES=" + str(k))
    print("  EPSILON=" + str(eps))
    print("  TAU_Q=" + str(taus[1]))
    print("  TAU_Q2=" + str(taus[2]))
    print("  TAU_SEQUENCE=" + str(taus[:10]))

    partial = Z
    for x in taus:
        partial += x

    print("  POWER_SUM_0_20=" + str(partial))

    # Compare both certificates with actual errors.
    for mu in initial_vectors(n):
        for t in range(MAX_T+1):
            true = vm(vm(mu, power(P, t)), S)
            predicted = vm(vm(mu, S), power(Q, t))
            actual = l1(vsub(true, predicted))/2

            multi = min(
                O,
                eps * sum(taus[:t], Z)/2
            )

            old = min(
                O,
                eps * sum((taus[1]**s for s in range(t)), Z)/2
            )

            check(actual <= multi,
                  name + ": multi-step bound t=" + str(t))

            check(actual <= old,
                  name + ": old bound t=" + str(t))

            HORIZON_CHECKS += 1

        for t in (0, 1, 2, 3, 5, 10, 20, 30):
            check(telescope(P, S, E, Q, t),
                  name + ": telescope " + str(t))

    mu = [F(1,n)]*n

    print("  UNIFORM_INITIAL_HORIZONS:", flush=True)

    for t in (0,1,2,3,5,10,20,30):
        true = vm(vm(mu, power(P,t)), S)
        predicted = vm(vm(mu,S),power(Q,t))
        actual = l1(vsub(true,predicted))/2

        multi = min(O, eps*sum(taus[:t],Z)/2)
        old = min(
            O,
            eps*sum((taus[1]**s for s in range(t)),Z)/2
        )

        print(
            "    t=" + str(t)
            + " ACTUAL=" + str(actual)
            + " MULTISTEP=" + str(multi)
            + " ONE_STEP=" + str(old),
            flush=True
        )

    print("  CASE=PASS", flush=True)

    return Q, taus, eps


def main():
    global SWEEP_CASES

    start = datetime.now(timezone.utc)

    print("AQARION TRACK D MULTI-STEP CONTRACTION AUDIT")
    print("UTC_START=" + start.isoformat())
    print("PYTHON=" + sys.version.replace("\n"," "))
    print("ARITHMETIC=EXACT_FRACTION")
    print("MAX_T=" + str(MAX_T))

    # Four-state exact counterexample.
    P = [
        [F(3,5), Z, F(2,5), Z],
        [F(2,5), Z, F(3,5), Z],
        [Z, Z, Z, O],
        [Z, Z, Z, O],
    ]

    labels = (0,0,1,2)

    Q, taus, eps = audit(
        "PRIMARY_WITNESS",
        P,
        labels,
        F(1,5)
    )

    # Verify the infinite sum analytically:
    # tau(I)=1, tau(Q)=1,
    # tau(Q^s)=2^{-(s-1)} for s>=2.
    expected_sum = F(3)

    partial_sum = sum(taus, Z)

    # Tail after the last computed term is positive.
    check(partial_sum < expected_sum,
          "finite partial sum below infinite sum")

    check(partial_sum + taus[-1] == expected_sum,
          "exact geometric tail completion")

    final_bound = eps*expected_sum/2

    check(final_bound == F(3,10),
          "uniform infinite certificate")

    print("\nPRIMARY_INFINITE_CERTIFICATE=" + str(final_bound))
    print("PRIMARY_POWER_SUM=" + str(expected_sum))

    # Adversarial rational perturbation sweep.
    # Perturb both rows in the first block while
    # preserving their average and coarse matrix.
    for delta in (F(1,20), F(1,10), F(1,5), F(1,4)):
        p = [
            [F(1,2)+delta, Z, F(1,2)-delta, Z],
            [F(1,2)-delta, Z, F(1,2)+delta, Z],
            [Z,Z,Z,O],
            [Z,Z,Z,O],
        ]

        audit(
            "PERTURB_" + str(delta),
            p,
            labels,
            2*delta
        )

        SWEEP_CASES += 1

    end = datetime.now(timezone.utc)

    print("\n=== FINAL RECEIPT ===")
    print("PRIMARY_WITNESS=PASS")
    print("PERTURBATION_CASES=" + str(SWEEP_CASES))
    print("CHECKS_PASSED=" + str(CHECKS))
    print("HORIZON_CHECKS=" + str(HORIZON_CHECKS))
    print("MULTISTEP_THEOREM=ANALYTICALLY_DERIVED")
    print("LEAN_PROOF=NOT_RUN")
    print("INDEPENDENT_REPLAY=NOT_CLAIMED")
    print("NOVELTY=NOT_CLAIMED")
    print("UTC_END=" + end.isoformat())
    print("STATUS=COMPLETED_MULTISTEP_AUDIT", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("\nSTATUS=FAILED")
        print("ERROR=" + repr(exc))
        traceback.print_exc()
        sys.exit(1)
