#!/usr/bin/env python3
"""Exact replay of closure-gap registry claims. Exit 0 = all checks pass."""
import itertools, sys, time
from fractions import Fraction as F
import sympy as sp

def rgs(n):
    def rec(i, lab, m):
        if i == n: yield tuple(lab); return
        for l in range(m + 1):
            lab.append(l); yield from rec(i + 1, lab, max(m, l + 1) if l == m else m); lab.pop()
    yield from rec(0, [], 0)

def rank_q(rows):
    A = [[F(v) for v in r] for r in rows]; rk = 0
    for c in range(len(A[0])):
        p = next((i for i in range(rk, len(A)) if A[i][c] != 0), None)
        if p is None: continue
        A[rk], A[p] = A[p], A[rk]; pv = A[rk][c]; A[rk] = [v / pv for v in A[rk]]
        for i in range(len(A)):
            if i != rk and A[i][c] != 0:
                f = A[i][c]; A[i] = [a - f * b for a, b in zip(A[i], A[rk])]
        rk += 1
    return rk

def stable_size(T, lab):
    cur, cnt = list(lab), len(set(lab))
    while True:
        mp = {}; new = [mp.setdefault((cur[x], cur[T[x]]), len(mp)) for x in range(len(T))]
        if len(mp) == cnt: return cnt
        cur, cnt = new, len(mp)

def gap(T, lab):
    n, k = len(T), max(lab) + 1; rows = []; cur = list(range(n))
    for _ in range(n):
        rows += [[1 if lab[cur[x]] == b else 0 for x in range(n)] for b in range(k)]
        cur = [T[c] for c in cur]
    return stable_size(T, lab) - rank_q(rows)

cyc = lambda n: tuple((x + 1) % n for x in range(n))
z = sp.symbols("z")
def formula(w):
    n = len(w); p = len({tuple(w[i:] + w[:i]) for i in range(n)})
    g = sp.gcd(sp.Poly(sum(c * z**i for i, c in enumerate(w)), z), sp.Poly(z**n - 1, z))
    return p - n + g.degree()


def check_regression_witnesses():
    fixtures = [
        ("six-cycle gap 2", cyc(6), (0,0,0,1,1,1), 2),
        ("general n=5", (0,0,0,1,1), (0,1,0,0,1), 1),
        ("general n=7", (1,5,5,1,2,6,6), (0,0,1,1,0,0,1), 3),
        ("general n=8", (5,6,6,5,0,2,0,2), (0,0,1,1,0,0,1,1), 4),
    ]
    for name, T, lab, expected in fixtures:
        observed = gap(T, lab)
        if observed != expected:
            raise AssertionError((name, observed, expected))
    for k in range(2, 9):
        observed = gap(cyc(2*k), tuple([1]*k + [0]*k))
        if observed != k - 1:
            raise AssertionError(("half-half", k, observed, k - 1))
    print("PASS: 4 fixed witnesses and 7 half-half fixtures")

if __name__ == "__main__":
    check_regression_witnesses()
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 11; t0 = time.time()
    tot = viol = neg = 0; census = {}
    for n in range(3, nmax + 1):
        best = 0
        for w in itertools.product((0, 1), repeat=n):
            if len(set(w)) == 1: continue
            g = gap(cyc(n), w); tot += 1
            if n <= 9: viol += g != formula(list(w))
            neg += g < 0; best = max(best, g)
        census[n] = best
    print(f"CG-CYCLIC-GAP-FORMULA: formula checked on n=3..9; violations={viol}; negative gaps (all n<={nmax})={neg}")
    print("CG-GAP-UNBOUNDED  half-half 1^k0^k gaps k=2..8:", [(k, gap(cyc(2*k), tuple([1]*k + [0]*k))) for k in range(2, 9)])
    print(f"CG-MAX-CENSUS     cyclic max gap n=3..{nmax}:", [census[n] for n in range(3, nmax + 1)])
    print("  n=9 word 000000111 gap =", gap(cyc(9), tuple(int(c) for c in "000000111")))
    T7 = (1, 5, 5, 1, 2, 6, 6)
    res = {}
    for lab in rgs(7): res[gap(T7, lab)] = res.get(gap(T7, lab), 0) + 1
    print("CG-GENERAL-MAX    registry T, gap distribution over all 877 partitions:", dict(sorted(res.items())))
    for name, T, lab in (("n=5", (0,0,0,1,1), (0,1,0,0,1)), ("n=7", T7, (0,0,1,1,0,0,1)), ("n=8", (5,6,6,5,0,2,0,2), (0,0,1,1,0,0,1,1))):
        print(f"  general example {name}: T={T} partition={lab} gap={gap(T, lab)}")
    print(f"done in {time.time()-t0:.0f}s")
    if viol or neg: raise SystemExit(1)
