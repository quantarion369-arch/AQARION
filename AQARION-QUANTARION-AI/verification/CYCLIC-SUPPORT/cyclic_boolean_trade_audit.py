#!/usr/bin/env python3
"""Exact audit of 4-bit, degree<=2 Boolean support dependencies."""
from fractions import Fraction
from itertools import combinations
from collections import Counter
import math

PRIME = 65521
HISTORIES = [format(i, "04b") for i in range(16)]
BITS = [tuple(map(int, s)) for s in HISTORIES]
PAIRS = [(i, j) for i in range(4) for j in range(i + 1, 4)]
FEATURES = [
    [1, *x, *(x[i] * x[j] for i, j in PAIRS)]
    for x in BITS
]

def rank_mod(rows, p=PRIME):
    a = [[v % p for v in row] for row in rows]
    m, n = len(a), len(rows[0]) if rows else 0
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][c], p - 2, p)
        a[r] = [(v * inv) % p for v in a[r]]
        for i in range(r + 1, m):
            if a[i][c]:
                f = a[i][c]
                a[i] = [
                    (a[i][j] - f * a[r][j]) % p
                    for j in range(n)
                ]
        r += 1
        if r == m:
            break
    return r

def rank_q(rows):
    """Exact rational Gaussian elimination."""
    a = [[Fraction(v) for v in row] for row in rows]
    m, n = len(a), len(a[0]) if a else 0
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        pv = a[r][c]
        a[r] = [v / pv for v in a[r]]
        for i in range(r + 1, m):
            if a[i][c]:
                f = a[i][c]
                a[i] = [
                    a[i][j] - f * a[r][j]
                    for j in range(n)
                ]
        r += 1
        if r == m:
            break
    return r

def mask_of(indices):
    return sum(1 << i for i in indices)

def indices(mask):
    return [i for i in range(16) if (mask >> i) & 1]

def support_words(mask):
    return [HISTORIES[i] for i in indices(mask)]

def graph_info(mask):
    """Return vertices, SCC sizes, source count, sink count, strong."""
    edges = indices(mask)
    vertices = sorted(
        set([e >> 1 for e in edges] + [e & 7 for e in edges])
    )
    adj = {v: [] for v in vertices}
    for e in edges:
        u, v = e >> 1, e & 7
        adj[u].append(v)

    def reach(start):
        seen, stack = {start}, [start]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        return seen

    reach_from = {v: reach(v) for v in vertices}
    unseen = set(vertices)
    comps = []
    while unseen:
        u = min(unseen)
        comp = {
            v for v in unseen
            if v in reach_from[u] and u in reach_from[v]
        }
        comps.append(comp)
        unseen -= comp

    comp_of = {
        v: ci for ci, comp in enumerate(comps) for v in comp
    }
    indeg = [0] * len(comps)
    outdeg = [0] * len(comps)
    for e in edges:
        u, v = e >> 1, e & 7
        cu, cv = comp_of[u], comp_of[v]
        if cu != cv:
            outdeg[cu] += 1
            indeg[cv] += 1

    sources = sum(d == 0 for d in indeg)
    sinks = sum(d == 0 for d in outdeg)
    return (
        len(vertices),
        sorted((len(c) for c in comps), reverse=True),
        sources,
        sinks,
        len(comps) == 1,
    )

def is_eulerian(mask):
    balance = Counter()
    for e in indices(mask):
        balance[e >> 1] += 1
        balance[e & 7] -= 1
    return all(v == 0 for v in balance.values())

def census(size):
    deficient, modular_candidates = [], 0
    for comb in combinations(range(16), size):
        rows = [FEATURES[i] for i in comb]
        if rank_mod(rows) < size:
            modular_candidates += 1
            # Exact rational check of every modularly deficient candidate.
            if rank_q(rows) < size:
                deficient.append(mask_of(comb))
            else:
                raise AssertionError(
                    "Modular candidate was rationally independent"
                )
    return deficient, modular_candidates

print("AQARION CYCLIC BOOLEAN TRADE AUDIT")
print("Features: 1, x_i, x_i*x_j; rank over Q")
print("Mask bit i represents history format(i, '04b')")
print("Full-rank mod 65521 proves rational full row rank.")

by_size = {}
for size in (8, 9, 10):
    deficient, candidates = census(size)
    by_size[size] = set(deficient)
    print(
        f"SIZE {size}: total={math.comb(16, size)} "
        f"mod_candidates={candidates} exact_deficient={len(deficient)}"
    )

# Candidate family: x_i=c and x_i XOR x_j=c.
family = set()
for i in range(4):
    for c in (0, 1):
        family.add(mask_of(
            h for h, x in enumerate(BITS) if x[i] == c
        ))
for i in range(4):
    for j in range(i + 1, 4):
        for c in (0, 1):
            family.add(mask_of(
                h for h, x in enumerate(BITS)
                if (x[i] ^ x[j]) == c
            ))

assert len(family) == 20
assert family == by_size[8]
assert all(
    rank_q([FEATURES[i] for i in indices(m)]) == 7
    for m in family
)
print("SIZE 8 CLASSIFICATION: PASS (8 faces + 12 parity supports, rank 7)")

# Generate all one-history extensions and record their unique parents.
parents = {}
for base in family:
    for h in range(16):
        if not ((base >> h) & 1):
            ext = base | (1 << h)
            parents.setdefault(ext, []).append((base, h))

assert len(parents) == 160
assert set(parents) == by_size[9]
assert all(len(v) == 1 for v in parents.values())
print("SIZE 9 CONTAINMENT: PASS (160 unique extensions, unique parent each)")

source_sink = Counter(
    (graph_info(base)[2], graph_info(base)[3])
    for base in family
)
assert (1, 1) not in source_sink
assert all(not graph_info(ext)[4] for ext in parents)
print("BASE SOURCE/SINK SCC COUNTS:", dict(sorted(source_sink.items())))
print("SIZE 9 GRAPH EXCLUSION: PASS (160/160 are not strongly connected)")

feasible10 = [
    m for m in sorted(by_size[10]) if graph_info(m)[4]
]
euler10 = [m for m in feasible10 if is_eulerian(m)]
assert len(feasible10) == 8
assert len(euler10) == 1
print(
    f"SIZE 10: deficient={len(by_size[10])}; "
    f"strongly_connected_deficient={len(feasible10)}; "
    f"Eulerian={len(euler10)}"
)
print("ALL FEASIBLE SIZE-10 SUPPORTS:")
for m in feasible10:
    info = graph_info(m)
    r = rank_q([FEATURES[i] for i in indices(m)])
    print(
        "  " + " ".join(support_words(m))
        + f" | vertices={info[0]} | rank={r}"
        + f" | Eulerian={is_eulerian(m)}"
    )

# Independent cyclic witness.
word = "0001011101"
windows = [
    int("".join(word[(j + t) % len(word)] for t in range(4)), 2)
    for j in range(len(word))
]
witness = mask_of(set(windows))
assert len(set(windows)) == 10
assert witness in by_size[10]
assert graph_info(witness)[4] and is_eulerian(witness)
assert rank_q([FEATURES[i] for i in indices(witness)]) == 9

# Coefficients are ordered by lexicographically sorted histories.
coeff = [-1, 1, -1, 2, -1, 1, -2, 1, -1, 1]
sorted_ids = indices(witness)
assert [HISTORIES[i] for i in sorted_ids] == sorted(
    HISTORIES[i] for i in windows
)
for col in range(11):
    assert sum(
        coeff[j] * FEATURES[i][col]
        for j, i in enumerate(sorted_ids)
    ) == 0
assert sum(c for c in coeff if c > 0) == 6
assert -sum(c for c in coeff if c < 0) == 6

print("CYCLIC WITNESS:", word)
print("  windows:", " ".join(HISTORIES[i] for i in windows))
print("  distinct=10; rank=9; nullity=1; SCC=1; Eulerian=True")
print("  sorted-history coefficients:", coeff)
print("  positive mass=6; negative mass=6; all feature sums cancel")
print("FINAL: PASS — minimum feasible deficient support size is 10.")
