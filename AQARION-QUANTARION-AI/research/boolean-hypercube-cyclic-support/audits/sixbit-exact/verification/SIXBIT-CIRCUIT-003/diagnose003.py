#!/usr/bin/env python3
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
CENSUS = BASE / "flat_census.json"

def parity(x):
    return x.bit_count() & 1

def feature(x):
    b = [(x >> i) & 1 for i in range(6)]
    return [1] + b + [
        b[i] * b[j]
        for i in range(6)
        for j in range(i + 1, 6)
    ]

def parameter_points(rep, basis):
    points = []
    for t in range(8):
        x = rep
        for j in range(3):
            if (t >> j) & 1:
                x ^= basis[j]
        points.append(x)
    return points

def exact_rref(a):
    a = [[Fraction(x) for x in row] for row in a]
    m = len(a)
    n = len(a[0]) if m else 0
    pivots = []
    r = 0

    for c in range(n):
        p = next((i for i in range(r, m) if a[i][c]), None)
        if p is None:
            continue

        a[r], a[p] = a[p], a[r]
        q = a[r][c]
        a[r] = [v / q for v in a[r]]

        for i in range(m):
            if i != r and a[i][c]:
                q = a[i][c]
                a[i] = [
                    a[i][j] - q * a[r][j]
                    for j in range(n)
                ]

        pivots.append(c)
        r += 1
        if r == m:
            break

    return a, pivots

def exact_rank(matrix):
    _, pivots = exact_rref(matrix)
    return len(pivots)

def primitive_null_vector(matrix):
    # Nullspace of M^T: a relation among the eight evaluation rows.
    a = [
        [Fraction(matrix[t][j]) for t in range(8)]
        for j in range(22)
    ]
    rref, pivots = exact_rref(a)
    free = [c for c in range(8) if c not in pivots]

    if len(free) != 1:
        return None

    f = free[0]
    v = [Fraction(0) for _ in range(8)]
    v[f] = Fraction(1)

    for row, pivot in enumerate(pivots):
        v[pivot] = -rref[row][f]

    den = 1
    for x in v:
        den = math.lcm(den, x.denominator)

    ints = [int(x * den) for x in v]
    g = 0
    for x in ints:
        g = math.gcd(g, abs(x))

    ints = [x // g for x in ints]

    first = next(x for x in ints if x)
    if first < 0:
        ints = [-x for x in ints]

    return ints

def walsh_character(v):
    for c in range(8):
        w = [-1 if parity(c & t) else 1 for t in range(8)]
        if v == w or v == [-x for x in w]:
            return c
    return None

with CENSUS.open(encoding="utf-8") as f:
    data = json.load(f)

assert data["direction_count"] == 1395
assert data["flat_count"] == 11160
assert data["feature_count"] == 22

rank_hist = Counter()
kernel_support_hist = Counter()
walsh_hist = Counter()
direction_cosets = defaultdict(Counter)
rank7_examples = []
exact_checks = 0
point_reconstruction_checks = 0

for flat in data["flats"]:
    basis = tuple(flat["direction_rref"])
    rep = flat["coset_representative"]
    points = parameter_points(rep, basis)

    assert len(set(points)) == 8
    assert set(points) == set(flat["points"])
    point_reconstruction_checks += 1

    M = [feature(x) for x in points]
    r = exact_rank(M)
    exact_checks += 1

    assert r == flat["rank_Q"], (
        "Independent exact rank disagrees with census",
        flat["flat_id"], r, flat["rank_Q"]
    )

    rank_hist[r] += 1
    direction_cosets[basis][r] += 1

    if r == 7:
        v = primitive_null_vector(M)
        assert v is not None
        support = sum(x != 0 for x in v)
        kernel_support_hist[support] += 1

        c = walsh_character(v)
        walsh_hist["WALSH" if c is not None else "NON_WALSH"] += 1

        if c is not None:
            walsh_hist[f"CHAR_{c:03b}"] += 1

        if len(rank7_examples) < 5:
            rank7_examples.append({
                "flat_id": flat["flat_id"],
                "direction_rref": list(basis),
                "representative": rep,
                "points_parameter_order": points,
                "primitive_kernel": v,
                "walsh_character": c,
            })

assert exact_checks == 11160
assert rank_hist[7] == 2800
assert rank_hist[8] == 8360

mixed_directions = [
    (list(k), dict(v))
    for k, v in direction_cosets.items()
    if len(v) != 1
]

print("SIXBIT-CIRCUIT-003 STRUCTURAL DIAGNOSTIC")
print("Independent exact rank checks:", exact_checks)
print("Point reconstruction checks:", point_reconstruction_checks)
print("Exact rank distribution:", dict(sorted(rank_hist.items())))
print("Kernel support-size distribution:", dict(sorted(kernel_support_hist.items())))
print("Walsh classification:", dict(sorted(walsh_hist.items())))
print("Directions with mixed coset ranks:", len(mixed_directions))

if mixed_directions:
    print("FIRST MIXED DIRECTIONS:", mixed_directions[:5])

print("\nFIRST FIVE RANK-SEVEN KERNEL WITNESSES:")
for item in rank7_examples:
    print(json.dumps(item, sort_keys=True))

print("\nDIAGNOSTIC COMPLETE — NO PASS CERTIFICATE CREATED")
