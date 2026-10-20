#!/usr/bin/env python3
"""
Exact classification, lengths n < 72 (and validation lengths), of binary words with:
   Phi_n | f  (primitive order absent),  support generating Z_n (full period),  sumset degree >= 4.
Step 1 (abstract): all sets D of proper divisors of n ("active orders", 1 in D because the word is nonzero) whose
        support S_D = union of classes C_m (m in D) generates Z_n and has degree >= 4.
Step 2 (realizability, EXACT): a binary word whose active set is contained in D is divisible by P_D = prod_{d|n, d not in D} Phi_d.
        deg P_D = n - r, r = sum_{d in D} phi(d).  f = P_D * q with q integer, deg q < r, and P_D(0) = +-1 so q is fixed by
        the first r coefficients of f.  Enumerate all 2^r choices of those bits, rebuild f, keep binary f.   (no floats)
Step 3: for every binary f found compute its TRUE active set and degree; report those with full period and degree >= 4.
"""

# ---------- exact cyclotomic helpers (integer arithmetic)
import sys
import numpy as np
from math import gcd

def polydiv_exact(num, den):          # integer polynomials, lowest degree first, den monic
    num = num[:]; q = [0] * (len(num) - len(den) + 1)
    for i in range(len(num) - len(den), -1, -1):
        c = num[i + len(den) - 1]; q[i] = c
        for j, d in enumerate(den): num[i + j] -= c * d
    assert all(v == 0 for v in num), "inexact division"
    return q

_phi = {}
def cyclo(m):
    if m in _phi: return _phi[m]
    p = [-1] + [0] * (m - 1) + [1]
    for d in range(1, m):
        if m % d == 0: p = polydiv_exact(p, cyclo(d))
    while p and p[-1] == 0: p.pop()
    _phi[m] = p; return p

def polymod(poly, mod):               # remainder of integer poly by monic mod
    r = poly[:]
    for i in range(len(r) - 1, len(mod) - 2, -1):
        c = r[i]
        if c:
            for j, d in enumerate(mod): r[i - len(mod) + 1 + j] -= c * d
    return (r + [0] * len(mod))[:len(mod) - 1]

def remainder_matrix(m):              # row r = coefficients of x^r mod Phi_m
    ph = cyclo(m)
    return np.array([polymod([0] * r + [1], ph) for r in range(m)], dtype=np.int64)

def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]

def min_degree(S, n):                 # least d with d-fold sumset = Z_n ; None if never (0 in S assumed)
    cur = set(S)
    for d in range(1, n + 1):
        if len(cur) == n: return d
        cur = {(x + s) % n for x in cur for s in S}
    return None


# ---------- classification
def phi(m): return len(cyclo(m)) - 1
def cls(n, m): return [k for k in range(n) if n // gcd(n, k) == m]
def support(n, D): return sorted({k for m in D for k in cls(n, m)})
def full_period(n, S):
    g = n
    for k in S: g = gcd(g, k)
    return g == 1
def degree(S, n): return min_degree(S, n)

def abstract_patterns(n, mindeg=4):
    divs = [d for d in divisors(n) if d < n]
    out = []
    for mask in range(1 << len(divs)):
        D = [divs[i] for i in range(len(divs)) if mask >> i & 1]
        if 1 not in D: continue
        S = support(n, D)
        if not full_period(n, S): continue
        dg = degree(S, n)
        if dg is None or dg >= mindeg: out.append((D, dg))
    return out

def polymul(a, c): return list(np.convolve(np.array(a, dtype=object), np.array(c, dtype=object)))

def binary_words_for(n, D):
    r = sum(phi(m) for m in D)
    P = [1]
    for d in divisors(n):
        if d not in D: P = polymul(P, cyclo(d))
    P = [int(x) for x in P]
    assert len(P) == n - r + 1 and abs(P[0]) == 1
    words = []
    CH = 1 << min(r, 20)
    Pn = np.array(P, dtype=np.int64)
    for s in range(0, 1 << r, CH):
        idx = np.arange(s, min(1 << r, s + CH), dtype=np.int64)
        f0 = ((idx[:, None] >> np.arange(r)) & 1).astype(np.int64)
        q = np.zeros_like(f0)
        for i in range(r):
            acc = f0[:, i].copy()
            for j in range(i): acc -= q[:, j] * (P[i - j] if i - j < len(P) else 0)
            q[:, i] = acc * P[0]                      # divide by P[0] = +-1
        f = np.zeros((len(idx), n), dtype=np.int64)
        for i in range(r): f[:, i:i + len(P)] += q[:, i, None] * Pn[None, :]
        ok = ((f >= 0) & (f <= 1)).all(axis=1)
        words.extend(map(tuple, f[ok].tolist()))
    return words

def true_active(w):
    n = len(w); act = []
    for m in divisors(n):
        bb = np.zeros(m, dtype=object)
        for j, x in enumerate(w): bb[j % m] += x
        if any(v != 0 for v in bb.dot(remainder_matrix(m).astype(object))): act.append(m)
    return act

def classify(n, mindeg=4, verbose=True):
    pats = abstract_patterns(n, mindeg); found = []; rs = []; seen = set()   # dedupe: a word lies in every pattern D containing its true active set
    for D, dg in pats:
        r = sum(phi(m) for m in D); rs.append(r)
        for w in binary_words_for(n, D):
            if w in seen: continue
            seen.add(w)
            act = true_active(w)
            if n in act or sum(w) in (0, n): continue
            S = support(n, act)
            if not full_period(n, S): continue
            d2 = degree(S, n)
            if d2 is None or d2 >= mindeg: found.append((tuple(act), d2, w))
    return pats, rs, found

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "validate":        # method check against the exhaustive 2^n search: n=24, degree>=3 -> expect 48 words
        pats, rs, found = classify(24, mindeg=3)
        print("n=24 degree>=3: patterns", len(pats), "max r", max(rs), " realizing words:", len(found),
              " distinct (active, degree):", sorted({(a, d) for a, d, _ in found}))
        pats, rs, found = classify(72, mindeg=4)
        fam = [x for x in found if x[0] == (1, 2, 8, 9, 18)]
        print("n=72 degree>=4: patterns", len(pats), "max r", max(rs), " realizing words:", len(found), " with active (1,2,8,9,18):", len(fam),
              " degrees:", sorted({d for _, d, _ in found}))
    else:
        tot_p = tot_w = 0
        for n in range(2, 72):
            pats, rs, found = classify(n)
            if pats:
                print(f"n={n:3d}: abstract patterns surviving (full period, no primitive, degree>=4): {len(pats):3d}   max r = {max(rs):2d}   binary words realizing: {len(found)}")
            tot_p += len(pats); tot_w += len(found)
        print("TOTAL abstract patterns:", tot_p, " TOTAL realizing binary words for n<72:", tot_w)
        print("RESULT:", "NO DEGREE>=4 WORD BELOW 72" if tot_w == 0 else "COUNTEREXAMPLE FOUND")
