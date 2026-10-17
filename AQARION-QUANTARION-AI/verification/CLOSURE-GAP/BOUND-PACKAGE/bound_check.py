#!/usr/bin/env python3
"""Exact closure-gap bound replay. No repository edits or synthetic evidence."""
import argparse
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import sys

EXPECTED_COUNTS = {1: 1, 2: 8, 3: 135, 4: 3840}
WITNESSES = (
    (5, (0,0,0,1,1), (0,1,0,0,1), 1),
    (6, (1,2,3,4,5,0), (0,0,0,1,1,1), 2),
    (7, (1,5,5,1,2,6,6), (0,0,1,1,0,0,1), 3),
    (8, (5,6,6,5,0,2,0,2), (0,0,1,1,0,0,1,1), 4),
)

def partitions(n):
    if n < 1:
        raise ValueError('n must be positive')
    def rec(labels):
        if len(labels) == n:
            yield tuple(labels)
            return
        for label in range(max(labels) + 2):
            yield from rec(labels + [label])
    yield from rec([0])

def rank_q(rows):
    if not rows:
        return 0
    if any(len(row) != len(rows[0]) for row in rows):
        raise ValueError('ragged matrix')
    a = [[Fraction(v) for v in row] for row in rows]
    rank = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        value = a[rank][col]
        a[rank] = [v / value for v in a[rank]]
        for i in range(rank + 1, len(a)):
            if a[i][col]:
                factor = a[i][col]
                a[i] = [x - factor*y for x, y in zip(a[i], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank

def state_bound(n):
    if n < 1:
        raise ValueError('n must be positive')
    return n - 1 - (n - 1).bit_length()

def validate_system(T, labels):
    n = len(T)
    if n < 1 or len(labels) != n:
        raise ValueError('nonempty map and matching labels required')
    if any(type(x) is not int or not 0 <= x < n for x in T):
        raise ValueError('invalid map target')
    if any(type(b) is not int or b < 0 for b in labels):
        raise ValueError('invalid partition label')
    if set(labels) != set(range(max(labels) + 1)):
        raise ValueError('partition labels must be contiguous from zero')

def stable_size(T, labels):
    cur = tuple(labels)
    while True:
        keys = {}
        refined = tuple(keys.setdefault((cur[x], cur[T[x]]), len(keys))
                        for x in range(len(T)))
        if len(set(refined)) == len(set(cur)):
            return len(set(cur))
        cur = refined

def evaluate(T, labels):
    validate_system(T, labels)
    n, k = len(T), max(labels) + 1
    rows = []
    for x in range(n):
        cur, row = x, []
        for t in range(n):
            row.extend(int(labels[cur] == b) for b in range(k))
            cur = T[cur]
        rows.append(tuple(row))
    distinct = sorted(set(rows))
    m = len(distinct)
    if m != stable_size(T, labels):
        raise RuntimeError('finite itinerary / stable-refinement mismatch')
    r = rank_q(distinct)
    if rank_q([row + (1,) for row in distinct]) != r:
        raise RuntimeError('constant-column identity failed')
    gap = m - r
    if not (0 <= gap <= state_bound(m) <= state_bound(n)):
        raise RuntimeError('closure-gap bound violated')
    if m > 2 ** (r - 1):
        raise RuntimeError('binary-row bound violated')
    return {'n': n, 'blocks': k, 'm': m, 'r': r, 'gap': gap,
            'class_bound': state_bound(m), 'state_bound': state_bound(n)}

def require_count(n, count):
    if count != EXPECTED_COUNTS[n]:
        raise RuntimeError(f'incomplete enumeration n={n}: {count}')

def check_witness(T, labels, expected):
    result = evaluate(T, labels)
    if result['gap'] != expected or result['gap'] != result['state_bound']:
        raise RuntimeError('witness does not attain its expected bound')
    return dict(result, T=list(T), labels=list(labels))

def run():
    exhaustive = []
    for n in range(1, 5):
        parts = list(partitions(n))
        if len(parts) != len(set(parts)):
            raise RuntimeError('duplicate partitions')
        count, maximum = 0, 0
        for T in itertools.product(range(n), repeat=n):
            for labels in parts:
                result = evaluate(T, labels)
                maximum = max(maximum, result['gap'])
                count += 1
        require_count(n, count)
        exhaustive.append({'n': n, 'partitions': len(parts),
                           'pairs': count, 'maximum_gap': maximum})
        print(f'PASS exhaustive n={n}: {count} pairs', flush=True)
    witnesses = []
    for n, T, labels, expected in WITNESSES:
        if len(T) != n:
            raise RuntimeError('fixture size mismatch')
        witnesses.append(check_witness(T, labels, expected))
        print(f'PASS attainment n={n}: gap={expected}', flush=True)
    return {
        'status': 'PASS',
        'encoding': 'all block indicators at times 0..n-1; distinct state rows',
        'arithmetic': 'fractions.Fraction over Q',
        'exhaustive': exhaustive,
        'total_exhaustive_pairs': sum(x['pairs'] for x in exhaustive),
        'witnesses': witnesses,
        'checks': ['stable-class identity', 'constant-column rank identity',
                   'nonnegative gap', 'binary-row bound', 'class and state bounds',
                   'expected enumeration counts', 'attainment fixtures'],
        'scope': 'Finite replay, not a universal proof, novelty search, or Lean certification',
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'environment': {'python': sys.version, 'platform': sys.platform}
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', required=True, type=Path,
                        help='new output file; an existing file is never overwritten')
    args = parser.parse_args()
    if args.receipt.exists():
        parser.error('receipt already exists; choose a new path')
    if not args.receipt.parent.is_dir():
        parser.error('receipt parent directory does not exist')
    receipt = run()
    with args.receipt.open('x') as stream:
        json.dump(receipt, stream, indent=2)
        stream.write(chr(10))
    print('PASS: receipt saved:', args.receipt, flush=True)

if __name__ == '__main__':
    main()
