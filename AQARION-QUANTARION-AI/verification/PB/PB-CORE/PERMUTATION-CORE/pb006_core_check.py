#!/usr/bin/env python3
"""Finite permutation-core check; not Lean certification or a novelty claim."""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from math import factorial
from pathlib import Path
import sys

BELLS = (1, 1, 2, 5, 15, 52, 203)

def partitions(n):
    if n == 0:
        yield ()
        return
    def rec(labels):
        if len(labels) == n:
            yield tuple(labels)
            return
        for value in range(max(labels)+2):
            yield from rec(labels+[value])
    yield from rec([0])

def shape(labels):
    return tuple(sorted(Counter(labels).values(), reverse=True))

def integer_partition_count(n):
    counts = [1] + [0]*n
    for part in range(1, n+1):
        for total in range(part, n+1):
            counts[total] += counts[total-part]
    return counts[n]

def invariant(perm, labels):
    return all((labels[x] == labels[y]) ==
               (labels[perm[x]] == labels[perm[y]])
               for x in range(len(labels)) for y in range(x))

def stabilizer_size(block_sizes):
    result = 1
    for size, multiplicity in Counter(block_sizes).items():
        result *= factorial(size)**multiplicity * factorial(multiplicity)
    return result

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def run():
    require(invariant((0,1,2), (0,0,1)), 'identity control failed')
    require(not invariant((0,2,1), (0,0,1)), 'non-invariance control failed')
    rows = []
    for n in range(7):
        parts = list(partitions(n))
        require(len(parts) == BELLS[n], 'partition count mismatch')
        require(len(set(parts)) == len(parts), 'duplicate partitions')
        perms = list(itertools.permutations(range(n)))
        require(len(perms) == factorial(n), 'permutation count mismatch')
        stabilizers = [0]*len(parts)
        fixed_total = 0
        for perm in perms:
            for i, labels in enumerate(parts):
                if invariant(perm, labels):
                    stabilizers[i] += 1
                    fixed_total += 1
        types = Counter(shape(labels) for labels in parts)
        for labels, actual in zip(parts, stabilizers):
            require(actual == stabilizer_size(shape(labels)), 'stabilizer mismatch')
        for block_sizes, actual in types.items():
            predicted = factorial(n)//stabilizer_size(block_sizes)
            require(actual == predicted, 'block-type cardinality mismatch')
        p = integer_partition_count(n)
        require(len(types) == p, 'integer-partition classification mismatch')
        require(fixed_total == factorial(n)*p, 'aggregate identity mismatch')
        rows.append({'k': n, 'set_partitions': len(parts),
                     'permutations': len(perms), 'integer_partitions': p,
                     'pairs_examined': len(parts)*len(perms),
                     'invariant_pairs': fixed_total, 'factorial_times_p': factorial(n)*p})
        print(f'PASS k={n}: S_k={fixed_total}, k!*p(k)={factorial(n)*p}', flush=True)
    return {'status': 'PASS', 'range': 'k=0..6', 'results': rows,
            'pairs_examined': sum(row['pairs_examined'] for row in rows),
            'scope': 'Finite abstract permutation-core check; not Lean execution, historical source audit, or endofunction aggregate verification',
            'controls': ['identity invariant', 'known non-invariant permutation rejected'],
            'python': sys.version, 'platform': sys.platform}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', required=True, type=Path)
    args = parser.parse_args()
    if args.receipt.exists() or not args.receipt.parent.is_dir():
        parser.error('receipt must be a new file in an existing directory')
    report = run()
    report['source_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    with args.receipt.open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write(chr(10))
    print('PASS: pairs examined =', report['pairs_examined'])
    print('Receipt:', args.receipt)

if __name__ == '__main__':
    main()
