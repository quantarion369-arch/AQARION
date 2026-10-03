#!/usr/bin/env python3

from fractions import Fraction


ZERO = Fraction(0)
ONE = Fraction(1)
HALF = Fraction(1, 2)


def delta(a, b):
    return int(a == b)


def lag_scalar(k, d, m):
    """
    L_m(d) = u_d^T K^m u_d

    Convention:
        K e_j = e_{j-1 mod k}
        u_d = e_0 - e_d
    """
    m %= k
    return (
        2 * delta(m, 0)
        - delta(m, d)
        - delta(m, (-d) % k)
    )


def shifted_difference(k, d, m):
    """
    u_d^T K^m = e_m^T - e_{m+d}^T
    represented sparsely.
    """
    out = {}

    i = m % k
    j = (m + d) % k

    out[i] = out.get(i, ZERO) + ONE
    out[j] = out.get(j, ZERO) - ONE

    return {i: v for i, v in out.items() if v != ZERO}


def lag_row(k, d, m):
    """
    a_d^(m)^T = u_d^T K^m P_d
              = e_m^T - e_{m+d}^T
                - 1/2 L_m(d) u_d^T
    """
    out = shifted_difference(k, d, m)
    L = lag_scalar(k, d, m)

    out[0] = out.get(0, ZERO) - HALF * L
    out[d] = out.get(d, ZERO) + HALF * L

    return {i: v for i, v in out.items() if v != ZERO}


def closed_factor(k, d):
    """
    m=1 specialization.
    """
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
    # Independent derivation of the closed factor.
    derived = lag_row(k, d, 1)
    closed = closed_factor(k, d)

    assert sparse_equal(
        derived,
        closed
    ), (k, d, derived, closed)

    # P_d u_d = 0 => a_d^T u_d = 0.
    assert dot_with_u(k, d, derived) == ZERO

    # Direct scalar identity.
    expected_lag = -int(d == 1) - int(d == k - 1)
    assert lag_scalar(k, d, 1) == expected_lag

    return True


def dense_projection(k, d):
    """
    Independent dense construction for small k only.
    Used as an adversarial check against the symbolic sparse derivation.
    """
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
        [
            Fraction(int(i == j)) - P[i][j]
            for j in range(k)
        ]
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


def run():
    symbolic_cases = 0

    # Full symbolic domain.
    for k in range(3, 1001):
        for d in range(1, k):
            symbolic_case(k, d)
            symbolic_cases += 1

    # Independent dense matrix domain.
    dense_cases = 0

    for k in range(3, 21):
        for d in range(1, k):
            dense_projection(k, d)
            dense_cases += 1

    # Exact boundary/interior norm law.
    for k in range(3, 1001):
        for d in range(1, k):
            value = norm_squared(k, d)

            if d in (1, k - 1):
                assert value == Fraction(3, 4)
            else:
                assert value == ONE

    # Scalar autocorrelation cannot distinguish d from k-d.
    for k in range(3, 1001):
        for d in range(1, k):
            assert [
                lag_scalar(k, d, m)
                for m in range(k)
            ] == [
                lag_scalar(k, (k - d) % k, m)
                for m in range(k)
            ]

    print("D22-DIRECT-PROJECTION-AUDIT")
    print(f"SYMBOLIC_CASES={symbolic_cases}")
    print(f"DENSE_CASES={dense_cases}")
    print("CLOSED_FORM=PASS")
    print("LAG_IDENTITY=PASS")
    print("A_D_ORTHOGONAL_U=PASS")
    print("RANK_ONE_FACTOR=PASS")
    print("NILPOTENCY=PASS")
    print("FROBENIUS_SPLIT=PASS")
    print("AUTOCORRELATION_ORIENTATION_AMBIGUITY=CONFIRMED")
    print("STATUS=ANALYTICALLY_SUPPORTED_UNDER_LOCKED_CONVENTION")


if __name__ == "__main__":
    run()
