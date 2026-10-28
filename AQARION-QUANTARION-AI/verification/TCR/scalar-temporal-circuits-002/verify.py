"""Targeted exact checks only; no exhaustive map census."""
from fractions import Fraction as F
from math import comb, factorial, gcd
import json


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def rank(rows):
    if not rows:
        return 0
    a = [[F(x) for x in row] for row in rows]
    r = 0
    for c in range(len(a[0])):
        p = next((i for i in range(r, len(a)) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        pivot = a[r][c]
        a[r] = [x / pivot for x in a[r]]
        for i in range(r + 1, len(a)):
            factor = a[i][c]
            a[i] = [x - factor*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def matrix(T, h):
    rows = []
    for state in range(len(T)):
        row = [F(1)]
        for _ in range(len(T)):
            row.append(F(h[state]))
            state = T[state]
        rows.append(row)
    return rows


def permutation_count(m):
    return F(factorial(m-1)) + sum(
        (F(factorial(m), 2*a*(m-a))
         for a in range(1, m) if gcd(a, m-a) == 1), F(0))


def map_count(n):
    result = permutation_count(n) + sum(
        (comb(n, m)*factorial(n-m)*m*permutation_count(m)
         for m in range(1, n)), F(0))
    require(result.denominator == 1, 'Nonintegral map count')
    return result.numerator


def main():
    cases = [
        ('constant_three', (1,1,1), (0,1,4), 2, True, True, (3,-4,1)),
        ('image_collapse', (0,0,1,1), (0,1,2,5), 3, True, True, (3,-3,-1,1)),
        ('image_exchange', (1,0,0,1), (0,1,3,7), 3, True, True, (2,-7,7,-2)),
        ('image_fixed', (0,0,2,2), (0,1,'5/2',9), 3, True, True, ('13/2','-13/2',-1,1)),
        ('cycle_rank_three', (1,2,3,0), (0,1,3,2), 3, True, True, (-1,1,-1,1)),
        ('cycle_label_swap', (1,2,3,0), (0,1,2,3), 4, True, False, None),
        ('equal_within_fiber', (0,0,1,1), (0,0,2,5), 2, False, False, None),
        ('equal_image_outputs', (0,0,2,2), (0,1,0,5), 2, False, False, None),
        ('constant_four', (0,0,0,0), (0,1,2,3), 2, True, False, None),
    ]
    checked = []
    for name, T, h, expected_rank, observable, circuit, vector in cases:
        a = matrix(T, h)
        r = rank(a)
        obs = len({tuple(row[1:]) for row in a}) == len(T)
        deleted = [rank(a[:i]+a[i+1:]) for i in range(len(T))]
        circ = r == len(T)-1 and all(x == len(T)-1 for x in deleted)
        require((r, obs, circ) == (expected_rank, observable, circuit), name)
        certificate = None
        if vector is not None:
            v = [F(x) for x in vector]
            certificate = all(v) and all(
                sum(v[i]*a[i][j] for i in range(len(T))) == 0
                for j in range(len(a[0])))
            require(certificate, name + ': dependence failed')
        checked.append(dict(name=name, T=T, h=h, rank=r,
            observable=obs, affine_circuit=circ, deletion_ranks=deleted,
            supplied_relation=vector, relation_verified=certificate))
    expected = [1,4,23,146,1014,8124,68592,681456,7112592,82444320]
    counts = [map_count(n) for n in range(1,11)]
    require(counts == expected, 'Count arithmetic disagrees with pinned targets')
    print(json.dumps(dict(status='PASS', arithmetic='Fraction over Q',
        witness_checks=checked,
        counting_formula_values={str(n): x for n,x in enumerate(counts,1)},
        counting_check_scope='Formula arithmetic, not map enumeration',
        exhaustive_census_executed=False,
        formal_proof_machine_check=False), indent=2))


if __name__ == '__main__':
    main()
