from fractions import Fraction as F
from itertools import product
from datetime import datetime, timezone
import random
import hashlib

Z, O = F(0), F(1)
SEED = 0xD0B2A51
RANDOM_CASES = 120
RANDOM_HORIZON = 12
EXHAUSTIVE_HORIZON = 8

CHECKS = 0
HORIZON_CHECKS = 0
CASES = 0
STRICT_IMPROVEMENTS = 0
MAX_RATIO = Z
MAX_RATIO_CASE = None


def check(ok, msg):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise AssertionError(msg)


def mm(A, B):
    return [
        [
            sum((A[i][h] * B[h][j] for h in range(len(B))), Z)
            for j in range(len(B[0]))
        ]
        for i in range(len(A))
    ]


def add(A, B):
    return [
        [A[i][j] + B[i][j] for j in range(len(A[0]))]
        for i in range(len(A))
    ]


def sub(A, B):
    return [
        [A[i][j] - B[i][j] for j in range(len(A[0]))]
        for i in range(len(A))
    ]


def ident(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def norm(A):
    return max(
        (sum((abs(x) for x in row), Z) for row in A),
        default=Z
    )


def tau(A):
    if len(A) <= 1:
        return Z
    return max(
        (
            sum(
                (abs(A[i][h] - A[j][h]) for h in range(len(A))),
                Z
            ) / 2
            for i in range(len(A))
            for j in range(len(A))
        ),
        default=Z
    )


def mv(v, A):
    return [
        sum((v[i] * A[i][j] for i in range(len(v))), Z)
        for j in range(len(A[0]))
    ]


def tv(a, b):
    return sum((abs(x-y) for x, y in zip(a, b)), Z) / 2


def power_step(A, B):
    return mm(A, B)


def partitions_rgs(n):
    # Restricted-growth strings enumerate every set partition once.
    if n == 0:
        yield []
        return

    labels = [0] * n

    def rec(pos, max_label):
        if pos == n:
            yield labels[:]
            return
        for v in range(max_label + 2):
            labels[pos] = v
            yield from rec(pos + 1, max(max_label, v))

    labels[0] = 0
    yield from rec(1, 0)


def build(P, labels):
    n = len(P)
    blocks = sorted(set(labels))
    k = len(blocks)
    index = {b: i for i, b in enumerate(blocks)}

    S = [
        [F(index[labels[x]] == j) for j in range(k)]
        for x in range(n)
    ]

    sizes = [labels.count(b) for b in blocks]
    L = [
        [
            F(1, sizes[j]) if labels[x] == blocks[j] else Z
            for x in range(n)
        ]
        for j in range(k)
    ]

    R = mm(S, L)
    Q = mm(mm(L, P), S)
    E = sub(mm(P, S), mm(S, Q))

    check(mm(L, S) == ident(k), "LS=I")
    check(mm(S, L) == R, "SL=R")
    check(mm(R, R) == R, "R2=R")
    check(norm(E) == norm(mm(E, L)), "D=EL norm")
    check(
        all(sum(row, Z) == Z for row in E),
        "E row sums zero"
    )

    return S, Q, E


def audit(name, P, labels, horizon):
    global CASES, HORIZON_CHECKS
    global STRICT_IMPROVEMENTS, MAX_RATIO, MAX_RATIO_CASE

    n = len(P)
    S, Q, E = build(P, labels)
    k = len(Q)

    check(
        all(
            all(x >= Z for x in row) and sum(row) == O
            for row in P
        ),
        name + ": P stochastic"
    )
    check(
        all(
            all(x >= Z for x in row) and sum(row) == O
            for row in Q
        ),
        name + ": Q stochastic"
    )

    eps = norm(E)

    # Exact powers.
    Ppowers = [ident(n)]
    Qpowers = [ident(k)]
    etas = []
    taus = []

    for r in range(horizon + 1):
        etas.append(norm(mm(Ppowers[r], E)))
        taus.append(tau(Qpowers[r]))
        if r < horizon:
            Ppowers.append(mm(Ppowers[-1], P))
            Qpowers.append(mm(Qpowers[-1], Q))

    check(etas[0] == eps, name + ": eta0")
    check(
        all(etas[i+1] <= etas[i] for i in range(horizon)),
        name + ": eta monotonicity"
    )
    check(
        all(taus[i+1] <= taus[i] for i in range(horizon)),
        name + ": tau monotonicity"
    )

    for i in range(horizon + 1):
        for j in range(horizon + 1 - i):
            check(
                taus[i+j] <= taus[i] * taus[j],
                name + ": tau submultiplicativity"
            )

    max_dual = Z
    max_old = Z
    max_actual = Z
    max_t = 0

    for t in range(horizon + 1):
        lhs = sub(mm(Ppowers[t], S), mm(S, Qpowers[t]))

        rhs = [[Z for _ in range(k)] for _ in range(n)]
        for r in range(t):
            term = mm(
                mm(Ppowers[r], E),
                Qpowers[t-1-r]
            )
            rhs = add(rhs, term)

        check(lhs == rhs, name + f": telescoping t={t}")

        dual = min(
            O,
            sum(
                (
                    etas[r] * taus[t-1-r]
                    for r in range(t)
                ),
                Z
            ) / 2
        )

        old = min(
            O,
            eps * sum(taus[:t], Z) / 2
        )

        check(dual <= old, name + f": dual<=old t={t}")

        actual_t = Z
        for x in range(n):
            mu = [F(i == x) for i in range(n)]
            true = mv(mu, mm(Ppowers[t], S))
            coarse = mv(mv(mu, S), Qpowers[t])
            actual = tv(true, coarse)

            check(
                actual <= dual,
                name + f": point mass t={t}, x={x}"
            )
            actual_t = max(actual_t, actual)
            HORIZON_CHECKS += 1

        check(
            actual_t <= dual,
            name + f": worst point mass t={t}"
        )

        if dual < old:
            STRICT_IMPROVEMENTS += 1

        if old > Z:
            ratio = dual / old
            if ratio > MAX_RATIO:
                MAX_RATIO = ratio
                MAX_RATIO_CASE = (name, t)

        max_dual = max(max_dual, dual)
        max_old = max(max_old, old)
        max_actual = max(max_actual, actual_t)

        if dual > max_t * O:
            pass

    CASES += 1

    return {
        "eps": eps,
        "max_dual": max_dual,
        "max_old": max_old,
        "max_actual": max_actual,
    }


def compositions(total, n):
    if n == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total-first, n-1):
            yield (first,) + rest


def exhaustive_n3():
    rows = list(compositions(2, 3))
    matrices = list(product(rows, repeat=3))
    parts = list(partitions_rgs(3))

    print("\nEXHAUSTIVE_N3")
    print("ROW_TYPES=" + str(len(rows)))
    print("STOCHASTIC_MATRICES=" + str(len(matrices)))
    print("PARTITIONS=" + str(len(parts)))
    print("EXPECTED_CASES=" + str(len(matrices) * len(parts)))

    for mi, raw in enumerate(matrices):
        P = [[F(x, 2) for x in row] for row in raw]
        for pi, labels in enumerate(parts):
            audit(
                f"EXH3_M{mi}_P{pi}",
                P,
                labels,
                EXHAUSTIVE_HORIZON
            )


def randomized_sweep():
    rng = random.Random(SEED)
    print("\nRANDOMIZED_SWEEP")
    print("SEED=" + hex(SEED))
    print("CASES=" + str(RANDOM_CASES))

    for case in range(RANDOM_CASES):
        n = rng.randint(4, 7)
        k = rng.randint(2, n)

        P = []
        for _ in range(n):
            weights = [rng.randint(0, 8) for _ in range(n)]
            if sum(weights) == 0:
                weights[rng.randrange(n)] = 1
            total = sum(weights)
            P.append([F(x, total) for x in weights])

        raw_labels = [rng.randrange(k) for _ in range(n)]
        # Ensure every block is represented.
        raw_labels[:k] = list(range(k))
        labels = raw_labels

        audit(
            f"RAND_{case:03d}_N{n}_K{k}",
            P,
            labels,
            RANDOM_HORIZON
        )


def main():
    print("AQARION TRACK D ADVERSARIAL SWEEP")
    print("UTC_START=" + datetime.now(timezone.utc).isoformat())
    print("ARITHMETIC=EXACT_FRACTION")
    print("EXHAUSTIVE_HORIZON=" + str(EXHAUSTIVE_HORIZON))
    print("RANDOM_HORIZON=" + str(RANDOM_HORIZON))

    exhaustive_n3()
    randomized_sweep()

    print("\n=== FINAL RECEIPT ===")
    print("CASES_COMPLETED=" + str(CASES))
    print("CHECKS_PASSED=" + str(CHECKS))
    print("HORIZON_CHECKS=" + str(HORIZON_CHECKS))
    print("STRICT_DUAL_IMPROVEMENTS=" + str(STRICT_IMPROVEMENTS))
    print("MAX_DUAL_TO_OLD_RATIO=" + str(MAX_RATIO))
    print("MAX_RATIO_CASE=" + str(MAX_RATIO_CASE))
    print("SEED=" + hex(SEED))
    print("LEAN_PROOF=NOT_RUN")
    print("NOVELTY=NOT_CLAIMED")
    print("UTC_END=" + datetime.now(timezone.utc).isoformat())
    print("STATUS=COMPLETED_ADVERSARIAL_SWEEP")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("\nSTATUS=FAILED")
        print("ERROR=" + repr(exc))
        raise
