#!/usr/bin/env python3
"""
Congruence lattice of a finite permutation that is a disjoint union of cycles.

Self-contained, stdlib only.  Running this file:
  A. counts invariant equivalence relations by brute force (N<=8) and checks the formula
        |Con| = sum over set-partitions pi of cycles, prod over blocks B of sum_{d | gcd(B)} d^(|B|-1)
  B. checks SET EQUALITY between brute-force congruences and the quotient-data enumeration
  C. checks the derived MEET rule and JOIN rule against the concrete partition meet/join
Exit code 0 only if every check passes.

Encoding of a congruence: (pi, d, ph)
  pi : set partition of cycle indices (blocks sorted, smallest index first)
  d  : dict block -> modulus (divides gcd of the cycle lengths in the block)
  ph : dict cycle -> phase mod d(block); phase of each block's first cycle is 0
  element t of cycle i has class label (t + ph[i]) mod d  inside its block.

JOIN rule: grouping = join of the two groupings.  In each joined group the modulus is
  gcd( all moduli of the sub-blocks touching it, all loop inconsistencies of the phase constraints ).
MEET rule: cycles i,j stay grouped iff same block in BOTH inputs and the two phase
  differences agree mod gcd(d1,d2); the modulus is lcm(d1,d2); phases by CRT.
"""
import sys
from math import gcd
from itertools import product
from functools import reduce
from collections import defaultdict, deque

# ---------------------------------------------------------------- basics
def lcm(a, b): return a * b // gcd(a, b)

def set_partitions(xs):
    if not xs:
        yield []
        return
    f, r = xs[0], xs[1:]
    for p in set_partitions(r):
        for i in range(len(p)):
            yield p[:i] + [[f] + p[i]] + p[i + 1:]
        yield [[f]] + p

def build(cl):
    N = sum(cl); perm = [0] * N; cycles = []; idx = 0
    for L in cl:
        b = list(range(idx, idx + L)); cycles.append(b)
        for k in range(L): perm[b[k]] = b[(k + 1) % L]
        idx += L
    return perm, cycles

def canon(blocks): return tuple(sorted(tuple(sorted(b)) for b in blocks))

def is_invariant(part, perm):
    label = {}
    for bi, b in enumerate(part):
        for x in b: label[x] = bi
    for b in part:
        if len(b) < 2: continue
        t = label[perm[b[0]]]
        for x in b[1:]:
            if label[perm[x]] != t: return False
    return True

def meet_p(A, B):
    out = []
    for a in A:
        sa = set(a)
        for b in B:
            i = sa & set(b)
            if i: out.append(sorted(i))
    return canon(out)

def join_p(A, B, N):
    par = list(range(N))
    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for P in (A, B):
        for b in P:
            for y in b[1:]:
                ra, rb = f(b[0]), f(y)
                if ra != rb: par[ra] = rb
    g = defaultdict(list)
    for x in range(N): g[f(x)].append(x)
    return canon(g.values())

# ---------------------------------------------------- quotient-data side
def qd_to_part(cl, cycles, q):
    pi, d, ph = q
    out = []
    for B in pi:
        cls = {}
        for i in B:
            for t in range(cl[i]):
                cls.setdefault((t + ph[i]) % d[B], []).append(cycles[i][t])
        out.extend(cls.values())
    return canon(out)

def divisors(g): return [x for x in range(1, g + 1) if g % x == 0]

def enum_qd(cl):
    r = len(cl); res = []
    for pi in set_partitions(list(range(r))):
        pit = tuple(sorted(tuple(sorted(B)) for B in pi))
        per = []
        for B in pit:
            g = reduce(gcd, [cl[i] for i in B]); ch = []
            for d in divisors(g):
                for pt in product(range(d), repeat=len(B) - 1):
                    ph = {B[0]: 0}
                    for k, i in enumerate(B[1:]): ph[i] = pt[k]
                    ch.append((d, ph))
            per.append((B, ch))
        def rec(k, dB, ph):
            if k == len(per):
                res.append((pit, dict(dB), dict(ph))); return
            B, ch = per[k]
            for d, p in ch:
                d2 = dict(dB); d2[B] = d; p2 = dict(ph); p2.update(p)
                rec(k + 1, d2, p2)
        rec(0, {}, {})
    return res

def formula_count(cl):
    tot = 0
    for pi in set_partitions(list(range(len(cl)))):
        prod = 1
        for B in pi:
            g = reduce(gcd, [cl[i] for i in B])
            prod *= sum(d ** (len(B) - 1) for d in divisors(g))
        tot += prod
    return tot

def pi_join(p1, p2, r):
    par = list(range(r))
    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for P in (p1, p2):
        for B in P:
            for i in B[1:]:
                a, b = f(B[0]), f(i)
                if a != b: par[a] = b
    g = defaultdict(list)
    for i in range(r): g[f(i)].append(i)
    return tuple(sorted(tuple(v) for v in g.values()))

# ------------------------------------------------------------ JOIN rule
def predict_join(r, q1, q2):
    adj = defaultdict(list); moduli = defaultdict(list)
    for (pi, d, ph) in (q1, q2):
        for B in pi:
            m = d[B]
            for i in B: moduli[i].append(m)
            b0 = B[0]
            for i in B[1:]:
                adj[b0].append((i, ph[i])); adj[i].append((b0, -ph[i]))
    pj = pi_join(q1[0], q2[0], r)
    dB = {}; phase = {}
    for B in pj:
        root = B[0]; pot = {root: 0}; dq = deque([root])
        while dq:
            i = dq.popleft()
            for (j, delta) in adj[i]:
                if j not in pot:
                    pot[j] = pot[i] + delta; dq.append(j)
        D = 0
        for i in B:
            for m in moduli[i]: D = gcd(D, m)
            for (j, delta) in adj[i]: D = gcd(D, abs(pot[j] - pot[i] - delta))
        dB[B] = D
        for i in B: phase[i] = (pot[i] - pot[root]) % D
    return pj, dB, phase

# ------------------------------------------------------------ MEET rule
def block_of(pi, i):
    for B in pi:
        if i in B: return B

def predict_meet(r, q1, q2):
    (pi1, d1, ph1), (pi2, d2, ph2) = q1, q2
    par = list(range(r))
    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for i in range(r):
        for j in range(i + 1, r):
            B1, B2 = block_of(pi1, i), block_of(pi1, j)
            C1, C2 = block_of(pi2, i), block_of(pi2, j)
            if B1 != B2 or C1 != C2: continue
            g = gcd(d1[B1], d2[C1])
            if (ph1[i] - ph1[j] - (ph2[i] - ph2[j])) % g == 0:
                par[f(i)] = f(j)
    groups = defaultdict(list)
    for i in range(r): groups[f(i)].append(i)
    pm = tuple(sorted(tuple(sorted(v)) for v in groups.values()))
    dB = {}; phase = {}
    for B in pm:
        r0 = B[0]
        D1 = d1[block_of(pi1, r0)]; D2 = d2[block_of(pi2, r0)]; D = lcm(D1, D2)
        dB[B] = D
        for i in B:
            x = (ph1[i] - ph1[r0]) % D1; y = (ph2[i] - ph2[r0]) % D2
            sols = [p for p in range(D) if p % D1 == x and p % D2 == y]
            phase[i] = sols[0] if sols else None
    return pm, dB, phase

def same(pred, actual, r):
    pm, dB, ph = pred
    return (tuple(sorted(pm)) == tuple(sorted(actual[0])) and
            all(dB[B] == actual[1][B] for B in pm) and
            all(ph[i] == actual[2][i] for i in range(r)))

# ------------------------------------------------------------------ main
def main():
    ok = True
    print("A+B  count formula and set equality vs brute force")
    for cl in [(4,), (3, 1), (3, 2), (2, 2), (4, 2), (6,), (2, 2, 2), (3, 3), (4, 3),
               (2, 2, 2, 2), (4, 2, 2), (6, 2)]:
        perm, cycles = build(cl); N = len(perm)
        if N > 8:
            continue
        brute = {canon(p) for p in set_partitions(list(range(N))) if is_invariant(p, perm)}
        qd = enum_qd(cl)
        qparts = {qd_to_part(cl, cycles, q) for q in qd}
        good = (brute == qparts and len(brute) == formula_count(cl) == len(qd))
        ok &= good
        print(f"  {cl!s:14s} |Con|={len(brute):4d} formula={formula_count(cl):4d} set-equal={brute == qparts}  {'PASS' if good else 'FAIL'}")

    print("C    meet and join rules vs concrete partition meet/join (all ordered pairs)")
    tot_j = tot_m = bad_j = bad_m = 0
    for cl in [(4,), (6,), (4, 2), (3, 3), (6, 4), (2, 2, 2), (4, 2, 2), (6, 3),
               (2, 2, 2, 2), (6, 4, 2), (4, 4, 2)]:
        perm, cycles = build(cl); N = len(perm); r = len(cl)
        qd = enum_qd(cl)
        p2q = {qd_to_part(cl, cycles, q): q for q in qd}
        items = list(p2q.items()); bj = bm = 0
        for pa, qa in items:
            for pb, qb in items:
                if not same(predict_join(r, qa, qb), p2q[join_p(pa, pb, N)], r): bj += 1
                if not same(predict_meet(r, qa, qb), p2q[meet_p(pa, pb)], r): bm += 1
        n = len(items) ** 2
        tot_j += n; tot_m += n; bad_j += bj; bad_m += bm
        print(f"  {cl!s:12s} pairs={n:6d} join_mismatch={bj} meet_mismatch={bm}")
    ok &= (bad_j == 0 and bad_m == 0)
    print(f"TOTAL pairs={tot_j}  join mismatches={bad_j}  meet mismatches={bad_m}")
    print("RESULT:", "ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
