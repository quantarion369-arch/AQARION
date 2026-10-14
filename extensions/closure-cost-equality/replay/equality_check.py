"""Equality in the profile bound."""
import itertools, random, sys
from collections import Counter
from prof import profile, stable_size, rgs

def bound(k, delta):
    p = 1
    for x in delta:
        p *= 1 + x
    return k * (p - 1)

def analyse(T, lab, delta):
    d = len(delta) + 1
    S = {}
    for x in range(len(T)):
        y = x
        w = []
        for _ in range(d):
            w.append(lab[y])
            y = T[y]
        S.setdefault(tuple(w), set()).add(lab[y])
    A = [{w[j] for w in S} for j in range(d)]
    size = 1
    for a in A:
        size *= len(a)
    prod_ok = (size == len(S) and len(A[0]) == max(lab) + 1
               and all(len(A[j]) == 1 + delta[j - 1] for j in range(1, d)))
    nested = all(A[j] <= A[j - 1] for j in range(1, d))
    fb = None
    if all(len(v) == 1 for v in S.values()):
        for i in range(d):
            m = {}
            if all(m.setdefault(w[i], next(iter(v))) == next(iter(v))
                   for w, v in S.items()):
                fb = i
                break
    into_last = all(next(iter(v)) in A[d - 1] for v in S.values() if len(v) == 1)
    return prod_ok, nested, fb, into_last

def check(T, lab, stats):
    k, dl = profile(T, lab)
    s = stable_size(T, lab)
    C = sum(dl)
    ub = bound(k, dl)
    ctx = (T, lab, k, dl, s)
    assert C <= s - k <= ub, ("bound violated", ctx)
    attained = (s - k == ub)
    prod_ok, nested, fb, into_last = analyse(T, lab, dl)
    assert attained == prod_ok, ("product equivalence fails", ctx)
    if not dl:
        assert s == k and attained and fb == 0, ("empty-profile case", ctx)
        stats["empty"] += 1
    if attained:
        assert nested, ("not nested", ctx)
        assert fb is not None and into_last, ("no common-coordinate feedback", ctx)
        stats["attained"] += 1
        if dl:
            stats["attained_nonempty"] += 1
    stats["cases"] += 1

def build(A, i, psi):
    words = list(itertools.product(*A))
    ix = {w: j for j, w in enumerate(words)}
    return (tuple(ix[w[1:] + (psi[w[i]],)] for w in words),
            tuple(w[0] for w in words))

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
random.seed(seed)
print(f"seed={seed}")

st = Counter()
for n in range(1, 6):
    P = list(rgs(n))
    for T in itertools.product(range(n), repeat=n):
        for lab in P:
            check(T, lab, st)
print(f"exhaustive n<=5: cases={st['cases']} attained={st['attained']} "
      f"(nonempty profile {st['attained_nonempty']}) empty-profile={st['empty']}  all assertions passed")

st = Counter()
for _ in range(40000):
    n = random.choice((8, 9))
    k = random.choice((2, 3, 4))
    T = tuple(random.randrange(n) for _ in range(n))
    lab = tuple(random.randrange(k) for _ in range(n))
    if len(set(lab)) < k:
        continue
    check(T, lab, st)
print(f"random n in (8,9), k in (2,3,4): cases={st['cases']} attained={st['attained']} "
      f"(nonempty profile {st['attained_nonempty']}) empty-profile={st['empty']}  all assertions passed")

st = Counter()
classes = set()
tot = 0
while tot < 300:
    k = random.choice((2, 3, 4, 5))
    d = random.choice((2, 3, 4))
    sz = [k]
    for _ in range(1, d):
        sz.append(random.randint(2, sz[-1]))
    n = 1
    for z in sz:
        n *= z
    if n > 150:
        continue
    A = [list(range(k))]
    for z in sz[1:]:
        A.append(sorted(random.sample(A[-1], z)))
    i = random.randrange(d)
    psi = {a: random.choice(A[-1]) for a in A[i]}
    T, lab = build(A, i, psi)
    kk, dl = profile(T, lab)
    tot += 1
    assert dl == tuple(z - 1 for z in sz[1:])
    assert stable_size(T, lab) - kk == bound(kk, dl)
    check(T, lab, st)
    classes.add((k, dl))
print(f"constructions: {tot}/{tot} nested-product shift systems attain the bound "
      f"with profile (|A_j|-1); distinct (k,profile) classes={len(classes)}  all assertions passed")

st = Counter()
for _ in range(2000):
    k = random.randint(1, 4)
    n = random.randint(k, 8)
    lab = list(range(k)) + [random.randrange(k) for _ in range(n - k)]
    random.shuffle(lab)
    lab = tuple(lab)
    Q = [random.randrange(k) for _ in range(k)]
    blocks = {b: [x for x in range(n) if lab[x] == b] for b in range(k)}
    T = tuple(random.choice(blocks[Q[lab[x]]]) for x in range(n))
    mp = {}
    lab2 = tuple(mp.setdefault(b, len(mp)) for b in lab)
    assert profile(T, lab2)[1] == ()
    check(T, lab2, st)
print(f"empty-profile constructions: {st['cases']} cases, all attain equality (s==k)  all assertions passed")

print("ALL CHECKS PASSED")
