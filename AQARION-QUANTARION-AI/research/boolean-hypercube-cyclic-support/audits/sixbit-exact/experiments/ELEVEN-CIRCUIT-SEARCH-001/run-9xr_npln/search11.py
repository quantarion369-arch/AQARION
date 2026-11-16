#!/usr/bin/env python3
"""Seeded exploratory search for eleven-point rational circuits."""

import hashlib
import itertools
import json
import math
import random
import sys
import tempfile
import time
import traceback
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

SOURCE = Path(__file__).resolve()
PRIME = 2147483647
SEED = 6007001
DRAWS = 100000
SAMPLES_PER_FLAT = 50

ROWS = [
    [1]
    + [(x >> i) & 1 for i in range(6)]
    + [
        ((x >> i) & 1) * ((x >> j) & 1)
        for i, j in itertools.combinations(range(6), 2)
    ]
    for x in range(64)
]

def need(condition, message):
    if not condition:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def rank_mod(rows):
    a = [row[:] for row in rows]
    rank = 0
    for col in range(len(a[0])):
        pivot = next(
            (i for i in range(rank, len(a))
             if a[i][col] % PRIME),
            None,
        )
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inverse = pow(a[rank][col] % PRIME, -1, PRIME)
        a[rank] = [(v * inverse) % PRIME for v in a[rank]]
        for i in range(rank + 1, len(a)):
            factor = a[i][col] % PRIME
            if factor:
                a[i] = [
                    (x - factor * y) % PRIME
                    for x, y in zip(a[i], a[rank])
                ]
        rank += 1
        if rank == len(a):
            break
    return rank

def exact_test(support):
    a = [
        [Fraction(ROWS[x][j]) for x in support]
        for j in range(22)
    ]
    rank = 0
    pivots = []

    for col in range(11):
        pivot = next(
            (i for i in range(rank, 22) if a[i][col]),
            None,
        )
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        value = a[rank][col]
        a[rank] = [v / value for v in a[rank]]

        for i in range(22):
            if i != rank and a[i][col]:
                factor = a[i][col]
                a[i] = [
                    x - factor * y
                    for x, y in zip(a[i], a[rank])
                ]

        pivots.append(col)
        rank += 1

    if rank != 10:
        return "rational_rank_" + str(rank), None

    free = next(i for i in range(11) if i not in pivots)
    coefficients = [Fraction(0)] * 11
    coefficients[free] = Fraction(1)
    for row, pivot in enumerate(pivots):
        coefficients[pivot] = -a[row][free]

    if not all(coefficients):
        size = sum(v != 0 for v in coefficients)
        return "proper_dependent_support_" + str(size), None

    denominator = math.lcm(*(v.denominator for v in coefficients))
    coefficients = [int(v * denominator) for v in coefficients]
    divisor = math.gcd(*coefficients)
    coefficients = [v // divisor for v in coefficients]
    if coefficients[0] < 0:
        coefficients = [-v for v in coefficients]

    need(all(
        sum(c * ROWS[x][j]
            for x, c in zip(support, coefficients)) == 0
        for j in range(22)
    ), "Exact kernel identity failed")

    return "eleven_point_circuit", coefficients

def experiment(report):
    need(
        PRIME % 2 != 0 and all(
            PRIME % d for d in range(3, math.isqrt(PRIME) + 1, 2)
        ),
        "Modulus primality check failed",
    )

    rng = random.Random(SEED)
    seen = set()
    circuits = []
    rejection_counts = {}
    draws = 0
    candidates = 0
    flat_batches = 0

    while draws < DRAWS:
        a, b, c = rng.sample(range(1, 64), 3)
        direction = {
            0, a, b, c, a ^ b, a ^ c, b ^ c, a ^ b ^ c
        }
        if len(direction) != 8:
            continue

        shift = rng.randrange(64)
        flat = {x ^ shift for x in direction}
        if rank_mod([ROWS[x] for x in sorted(flat)]) != 8:
            continue

        flat_batches += 1
        outside = sorted(set(range(64)) - flat)

        for _ in range(min(SAMPLES_PER_FLAT, DRAWS - draws)):
            draws += 1
            support = tuple(sorted(
                flat | set(rng.sample(outside, 3))
            ))

            if support not in seen:
                seen.add(support)
                modular_rank = rank_mod([ROWS[x] for x in support])

                if modular_rank <= 10:
                    candidates += 1
                    outcome, coefficients = exact_test(support)

                    if coefficients is not None:
                        odd_support = [
                            x for x, value in zip(support, coefficients)
                            if value % 2
                        ]
                        need(set(odd_support) == flat,
                             "Circuit parity/flat consistency failed")

                        circuits.append({
                            "support": list(support),
                            "primitive_integer_kernel": coefficients,
                            "contained_affine_flat": sorted(flat),
                            "rational_rank": 10,
                            "all_kernel_coefficients_nonzero": True,
                            "exact_feature_identity_verified": True,
                        })
                        print(
                            "DISCOVERY:", len(circuits), support,
                            coefficients, flush=True,
                        )
                    else:
                        rejection_counts[outcome] = (
                            rejection_counts.get(outcome, 0) + 1
                        )

            if draws % 10000 == 0:
                print(
                    "DRAWS:", draws,
                    "UNIQUE:", len(seen),
                    "EXACT TESTS:", candidates,
                    "CIRCUITS:", len(circuits),
                    flush=True,
                )

    report.update({
        "draws_completed": draws,
        "unique_supports_tested": len(seen),
        "duplicate_draws": draws - len(seen),
        "rank_eight_flat_batches": flat_batches,
        "modular_candidates_exactly_tested": candidates,
        "exact_rejection_counts": rejection_counts,
        "distinct_circuits_found": len(circuits),
        "circuits": circuits,
        "exhaustive": False,
        "nonexistence_claim": False,
    })

def main():
    started = time.monotonic()
    source = SOURCE.read_bytes()
    run = Path(tempfile.mkdtemp(prefix="run-", dir=SOURCE.parent))
    (run / "search11.py").write_bytes(source)

    report = {
        "experiment": "ELEVEN-CIRCUIT-SEARCH-001",
        "status": "RUNNING",
        "seed": SEED,
        "requested_draws": DRAWS,
        "samples_per_flat": SAMPLES_PER_FLAT,
        "prime": PRIME,
        "source_sha256": sha(source),
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "scope": (
            "Seeded sampling of a rank-eight affine 3-flat plus "
            "three outside points; exact certification of discoveries. "
            "Not exhaustive and not a nonexistence proof."
        ),
    }

    print("RETAINED:", run, flush=True)
    try:
        experiment(report)
        need(SOURCE.read_bytes() == source, "Source changed")
        report["status"] = "COMPLETED"
        report["source_unchanged"] = True
    except Exception as exc:
        report["status"] = "ERROR"
        report["error"] = type(exc).__name__ + ": " + str(exc)
        (run / "traceback.txt").write_text(traceback.format_exc())

    report["finished_utc"] = datetime.now(timezone.utc).isoformat()
    report["elapsed_seconds"] = round(time.monotonic() - started, 6)
    (run / "SEARCH-REPORT.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )

    files = sorted(p for p in run.iterdir() if p.is_file())
    (run / "SHA256SUMS").write_text("".join(
        sha(p.read_bytes()) + "  " + p.name + "\n"
        for p in files
    ))

    summary = {k: v for k, v in report.items() if k != "circuits"}
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)
    print("RETAINED:", run, flush=True)
    return 0 if report["status"] == "COMPLETED" else 2

if __name__ == "__main__":
    raise SystemExit(main())
