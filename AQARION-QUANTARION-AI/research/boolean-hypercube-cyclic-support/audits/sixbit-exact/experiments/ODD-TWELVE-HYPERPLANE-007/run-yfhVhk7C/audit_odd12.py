#!/usr/bin/env python3
"""Exact odd-support-twelve hyperplane audit; no historical imports."""

import hashlib
import itertools as it
import json
import math
import sys
import time
import traceback
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def feature(x, n):
    b = [(x >> i) & 1 for i in range(n)]
    return [1] + b + [
        b[i]*b[j] for i,j in it.combinations(range(n), 2)
    ]

def marginal(x):
    return [
        int(((x >> i) & 1) == a and ((x >> j) & 1) == b)
        for i,j in it.combinations(range(6), 2)
        for a,b in it.product((0,1), repeat=2)
    ]

def rref(rows):
    a = [[Fraction(v) for v in row] for row in rows]
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
        a[rank] = [v/value for v in a[rank]]
        for i in range(len(a)):
            if i != rank and a[i][col]:
                value = a[i][col]
                a[i] = [
                    v-value*w for v,w in zip(a[i], a[rank])
                ]
        pivots.append(col)
        rank += 1
        if rank == len(a):
            break
    return a, pivots

def binary_rank(vectors):
    pivots = {}
    for value in vectors:
        while value:
            pivot = value.bit_length()-1
            if pivot in pivots:
                value ^= pivots[pivot]
            else:
                pivots[pivot] = value
                break
    return len(pivots)

def identity(support, coefficients, table):
    return all(
        sum(
            coefficients[i]*table[x][j]
            for i,x in enumerate(support)
        ) == 0
        for j in range(len(table[0]))
    )

def exact_kernel(support, table):
    a, pivots = rref([
        [table[x][j] for x in support]
        for j in range(len(table[0]))
    ])
    if len(pivots) == 12:
        return 12, None

    need(len(pivots) == 11, "Unexpected lower-rank base support")
    free = next(j for j in range(12) if j not in pivots)
    vector = [Fraction(0)]*12
    vector[free] = Fraction(1)

    for row, pivot in enumerate(pivots):
        vector[pivot] = -a[row][free]

    denominator = math.lcm(*(v.denominator for v in vector))
    coefficients = [int(v*denominator) for v in vector]
    divisor = math.gcd(*coefficients)
    need(divisor != 0, "Zero kernel")
    coefficients = [v//divisor for v in coefficients]

    if coefficients[0] < 0:
        coefficients = [-v for v in coefficients]

    need(
        all(v != 0 and v % 2 for v in coefficients),
        "Base kernel is not full-support and all-odd",
    )
    need(identity(support, coefficients, table),
         "Base integer identity failed")
    return 11, tuple(coefficients)

def coordinate_maps(n):
    return [
        tuple(
            sum(((x >> p[i]) & 1) << i for i in range(n))
            for x in range(1 << n)
        )
        for p in it.permutations(range(n))
    ]

def pattern(coefficients):
    return " ".join(
        str(value)+"^"+str(count)
        for value,count in sorted(
            Counter(map(abs, coefficients)).items()
        )
    )

def support_digest(supports):
    h = hashlib.sha256()
    for support in sorted(supports):
        h.update(bytes(support))
    return h.hexdigest()

def certify_sample(support, coefficients, monomials, marginals):
    result = {}
    for label, table in (
        ("monomial", monomials),
        ("marginal", marginals),
    ):
        rows = [table[x] for x in support]
        need(identity(support, coefficients, table),
             label+" sample identity failed")
        need(len(rref(rows)[1]) == 11,
             label+" sample rank failed")

        deletions = [
            len(rref(rows[:i]+rows[i+1:])[1])
            for i in range(12)
        ]
        need(deletions == [11]*12,
             label+" sample deletion failed")

        corrupted = list(coefficients)
        corrupted[0] += 1
        corrupted[1] -= 1
        need(
            not identity(support, corrupted, table),
            label+" corrupted-kernel control failed",
        )
        result[label] = {
            "rank": 11,
            "deletion_ranks": deletions,
            "corrupted_kernel_rejected": True,
        }
    return result

def audit(report, output):
    need(len(rref([[0,1], [1,0]])[1]) == 2,
         "Row-swap control failed")
    need(len(rref([[1,2,3], [2,4,6]])[1]) == 1,
         "Singular control failed")

    f5 = [feature(x,5) for x in range(32)]
    f6 = [feature(x,6) for x in range(64)]
    m6 = [marginal(x) for x in range(64)]

    masks = [
        sum(f5[x][j] << x for x in range(32))
        for j in range(16)
    ]
    need(binary_rank(masks) == 16, "Binary feature rank failed")
    need(
        all((a & b).bit_count() % 2 == 0
            for a in masks for b in masks),
        "Binary self-orthogonality failed",
    )

    word = 0
    candidates = set()
    weights = Counter({0: 1})

    for index in range(1, 1 << 16):
        word ^= masks[(index & -index).bit_length()-1]
        weights[word.bit_count()] += 1
        if word.bit_count() == 12:
            candidates.add(tuple(
                x for x in range(32) if (word >> x) & 1
            ))

    need(sum(weights.values()) == 65536,
         "Binary codeword coverage failed")
    need(len(candidates) == 13888,
         "Weight-twelve candidate count mismatch")
    need(
        all(
            binary_rank([x ^ support[0] for x in support]) == 5
            for support in candidates
        ),
        "Five-bit candidate affine dimension failed",
    )

    remaining = set(candidates)
    base = {}
    base_records = []
    maps5 = coordinate_maps(5)

    while remaining:
        support = min(remaining)
        rank, coefficients = exact_kernel(support, f5)
        family = {}

        for mapping in maps5:
            for shift in range(32):
                pairs = sorted(
                    (
                        mapping[x] ^ shift,
                        coefficients[i] if coefficients else 0,
                    )
                    for i,x in enumerate(support)
                )
                transformed = tuple(x for x,c in pairs)
                kernel = (
                    tuple(c for x,c in pairs)
                    if coefficients else None
                )

                if kernel and kernel[0] < 0:
                    kernel = tuple(-v for v in kernel)

                if transformed in family:
                    need(
                        family[transformed] == kernel,
                        "Transported kernel conflict",
                    )
                family[transformed] = kernel

        need(
            set(family) <= remaining,
            "Base orbit overlaps or leaves candidate universe",
        )
        remaining.difference_update(family)

        if coefficients:
            base.update(family)

        base_records.append({
            "support": support,
            "rank_Q": rank,
            "primitive_kernel": coefficients,
            "orbit_size": len(family),
        })

    need(len(base_records) == 23, "Base orbit count mismatch")
    print(
        "BASE CENSUS:", len(candidates), "SUPPORTS;",
        len(base_records), "ORBITS;",
        len(base), "RANK-ELEVEN SUPPORTS",
        flush=True,
    )

    cases = []
    global_sets = defaultdict(set)
    planes = 0

    for normal_weight in range(1,7):
        low = (1 << (normal_weight-1))-1
        normal = 32 | low
        accepted = []
        counts = Counter()
        samples = {}

        for support, coefficients in base.items():
            lifted = tuple(
                x | (((x & low).bit_count() % 2) << 5)
                for x in support
            )
            if not identity(lifted, coefficients, f6):
                continue

            pairs = sorted(zip(lifted, coefficients))
            points = tuple(x for x,c in pairs)
            kernel = tuple(c for x,c in pairs)
            if kernel[0] < 0:
                kernel = tuple(-v for v in kernel)

            need(
                binary_rank([x ^ points[0] for x in points]) == 5,
                "Lifted affine dimension failed",
            )
            need(
                all((x & normal).bit_count() % 2 == 0
                    for x in points),
                "Representative hyperplane equation failed",
            )

            key = pattern(kernel)
            counts[key] += 1
            accepted.append((points, kernel, key))

            if key not in samples:
                samples[key] = {
                    "support": points,
                    "primitive_kernel": kernel,
                    "checks": certify_sample(points, kernel, f6, m6),
                }

        normal_positions = [
            i for i in range(6) if (normal >> i) & 1
        ]
        remaining_positions = [
            i for i in range(6) if i not in normal_positions
        ]

        for target in it.combinations(range(6), normal_weight):
            other = [i for i in range(6) if i not in target]
            permutation = dict(zip(normal_positions, target))
            permutation.update(zip(remaining_positions, other))

            mapping = [
                sum(
                    ((x >> i) & 1) << permutation[i]
                    for i in range(6)
                )
                for x in range(64)
            ]

            for parity in (0,1):
                planes += 1
                shift = (1 << target[0]) if parity else 0

                for points, kernel, key in accepted:
                    transformed = tuple(sorted(
                        mapping[x] ^ shift for x in points
                    ))
                    need(
                        transformed not in global_sets[key],
                        "Duplicate support across unique hyperplanes",
                    )
                    global_sets[key].add(transformed)

        multiplicity = 2*math.comb(6, normal_weight)
        cases.append({
            "normal_weight": normal_weight,
            "hyperplane_count": multiplicity,
            "counts_per_representative_hyperplane": dict(counts),
            "cross_representation_samples": samples,
        })
        print(
            "NORMAL WEIGHT:", normal_weight,
            "HYPERPLANES:", multiplicity,
            "COUNTS:", dict(counts),
            flush=True,
        )

    need(planes == 126, "Hyperplane coverage failed")
    need(
        sum(map(len, global_sets.values()))
        == len(set().union(*global_sets.values())),
        "Different coefficient-pattern families overlap",
    )

    simple = global_sets.get("1^12", set())
    weighted = global_sets.get("1^10 3^2", set())
    need(
        support_digest(simple)
        == "a44774950d547afd1f42ac3976b68d9fa17cd61a9fddff84c61ecd0d8629d1a8",
        "Retained simple-family support digest not reproduced",
    )

    maps6 = coordinate_maps(6)
    published_family = set()

    for seed in (
        [0,1,2,4,8,15,16,23,27,29,30,31],
        [0,1,2,4,8,15,48,55,59,61,62,63],
    ):
        published_family.update(
            tuple(sorted(mapping[x] ^ shift for x in seed))
            for mapping in maps6
            for shift in range(64)
        )

    need(
        len(published_family) == 672
        and published_family <= weighted,
        "Published-seed family reconciliation failed",
    )

    total = sum(map(len, global_sets.values()))
    report.update({
        "binary_codewords_enumerated": 65536,
        "five_bit_weight_twelve_supports": len(candidates),
        "five_bit_support_orbits": len(base_records),
        "five_bit_rank_eleven_supports": len(base),
        "five_bit_rank_twelve_supports":
            len(candidates)-len(base),
        "hyperplanes_covered": planes,
        "representative_hyperplane_candidates":
            6*len(candidates),
        "actual_six_bit_kernel_vector_tests": 6*len(base),
        "global_pattern_counts": {
            key: len(supports)
            for key,supports in global_sets.items()
        },
        "support_set_sha256": {
            key: support_digest(supports)
            for key,supports in global_sets.items()
        },
        "odd_support_twelve_sector_count": total,
        "published_seed_family_reconstructed":
            len(published_family),
        "other_weighted_supports":
            len(weighted-published_family),
        "all_actual_six_bit_ranks_individually_recomputed": False,
        "rank_certificate":
            "Exact base-orbit ranks give lower bounds by coordinate "
            "projection. Actual six-bit integer identities give "
            "matching upper bounds. Full-support kernels establish "
            "minimality.",
        "classical_coverage_dependency":
            "Ghorbani et al. 2020, Lemma 13: the relevant weight-twelve "
            "RM(3,6) supports have affine dimension five.",
        "odd_support_eight_sector_completed": False,
        "complete_twelve_circuit_census": False,
        "conditional_lower_bound_if_retained_44800_family_valid":
            total+44800,
        "historical_44800_family_reenumerated": False,
        "novelty_claim": False,
    })

    (output/"CASES.json").write_text(
        json.dumps({
            "base_orbit_certificates": base_records,
            "hyperplane_cases": cases,
        }, indent=2) + "\n"
    )

def main():
    started = time.monotonic()
    source = Path(__file__).resolve()
    original = source.read_bytes()
    output = Path(sys.argv[1]).resolve()

    report = {
        "experiment": "ODD-TWELVE-HYPERPLANE-007",
        "status": "RUNNING",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": sha(original),
        "python_version": sys.version,
        "scope":
            "Exact odd-support-twelve sector audit conditional on "
            "the cited classical binary-support theorem. Not the "
            "odd-support-eight sector or a full twelve-circuit census.",
    }

    try:
        audit(report, output)
        need(source.read_bytes() == original, "Source changed")
        report["source_unchanged"] = True
        report["status"] = "PASS"
    except Exception as exc:
        report["status"] = "FAIL"
        report["error"] = type(exc).__name__ + ": " + str(exc)
        (output/"traceback.txt").write_text(traceback.format_exc())

    report["finished_utc"] = datetime.now(timezone.utc).isoformat()
    report["elapsed_seconds"] = round(time.monotonic()-started, 6)
    (output/"REPORT.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(report, indent=2, sort_keys=True), flush=True)
    return 0 if report["status"] == "PASS" else 2

if __name__ == "__main__":
    raise SystemExit(main())
