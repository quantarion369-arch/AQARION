#!/usr/bin/env python3
"""Exact witness/orbit and four-bit weighted-circuit experiment."""

import hashlib
import itertools as it
import json
import math
import sys
import time
import traceback
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

WITNESSES = [
    (
        [2,3,6,7,32,34,36,38,57,58,61,62],
        [1,-1,-1,1,-1,1,1,-1,1,-1,-1,1],
    ),
    (
        [2,10,22,25,27,28,32,40,49,51,54,60],
        [1,-1,-1,-1,1,1,-1,1,1,-1,1,-1],
    ),
    (
        [0,1,7,15,16,25,38,47,49,54,55,57],
        [1,-1,1,-1,-1,1,-1,1,1,1,-1,-1],
    ),
    (
        [20,21,22,23,24,26,29,31,32,34,36,38],
        [1,-1,-1,1,-1,1,1,-1,1,-1,-1,1],
    ),
]

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def features(x, n):
    b = [(x >> i) & 1 for i in range(n)]
    return (
        [1] + b
        + [b[i]*b[j] for i in range(n) for j in range(i+1,n)]
    )

def rref(rows):
    a = [[Fraction(x) for x in row] for row in rows]
    pivots = []
    rank = 0

    for col in range(len(a[0])):
        pivot = next(
            (i for i in range(rank, len(a)) if a[i][col]),
            None,
        )
        if pivot is None:
            continue

        a[rank], a[pivot] = a[pivot], a[rank]
        value = a[rank][col]
        a[rank] = [x/value for x in a[rank]]

        for i in range(len(a)):
            if i != rank and a[i][col]:
                value = a[i][col]
                a[i] = [
                    x-value*y for x,y in zip(a[i],a[rank])
                ]

        pivots.append(col)
        rank += 1
        if rank == len(a):
            break

    return a, pivots

def rank(rows):
    return len(rref(rows)[1])

def primitive(values):
    values = [Fraction(x) for x in values]
    den = math.lcm(*(x.denominator for x in values))
    z = [int(x*den) for x in values]
    g = math.gcd(*z)
    need(g != 0, "Zero primitive-vector input")
    z = [x//g for x in z]
    if next(x for x in z if x) < 0:
        z = [-x for x in z]
    return tuple(z)

def affine_flat(points):
    v = {x ^ points[0] for x in points}
    return (
        len(v) == 8
        and all(a ^ b in v for a in v for b in v)
    )

def exact_identity(points, z, n):
    rows = [features(x,n) for x in points]
    return all(
        sum(a*row[j] for a,row in zip(z,rows)) == 0
        for j in range(len(rows[0]))
    )

def support_digest(supports):
    h = hashlib.sha256()
    for support in sorted(supports):
        h.update(bytes(support))
    return h.hexdigest()

def cube_orbit(support):
    result = set()

    for perm in it.permutations(range(6)):
        transformed = [
            sum(((x >> perm[i]) & 1) << i for i in range(6))
            for x in support
        ]
        for shift in range(64):
            result.add(tuple(sorted(x ^ shift for x in transformed)))

    return result

def five_block_partitions():
    # Position zero is the constant-block marker.
    a = [0]*7

    def rec(i, largest):
        if i == 7:
            if largest == 4:
                yield tuple(a)
            return

        for value in range(min(largest+1,4)+1):
            a[i] = value
            yield from rec(i+1, max(largest,value))

    yield from rec(1,0)

def audit(report):
    witness_results = []
    simple_union = set()
    expected_orbits = [11520,3840,5760,11520]

    for number,(support,z) in enumerate(WITNESSES,1):
        need(
            support == sorted(set(support))
            and len(support) == 12,
            "Invalid witness support",
        )
        need(exact_identity(support,z,6),
             "Witness identity failed")

        rows = [features(x,6) for x in support]
        need(rank(rows) == 11, "Witness rank failed")

        deletion_ranks = [
            rank(rows[:i]+rows[i+1:])
            for i in range(12)
        ]
        need(deletion_ranks == [11]*12,
             "Witness deletion-rank failure")

        flat_count = sum(
            affine_flat(t)
            for t in it.combinations(support,8)
        )
        need(flat_count == 0, "Witness contains a three-flat")

        # Sum-preserving coefficient corruption control.
        bad = list(z)
        bad[0] += 1
        bad[1] -= 1
        need(not exact_identity(support,bad,6),
             "Corrupted-kernel control failed")

        orbit = cube_orbit(support)
        need(len(orbit) == expected_orbits[number-1],
             "Unexpected orbit size")
        need(not (simple_union & orbit),
             "Witness orbits overlap")
        simple_union.update(orbit)

        witness_results.append({
            "witness": number,
            "support": support,
            "primitive_kernel": z,
            "rank_Q": 11,
            "deletion_ranks": deletion_ranks,
            "contained_affine_three_flats": 0,
            "orbit_size": len(orbit),
            "orbit_sha256": support_digest(orbit),
        })

        print(
            "WITNESS", number,
            "PASS; ORBIT", len(orbit),
            flush=True,
        )

    need(len(simple_union) == 32640,
         "Simple orbit-union count mismatch")

    # Exact Fourier basis for the four-bit rational kernel.
    K = []
    for x in range(16):
        y = [1-2*((x >> i)&1) for i in range(4)]
        p = math.prod(y)
        K.append([p]+[p*a for a in y])

    need(rank(K) == 5, "Four-bit kernel-basis rank")
    need(all(
        sum(K[x][j]*features(x,4)[k] for x in range(16)) == 0
        for j in range(5) for k in range(11)
    ), "Four-bit kernel-basis identity")

    nullities = Counter()
    patterns = Counter()
    weighted = []
    tested = 0

    for omitted in it.combinations(range(16),4):
        tested += 1
        a,pivots = rref([K[x] for x in omitted])
        nullity = 5-len(pivots)
        nullities[nullity] += 1

        if nullity != 1:
            continue

        free = next(j for j in range(5) if j not in pivots)
        v = [Fraction(0)]*5
        v[free] = Fraction(1)

        for i,j in enumerate(pivots):
            v[j] = -a[i][free]

        z = primitive([
            sum(Fraction(t)*b for t,b in zip(row,v))
            for row in K
        ])
        support = tuple(x for x in range(16) if z[x])

        if len(support) != 12:
            continue

        coefficients = [z[x] for x in support]
        need(exact_identity(support,coefficients,4),
             "Weighted circuit identity")
        need(rank([features(x,4) for x in support]) == 11,
             "Weighted circuit rank")

        patterns[
            tuple(sorted(Counter(abs(a) for a in coefficients).items()))
        ] += 1
        weighted.append((support,z))

    need(tested == 1820, "Four-bit subset coverage")
    need(nullities == Counter({1:1720,2:100}),
         "Four-bit nullity distribution")
    need(len(weighted) == 80, "Weighted circuit count")
    need(
        patterns == Counter({((1,7),(2,4),(3,1)):80}),
        "Weighted coefficient pattern",
    )

    print("FOUR-BIT CENSUS PASS: 80 CIRCUITS", flush=True)

    partitions = list(five_block_partitions())
    need(len(partitions) == 140, "Block-partition count")

    embedded = set()
    generated = 0

    for blocks in partitions:
        anchors = [
            next(i for i in range(6) if blocks[i+1] == j)
            for j in range(1,5)
        ]
        free_coordinates = [
            i for i in range(6) if i not in anchors
        ]
        need(len(free_coordinates) == 2,
             "Embedding normalization")

        for mask in range(4):
            offset = sum(
                ((mask >> k)&1) << i
                for k,i in enumerate(free_coordinates)
            )

            for support,z in weighted:
                output = []

                for x in support:
                    point = offset
                    for i in range(6):
                        block = blocks[i+1]
                        if block and ((x >> (block-1))&1):
                            point ^= 1 << i
                    output.append(point)

                need(len(set(output)) == 12,
                     "Embedding collapsed distinct points")
                embedded.add(tuple(sorted(output)))
                generated += 1

    need(generated == 44800, "Embedding generation count")
    need(len(embedded) == 44800, "Embedding duplicates")
    need(not (embedded & simple_union),
         "Constructed families overlap")

    union = simple_union | embedded
    need(len(union) == 77440, "Combined lower-bound count")

    report.update({
        "witness_results": witness_results,
        "four_simple_orbits_disjoint": True,
        "simple_orbit_union_count": len(simple_union),
        "simple_orbit_union_sha256": support_digest(simple_union),
        "four_bit_subsets_tested": tested,
        "four_bit_nullity_distribution": dict(nullities),
        "four_bit_twelve_circuits": len(weighted),
        "weighted_absolute_coefficient_pattern":
            [[1,7],[2,4],[3,1]],
        "embedding_block_partitions": len(partitions),
        "weighted_embeddings_generated": generated,
        "weighted_embeddings_distinct": len(embedded),
        "weighted_embedding_sha256": support_digest(embedded),
        "constructed_family_intersection_size": 0,
        "constructed_union_count": len(union),
        "six_bit_twelve_circuit_lower_bound": len(union),
        "embedded_circuit_certification_method":
            "Exact four-bit circuit plus feature-preserving embedding",
        "all_44800_embedded_ranks_directly_recomputed": False,
        "scope":
            "Four exact witnesses, four complete cube-symmetry orbits, "
            "exhaustive four-bit twelve-circuit census, and canonical "
            "six-bit embeddings. Not a complete six-bit twelve-circuit "
            "census, formal proof, or novelty claim.",
    })

def main():
    started = time.monotonic()
    source = Path(__file__).resolve()
    original = source.read_bytes()
    output = Path(sys.argv[1]).resolve()

    report = {
        "experiment": "TWELVE-CIRCUIT-FAMILIES-004",
        "status": "RUNNING",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": hashlib.sha256(original).hexdigest(),
        "python_version": sys.version,
        "bit_convention": "x_i = (x >> i) & 1",
    }

    try:
        audit(report)
        need(source.read_bytes() == original, "Source changed")
        report["source_unchanged"] = True
        report["status"] = "PASS"

    except Exception as exc:
        report["status"] = "FAIL"
        report["error"] = type(exc).__name__ + ": " + str(exc)
        (output/"traceback.txt").write_text(traceback.format_exc())

    report["finished_utc"] = datetime.now(timezone.utc).isoformat()
    report["elapsed_seconds"] = round(time.monotonic()-started,6)

    (output/"REPORT.json").write_text(
        json.dumps(report,indent=2,sort_keys=True)+"\n"
    )
    print(json.dumps(report,indent=2,sort_keys=True),flush=True)
    return 0 if report["status"] == "PASS" else 2

if __name__ == "__main__":
    raise SystemExit(main())
