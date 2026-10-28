from fractions import Fraction as F

n = 6
blocks = ((0, 3), (1, 4), (2, 5))
owner = {x: i for i, block in enumerate(blocks) for x in block}

def identity(size):
    return [
        [F(i == j) for j in range(size)]
        for i in range(size)
    ]

def multiply(A, B):
    return [
        [sum(x*y for x, y in zip(row, col)) for col in zip(*B)]
        for row in A
    ]

def subtract(A, B):
    return [
        [x-y for x, y in zip(a, b)]
        for a, b in zip(A, B)
    ]

def is_zero(A):
    return all(x == 0 for row in A for x in row)

P = [
    [F(owner[i] == owner[j], 2) for j in range(n)]
    for i in range(n)
]
I = identity(n)
hidden_projector = subtract(I, P)

base = [
    [F((j-i) % n in (0, 1, 3, 4)) for j in range(n)]
    for i in range(n)
]

cases = [
    ("ORIGINAL", [row[:] for row in base]),
    ("NO_LOOPS", subtract(base, I)),
    ("ONE_EDGE_REMOVED", [row[:] for row in base]),
]
cases[2][1][0][1] = F(0)

expected = {
    "ORIGINAL": (True, True, True, F(0)),
    "NO_LOOPS": (True, True, False, F(0)),
    "ONE_EDGE_REMOVED": (False, False, False, F(1, 4)),
}

for name, A in cases:
    D = multiply(multiply(hidden_projector, A), P)
    commutator = subtract(multiply(A, P), multiply(P, A))
    reconstruction_error = subtract(
        A, multiply(multiply(P, A), P)
    )
    energy = sum(x*x for row in D for x in row)

    actual = (
        is_zero(D),
        is_zero(commutator),
        is_zero(reconstruction_error),
        energy,
    )
    if actual != expected[name]:
        raise RuntimeError((name, "Unexpected result", actual))

    print("CASE:", name)
    print("CLOSURE_EXACT:", actual[0])
    print("COMMUTES_WITH_PROJECTOR:", actual[1])
    print("QUOTIENT_ONLY_RECONSTRUCTION:", actual[2])
    print("DEFECT_ENERGY:", energy)

    if name != "ONE_EDGE_REMOVED":
        Q = [
            [sum(A[block[0]][y] for y in target) for target in blocks]
            for block in blocks
        ]
        Ad = identity(6)
        Qd = identity(3)

        for d in range(1, 7):
            Ad = multiply(Ad, A)
            Qd = multiply(Qd, Q)

            for x in range(6):
                for c, target in enumerate(blocks):
                    if sum(Ad[x][y] for y in target) != Qd[owner[x]][c]:
                        raise RuntimeError("Block walk-count mismatch")

                for y in range(6):
                    hidden = F(0)
                    if name == "NO_LOOPS":
                        hidden = (-1)**d * hidden_projector[x][y]

                    predicted = Qd[owner[x]][owner[y]] / 2 + hidden
                    if Ad[x][y] != predicted:
                        raise RuntimeError("Hidden-mode reconstruction mismatch")

        print("BLOCK_AND_HIDDEN_POWER_CHECKS_1_TO_6=PASS")

    print()

print("THREE_CASE_BOUNDARY_EXPERIMENT=PASS")
