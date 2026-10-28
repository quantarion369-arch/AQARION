from fractions import Fraction as F


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def eye(n):
    return [
        [F(i == j) for j in range(n)]
        for i in range(n)
    ]


def mm(A, B):
    return [
        [
            sum((x*y for x, y in zip(row, col)), F(0))
            for col in zip(*B)
        ]
        for row in A
    ]


def op(A, B, sign):
    return [
        [x + sign*y for x, y in zip(a, b)]
        for a, b in zip(A, B)
    ]


def rank(A):
    A = [[F(x) for x in row] for row in A]
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
        A[r] = [x/pivot for x in A[r]]

        for i in range(r + 1, len(A)):
            factor = A[i][j]
            A[i] = [
                x - factor*y
                for x, y in zip(A[i], A[r])
            ]

        r += 1
        if r == len(A):
            break

    return r


def profile(A, labels):
    n = len(A)
    H = [
        [
            F(labels[i] == b)
            for b in range(max(labels) + 1)
        ]
        for i in range(n)
    ]

    rows = [[] for _ in range(n)]
    current = H

    for unused in range(n):
        for i in range(n):
            rows[i].extend(current[i])
        current = mm(A, current)

    r = rank(rows)
    labels = labels[:]

    while True:
        k = max(labels) + 1

        signatures = [
            (
                labels[i],
                tuple(
                    sum(
                        A[i][j]
                        for j in range(n)
                        if labels[j] == b
                    )
                    for b in range(k)
                ),
            )
            for i in range(n)
        ]

        ids = {}
        new = [
            ids.setdefault(s, len(ids))
            for s in signatures
        ]

        if len(ids) == k:
            return k, r

        labels = new


def delayed(A, d):
    n = len(A)

    H = [
        [F(i//2 == j) for j in range(d)]
        for i in range(n)
    ]
    L = [
        [x/2 for x in row]
        for row in zip(*H)
    ]

    P = mm(H, L)
    Q = mm(mm(L, A), H)
    R = op(A, mm(mm(P, A), P), -1)

    need(mm(A, H) == mm(H, Q), "Closure failed")
    need(mm(A, P) == mm(P, A), "Commutation failed")

    Z = [[F(0)] * n for unused in range(n)]
    Ap, Qp, Rp = eye(n), eye(d), eye(n)

    for t in range(1, d + 2):
        Ap = mm(Ap, A)
        Qp = mm(Qp, Q)
        Rp = mm(Rp, R)

        reconstructed = mm(mm(H, Qp), L)

        need(
            Ap == op(reconstructed, Rp, 1),
            "Decomposition failed",
        )
        need(
            (Rp == Z) == (t >= d),
            "Nilpotency index failed",
        )
        need(
            (Ap == reconstructed) == (t >= d),
            "Delay failed",
        )


for d in range(2, 7):
    n = 2*d

    A = [
        [
            F(i % 2 == j % 2)
            if j//2 == i//2 + 1
            else F(1)
            for j in range(n)
        ]
        for i in range(n)
    ]

    need(
        all(x in (0, 1) for row in A for x in row),
        "Not binary",
    )
    need(
        all(x > 0 for row in mm(A, A) for x in row),
        "A squared not positive",
    )

    delayed(A, d)

    T = [
        [x/sum(row) for x in row]
        for row in A
    ]

    need(
        all(sum(row) == 1 for row in T),
        "Normalization failed",
    )

    delayed(T, d)

    print(
        "DELAY_FAMILY d=%d vertices=%d "
        "adjacency=PASS stochastic=PASS" % (d, n)
    )


for n in range(3, 11):
    v = [F(2*i - (n - 1)) for i in range(n)]
    eps = F(1, 2*n*(n - 1)**2)

    T = [
        [
            F(1, n) + eps*v[i]*v[j]
            for j in range(n)
        ]
        for i in range(n)
    ]

    need(
        all(sum(row) == 1 for row in T),
        "Not stochastic",
    )
    need(
        all(x > 0 for row in T for x in row),
        "Not positive",
    )
    need(
        T == [list(row) for row in zip(*T)],
        "Not symmetric",
    )

    m, r = profile(T, [0]*(n - 1) + [1])
    gap = m - r
    old = m - 1 - (m - 1).bit_length()

    need(
        (m, r, gap) == (n, 3, n - 3),
        "Wrong gap profile",
    )
    need(
        (gap > old) == (n >= 5),
        "Wrong violation threshold",
    )

    print(
        "GAP_FAMILY n=%d stable=%d rank=%d gap=%d "
        "old_bound=%d violation=%s"
        % (
            n, m, r, gap, old,
            "YES" if gap > old else "NO",
        )
    )


print("FAMILY_CERTIFICATE=PASS")
print("SCOPE=BOUNDED_EXACT_TESTS_NOT_AN_ALL_SIZE_PROOF")
