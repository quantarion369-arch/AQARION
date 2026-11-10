#!/usr/bin/env python3
import hashlib
import itertools
import json
import math
import sys
import time
import traceback
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

OUT = Path(sys.argv[1]).resolve()
START = time.monotonic()
SOURCE = Path(__file__).read_bytes()

REPORT = {
    "experiment": "INDEPENDENT_ODD12_FIVEBIT_STAGE1",
    "status": "RUNNING",
    "started_utc": datetime.now(timezone.utc).isoformat(),
    "source_sha256": hashlib.sha256(SOURCE).hexdigest(),
    "python": sys.version,
    "method": (
        "Direct codeword-span enumeration and individual "
        "integer-elimination ranks; no symmetry-orbit reduction"
    ),
    "sixbit_sector_verified": False,
    "full_census_verified": False,
    "promotion": False,
}

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def eliminate(rows):
    a = [list(map(int, row)) for row in rows]
    need(bool(a) and bool(a[0]), "Empty matrix")
    width = len(a[0])
    need(all(len(row) == width for row in a), "Ragged matrix")
    pivots = []

    for col in range(width):
        r = len(pivots)
        found = next(
            (i for i in range(r, len(a)) if a[i][col]),
            None,
        )
        if found is None:
            continue

        a[r], a[found] = a[found], a[r]

        for i in range(r + 1, len(a)):
            if not a[i][col]:
                continue

            u, v = a[r][col], a[i][col]
            common = math.gcd(u, v)
            a[i] = [
                (u // common) * x - (v // common) * y
                for x, y in zip(a[i], a[r])
            ]

            divisor = math.gcd(*a[i])
            if divisor:
                a[i] = [x // divisor for x in a[i]]

        pivots.append(col)
        if len(pivots) == len(a):
            break

    return a, pivots

def kernel(upper, pivots):
    free = next(j for j in range(12) if j not in pivots)
    vector = [Fraction(0)] * 12
    vector[free] = Fraction(1)

    for i in reversed(range(len(pivots))):
        col = pivots[i]
        vector[col] = -sum(
            upper[i][j] * vector[j]
            for j in range(col + 1, 12)
        ) / upper[i][col]

    denominator = math.lcm(*(v.denominator for v in vector))
    vector = [int(v * denominator) for v in vector]
    divisor = math.gcd(*vector)
    need(divisor != 0, "Zero kernel")
    vector = [v // divisor for v in vector]

    if next(v for v in vector if v) < 0:
        vector = [-v for v in vector]

    return vector

exit_code = 2

try:
    need(len(eliminate([[0, 1], [1, 0]])[1]) == 2,
         "Row-swap control failed")
    need(len(eliminate([[1, 2, 3], [2, 4, 6]])[1]) == 1,
         "Dependent-row control failed")
    need(len(eliminate([[0, 0], [0, 0]])[1]) == 0,
         "Zero-matrix control failed")

    # Evaluations of all multilinear monomials of degree <= 2.
    features = [[1] * 32]
    features += [
        [(x >> i) & 1 for x in range(32)]
        for i in range(5)
    ]
    features += [
        [((x >> i) & 1) * ((x >> j) & 1)
         for x in range(32)]
        for i, j in itertools.combinations(range(5), 2)
    ]
    need(len(features) == 16, "Incorrect feature count")

    masks = [
        sum(value << x for x, value in enumerate(row))
        for row in features
    ]

    # Build the binary span by repeated doubling, not Gray-code traversal.
    words = [0]
    for mask in masks:
        words += [word ^ mask for word in words]

    need(len(words) == 65536, "Wrong codeword count")
    need(len(set(words)) == 65536, "Binary generators are dependent")

    weights = Counter(word.bit_count() for word in words)
    candidates = sorted(
        tuple(x for x in range(32) if (word >> x) & 1)
        for word in words
        if word.bit_count() == 12
    )
    need(len(candidates) == 13888, "Unexpected candidate count")
    need(len(set(candidates)) == 13888, "Duplicate candidates")

    print("CODEWORDS:", len(words), flush=True)
    print("WEIGHT-TWELVE CANDIDATES:", len(candidates), flush=True)
    print("RANKING EVERY CANDIDATE DIRECTLY", flush=True)

    ranks = Counter()
    patterns = Counter()
    support_digest = hashlib.sha256()
    accepted = 0

    with (
        (OUT / "ALL-CANDIDATE-DECISIONS.jsonl").open("w") as decisions,
        (OUT / "RANK11-KERNELS.jsonl").open("w") as certificates,
    ):
        for number, support in enumerate(candidates, 1):
            rows = [
                [row[x] for x in support]
                for row in features
            ]
            upper, pivots = eliminate(rows)
            rank = len(pivots)
            ranks[rank] += 1
            need(rank in (11, 12), "Unexpected candidate rank")

            decision = {
                "support": support,
                "rank_Q": rank,
            }

            if rank == 11:
                vector = kernel(upper, pivots)

                need(
                    all(v != 0 and v % 2 != 0 for v in vector),
                    "Kernel is not full-support and all-odd",
                )
                need(
                    all(
                        sum(
                            row[x] * coefficient
                            for x, coefficient in zip(support, vector)
                        ) == 0
                        for row in features
                    ),
                    "Exact kernel identity failed",
                )

                counts = Counter(map(abs, vector))
                pattern = " ".join(
                    f"{v}^{counts[v]}" for v in sorted(counts)
                )
                patterns[pattern] += 1
                accepted += 1
                support_digest.update(bytes(support))

                certificates.write(json.dumps({
                    "support": support,
                    "rank_Q": 11,
                    "primitive_kernel": vector,
                    "pattern": pattern,
                    "all_coefficients_odd": True,
                }) + "\n")

            decisions.write(json.dumps(decision) + "\n")

            if number % 1000 == 0:
                print(
                    "CHECKED:", number,
                    "RANK11:", ranks[11],
                    "RANK12:", ranks[12],
                    flush=True,
                )

    need(dict(ranks) == {11: 3808, 12: 10080},
         "Rank counts disagree with reference target")
    need(accepted == 3808, "Wrong accepted-kernel count")
    need(Path(__file__).read_bytes() == SOURCE,
         "Verifier source changed during execution")

    REPORT.update({
        "status": "PASS_FOR_FIVEBIT_CANDIDATE_LAYER",
        "distinct_codewords": len(words),
        "codeword_weight_distribution": dict(weights),
        "weight_twelve_candidates": len(candidates),
        "exact_rank_counts": dict(ranks),
        "full_support_all_odd_kernels": accepted,
        "rank11_pattern_counts": dict(patterns),
        "rank11_support_digest": support_digest.hexdigest(),
        "support_digest_format": (
            "SHA256 of concatenated 12-byte supports, "
            "each internally sorted, supports in lexicographic order"
        ),
        "limitations": [
            "Does not yet lift candidates to all six-bit hyperplanes.",
            "Does not yet compare full support sets with historical outputs.",
            "Does not establish the six-bit count 210336.",
            "Does not prove the classical binary-support coverage theorem.",
        ],
    })
    exit_code = 0

except Exception:
    REPORT["status"] = "FAIL_OR_BLOCKED"
    REPORT["error"] = traceback.format_exc()
    print(REPORT["error"], flush=True)

finally:
    REPORT["elapsed_seconds"] = round(time.monotonic() - START, 3)
    REPORT["finished_utc"] = datetime.now(timezone.utc).isoformat()
    (OUT / "REPORT.json").write_text(
        json.dumps(REPORT, indent=2) + "\n"
    )
    (OUT / "SHA256SUMS").write_text(
        "".join(
            hashlib.sha256(path.read_bytes()).hexdigest()
            + "  " + path.name + "\n"
            for path in sorted(OUT.iterdir())
            if path.is_file() and path.name != "SHA256SUMS"
        )
    )

print("\n=== FINAL ===")
print("STATUS:", REPORT["status"])
print("EXACT RANK COUNTS:", REPORT.get("exact_rank_counts"))
print("ALL-ODD KERNELS:", REPORT.get("full_support_all_odd_kernels"))
print("SIX-BIT SECTOR VERIFIED: FALSE")
print("RESULTS:", OUT)
print("NO STAGING, COMMIT, PUSH, OR PR")
print("PROMOTION: FALSE")
sys.exit(exit_code)
