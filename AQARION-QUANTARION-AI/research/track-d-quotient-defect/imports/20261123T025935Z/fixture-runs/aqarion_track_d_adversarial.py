
#!/usr/bin/env python3
"""AQARION Track D: independent six-state adversarial fixture."""

from fractions import Fraction
import hashlib
import json

from aqarion_track_d_exact import (
    equitable,
    lumpable,
    quotient_graph,
    quotient_markov,
    union_find_join,
    canonical,
    is_stochastic,
)


def make_graph():
    n = 6
    A = [[0] * n for _ in range(n)]

    edges = [
        (0, 1), (0, 2), (0, 4),
        (3, 4), (4, 5),
    ]

    for u, v in edges:
        A[u][v] = 1
        A[v][u] = 1

    return tuple(tuple(row) for row in A)


def make_random_walk(A):
    P = []
    for row in A:
        degree = sum(row)
        if degree == 0:
            raise ValueError("Isolated vertex in random-walk graph")
        P.append(tuple(Fraction(x, degree) for x in row))
    return tuple(P)


def meet_partition(p, q):
    return canonical(tuple((p[i], q[i]) for i in range(len(p))))


def main():
    A = make_graph()
    P = make_random_walk(A)

    pi = (0, 1, 2, 1, 0, 2)
    sigma = (0, 1, 2, 2, 0, 1)

    joined = union_find_join(pi, sigma)
    met = meet_partition(pi, sigma)

    print("AQARION TRACK D ADVERSARIAL FIXTURE")
    print("VERTICES=6")
    print("EDGES=01,02,04,34,45")
    print("PI=", pi)
    print("SIGMA=", sigma)
    print("JOIN=", joined)
    print("MEET=", met)

    # Graph tests.
    assert equitable(A, pi)
    assert equitable(A, sigma)
    assert not equitable(A, met)
    assert equitable(A, joined)

    B_pi = quotient_graph(A, pi)
    B_sigma = quotient_graph(A, sigma)
    B_join = quotient_graph(A, joined)

    print("GRAPH_PI_EQUITABLE=True")
    print("GRAPH_SIGMA_EQUITABLE=True")
    print("GRAPH_JOIN_EQUITABLE=True")
    print("GRAPH_MEET_EQUITABLE=False")
    print("GRAPH_MEET_COUNTEREXAMPLE=CONFIRMED")
    print("GRAPH_QUOTIENT_PI=", B_pi)
    print("GRAPH_QUOTIENT_SIGMA=", B_sigma)
    print("GRAPH_QUOTIENT_JOIN=", B_join)

    # Exact random-walk tests.
    assert is_stochastic(P)
    assert lumpable(P, pi)
    assert lumpable(P, sigma)
    assert lumpable(P, joined)
    assert not lumpable(P, met)

    Q_pi = quotient_markov(P, pi)
    Q_sigma = quotient_markov(P, sigma)
    Q_join = quotient_markov(P, joined)

    print("MARKOV_PI_STRONGLY_LUMPABLE=True")
    print("MARKOV_SIGMA_STRONGLY_LUMPABLE=True")
    print("MARKOV_JOIN_STRONGLY_LUMPABLE=True")
    print("MARKOV_MEET_STRONGLY_LUMPABLE=False")
    print("MARKOV_MEET_COUNTEREXAMPLE=CONFIRMED")
    print("MARKOV_QUOTIENT_PI=", Q_pi)
    print("MARKOV_QUOTIENT_SIGMA=", Q_sigma)
    print("MARKOV_QUOTIENT_JOIN=", Q_join)

    # Explicit unequal transition mass into singleton {1}.
    into_one_from_zero = P[0][1]
    into_one_from_four = P[4][1]

    assert into_one_from_zero == Fraction(1, 3)
    assert into_one_from_four == Fraction(0, 1)

    print("MEET_FAILURE_MASS_FROM_0=", into_one_from_zero)
    print("MEET_FAILURE_MASS_FROM_4=", into_one_from_four)

    print("ALL_FIXTURE_ASSERTIONS=SATISFIED")
    print("STATUS=FINITE_COUNTEREXAMPLE_REPRODUCED")
    print("NOVELTY=NOT CLAIMED")


if __name__ == "__main__":
    main()

