#!/usr/bin/env python3
"""Five-bit simple twelve-circuit census and six-bit extensions."""

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

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def features(x, n):
    b = [(x >> i) & 1 for i in range(n)]
    return [1] + b + [
        b[i]*b[j] for i,j in it.combinations(range(n), 2)
    ]

def rank_q(rows):
    a = [[Fraction(x) for x in row] for row in rows]
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
        for i in range(rank+1, len(a)):
            value = a[i][col]
            if value:
                a[i] = [
                    x-value*y for x,y in zip(a[i], a[rank])
                ]
        rank += 1
        if rank == len(a):
            break
    return rank

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

def coordinate_maps(n):
    return [
        tuple(
            sum(((x >> p[i]) & 1) << i for i in range(n))
            for x in range(1 << n)
        )
        for p in it.permutations(range(n))
    ]

def orbit(support, maps, n):
    return {
        tuple(sorted(mapping[x] ^ shift for x in support))
        for mapping in maps
        for shift in range(1 << n)
    }

def identity(support, coefficients, n):
    rows = [features(x, n) for x in support]
    return all(
        sum(c*row[j] for c,row in zip(coefficients, rows)) == 0
        for j in range(len(rows[0]))
    )

def support_digest(supports):
    h = hashlib.sha256()
    for support in sorted(supports):
        h.update(bytes(support))
    return h.hexdigest()

def bind_previous(base):
    d = base/"experiments/TWELVE-CIRCUIT-FAMILIES-004"
    r = d/"run-yIVqk7rI"
    expected = (
        "47d8fb91c48f2784ea2e4ba9a7f7005263"
        "ce7671a30efb40401a7c67da68fe43"
    )

    need(sha((d/"audit12_families.py").read_bytes()) == expected,
         "FAMILIES-004 source hash mismatch")
    need(sha((r/"audit12_families.py").read_bytes()) == expected,
         "FAMILIES-004 snapshot hash mismatch")

    entries = [
        line.split("  ", 1)
        for line in (r/"SHA256SUMS").read_text().splitlines()
    ]
    names = {"audit12_families.py", "run.log", "exit.txt", "REPORT.json"}
    need(
        len(entries) == 4
        and all(len(e) == 2 for e in entries)
        and {e[1] for e in entries} == names,
        "FAMILIES-004 manifest coverage mismatch",
    )

    paths = [d/"audit12_families.py", r/"SHA256SUMS"]
    for digest, name in entries:
        path = r/name
        need(sha(path.read_bytes()) == digest,
             "FAMILIES-004 manifest mismatch: " + name)
        paths.append(path)

    old = json.loads((r/"REPORT.json").read_text())
    for key, value in {
        "status": "PASS",
        "experiment": "TWELVE-CIRCUIT-FAMILIES-004",
        "source_sha256": expected,
        "source_unchanged": True,
        "simple_orbit_union_count": 32640,
        "weighted_embeddings_distinct": 44800,
        "constructed_union_count": 77440,
        "weighted_absolute_coefficient_pattern":
            [[1,7], [2,4], [3,1]],
    }.items():
        need(old.get(key) == value,
             "FAMILIES-004 receipt mismatch: " + key)

    need((r/"exit.txt").read_text().strip() == "0",
         "FAMILIES-004 exit status mismatch")

    return {
        str(path): sha(path.read_bytes()) for path in paths
    }

def audit(report, output):
    need(rank_q([[1,0], [0,1]]) == 2, "Independent rank control")
    need(rank_q([[1,2], [2,4]]) == 1, "Dependent rank control")

    terms = (
        [()] + [(i,) for i in range(5)]
        + list(it.combinations(range(5), 2))
    )
    masks = [
        sum(
            int(all((x >> i) & 1 for i in term)) << x
            for x in range(32)
        )
        for term in terms
    ]

    need(binary_rank(masks) == 16, "Binary feature rank mismatch")
    need(
        all((a & b).bit_count() % 2 == 0
            for a in masks for b in masks),
        "Binary self-orthogonality failed",
    )

    word = 0
    weights = Counter({0: 1})
    candidates = set()

    for index in range(1, 1 << 16):
        word ^= masks[(index & -index).bit_length()-1]
        weight = word.bit_count()
        weights[weight] += 1
        if weight == 12:
            candidates.add(tuple(
                x for x in range(32) if (word >> x) & 1
            ))

    need(sum(weights.values()) == 65536, "Enumeration total")
    report.update({
        "binary_codewords_enumerated": 65536,
        "binary_rank": 16,
        "binary_self_duality_verified": True,
        "binary_weight_enumerator": dict(sorted(weights.items())),
        "five_bit_weight_twelve_supports": len(candidates),
    })

    print("FIVE-BIT WEIGHT-TWELVE SUPPORTS:", len(candidates),
          flush=True)

    rows5 = [features(x, 5) for x in range(32)]
    maps5 = coordinate_maps(5)
    remaining = set(candidates)
    covered = set()
    seeds = []
    records5 = []
    count5 = 0

    while remaining:
        support = min(remaining)
        family = orbit(support, maps5, 5)
        need(family <= candidates and not (family & covered),
             "Five-bit orbit partition failure")
        covered.update(family)
        remaining.difference_update(family)

        totals = [
            sum(rows5[x][j] for x in support)
            for j in range(16)
        ]
        signings = []

        for chosen in it.combinations(range(1, 12), 5):
            positive = (0,) + chosen
            if all(
                2*sum(rows5[support[i]][j] for i in positive)
                == totals[j]
                for j in range(16)
            ):
                pos = set(positive)
                signings.append([
                    1 if i in pos else -1 for i in range(12)
                ])

        rq = rank_q([rows5[x] for x in support])

        if signings:
            need(rq == 11 and len(signings) == 1,
                 "Splittable support requires noncircuit analysis")
            coefficients = signings[0]
            need(identity(support, coefficients, 5),
                 "Five-bit kernel identity failed")
            need(all(
                rank_q([
                    rows5[x] for j,x in enumerate(support)
                    if j != i
                ]) == 11
                for i in range(12)
            ), "Five-bit deletion independence failed")

            bad = coefficients[:]
            bad[0] += 1
            bad[1] -= 1
            need(not identity(support, bad, 5),
                 "Corrupted-kernel control failed")

            seeds.append((support, coefficients))
            count5 += len(family)

        records5.append({
            "support": support,
            "orbit_size": len(family),
            "rank_Q": rq,
            "signings_up_to_global_sign": len(signings),
            "primitive_kernel": signings[0] if signings else None,
        })

        print(
            "FIVE-BIT ORBIT:", len(records5),
            "SIZE:", len(family),
            "SIGNINGS:", len(signings),
            "RANK:", rq,
            flush=True,
        )

    need(covered == candidates, "Incomplete five-bit coverage")

    maps6 = coordinate_maps(6)
    supports6 = set()
    records6 = []
    extensions = []

    for number, (support, coefficients) in enumerate(seeds, 1):
        accepted = 0

        for mask in range(1 << 12):
            selected = [
                i for i in range(12) if (mask >> i) & 1
            ]
            if any(
                sum(coefficients[i]*rows5[support[i]][j]
                    for i in selected)
                for j in range(6)
            ):
                continue

            accepted += 1
            pairs = sorted(
                (x | (((mask >> i) & 1) << 5), coefficients[i])
                for i,x in enumerate(support)
            )
            lifted = tuple(x for x,c in pairs)
            kernel = [c for x,c in pairs]
            need(identity(lifted, kernel, 6),
                 "Six-bit extension identity failed")

            if lifted in supports6:
                continue

            need(rank_q([features(x,6) for x in lifted]) == 11,
                 "Six-bit representative rank failed")
            family = orbit(lifted, maps6, 6)
            need(not (family & supports6),
                 "Overlapping six-bit orbits")
            supports6.update(family)

            records6.append({
                "support": lifted,
                "primitive_kernel": kernel,
                "rank_Q": 11,
                "orbit_size": len(family),
                "orbit_sha256": support_digest(family),
            })

        extensions.append({
            "seed_support": support,
            "assignments_tested": 4096,
            "accepted_assignments": accepted,
        })

        print(
            "EXTENDED SEED:", number,
            "ACCEPTED:", accepted,
            "SIX-BIT ORBITS:", len(records6),
            "SUPPORTS:", len(supports6),
            flush=True,
        )

    old_witnesses = [
        [2,3,6,7,32,34,36,38,57,58,61,62],
        [2,10,22,25,27,28,32,40,49,51,54,60],
        [0,1,7,15,16,25,38,47,49,54,55,57],
        [20,21,22,23,24,26,29,31,32,34,36,38],
    ]
    previous_simple = set()
    for support in old_witnesses:
        previous_simple.update(orbit(support, maps6, 6))

    need(len(previous_simple) == 32640,
         "Previous simple-family count mismatch")
    need(
        support_digest(previous_simple)
        == "8e9f818c173de93553aac9195c920ab91310a6d2f11f39b2754e80da3046fba6",
        "Previous simple-family digest mismatch",
    )
    need(previous_simple <= supports6,
         "Previous family not contained")

    report.update({
        "five_bit_binary_support_orbits": len(records5),
        "balanced_signings_tested_per_orbit": 462,
        "five_bit_simple_circuit_orbits": len(seeds),
        "five_bit_simple_circuit_supports": count5,
        "five_bit_simple_circuit_census_exhaustive": True,
        "extension_assignments_tested": 4096*len(seeds),
        "accepted_extension_assignments":
            sum(r["accepted_assignments"] for r in extensions),
        "six_bit_simple_orbits_generated": len(records6),
        "six_bit_simple_supports_generated": len(supports6),
        "six_bit_simple_supports_sha256":
            support_digest(supports6),
        "additional_simple_supports":
            len(supports6-previous_simple),
        "prior_simple_family_contained": True,
        "all_new_orbit_representatives_exact_rank_checked": True,
        "all_generated_supports_individually_rank_checked": False,
        "weighted_family_reenumerated": False,
        "complete_six_bit_twelve_circuit_census": False,
        "global_simple_completeness_claimed_by_program": False,
        "novelty_claim": False,
        "combined_lower_bound_using_retained_weighted_family":
            len(supports6)+44800,
        "weighted_disjointness_basis":
            "Rank-eleven supports have a unique primitive kernel "
            "up to sign. Unit coefficients differ from pattern "
            "1^7,2^4,3^1.",
    })

    (output/"ORBIT-CATALOG.json").write_text(
        json.dumps({
            "five_bit_orbits": records5,
            "extensions": extensions,
            "six_bit_simple_orbits": records6,
        }, indent=2) + "\n"
    )

def main():
    started = time.monotonic()
    source = Path(__file__).resolve()
    original = source.read_bytes()
    output = Path(sys.argv[1]).resolve()
    base = Path(sys.argv[2]).resolve()

    report = {
        "experiment": "SIMPLE-TWELVE-EXTENSIONS-005",
        "status": "RUNNING",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": sha(original),
        "python_version": sys.version,
        "scope":
            "Exhaustive five-bit unitrade-support and balanced-signing "
            "census; all one-coordinate extensions of simple circuit "
            "representatives; full cube orbits of constructed six-bit "
            "supports. Not a complete weighted six-bit census.",
    }

    try:
        bindings = bind_previous(base)
        report["historical_input_sha256"] = bindings
        audit(report, output)

        for name, digest in bindings.items():
            need(sha(Path(name).read_bytes()) == digest,
                 "Historical input changed: " + name)

        need(source.read_bytes() == original, "Source changed")
        report["historical_inputs_unchanged"] = True
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
