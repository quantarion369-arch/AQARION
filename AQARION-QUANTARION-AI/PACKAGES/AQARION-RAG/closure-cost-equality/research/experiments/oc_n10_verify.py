import math, time
from itertools import permutations
from collections import defaultdict

def canon(R):
    return tuple(sorted((tuple(sorted(b)) for b in R), key=lambda b: (b[0], len(b))))

def Timg(R, T):
    return canon([frozenset(T[x] for x in b) for b in R])

def pjoin(A, B, n):
    par = list(range(n))
    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for blk in (A, B):
        for b in blk:
            for x in b[1:]:
                ra, rb = find(b[0]), find(x)
                if ra != rb:
                    par[ra] = rb
    g = defaultdict(list)
    for x in range(n):
        g[find(x)].append(x)
    return canon([frozenset(v) for v in g.values()])

def closure_height(R, T, n):
    cur = canon(R)
    h = 1
    while True:
        nxt = pjoin(cur, Timg(cur, T), n)
        if nxt == cur:
            return h
        cur = nxt
        h += 1

def all_partitions_tuples(n):
    out = []
    def rec(x, maxlab, assign):
        if x == n:
            g = defaultdict(list)
            for i, l in enumerate(assign):
                g[l].append(i)
            out.append(canon([frozenset(v) for v in g.values()]))
            return
        for l in range(maxlab + 2):
            assign.append(l)
            rec(x + 1, max(maxlab, l), assign)
            assign.pop()
    rec(0, -1, [])
    return out

def cycle_type(p, n):
    seen = [False] * n
    ct = []
    for i in range(n):
        if seen[i]:
            continue
        j = i
        L = 0
        while not seen[j]:
            seen[j] = True
            L += 1
            j = p[j]
        ct.append(L)
    return tuple(sorted(ct, reverse=True))

def oc_formula(ct):
    L = sorted(ct, reverse=True)
    if len(L) == 1:
        return L[0] - 1
    return max(a + b - math.gcd(a, b) for i, a in enumerate(L) for b in L[i + 1:])

n = 10
parts = all_partitions_tuples(n)
print("Bell(10) check: %d partitions (expected 115975)" % len(parts))

if len(parts) != 115975:
    print("STOP: partition count mismatch")
else:
    type_reps = {}
    for p in permutations(range(n)):
        ct = cycle_type(p, n)
        if ct not in type_reps:
            type_reps[ct] = p

    print("Cycle types found: %d (expected 42)" % len(type_reps))
    t0 = time.time()
    mismatches = []
    idx = 0
    for ct in sorted(type_reps):
        idx += 1
        T = type_reps[ct]
        best = 0
        for R in parts:
            h = closure_height(R, T, n)
            if h > best:
                best = h
        f = oc_formula(ct)
        if best == f:
            status = "OK"
        else:
            status = "MISMATCH"
        print("[%2d/42] type=%s oc=%d formula=%d %s" % (idx, ct, best, f, status))
        if best != f:
            mismatches.append((ct, best, f))

    print("")
    print("Elapsed: %.1f seconds" % (time.time() - t0))
    print("MISMATCHES: %d" % len(mismatches))
    for m in mismatches:
        print(m)
