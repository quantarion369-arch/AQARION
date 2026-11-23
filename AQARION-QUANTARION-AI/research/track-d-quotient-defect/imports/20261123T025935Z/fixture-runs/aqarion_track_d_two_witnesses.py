
#!/usr/bin/env python3
"""AQARION: independent exact regression tests for two meet failures."""

from fractions import Fraction
from aqarion_track_d_exact import (
    equitable,
    lumpable,
    quotient_graph,
    quotient_markov,
    union_find_join,
    canonical,
    is_stochastic,
)


def graph(n, edges):
    A = [[0] * n for _ in range(n)]
    for u, v in edges:
        A[u][v] = A[v][u] = 1
    return tuple(tuple(row) for row in A)


def random_walk(A):
    rows = []
    for row in A:
        degree = sum(row)
        assert degree > 0
        rows.append(tuple(Fraction(x, degree) for x in row))
    return tuple(rows)


def meet(p, q):
    return canonical(tuple((p[i], q[i]) for i in range(len(p))))


FIXTURES = [
    {
        "name": "WITNESS_A",
        "edges": [(0, 4), (0, 5), (1, 2), (1, 3)],
        "E": (0, 0, 1, 2, 1, 2),
        "F": (0, 0, 1, 2, 2, 1),
        "expected_failure": Fraction(1, 2),
    },
    {
        "name": "WITNESS_B",
        "edges": [(0, 1), (0, 2), (0, 4), (3, 4), (4, 5)],
        "E": (0, 1, 2, 1, 0, 2),
        "F": (0, 1, 2, 2, 0, 1),
        "expected_failure": Fraction(1, 3),
    },
]


def run_fixture(f):
    n = 6
    A = graph(n, f["edges"])
    P = random_walk(A)
    E, F = f["E"], f["F"]
    J = union_find_join(E, F)
    M = meet(E, F)

    assert is_stochastic(P)

    # Positive controls.
    assert equitable(A, E)
    assert equitable(A, F)
    assert equitable(A, J)
    assert lumpable(P, E)
    assert lumpable(P, F)
    assert lumpable(P, J)

    # Negative controls.
    assert not equitable(A, M)
    assert not lumpable(P, M)

    # Quotient construction for positive controls.
    assert quotient_graph(A, E) is not None
    assert quotient_graph(A, F) is not None
    assert quotient_graph(A, J) is not None
    assert quotient_markov(P, E) is not None
    assert quotient_markov(P, F) is not None
    assert quotient_markov(P, J) is not None

    # Find an exact failure witness.
    blocks = [
        tuple(i for i, label in enumerate(M) if label == b)
        for b in sorted(set(M))
    ]

    witness = None
    for source in blocks:
        for x in source:
            for y in source:
                for target in blocks:
                    mx = sum(P[x][z] for z in target)
                    my = sum(P[y][z] for z in target)
                    if mx != my:
                        witness = (x, y, target, mx, my)
                        break
                if witness:
                    break
            if witness:
                break
        if witness:
            break

    assert witness is not None
    x, y, target, mx, my = witness

    assert f["expected_failure"] in (mx, my)

    print(f"\n{f['name']}")
    print("EDGES=", f["edges"])
    print("E=", E)
    print("F=", F)
    print("JOIN=", J)
    print("MEET=", M)
    print("E_EQUITABLE=True")
    print("F_EQUITABLE=True")
    print("JOIN_EQUITABLE=True")
    print("MEET_EQUITABLE=False")
    print("E_STRONGLY_LUMPABLE=True")
    print("F_STRONGLY_LUMPABLE=True")
    print("JOIN_STRONGLY_LUMPABLE=True")
    print("MEET_STRONGLY_LUMPABLE=False")
    print("FAILURE_SOURCE=", (x, y))
    print("FAILURE_TARGET=", target)
    print("FAILURE_MASSES=", (str(mx), str(my)))
    print("FIXTURE_ASSERTIONS=SATISFIED")


def main():
    print("AQARION TWO-WITNESS REGRESSION")
    for fixture in FIXTURES:
        run_fixture(fixture)
    print("\nTWO_DISTINCT_COUNTEREXAMPLES=CONFIRMED")
    print("UNIVERSAL_JOIN_THEOREM=NOT_PROVED")
    print("NOVELTY=NOT_CLAIMED")


if __name__ == "__main__":
    main()

