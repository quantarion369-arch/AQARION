#!/usr/bin/env python3
"""Independent six-bit direction/coset/direct modular-rank audit."""

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

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
PRIME = 2147483629

PINS = {
    "flat_census.json":
        "5e684e0152d240534632a9c0dc4916727c5b80e4baa5243727098a0710a1e161",
    "run_receipt.json":
        "745b853be897690264271064d05deb5bea3032c4ae0c85b033be542dc2c0fd12",
    "sixbit_flats.py":
        "700d2b036c8cf3617f26f4e97bcdc52fa00ad648514426598b948d38aea6d5b5",
}

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def integer(value):
    return type(value) is int

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def utc():
    return datetime.now(timezone.utc).isoformat()

def prime_by_trial_division(p):
    if p < 2:
        return False
    if p % 2 == 0:
        return p == 2
    return all(
        p % d != 0
        for d in range(3, math.isqrt(p) + 1, 2)
    )

def independent_rref_bases():
    """Enumerate RREF matrices by pivot/free-column assignments."""
    result = []

    for pivots in itertools.combinations(range(6), 3):
        slots = [
            (i, j)
            for i in range(3)
            for j in range(pivots[i] + 1, 6)
            if j not in pivots
        ]

        for mask in range(1 << len(slots)):
            basis = [1 << p for p in pivots]

            for k, (i, j) in enumerate(slots):
                basis[i] |= ((mask >> k) & 1) << j

            result.append(tuple(basis))

    return sorted(result)

def span(basis):
    return tuple(sorted(
        (a * basis[0]) ^ (b * basis[1]) ^ (c * basis[2])
        for a, b, c in itertools.product((0, 1), repeat=3)
    ))

def cosets(direction):
    remaining = set(range(64))
    result = []

    while remaining:
        representative = min(remaining)
        points = tuple(sorted(
            representative ^ x for x in direction
        ))

        require(
            len(points) == 8
            and set(points).issubset(remaining),
            "Independent coset construction failed",
        )

        result.append((representative, points))
        remaining.difference_update(points)

    require(len(result) == 8, "Independent coset count failed")
    return result

def feature_row(x):
    bits = [(x >> i) & 1 for i in range(6)]
    return (
        [1]
        + bits
        + [
            bits[i] * bits[j]
            for i in range(6)
            for j in range(i + 1, 6)
        ]
    )

def character_rank(basis):
    signatures = [
        sum(((v >> i) & 1) << j
            for j, v in enumerate(basis))
        for i in range(6)
    ]

    characters = {0}
    characters.update(signatures)
    characters.update(
        signatures[i] ^ signatures[j]
        for i in range(6)
        for j in range(i + 1, 6)
    )
    return len(characters)

def rank_mod(rows):
    """Direct modular elimination; Python integers do not overflow."""
    a = [[v % PRIME for v in row] for row in rows]
    height = len(a)
    width = len(a[0])
    rank = 0

    for col in range(width):
        pivot = next(
            (
                i for i in range(rank, height)
                if a[i][col] != 0
            ),
            None,
        )

        if pivot is None:
            continue

        a[rank], a[pivot] = a[pivot], a[rank]
        inverse = pow(a[rank][col], -1, PRIME)

        for j in range(col, width):
            a[rank][j] = a[rank][j] * inverse % PRIME

        for i in range(rank + 1, height):
            factor = a[i][col]
            if factor:
                for j in range(col, width):
                    a[i][j] = (
                        a[i][j] - factor * a[rank][j]
                    ) % PRIME

        rank += 1
        if rank == height:
            break

    return rank

def check_count_fields(obj, expected):
    for key, value in expected.items():
        require(
            integer(obj.get(key)) and obj[key] == value,
            "Count/metadata mismatch: " + key,
        )

def audit(report):
    for name, expected in PINS.items():
        path = BASE / name
        require(path.is_file(), "Missing input: " + name)
        require(sha(path) == expected, "Input hash mismatch: " + name)

    report["input_sha256"] = dict(PINS)

    require(
        prime_by_trial_division(PRIME),
        "Modulus failed independent primality test",
    )

    census = json.loads((BASE / "flat_census.json").read_text())
    receipt = json.loads((BASE / "run_receipt.json").read_text())

    check_count_fields(census, {
        "dimension": 6,
        "point_count": 64,
        "flat_dimension": 3,
        "flat_size": 8,
        "feature_count": 22,
        "direction_count": 1395,
        "flat_count": 11160,
        "rank_eight_target": 8360,
        "rank_eight_observed": 8360,
        "modular_rank_exception_count": 0,
    })

    require(census.get("field") == "Q", "Wrong rational field")
    require(
        census.get("modular_field") == f"F_{PRIME}",
        "Wrong modular field",
    )
    require(
        census.get("bit_convention") == "x_i = (x >> i) & 1",
        "Wrong bit convention",
    )
    require(
        census.get("rank_eight_target_match") is True,
        "Census target-match flag",
    )
    require(
        census.get("modular_rank_exception_flat_ids") == [],
        "Census exception IDs",
    )

    check_count_fields(receipt, {
        "prime": PRIME,
        "point_count": 64,
        "expected_direction_count": 1395,
        "observed_direction_count": 1395,
        "expected_flat_count": 11160,
        "observed_flat_count": 11160,
        "rank_eight_target": 8360,
        "rank_eight_observed": 8360,
        "modular_rank_exception_count": 0,
    })

    require(
        receipt.get("status") == "COMPUTATION_COMPLETE",
        "Receipt status",
    )
    require(receipt.get("prime_verified") is True, "Receipt prime flag")
    require(receipt.get("geometry_gate") == "PASS", "Receipt geometry gate")
    require(receipt.get("rank_eight_gate") == "PASS", "Receipt rank gate")
    require(
        receipt.get("rank_eight_target_match") is True,
        "Receipt target-match flag",
    )
    require(
        receipt.get("flat_census_sha256") == PINS["flat_census.json"],
        "Receipt census binding",
    )
    require(
        receipt.get("script_sha256") == PINS["sixbit_flats.py"],
        "Receipt generator binding",
    )

    records = census.get("flats")
    require(isinstance(records, list), "Census flats is not a list")
    require(len(records) == 11160, "Wrong record count")

    bases = independent_rref_bases()
    require(len(bases) == 1395, "Independent direction count")

    direction_spans = {span(basis) for basis in bases}
    require(len(direction_spans) == 1395, "Repeated direction spans")

    expected = {}
    flat_id = 0

    for direction_id, basis in enumerate(bases):
        direction = span(basis)
        rank_q = character_rank(basis)

        require(rank_q in (7, 8), "Unexpected character rank")

        for representative, points in cosets(direction):
            expected[points] = (
                flat_id, direction_id, basis, representative, rank_q
            )
            flat_id += 1

    require(len(expected) == 11160, "Independent flat count")

    seen = set()
    directions_seen = Counter()
    modular_counts = Counter()
    rational_counts = Counter()

    for number, rec in enumerate(records, 1):
        require(isinstance(rec, dict), "Invalid flat record")
        points_list = rec.get("points")

        require(
            isinstance(points_list, list)
            and len(points_list) == 8
            and all(integer(x) and 0 <= x < 64 for x in points_list),
            "Invalid point list",
        )

        points = tuple(points_list)
        require(
            points == tuple(sorted(set(points))),
            "Noncanonical or repeated flat points",
        )
        require(points in expected, "Unexpected affine flat")
        require(points not in seen, "Duplicate affine flat")
        seen.add(points)

        fid, did, basis, representative, rank_q = expected[points]

        for key, value in (
            ("flat_id", fid),
            ("direction_id", did),
            ("coset_representative", representative),
        ):
            require(
                integer(rec.get(key)) and rec[key] == value,
                "Incorrect flat metadata: " + key,
            )

        recorded_basis = rec.get("direction_rref")
        require(
            isinstance(recorded_basis, list)
            and all(integer(x) for x in recorded_basis)
            and recorded_basis == list(basis),
            "Incorrect canonical direction RREF",
        )

        actual_direction = tuple(sorted(
            x ^ points[0] for x in points
        ))
        require(
            actual_direction == span(basis),
            "Point geometry and direction disagree",
        )
        require(
            representative == min(points),
            "Noncanonical coset representative",
        )

        rank_fp = rank_mod([feature_row(x) for x in points])

        require(
            integer(rec.get("rank_Q"))
            and rec["rank_Q"] == rank_q,
            "Recorded rational rank mismatch",
        )
        require(
            integer(rec.get("rank_Fp"))
            and rec["rank_Fp"] == rank_fp,
            "Recorded modular rank mismatch",
        )
        require(
            rank_fp == rank_q,
            "Direct modular and character ranks disagree",
        )
        require(
            rec.get("modular_rank_exception") is False,
            "Incorrect modular exception flag",
        )

        directions_seen[did] += 1
        rational_counts[rank_q] += 1
        modular_counts[rank_fp] += 1

        if number % 1000 == 0:
            print("CHECKED:", number, "flats", flush=True)

    require(seen == set(expected), "Incomplete flat coverage")
    require(
        directions_seen == Counter({i: 8 for i in range(1395)}),
        "Direction/coset multiplicity mismatch",
    )

    distribution = {"7": 2800, "8": 8360}

    for obj in (census, receipt):
        for field in ("rank_Q_distribution", "rank_Fp_distribution"):
            require(
                obj.get(field) == distribution,
                "Distribution mismatch: " + field,
            )

    require(
        dict(rational_counts) == {7: 2800, 8: 8360},
        "Independent rational distribution mismatch",
    )
    require(
        dict(modular_counts) == {7: 2800, 8: 8360},
        "Independent modular distribution mismatch",
    )

    for name, digest in PINS.items():
        require(sha(BASE / name) == digest, "Input changed: " + name)

    report.update({
        "directions_checked": 1395,
        "affine_flats_checked": 11160,
        "direct_modular_rank_checks": 11160,
        "rational_rank_method": "Independent Walsh character count",
        "modular_rank_method": "Direct Gaussian elimination",
        "prime": PRIME,
        "prime_test": "Trial division through integer square root",
        "canonical_direction_ids_verified": True,
        "canonical_direction_rrefs_verified": True,
        "canonical_coset_representatives_verified": True,
        "eight_cosets_per_direction_verified": True,
        "rank_distribution": distribution,
        "inputs_unchanged": True,
        "status": "PASS",
    })

def main():
    started = time.monotonic()
    run = Path(tempfile.mkdtemp(prefix="run-", dir=HERE))

    report = {
        "gate": "SIXBIT-VERIFY-005",
        "status": "RUNNING",
        "started_utc": utc(),
        "source_sha256": sha(Path(__file__).resolve()),
        "python_version": sys.version,
        "scope": (
            "Independent RREF-pivot enumeration, exact canonical "
            "direction/coset reconciliation and direct finite-field "
            "rank checks. No circuit search, mutation suite, formal "
            "proof, or global circuit-completeness claim."
        ),
    }

    print("RESULT DIRECTORY:", run, flush=True)

    try:
        audit(report)
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

    (run / "SHA256SUMS").write_text(
        sha(target) + "  " + target.name + "\n"
    )

    print(json.dumps(report, indent=2, sort_keys=True), flush=True)
    print("REPORT:", target, flush=True)

    return 0 if report["status"] == "PASS" else 2

if __name__ == "__main__":
    raise SystemExit(main())
