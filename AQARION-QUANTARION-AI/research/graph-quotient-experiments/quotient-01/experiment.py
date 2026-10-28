n = 6
moves = (0, 1, 3, 4)
blocks = ((0, 3), (1, 4), (2, 5))
owner = {x: i for i, block in enumerate(blocks) for x in block}

M = [
    [int((j-i) % n in moves) for j in range(n)]
    for i in range(n)
]

def multiply(A, B):
    return [
        [
            sum(x*y for x, y in zip(row, column))
            for column in zip(*B)
        ]
        for row in A
    ]

def identity(size):
    return [
        [int(i == j) for j in range(size)]
        for i in range(size)
    ]

Q = []
for block in blocks:
    rows = [
        [sum(M[x][y] for y in target) for target in blocks]
        for x in block
    ]
    if any(row != rows[0] for row in rows):
        raise RuntimeError("Vertices disagree on block transition counts")
    Q.append(rows[0])

print("BLOCKS:", blocks)
print("WEIGHTED_QUOTIENT:", Q)

P = identity(6)
R = identity(3)

for d in range(1, 5):
    P = multiply(P, M)
    R = multiply(R, Q)

    for x in range(6):
        for c, target in enumerate(blocks):
            if sum(P[x][y] for y in target) != R[owner[x]][c]:
                raise RuntimeError("Block walk-count mismatch")

        for y in range(6):
            if 2 * P[x][y] != R[owner[x]][owner[y]]:
                raise RuntimeError("Individual walk-count reconstruction failed")

    print("STEPS:", d)
    print("ORIGINAL_ROW:", P[0])
    print("QUOTIENT_ROW:", R[0])

unweighted = [[int(value > 0) for value in row] for row in Q]
if sum(unweighted[0]) == sum(M[0]):
    raise RuntimeError("Unweighted negative control failed")

print("UNWEIGHTED_COUNT_LOSS=DETECTED")
print("BLOCK_COUNTS_PRESERVED=PASS")
print("INDIVIDUAL_COUNTS_RECONSTRUCTED=PASS")
print("QUOTIENT_WALK_EXPERIMENT=PASS")
