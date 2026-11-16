#!/usr/bin/env python3
"""Exact symmetry-reduced eleven-point circuit exclusion.

Depends on retained VERIFY-006 parity lemmas. These force every
eleven-point rational circuit to contain a rank-eight affine 3-flat.

Coordinate permutations and bit complements preserve rational
degree-at-most-two features. Quotient by each representative flat:
zero residuals or proportional pairs give smaller dependencies.
Independence of every triple of distinct projective residuals then
excludes eleven-point circuits.

No random sampling, floating-point arithmetic, or modular filter.
"""

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
from fractions import Fraction
from pathlib import Path

SOURCE = Path(__file__).resolve()
BASE = SOURCE.parent.parent.parent
V6 = BASE / "verification/SIXBIT-VERIFY-006"
V6RUN = V6 / "run-m30_v6n0"
V6SHA = "3659c24a58c56b1998ce65a06e3aed52c6fc14989fecf6db85758cc46ccd84ee"

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

def utc():
    return datetime.now(timezone.utc).isoformat()

def rref(rows):
    a = [[Fraction(v) for v in row] for row in rows]
    pivots = []
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

        for i in range(len(a)):
            if i != rank and a[i][col]:
                factor = a[i][col]
                a[i] = [
                    x - factor * y
                    for x, y in zip(a[i], a[rank])
                ]

        pivots.append(col)
        rank += 1
        if rank == len(a):
            break

    return a[:rank], pivots

def primitive(vector):
    denominator = math.lcm(*(v.denominator for v in vector))
    values = [int(v * denominator) for v in vector]
    divisor = math.gcd(*values)
    need(divisor != 0, "Zero outside quotient residual")
    values = [v // divisor for v in values]

    if next(v for v in values if v) < 0:
        values = [-v for v in values]

    return tuple(values)

def quotient_groups(flat):
    reduced, pivots = rref([ROWS[x] for x in flat])
    need(len(pivots) == 8, "Representative rank is not eight")
    groups = {}

    for x in sorted(set(range(64)) - set(flat)):
        vector = [Fraction(v) for v in ROWS[x]]

        for row, pivot in zip(reduced, pivots):
            factor = vector[pivot]
            if factor:
                vector = [
                    a - factor * b
                    for a, b in zip(vector, row)
                ]

        key = primitive(vector)
        groups.setdefault(key, []).append(x)

    need(sum(map(len, groups.values())) == 56,
         "Outside-point coverage mismatch")
    return groups

def dependent_triple(u, v, w):
    a = next(q for q in range(len(u)) if u[q])
    b = next(
        (q for q in range(len(u))
         if u[a] * v[q] - u[q] * v[a]),
        None,
    )
    need(b is not None, "Expected distinct projective vectors")

    determinant = u[a] * v[b] - u[b] * v[a]
    left = w[a] * v[b] - w[b] * v[a]
    right = u[a] * w[b] - u[b] * w[a]

    return all(
        determinant * w[q] == left * u[q] + right * v[q]
        for q in range(len(u))
    )

def controls():
    need(
        dependent_triple((1, 0, 0), (0, 1, 0), (1, 1, 0)),
        "Dependent-triple positive control failed",
    )
    need(
        not dependent_triple((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        "Independent-triple negative control failed",
    )
    need(
        primitive([Fraction(-2), Fraction(-4), Fraction(0)])
        == (1, 2, 0),
        "Projective normalization control failed",
    )

def parity_dependency():
    source = (V6 / "parity_containment.py").read_bytes()
    need(sha(source) == V6SHA, "VERIFY-006 source hash mismatch")
    need((V6RUN / "parity_containment.py").read_bytes() == source,
         "VERIFY-006 source snapshot mismatch")

    expected_names = {
        "CONTAINMENT-ARGUMENT.md",
        "PASS.json",
        "parity_containment.py",
    }
    entries = [
        line.split("  ", 1)
        for line in (V6RUN / "SHA256SUMS").read_text().splitlines()
    ]
    need(
        len(entries) == 3
        and all(len(entry) == 2 for entry in entries)
        and {entry[1] for entry in entries} == expected_names,
        "VERIFY-006 manifest coverage mismatch",
    )
    for digest, name in entries:
        need(sha((V6RUN / name).read_bytes()) == digest,
             "VERIFY-006 manifest mismatch: " + name)

    raw = (V6RUN / "PASS.json").read_bytes()
    receipt = json.loads(raw)

    for key, expected in {
        "status": "PASS",
        "gate": "SIXBIT-VERIFY-006-PARITY",
        "source_sha256": V6SHA,
        "binary_feature_rank": 22,
        "binary_codewords_enumerated": 4194304,
        "affine_flats_enumerated": 11160,
        "directions_enumerated": 1395,
    }.items():
        need(receipt.get(key) == expected,
             "VERIFY-006 receipt mismatch: " + key)

    for flag in (
        "source_unchanged",
        "finite_parity_lemmas_verified",
        "all_flats_binary_orthogonal",
        "weight_eight_supports_classified_by_count_equality",
        "dual_weights_one_through_seven_absent",
        "dual_weights_nine_ten_eleven_absent",
    ):
        need(receipt.get(flag) is True, "Parity flag: " + flag)

    dual = receipt["dual_weight_enumerator"]
    need(dual["8"] == 11160, "Parity weight-eight count mismatch")
    need(all(dual[str(j)] == 0
             for j in (*range(1, 8), 9, 10, 11)),
         "Parity low-weight gap mismatch")

    return {
        "gate": receipt["gate"],
        "source_sha256": V6SHA,
        "receipt_sha256": sha(raw),
        "receipt_path": str(V6RUN / "PASS.json"),
    }

def audit(report):
    controls()
    report["arithmetic_controls_passed"] = True
    report["parity_dependency"] = parity_dependency()

    directions = set()
    for a, b, c in itertools.combinations(range(1, 64), 3):
        points = tuple(sorted({
            0, a, b, c, a ^ b, a ^ c, b ^ c, a ^ b ^ c
        }))
        if len(points) == 8:
            directions.add(points)

    need(len(directions) == 1395, "Direction count mismatch")

    rank_counts = Counter()
    rank_eight = set()

    print("COMPUTING: exact ranks of 1395 directions", flush=True)
    for number, flat in enumerate(sorted(directions), 1):
        _, pivots = rref([ROWS[x] for x in flat])
        rank = len(pivots)
        need(rank in (7, 8), "Unexpected rational direction rank")
        rank_counts[rank] += 1
        if rank == 8:
            rank_eight.add(flat)
        if number % 300 == 0:
            print("RANKED:", number, flush=True)

    need(dict(rank_counts) == {7: 350, 8: 1045},
         "Direction-rank distribution mismatch")

    maps = [
        tuple(
            sum(((x >> i) & 1) << p[i] for i in range(6))
            for x in range(64)
        )
        for p in itertools.permutations(range(6))
    ]

    remaining = set(rank_eight)
    covered = set()
    orbits = []

    while remaining:
        representative = min(remaining)
        orbit = {
            tuple(sorted(mapping[x] for x in representative))
            for mapping in maps
        }
        need(orbit <= rank_eight, "Orbit left rank-eight universe")
        need(not (orbit & covered), "Overlapping direction orbits")
        covered.update(orbit)
        remaining.difference_update(orbit)
        orbits.append((representative, len(orbit)))

    need(covered == rank_eight, "Incomplete orbit coverage")
    need(sum(size for _, size in orbits) == 1045,
         "Orbit-size reconciliation failed")

    report["direction_rank_distribution"] = dict(rank_counts)
    report["coordinate_permutation_orbits"] = len(orbits)
    report["orbit_results"] = []

    total_tests = 0
    total_dependent = 0

    for number, (flat, orbit_size) in enumerate(orbits, 1):
        groups = quotient_groups(flat)
        vectors = sorted(groups)
        tests = 0
        dependent = 0
        examples = []

        for i, j, k in itertools.combinations(range(len(vectors)), 3):
            u, v, w = vectors[i], vectors[j], vectors[k]
            tests += 1

            if dependent_triple(u, v, w):
                dependent += 1
                if len(examples) < 5:
                    examples.append([groups[u], groups[v], groups[w]])

        need(tests == math.comb(len(vectors), 3),
             "Projective-triple coverage mismatch")

        report["orbit_results"].append({
            "representative_flat": list(flat),
            "direction_orbit_size": orbit_size,
            "outside_points": 56,
            "distinct_projective_residuals": len(vectors),
            "residual_class_sizes": sorted(map(len, groups.values())),
            "exact_triples_tested": tests,
            "dependent_distinct_projective_triples": dependent,
            "dependent_examples_point_classes": examples,
        })

        total_tests += tests
        total_dependent += dependent

        print(
            "ORBIT:", number, "/", len(orbits),
            "SIZE:", orbit_size,
            "PROJECTIVE POINTS:", len(vectors),
            "TRIPLES:", tests,
            "DEPENDENT:", dependent,
            flush=True,
        )

    report.update({
        "directions_enumerated": 1395,
        "rank_eight_directions_covered": 1045,
        "affine_rank_eight_flats_covered_by_symmetry": 8360,
        "exact_projective_triples_tested": total_tests,
        "dependent_distinct_projective_triples": total_dependent,
        "all_outside_residuals_nonzero": True,
        "orbit_partition_complete": True,
        "no_eleven_point_rational_circuits_given_parity_dependency":
            total_dependent == 0,
        "symmetries_used": [
            "coordinate permutations",
            "bit complements / affine translations",
        ],
        "arbitrary_binary_linear_symmetry_used": False,
    })

    return total_dependent == 0

def main():
    started = time.monotonic()
    source = SOURCE.read_bytes()
    run = Path(tempfile.mkdtemp(prefix="run-", dir=SOURCE.parent))
    (run / "exhaustive11.py").write_bytes(source)

    report = {
        "experiment": "ELEVEN-CIRCUIT-EXHAUSTIVE-002",
        "status": "RUNNING",
        "started_utc": utc(),
        "source_sha256": sha(source),
        "python_version": sys.version,
        "scope": (
            "Exact exhaustive projective-triple exclusion reduced by "
            "coordinate permutations and translations. Global "
            "eleven-point exclusion depends on retained VERIFY-006 "
            "parity lemmas. No novelty or formal machine-checked "
            "proof claim."
        ),
    }

    print("RETAINED:", run, flush=True)

    try:
        excluded = audit(report)
        need(SOURCE.read_bytes() == source, "Source changed")
        report["source_unchanged"] = True
        report["status"] = (
            "PASS" if excluded else "DEPENDENT_TRIPLE_FOUND"
        )
    except Exception as exc:
        report["status"] = "ERROR"
        report["error"] = type(exc).__name__ + ": " + str(exc)
        (run / "traceback.txt").write_text(traceback.format_exc())

    report["finished_utc"] = utc()
    report["elapsed_seconds"] = round(time.monotonic() - started, 6)

    (run / "EXHAUSTIVE-REPORT.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )

    files = sorted(p for p in run.iterdir() if p.is_file())
    (run / "SHA256SUMS").write_text("".join(
        sha(p.read_bytes()) + "  " + p.name + "\n"
        for p in files
    ))

    summary = {
        key: value for key, value in report.items()
        if key != "orbit_results"
    }
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)
    print("RETAINED:", run, flush=True)

    return 0 if report["status"] == "PASS" else 2

if __name__ == "__main__":
    raise SystemExit(main())
