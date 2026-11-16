#!/usr/bin/env python3
import itertools as it
import collections as C
import math, json
from fractions import Fraction as Q

P = 2147483629

def span(b):
    out = {0}
    for v in b:
        out |= {x ^ v for x in tuple(out)}
    return tuple(sorted(out))

def rref2(b):
    a, r = list(b), 0
    for col in range(6):
        q = next((i for i in range(r, len(a))
                  if (a[i] >> col) & 1), None)
        if q is None:
            continue
        a[r], a[q] = a[q], a[r]
        for i in range(len(a)):
            if i != r and ((a[i] >> col) & 1):
                a[i] ^= a[r]
        r += 1
    return tuple(a[:r])

def feature(x):
    b = [(x >> i) & 1 for i in range(6)]
    return [1] + b + [
        b[i] * b[j] for i, j in it.combinations(range(6), 2)
    ]

V = [feature(x) for x in range(64)]

def rank_mod(A, p):
    M = [[v % p for v in row] for row in A]
    m, n, r = len(M), len(M[0]), 0
    for c in range(n):
        q = next((i for i in range(r, m) if M[i][c]), None)
        if q is None:
            continue
        M[r], M[q] = M[q], M[r]
        inv = pow(M[r][c], -1, p)
        M[r] = [(v * inv) % p for v in M[r]]
        for i in range(m):
            if i != r and M[i][c]:
                t = M[i][c]
                M[i] = [(a - t*b) % p
                        for a, b in zip(M[i], M[r])]
        r += 1
        if r == m:
            break
    return r

def character_rank(b):
    sig = {
        sum(((v >> i) & 1) << j for j, v in enumerate(b))
        for i in range(6)
    }
    return len({0} | sig | {u ^ v for u in sig for v in sig})

def cosets(U):
    left, out = set(range(64)), []
    while left:
        c = min(left)
        F = tuple(sorted(c ^ u for u in U))
        left.difference_update(F)
        out.append((c, F))
    return out

def augmented_rref(U):
    rows = [
        list(map(Q, V[u])) +
        [Q(int(i == j)) for j in range(8)]
        for i, u in enumerate(U)
    ]
    piv, r = [], 0
    for col in range(22):
        q = next((i for i in range(r, 8) if rows[i][col]), None)
        if q is None:
            continue
        rows[r], rows[q] = rows[q], rows[r]
        t = rows[r][col]
        rows[r] = [v/t for v in rows[r]]
        for i in range(8):
            if i != r and rows[i][col]:
                t = rows[i][col]
                rows[i] = [a-t*b for a, b in zip(rows[i], rows[r])]
        piv.append(col)
        r += 1
        if r == 8:
            break
    assert r == 8
    return rows, piv

def reduce_point(x, rows, piv):
    res = list(map(Q, V[x]))
    coeff = [Q(0)] * 8
    for row, pivot in zip(rows, piv):
        t = res[pivot]
        if t:
            res = [a-t*b for a, b in zip(res, row[:22])]
            coeff = [a+t*b for a, b in zip(coeff, row[22:])]
    scale = next((v for v in res if v), None)
    assert scale is not None
    return tuple(v/scale for v in res), scale, coeff

assert all(P % d for d in range(2, math.isqrt(P)+1))
assert P > 10**5

dirs = {}
for b in it.combinations(range(1, 64), 3):
    U = span(b)
    if len(U) == 8:
        dirs.setdefault(U, rref2(b))
assert len(dirs) == 1395

coset_map = {U: cosets(U) for U in dirs}
assert sum(map(len, coset_map.values())) == 11160

flat_ranks = C.Counter()
for U, b in dirs.items():
    for c, F in coset_map[U]:
        rq = character_rank(b)
        rp = rank_mod([V[x] for x in F], P)
        assert rq == rp
        flat_ranks[rp] += 1

assert flat_ranks == C.Counter({7: 2800, 8: 8360})

pairs, supports = 0, set()
rank8_directions = 0

for U, b in dirs.items():
    if character_rank(b) != 8:
        continue
    rank8_directions += 1
    rows, piv = augmented_rref(U)
    groups = C.defaultdict(list)

    for x in range(64):
        if x not in U:
            key, scale, coeff = reduce_point(x, rows, piv)
            groups[key].append((x, scale, coeff))

    for group in groups.values():
        for (x, sx, cx), (y, sy, cy) in it.combinations(group, 2):
            assert (x ^ y) in U
            t = sx / sy
            kernel = [-(a-t*b) for a,b in zip(cx,cy)]
            kernel += [Q(1), -t]
            assert all(kernel)

            for j in range(22):
                assert sum(
                    k * V[q][j]
                    for q, k in zip(U+(x,y), kernel)
                ) == 0

            pairs += 1
            for c, F in coset_map[U]:
                xx, yy = x ^ c, y ^ c
                S = tuple(sorted(F + (xx, yy)))
                assert S not in supports
                supports.add(S)

assert rank8_directions == 1045
assert pairs == 2800
assert len(supports) == 22400

full_ranks, deletion_ranks = C.Counter(), C.Counter()
for S in supports:
    A = [V[x] for x in S]
    r = rank_mod(A, P)
    full_ranks[r] += 1
    for j in range(10):
        B = A[:j] + A[j+1:]
        deletion_ranks[rank_mod(B, P)] += 1

assert full_ranks == C.Counter({9: 22400})
assert deletion_ranks == C.Counter({9: 224000})

print(json.dumps({
    "status": "PASS",
    "prime": P,
    "directions": len(dirs),
    "affine_flats": 11160,
    "flat_ranks": dict(flat_ranks),
    "rank_eight_directions": rank8_directions,
    "base_pairs": pairs,
    "unique_ten_point_supports": len(supports),
    "ten_point_ranks": dict(full_ranks),
    "deletion_ranks": dict(deletion_ranks),
    "deletions_checked": sum(deletion_ranks.values()),
    "scope": "All ten-point circuits containing an enumerated rank-eight affine three-flat; not all ten-point circuits globally."
}, indent=2))
