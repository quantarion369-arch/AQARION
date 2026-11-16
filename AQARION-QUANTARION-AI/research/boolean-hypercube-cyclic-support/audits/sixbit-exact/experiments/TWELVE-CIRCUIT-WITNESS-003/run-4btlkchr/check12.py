#!/usr/bin/env python3
"""Exact twelve-point circuit and affine-flat-free witness check."""

import hashlib
import itertools
import json
import math
import sys
import tempfile
import time
import traceback
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

SOURCE = Path(__file__).resolve()

SUPPORT = [20, 21, 22, 23, 24, 26, 29, 31, 32, 34, 36, 38]
COEFFICIENTS = [1, -1, -1, 1, -1, 1, 1, -1, 1, -1, -1, 1]

def need(condition, message):
    if not condition:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def features(x):
    bits = [(x >> i) & 1 for i in range(6)]
    return (
        [1] + bits
        + [bits[i] * bits[j]
           for i, j in itertools.combinations(range(6), 2)]
    )

def rank_q(rows):
    a = [[Fraction(v) for v in row] for row in rows]
    rank = 0

    for col in range(22):
        pivot = next(
            (i for i in range(rank, len(a)) if a[i][col]),
            None,
        )
        if pivot is None:
            continue

        a[rank], a[pivot] = a[pivot], a[rank]
        value = a[rank][col]
        a[rank] = [v / value for v in a[rank]]

        for i in range(rank + 1, len(a)):
            factor = a[i][col]
            if factor:
                a[i] = [
                    x - factor * y
                    for x, y in zip(a[i], a[rank])
                ]

        rank += 1
        if rank == len(a):
            break

    return rank

def affine_three_flat(points):
    origin = min(points)
    differences = {x ^ origin for x in points}
    return (
        len(differences) == 8
        and 0 in differences
        and all(a ^ b in differences
                for a in differences for b in differences)
    )

def check(report):
    need(
        SUPPORT == sorted(set(SUPPORT))
        and len(SUPPORT) == 12
        and all(0 <= x < 64 for x in SUPPORT),
        "Invalid twelve-point support",
    )
    need(len(COEFFICIENTS) == 12 and all(COEFFICIENTS),
         "Invalid kernel coefficients")
    need(math.gcd(*COEFFICIENTS) == 1, "Kernel is not primitive")

    rows = [features(x) for x in SUPPORT]
    need(all(len(row) == 22 for row in rows),
         "Feature count mismatch")

    sums = [
        sum(c * row[j] for c, row in zip(COEFFICIENTS, rows))
        for j in range(22)
    ]
    need(sums == [0] * 22, "Exact kernel identity failed")

    corrupted = COEFFICIENTS[:]
    corrupted[0] += 1
    need(any(
        sum(c * row[j] for c, row in zip(corrupted, rows))
        for j in range(22)
    ), "Corrupted-kernel rejection control failed")

    rank = rank_q(rows)
    need(rank == 11, "Support rank is not eleven")

    deletion_ranks = {}
    for i, point in enumerate(SUPPORT):
        deletion_rank = rank_q(rows[:i] + rows[i + 1:])
        deletion_ranks[str(point)] = deletion_rank
        need(deletion_rank == 11,
             "Dependent deletion after removing " + str(point))
        print("INDEPENDENT DELETION:", point, flush=True)

    flats = []
    tested = 0
    for subset in itertools.combinations(SUPPORT, 8):
        tested += 1
        if affine_three_flat(subset):
            flats.append(list(subset))

    need(tested == math.comb(12, 8), "Subset coverage mismatch")
    need(not flats, "Support contains an affine 3-flat")

    report.update({
        "support": SUPPORT,
        "primitive_integer_kernel": COEFFICIENTS,
        "feature_sums": sums,
        "rational_rank": rank,
        "deletion_ranks": deletion_ranks,
        "all_eleven_point_deletions_independent": True,
        "corrupted_kernel_rejected": True,
        "eight_point_subsets_tested": tested,
        "affine_three_flats_contained": flats,
        "is_twelve_point_rational_circuit": True,
        "contains_no_affine_three_flat": True,
    })

def main():
    started = time.monotonic()
    source = SOURCE.read_bytes()
    run = Path(tempfile.mkdtemp(prefix="run-", dir=SOURCE.parent))
    (run / "check12.py").write_bytes(source)

    report = {
        "experiment": "TWELVE-CIRCUIT-WITNESS-003",
        "status": "RUNNING",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": sha(source),
        "python_version": sys.version,
        "scope": (
            "Exact certification of one twelve-point rational circuit "
            "containing no affine 3-flat. Not an enumeration of all "
            "twelve-point circuits, an orbit classification, or a "
            "novelty claim."
        ),
    }

    print("RETAINED:", run, flush=True)

    try:
        check(report)
        need(SOURCE.read_bytes() == source, "Source changed")
        report["source_unchanged"] = True
        report["status"] = "PASS"
    except Exception as exc:
        report["status"] = "ERROR"
        report["error"] = type(exc).__name__ + ": " + str(exc)
        (run / "traceback.txt").write_text(traceback.format_exc())

    report["finished_utc"] = datetime.now(timezone.utc).isoformat()
    report["elapsed_seconds"] = round(time.monotonic() - started, 6)

    (run / "WITNESS-REPORT.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )

    files = sorted(p for p in run.iterdir() if p.is_file())
    (run / "SHA256SUMS").write_text("".join(
        sha(p.read_bytes()) + "  " + p.name + "\n"
        for p in files
    ))

    print(json.dumps(report, indent=2, sort_keys=True), flush=True)
    print("RETAINED:", run, flush=True)
    return 0 if report["status"] == "PASS" else 2

if __name__ == "__main__":
    raise SystemExit(main())
