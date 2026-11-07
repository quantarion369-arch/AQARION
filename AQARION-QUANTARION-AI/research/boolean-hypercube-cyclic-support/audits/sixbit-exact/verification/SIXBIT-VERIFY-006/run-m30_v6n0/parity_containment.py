#!/usr/bin/env python3
"""Independent finite parity lemmas for six-bit quadratic circuits."""

import hashlib
import itertools
import json
import math
import sys
import tempfile
import time
import traceback
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

SOURCE = Path(__file__).resolve()
HERE = SOURCE.parent

PROOF = """# Six-bit ten-point circuit containment

Feature row:
v(x) = (1, x_i, x_i*x_j for i<j), for x in {0,1}^6.

Let S be a ten-point rational circuit. Clear denominators in its
dependence and divide by the coefficient gcd. This gives a primitive
integer dependence c, with every coefficient on S nonzero.

Reduce c modulo two. The resulting binary vector b is nonzero by
primitivity and is orthogonal to every degree-at-most-two feature.

The finite checks in this run establish:
1. Every nonzero such binary vector supported on at most ten points
   has weight eight.
2. Every weight-eight such vector is an affine 3-flat incidence vector.

Thus the odd coefficients of c identify an eight-point affine 3-flat
F contained in S. Since S is a rational circuit, every proper subset
is independent, so the eight feature rows indexed by F have rank eight.

Uniqueness: two distinct affine 3-flats have intersection size at most
four, hence union size at least twelve. A ten-point support cannot
contain two of them.

Scope:
This proves containment from the checked finite parity lemmas and
elementary rational circuit properties. This run does not enumerate
rational ten-point circuits, rerun VERIFY-002, or independently certify
the global count 22400. That count requires the separate exhaustive
construction-family certificate and its verification.

Reference for the MacWilliams identity and Reed-Muller background:
https://people.math.harvard.edu/~elkies/M256.13/index.html
"""

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def utc():
    return datetime.now(timezone.utc).isoformat()

def binary_rank(vectors):
    pivots = {}
    for value in vectors:
        while value:
            pivot = value.bit_length() - 1
            if pivot in pivots:
                value ^= pivots[pivot]
            else:
                pivots[pivot] = value
                break
    return len(pivots)

def krawtchouk(j, weight):
    return sum(
        (-1) ** a
        * math.comb(weight, a)
        * math.comb(64 - weight, j - a)
        for a in range(
            max(0, j - (64 - weight)),
            min(j, weight) + 1,
        )
    )

def audit(report):
    terms = (
        [()]
        + [(i,) for i in range(6)]
        + list(itertools.combinations(range(6), 2))
    )
    masks = [
        sum(
            int(all((x >> i) & 1 for i in term)) << x
            for x in range(64)
        )
        for term in terms
    ]

    require(len(masks) == 22, "Feature count mismatch")
    require(binary_rank(masks) == 22, "Binary feature rank mismatch")
    report["binary_feature_rank"] = 22

    print("ENUMERATING: 4194304 binary codewords", flush=True)
    weights = Counter({0: 1})
    word = 0
    total = 1 << 22

    for index in range(1, total):
        changed = (index & -index).bit_length() - 1
        word ^= masks[changed]
        weights[word.bit_count()] += 1
        if index % (1 << 20) == 0:
            print("ENUMERATED:", index + 1, flush=True)

    require(sum(weights.values()) == total, "Enumeration count mismatch")
    require(weights[0] == 1, "Unexpected zero-word multiplicity")

    print("COMPUTING: exact dual weight enumerator", flush=True)
    dual = {}
    for j in range(65):
        numerator = sum(
            count * krawtchouk(j, weight)
            for weight, count in weights.items()
        )
        require(numerator % total == 0, "Nonintegral dual coefficient")
        coefficient = numerator // total
        require(coefficient >= 0, "Negative dual coefficient")
        dual[j] = coefficient

    require(dual[0] == 1, "Dual zero-word mismatch")
    require(sum(dual.values()) == 1 << 42, "Dual size mismatch")
    require(all(dual[j] == 0 for j in range(1, 8)),
            "Unexpected dual word below weight eight")
    require(dual[8] == 11160, "Weight-eight count mismatch")
    require(all(dual[j] == 0 for j in (9, 10, 11)),
            "Unexpected dual word of weight nine, ten, or eleven")

    print("ENUMERATING: independent affine 3-flats", flush=True)
    directions = set()
    for a, b, c in itertools.combinations(range(1, 64), 3):
        points = tuple(sorted({
            0, a, b, c, a ^ b, a ^ c, b ^ c, a ^ b ^ c
        }))
        if len(points) == 8:
            directions.add(points)

    require(len(directions) == 1395, "Direction count mismatch")
    flats = set()

    for direction in sorted(directions):
        remaining = set(range(64))
        coset_count = 0

        while remaining:
            representative = min(remaining)
            points = {representative ^ x for x in direction}
            require(len(points) == 8, "Coset size mismatch")
            require(points <= remaining, "Coset partition failure")
            remaining.difference_update(points)

            mask = sum(1 << x for x in points)
            require(mask.bit_count() == 8, "Flat weight mismatch")
            require(
                all((mask & feature).bit_count() % 2 == 0
                    for feature in masks),
                "Flat is not binary-orthogonal to the features",
            )
            require(mask not in flats, "Repeated affine flat")
            flats.add(mask)
            coset_count += 1

        require(coset_count == 8, "Coset count mismatch")

    require(len(flats) == 11160, "Affine-flat count mismatch")
    require(len(flats) == dual[8], "Weight-eight classification mismatch")

    report.update({
        "binary_codewords_enumerated": total,
        "binary_weight_enumerator": dict(sorted(weights.items())),
        "dual_weight_enumerator": dual,
        "directions_enumerated": len(directions),
        "affine_flats_enumerated": len(flats),
        "all_flats_binary_orthogonal": True,
        "weight_eight_supports_classified_by_count_equality": True,
        "dual_weights_one_through_seven_absent": True,
        "dual_weights_nine_ten_eleven_absent": True,
        "finite_parity_lemmas_verified": True,
    })

def main():
    started = time.monotonic()
    source_bytes = SOURCE.read_bytes()
    run = Path(tempfile.mkdtemp(prefix="run-", dir=HERE))
    (run / "parity_containment.py").write_bytes(source_bytes)

    report = {
        "gate": "SIXBIT-VERIFY-006-PARITY",
        "status": "RUNNING",
        "started_utc": utc(),
        "source_sha256": digest(source_bytes),
        "python_version": sys.version,
        "scope": (
            "Independent finite binary parity lemmas supporting "
            "ten-point rational circuit containment. No rational "
            "circuit enumeration, VERIFY-002 rerun, global-count "
            "execution certificate, or formal proof."
        ),
    }

    print("RETAINED DIRECTORY:", run, flush=True)

    try:
        audit(report)
        require(SOURCE.read_bytes() == source_bytes,
                "Source changed during execution")
        report["source_unchanged"] = True
        report["status"] = "PASS"
    except Exception as exc:
        report["status"] = "FAIL"
        report["error"] = type(exc).__name__ + ": " + str(exc)
        (run / "traceback.txt").write_text(traceback.format_exc())

    report["finished_utc"] = utc()
    report["elapsed_seconds"] = round(time.monotonic() - started, 6)

    target = run / (
        "PASS.json" if report["status"] == "PASS" else "FAIL.json"
    )
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    (run / "CONTAINMENT-ARGUMENT.md").write_text(PROOF)

    files = sorted(p for p in run.iterdir() if p.is_file())
    (run / "SHA256SUMS").write_text("".join(
        digest(p.read_bytes()) + "  " + p.name + "\n"
        for p in files
    ))

    summary = {
        key: value for key, value in report.items()
        if key not in ("binary_weight_enumerator", "dual_weight_enumerator")
    }
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)
    print("REPORT:", target, flush=True)
    print("RETAINED:", run, flush=True)
    return 0 if report["status"] == "PASS" else 2

if __name__ == "__main__":
    raise SystemExit(main())
