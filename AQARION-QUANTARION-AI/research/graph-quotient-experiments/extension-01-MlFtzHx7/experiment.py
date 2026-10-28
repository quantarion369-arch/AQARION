from fractions import Fraction as F
import platform
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def matrix(rows):
    return [[F(x) for x in row] for row in rows]


def eye(n):
    return matrix([
        [int(i == j) for j in range(n)]
        for i in range(n)
    ])


def mm(A, B):
    return [
        [
            sum((a * b for a, b in zip(row, col)), F(0))
            for col in zip(*B)
        ]
        for row in A
    ]


def sub(A, B):
    return [
        [a - b for a, b in zip(x, y)]
        for x, y in zip(A, B)
    ]


def add(A, B):
    return [
        [a + b for a, b in zip(x, y)]
        for x, y in zip(A, B)
    ]


def rank(A):
    A = matrix(A)
    r = 0

    for j in range(len(A[0])):
        p = next(
            (i for i in range(r, len(A)) if A[i][j]),
            None,
        )
        if p is None:
            continue

        A[r], A[p] = A[p], A[r]
        pivot = A[r][j]
        A[r] = [x / pivot for x in A[r]]

        for i in range(r + 1, len(A)):
            factor = A[i][j]
            A[i] = [
                x - factor * y
                for x, y in zip(A[i], A[r])
            ]

        r += 1
        if r == len(A):
            break

    return r


def refined_labels(A, labels):
    labels = list(labels)

    while True:
        k = max(labels) + 1
        signatures = [
            (
                labels[i],
                tuple(
                    sum(
                        A[i][j]
                        for j in range(len(A))
                        if labels[j] == b
                    )
                    for b in range(k)
                ),
            )
            for i in range(len(A))
        ]

        ids = {}
        new = [
            ids.setdefault(signature, len(ids))
            for signature in signatures
        ]

        if len(ids) == k:
            return new

        labels = new


def krylov_rank(A, labels):
    n = len(A)
    k = max(labels) + 1

    current = matrix([
        [int(labels[i] == b) for b in range(k)]
        for i in range(n)
    ])

    rows = [[] for _ in range(n)]

    for unused in range(n):
        for i in range(n):
            rows[i].extend(current[i])
        current = mm(A, current)

    return rank(rows)


def test_delayed():
    A = matrix([
        [1, 1, 1, 0],
        [1, 1, 0, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
    ])

    H = matrix([
        [1, 0],
        [1, 0],
        [0, 1],
        [0, 1],
    ])

    L = [
        [F(x, 2) for x in row]
        for row in zip(*H)
    ]

    P = mm(H, L)
    Q = mm(mm(L, A), H)
    R = sub(A, mm(mm(P, A), P))
    Z = matrix([[0] * 4 for unused in range(4)])

    require(
        Q == matrix([[2, 1], [2, 2]]),
        "Wrong quotient",
    )
    require(mm(A, H) == mm(H, Q), "Block closure failed")
    require(mm(A, P) == mm(P, A), "Commutation failed")
    require(
        R != Z and mm(R, R) == Z,
        "Wrong hidden nilpotency",
    )

    Ap, Qp, Rp = eye(4), eye(2), eye(4)

    for t in range(1, 9):
        Ap = mm(Ap, A)
        Qp = mm(Qp, Q)
        Rp = mm(Rp, R)

        reconstructed = mm(mm(H, Qp), L)

        require(
            Ap == add(reconstructed, Rp),
            "Hidden decomposition failed",
        )
        require(
            (Ap == reconstructed) == (t >= 2),
            "Wrong reconstruction delay",
        )

    require(
        rank(A) == 3 and rank(mm(A, A)) == 2,
        "Wrong ranks",
    )

    print("DELAYED_RECONSTRUCTION=PASS")
    print("DELAY=2; POWERS_CHECKED=1..8; RANK_A=3; RANK_A2=2")


def test_markov():
    integers = [
        [12, 10, 8, 6, 4],
        [10, 9, 8, 7, 6],
        [8, 8, 8, 8, 8],
        [6, 7, 8, 9, 10],
        [4, 6, 8, 10, 12],
    ]

    T = [[F(x, 40) for x in row] for row in integers]
    labels = [0, 0, 0, 0, 1]

    require(
        all(sum(row) == 1 for row in T),
        "Not stochastic",
    )
    require(
        all(x > 0 for row in T for x in row),
        "Not positive",
    )
    require(
        T == [list(row) for row in zip(*T)],
        "Not symmetric",
    )
    require(
        all(
            sum(T[i][j] for i in range(5)) == 1
            for j in range(5)
        ),
        "Uniform stationary law failed",
    )

    refined = refined_labels(T, labels)
    m = len(set(refined))
    r = krylov_rank(T, labels)
    gap = m - r
    deterministic_bound = m - 1 - (m - 1).bit_length()

    require(
        (m, r, gap, deterministic_bound) == (5, 3, 2, 1),
        "Unexpected profile",
    )
    require(
        gap > deterministic_bound,
        "Expected violation not detected",
    )

    print("POSITIVE_REVERSIBLE_MARKOV_COUNTEREXAMPLE=PASS")
    print("INITIAL_BLOCKS=2; STABLE_CLASSES=5; KRYLOV_RANK=3")
    print("GAP=2; DETERMINISTIC_BOUND=1; VIOLATION_DETECTED=YES")


print("PYTHON:", sys.version)
print("PLATFORM:", platform.platform())
print("ARITHMETIC=EXACT_FRACTION")

test_delayed()
test_markov()

print("RESEARCH_EXTENSION=PASS")
