#!/usr/bin/env python3
from itertools import combinations, combinations_with_replacement
from collections import defaultdict, Counter
from fractions import Fraction
from math import gcd
from functools import reduce

CELLS = range(16)
PAIRS = tuple(combinations(range(4), 2))
HIGH = tuple(combinations(range(4), 3)) + ((0, 1, 2, 3),)

def bit(i, j):
    return (i >> j) & 1

def qcol(i):
    return ((1,)
            + tuple(bit(i, j) for j in range(4))
            + tuple(bit(i, a)*bit(i, b) for a,b in PAIRS))

def stats(table):
    return (
        len(table),
        tuple(sum(bit(i,j) for i in table) for j in range(4)),
        tuple(sum(bit(i,a)*bit(i,b) for i in table)
              for a,b in PAIRS)
    )

def rank(matrix):
    if not matrix:
        return 0
    a = [[Fraction(x) for x in row] for row in matrix]
    nr, nc = len(a), len(a[0])
    r = 0

    for c in range(nc):
        pivot = None
        for i in range(r, nr):
            if a[i][c] != 0:
                pivot = i
                break

        if pivot is None:
            continue

        a[r], a[pivot] = a[pivot], a[r]
        z = a[r][c]
        a[r] = [x/z for x in a[r]]

        for i in range(nr):
            if i != r and a[i][c] != 0:
                z = a[i][c]
                a[i] = [
                    a[i][j] - z*a[r][j]
                    for j in range(nc)
                ]

        r += 1
        if r == nr:
            break

    return r

def high_moments(delta):
    out = []
    for S in HIGH:
        total = 0
        for i,d in enumerate(delta):
            parity = sum(bit(i,j) for j in S) % 2
            total += d * (-1 if parity else 1)
        out.append(total)
    return tuple(out)

def geometry(union):
    fixed = []
    for j in range(4):
        vals = {bit(i,j) for i in union}
        if len(vals) == 1:
            fixed.append((j, next(iter(vals))))

    diagonal = []
    for a,b in PAIRS:
        vals = {bit(i,a)^bit(i,b) for i in union}
        if len(vals) == 1:
            diagonal.append((a,b,next(iter(vals))))

    if len(fixed) == 1 and not diagonal:
        j,v = fixed[0]
        return ("FIXED_ONE" if v else "FIXED_ZERO", (j,v))

    if not fixed and len(diagonal) == 1:
        a,b,v = diagonal[0]
        return ("DIAGONAL", (a,b,v))

    raise AssertionError(("unexpected geometry", fixed, diagonal))

fibers = defaultdict(list)
total = 0

for table in combinations_with_replacement(CELLS, 4):
    fibers[stats(table)].append(table)
    total += 1

sizes = Counter(map(len, fibers.values()))
nontrivial = sorted(
    tuple(sorted(v)) for v in fibers.values() if len(v) > 1
)

assert total == 3876
assert len(fibers) == 3856
assert sizes == Counter({1: 3836, 2: 20})
assert len(nontrivial) == 20

print("AQ TOTAL-4 EXACT AUDIT")
print("tables =", total)
print("distinct quadratic fibers =", len(fibers))
print("fiber-size distribution =", dict(sorted(sizes.items())))
print()

sector_counts = Counter()

for number, (A,B) in enumerate(nontrivial, 1):
    ca = [A.count(i) for i in CELLS]
    cb = [B.count(i) for i in CELLS]
    delta = [cb[i]-ca[i] for i in CELLS]

    support = [i for i,d in enumerate(delta) if d]
    positive = [i for i,d in enumerate(delta) if d > 0]
    negative = [i for i,d in enumerate(delta) if d < 0]

    assert len(support) == 8
    assert all(abs(delta[i]) == 1 for i in support)

    qdelta = [
        sum(qcol(i)[r]*delta[i] for i in CELLS)
        for r in range(11)
    ]
    assert qdelta == [0]*11

    restricted = [
        [qcol(i)[r] for i in support]
        for r in range(11)
    ]
    rr = rank(restricted)
    assert rr == len(support)-1

    g = reduce(gcd, (abs(delta[i]) for i in support), 0)
    assert g == 1

    kind, detail = geometry(set(A)|set(B))
    sector_counts[kind] += 1

    print(f"{number:02d} {kind} {detail}")
    print("   A =", A)
    print("   B =", B)
    print("   positive cells =", positive)
    print("   negative cells =", negative)
    print("   A*delta =", qdelta)
    print(f"   rank(A_S)={rr}; |S|-1={len(support)-1}; gcd={g}")
    print("   high-moment increment =", high_moments(delta))

print()
print("SECTOR TOTALS =", dict(sorted(sector_counts.items())))

assert sector_counts == Counter({
    "DIAGONAL": 12,
    "FIXED_ZERO": 4,
    "FIXED_ONE": 4,
})

print("PASS: all 20 fiber and circuit checks")
print("SELECTED FIVE-MOVE CONNECTIVITY: NOT TESTED")
