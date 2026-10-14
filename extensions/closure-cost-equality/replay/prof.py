"""Compatible local reconstruction of prof.py for equality_check.py.

This is NOT the Claude-reported dependency whose SHA-256 is
829be3fc64d139a9947ec39a58056347c030e8a4a177b39442c93e9d9acd9f08.
It implements the same three functions and conventions:
  profile(T, lab) -> (k, positive delta profile)
  stable_size(T, lab) -> number of itinerary classes
  rgs(n) -> restricted-growth label partitions
Uses exact Fraction arithmetic for profile ranks.
"""
from fractions import Fraction

def _rank(vectors):
    rows = [list(map(Fraction, v)) for v in vectors if any(v)]
    rank = 0
    cols = len(rows[0]) if rows else 0
    for c in range(cols):
        pivot = next((r for r in range(rank, len(rows)) if rows[r][c] != 0), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pv = rows[rank][c]
        rows[rank] = [x / pv for x in rows[rank]]
        for r in range(len(rows)):
            if r != rank and rows[r][c] != 0:
                factor = rows[r][c]
                rows[r] = [a - factor * b for a, b in zip(rows[r], rows[rank])]
        rank += 1
    return rank

def _orbit(x, T):
    seen = []
    y = x
    while y not in seen:
        seen.append(y)
        y = T[y]
    return seen

def profile(T, lab):
    n = len(T)
    k = len(set(lab))
    labels = sorted(set(lab))
    vectors = []
    for b in labels:
        vectors.append([1 if lab[x] == b else 0 for x in range(n)])
    prev = _rank(vectors)
    deltas = []
    j = 1
    while True:
        for b in labels:
            v = [0] * n
            for x in range(n):
                y = x
                for _ in range(j):
                    y = T[y]
                if lab[y] == b:
                    v[x] = 1
            vectors.append(v)
        cur = _rank(vectors)
        d = cur - prev
        if d == 0:
            break
        deltas.append(d)
        prev = cur
        j += 1
    return k, tuple(deltas)

def stable_size(T, lab):
    n = len(T)
    ids = list(lab)
    while True:
        keys = [(ids[x], ids[T[x]]) for x in range(n)]
        mapping = {}
        new = []
        for key in keys:
            if key not in mapping:
                mapping[key] = len(mapping)
            new.append(mapping[key])
        if new == ids:
            return len(set(ids))
        ids = new

def rgs(n):
    if n == 0:
        yield ()
        return
    cur = [0] * n
    def rec(i, maxused):
        if i == n:
            yield tuple(cur)
            return
        for v in range(maxused + 2):
            cur[i] = v
            yield from rec(i + 1, max(maxused, v))
    yield from rec(1, 0)
