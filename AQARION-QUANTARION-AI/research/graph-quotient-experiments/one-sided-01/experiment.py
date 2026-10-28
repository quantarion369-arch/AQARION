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

def energy(A):
    return sum(x*x for row in A for x in row)

P = [
    [F(owner[i] == owner[j], 2) for j in range(n)]
    for i in range(n)
]
Z = subtract(identity(n), P)

A = [
    [F((j-i) % n in (1, 3, 4)) for j in range(n)]
    for i in range(n)
]

A[0][3] = F(0)
A[0][0] = F(1)

closure = multiply(multiply(Z, A), P)
opposite = multiply(multiply(P, A), Z)
commutator = subtract(multiply(A, P), multiply(P, A))

Q = []
for block in blocks:
    rows = [
        [sum(A[x][y] for y in target) for target in blocks]
        for x in block
    ]
    if any(row != rows[0] for row in rows):
        raise RuntimeError("Block transition totals disagree")
    Q.append(rows[0])

expected_Q = [[1, 2, 0], [0, 1, 2], [2, 0, 1]]

if Q != expected_Q:
    raise RuntimeError("Quotient unexpectedly changed")
if energy(closure) != 0:
    raise RuntimeError("Closure did not survive")
if energy(opposite) != 1:
    raise RuntimeError("Unexpected opposite-coupling energy")
if energy(commutator) != 1:
    raise RuntimeError("Unexpected commutator energy")

print("EDGE_CHANGE: 0->3 replaced by 0->0")
print("QUOTIENT:", [[int(x) for x in row] for row in Q])
print("CLOSURE_DEFECT_ENERGY:", energy(closure))
print("OPPOSITE_COUPLING_ENERGY:", energy(opposite))
print("COMMUTATOR_ENERGY:", energy(commutator))

Ad = identity(6)
Qd = identity(3)

for d in range(1, 7):
    Ad = multiply(Ad, A)
    Qd = multiply(Qd, Q)

    for x in range(6):
        for c, target in enumerate(blocks):
            if sum(Ad[x][y] for y in target) != Qd[owner[x]][c]:
                raise RuntimeError("Aggregated walk-count mismatch")

    print("BLOCK_COUNTS_STEP_" + str(d) + "=PASS")

print("CLOSURE_WITHOUT_COMMUTATION=PASS")
print("ONE_SIDED_EXPERIMENT=PASS")
