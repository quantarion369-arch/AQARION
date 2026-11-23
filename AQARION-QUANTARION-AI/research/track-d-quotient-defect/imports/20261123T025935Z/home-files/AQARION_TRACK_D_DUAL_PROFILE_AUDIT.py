from fractions import Fraction as F
from datetime import datetime, timezone
import hashlib
import sys

Z, O = F(0), F(1)
MAX_T = 60
CHECKS = 0
HORIZON_CHECKS = 0


def check(ok, message):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise AssertionError(message)


def mm(A, B):
    return [
        [
            sum((A[i][h] * B[h][j] for h in range(len(B))), Z)
            for j in range(len(B[0]))
        ]
        for i in range(len(A))
    ]


def ident(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def sub(A, B):
    return [
        [A[i][j] - B[i][j] for j in range(len(A[0]))]
        for i in range(len(A))
    ]


def add(A, B):
    return [
        [A[i][j] + B[i][j] for j in range(len(A[0]))]
        for i in range(len(A))
    ]


def scale(c, A):
    return [[c*x for x in row] for row in A]


def power(A, n):
    R = ident(len(A))
    B = A
    while n:
        if n & 1:
            R = mm(R, B)
        B = mm(B, B)
        n >>= 1
    return R


def norm(A):
    return max(
        (sum((abs(x) for x in row), Z) for row in A),
        default=Z
    )


def tau(A):
    # Dobrushin coefficient for a stochastic square matrix.
    if len(A) <= 1:
        return Z
    best = Z
    for i in range(len(A)):
        for j in range(len(A)):
            d = sum(
                (abs(A[i][h] - A[j][h]) for h in range(len(A))),
                Z
            ) / 2
            best = max(best, d)
    return best


def rowvec(i, n):
    return [F(j == i) for j in range(n)]


def mv(v, A):
    return [
        sum((v[i] * A[i][j] for i in range(len(v))), Z)
        for j in range(len(A[0]))
    ]


def tv(a, b):
    return sum((abs(x-y) for x, y in zip(a, b)), Z) / 2


def build(P, labels):
    n = len(P)
    blocks = sorted(set(labels))
    k = len(blocks)
    index = {b: i for i, b in enumerate(blocks)}

    S = [[F(index[labels[x]] == j) for j in range(k)]
         for x in range(n)]

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
    D = mm(mm(sub(ident(n), R), P), R)

    check(mm(L, S) == ident(k), "LS=I")
    check(mm(S, L) == R, "SL=R")
    check(mm(R, R) == R, "R^2=R")
    check(mm(E, L) == D, "D=EL")
    check(norm(D) == norm(E), "norm identity")

    return S, L, Q, E


def audit(name, P, labels, expected_eps):
    global HORIZON_CHECKS

    n = len(P)
    S, L, Q, E = build(P, labels)
    k = len(Q)

    check(
        all(all(x >= Z for x in row) and sum(row) == O for row in P),
        name + ": P stochastic"
    )
    check(
        all(all(x >= Z for x in row) and sum(row) == O for row in Q),
        name + ": Q stochastic"
    )

    eps = norm(E)
    check(eps == expected_eps, name + ": exact epsilon")

    # Build both profiles.
    taus = [tau(power(Q, s)) for s in range(MAX_T + 1)]

    Ppowers = [ident(n)]
    etas = []
    for r in range(MAX_T):
        etas.append(norm(mm(Ppowers[-1], E)))
        Ppowers.append(mm(Ppowers[-1], P))

    check(etas[0] == eps, name + ": eta_0=epsilon")
    check(all(x <= eps for x in etas), name + ": eta_r<=epsilon")

    # Verify exact telescoping identity and dual-profile bound.
    worst_actual = Z
    worst_bound = Z
    worst_t = 0
    previous_uniform_bound = Z

    for t in range(MAX_T + 1):
        Pt = Ppowers[t]
        Qt = power(Q, t)

        lhs = sub(mm(Pt, S), mm(S, Qt))

        rhs = [[Z for _ in range(k)] for _ in range(n)]
        if t:
            for r in range(t):
                term = mm(mm(Ppowers[r], E), power(Q, t-1-r))
                rhs = add(rhs, term)

        check(lhs == rhs, name + f": telescope t={t}")

        bound = sum(
            (etas[r] * taus[t-1-r] for r in range(t)),
            Z
        ) / 2
        bound = min(O, bound)

        old_bound = min(
            O,
            eps * sum(taus[:t], Z) / 2
        )
        check(bound <= old_bound, name + f": refinement t={t}")

        actual_at_t = Z

        # Every point mass. Convexity then covers every initial distribution.
        for x in range(n):
            mu = rowvec(x, n)
            true = mv(mu, mm(Pt, S))
            coarse = mv(mv(mu, S), Qt)
            actual = tv(true, coarse)
            check(actual <= bound, name + f": point mass x={x}, t={t}")
            actual_at_t = max(actual_at_t, actual)
            HORIZON_CHECKS += 1

        # Uniform initial distribution.
        mu = [F(1, n)] * n
        true = mv(mu, mm(Pt, S))
        coarse = mv(mv(mu, S), Qt)
        uniform_actual = tv(true, coarse)
        check(
            uniform_actual <= bound,
            name + f": uniform initial t={t}"
        )
        HORIZON_CHECKS += 1

        if bound > worst_bound:
            worst_bound = bound
            worst_t = t

        worst_actual = max(worst_actual, actual_at_t)

        if t in (0, 1, 2, 3, 5, 10, 20, 30, 60):
            print(
                f"  t={t} ETA_BOUND={bound} "
                f"OLD_BOUND={old_bound} "
                f"WORST_POINT_ACTUAL={actual_at_t} "
                f"UNIFORM_ACTUAL={uniform_actual}"
            )

        previous_uniform_bound = bound

    print("  EPSILON=" + str(eps))
    print("  TAU_Q=" + str(taus[1]))
    print("  TAU_Q2=" + str(taus[2]))
    print("  ETA_PROFILE_FIRST_10=" + str(etas[:10]))
    print("  TAU_PROFILE_FIRST_10=" + str(taus[:10]))
    print("  MAX_DUAL_BOUND_0_60=" + str(worst_bound))
    print("  MAX_DUAL_BOUND_HORIZON=" + str(worst_t))
    print("  MAX_POINT_ACTUAL_0_60=" + str(worst_actual))
    print("  CASE=PASS")


def main():
    print("AQARION TRACK D DUAL-PROFILE AUDIT")
    print("UTC_START=" + datetime.now(timezone.utc).isoformat())
    print("ARITHMETIC=EXACT_FRACTION")
    print("MAX_T=" + str(MAX_T))

    labels = [0, 0, 1, 2]

    primary = [
        [F(3,5), Z, F(2,5), Z],
        [F(2,5), Z, F(3,5), Z],
        [Z, Z, Z, O],
        [Z, Z, Z, O],
    ]

    print("\nCASE=PRIMARY_WITNESS")
    audit("PRIMARY_WITNESS", primary, labels, F(1,5))

    for delta in (F(1,20), F(1,10), F(1,5), F(1,4)):
        P = [
            [F(1,2)+delta, Z, F(1,2)-delta, Z],
            [F(1,2)-delta, Z, F(1,2)+delta, Z],
            [Z, Z, Z, O],
            [Z, Z, Z, O],
        ]
        name = "PERTURB_" + str(delta)
        print("\nCASE=" + name)
        audit(name, P, labels, 2*delta)

    print("\n=== FINAL RECEIPT ===")
    print("CASES=5")
    print("CHECKS_PASSED=" + str(CHECKS))
    print("HORIZON_CHECKS=" + str(HORIZON_CHECKS))
    print("DUAL_PROFILE_BOUND=ANALYTICALLY_DERIVED")
    print("LEAN_PROOF=NOT_RUN")
    print("NOVELTY=NOT_CLAIMED")
    print("UTC_END=" + datetime.now(timezone.utc).isoformat())
    print("STATUS=COMPLETED_DUAL_PROFILE_AUDIT")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("\nSTATUS=FAILED")
        print("ERROR=" + repr(exc))
        raise
