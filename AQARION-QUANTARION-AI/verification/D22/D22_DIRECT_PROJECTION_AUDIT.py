#!/usr/bin/env python3
"""D22 direct-projection audit under the locked cyclic-shift convention.

This program performs bounded exact-arithmetic checks. Its PASS labels refer
only to the domains printed in the report; they are not unbounded proof
certificates and do not establish equivalence with an external D22 source.
"""

from fractions import Fraction


ZERO = Fraction(0)
ONE = Fraction(1)
HALF = Fraction(1, 2)

SYMBOLIC_K_MIN = 3
SYMBOLIC_K_MAX = 1000
DENSE_K_MIN = 3
DENSE_K_MAX = 20


def delta(a, b):
    return int(a == b)


def lag_scalar(k, d, m):
    """L_m(d) = u_d^T K^m u_d, with K e_j = e_(j-1 mod k)."""
    m %= k
    return 2 * delta(m, 0) - delta(m, d) - delta(m, (-d) % k)


def shifted_difference(k, d, m):
    """Sparse row e_m^T - e_(m+d)^T, with indices modulo k."""
    out = {}
    i = m % k
    j = (m + d) % k

    out[i] = out.get(i, ZERO) + ONE
    out[j] = out.get(j, ZERO) - ONE

    return {i: v for i, v in out.items() if v != ZERO}


def lag_row(k, d, m):
    """Sparse row a_d^(m)^T = u_d^T K^m P_d."""
    out = shifted_difference(k, d, m)
    L = lag_scalar(k, d, m)

    out[0] = out.get(0, ZERO) - HALF * L
    out[d] = out.get(d, ZERO) + HALF * L

    return {i: v for i, v in out.items() if v != ZERO}


def closed_factor(k, d):
    """Closed factor for the m=1 specialization."""
    out = shifted_difference(k, d, 1)
    boundary = int(d == 1) + int(d == k - 1)

    out[0] = out.get(0, ZERO) + HALF * boundary
    out[d] = out.get(d, ZERO) - HALF * boundary

    return {i: v for i, v in out.items() if v != ZERO}


def sparse_equal(a, b):
    a = {i: v for i, v in a.items() if v != ZERO}
    b = {i: v for i, v in b.items() if v != ZERO}
    return a == b


def dot_with_u(k, d, row):
    return row.get(0, ZERO) - row.get(d, ZERO)


def symbolic_case(k, d):
    derived = lag_row(k, d, 1)
    closed = closed_factor(k, d)

    assert sparse_equal(derived, closed), (k, d, derived, closed)

    # P_d u_d = 0, so a_d^T u_d = 0.
    assert dot_with_u(k, d, derived) == ZERO

    expected_lag = -int(d == 1) - int(d == k - 1)
    assert lag_scalar(k, d, 1) == expected_lag

    return True


def dense_projection(k, d):
    """Independent exact dense construction for small k."""
    K = [
        [Fraction(int(i == (j - 1) % k)) for j in range(k)]
        for i in range(k)
    ]

    u = [
        Fraction(int(i == 0) - int(i == d))
        for i in range(k)
    ]

    P = [
        [
            Fraction(int(i == j)) - HALF * u[i] * u[j]
            for j in range(k)
        ]
        for i in range(k)
    ]

    Q = [
        [Fraction(int(i == j)) - P[i][j] for j in range(k)]
        for i in range(k)
    ]

    D = [
        [
            sum(
                Q[i][r] * K[r][s] * P[s][j]
                for r in range(k)
                for s in range(k)
            )
            for j in range(k)
        ]
        for i in range(k)
    ]

    a = closed_factor(k, d)

    R = [
        [
            HALF * u[i] * a.get(j, ZERO)
            for j in range(k)
        ]
        for i in range(k)
    ]

    assert D == R, (k, d, D, R)

    D2 = [
        [
            sum(D[i][r] * D[r][j] for r in range(k))
            for j in range(k)
        ]
        for i in range(k)
    ]

    assert all(
        value == ZERO
        for row in D2
        for value in row
    )

    return True


def norm_squared(k, d):
    a = closed_factor(k, d)
    return sum(v * v for v in a.values()) / 2


def check_autocorrelation_orientation(k, d):
    """Check all potentially nonzero lag residues for d versus k-d.

    The formula

        L_m(d) = 2*delta(m, 0) - delta(m, d) - delta(m, -d)

    is zero outside m in {0, d, -d mod k}. The reflected parameter k-d
    has the corresponding support at {0, k-d, d}. Checking the union
    of these residues is exhaustive for this formula and avoids comparing
    two length-k lists for every (k, d) pair.
    """
    reflected = (k - d) % k

    candidate_lags = {
        0,
        d % k,
        (-d) % k,
        reflected,
        (-reflected) % k,
    }

    for m in candidate_lags:
        left = lag_scalar(k, d, m)
        right = lag_scalar(k, reflected, m)

        assert left == right, (k, d, m, left, right)

    return len(candidate_lags)


def run():
    symbolic_cases = 0

    # Bounded exhaustive parameter sweep, not an unbounded symbolic proof.
    for k in range(SYMBOLIC_K_MIN, SYMBOLIC_K_MAX + 1):
        for d in range(1, k):
            symbolic_case(k, d)
            symbolic_cases += 1

    # Independent dense matrix check over a smaller parameter range.
    dense_cases = 0

    for k in range(DENSE_K_MIN, DENSE_K_MAX + 1):
        for d in range(1, k):
            dense_projection(k, d)
            dense_cases += 1

    # Exact norm law over the declared bounded parameter range.
    norm_cases = 0

    for k in range(SYMBOLIC_K_MIN, SYMBOLIC_K_MAX + 1):
        for d in range(1, k):
            value = norm_squared(k, d)

            if d in (1, k - 1):
                assert value == Fraction(3, 4), (k, d, value)
            else:
                assert value == ONE, (k, d, value)

            norm_cases += 1

    # Exhaustive check of the potentially nonzero lag residues.
    orientation_cases = 0
    orientation_lag_checks = 0

    for k in range(SYMBOLIC_K_MIN, SYMBOLIC_K_MAX + 1):
        for d in range(1, k):
            orientation_lag_checks += check_autocorrelation_orientation(k, d)
            orientation_cases += 1

    print("D22-DIRECT-PROJECTION-AUDIT")
    print(f"SYMBOLIC_K_RANGE={SYMBOLIC_K_MIN}..{SYMBOLIC_K_MAX}")
    print("SYMBOLIC_D_RANGE=1..k-1")
    print(f"SYMBOLIC_CASES={symbolic_cases}")

    print(f"DENSE_K_RANGE={DENSE_K_MIN}..{DENSE_K_MAX}")
    print("DENSE_D_RANGE=1..k-1")
    print(f"DENSE_CASES={dense_cases}")

    print(f"NORM_K_RANGE={SYMBOLIC_K_MIN}..{SYMBOLIC_K_MAX}")
    print(f"NORM_CASES={norm_cases}")

    print(f"ORIENTATION_K_RANGE={SYMBOLIC_K_MIN}..{SYMBOLIC_K_MAX}")
    print(f"ORIENTATION_CASES={orientation_cases}")
    print(f"ORIENTATION_LAG_CHECKS={orientation_lag_checks}")

    print("CLOSED_FORM=PASS")
    print("LAG_IDENTITY=PASS")
    print("A_D_ORTHOGONAL_U=PASS")
    print("RANK_ONE_FACTOR=PASS")
    print("NILPOTENCY=PASS")
    print("FROBENIUS_SPLIT=PASS")
    print("AUTOCORRELATION_ORIENTATION_AMBIGUITY=CONFIRMED")

    print("STATUS=BOUNDED_EXHAUSTIVE_CHECKS_PASS_UNDER_LOCKED_CONVENTION")
    print("SOURCE_EQUIVALENCE=OPEN")
    print("LEAN_FORMAL_VERIFICATION=NOT_ESTABLISHED_BY_THIS_SCRIPT")


if __name__ == "__main__":
    run()
