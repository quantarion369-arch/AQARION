#!/usr/bin/env python3
import ast
import hashlib
import itertools
import json
import math
import os
import subprocess
import sys
import time
import traceback
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
PREV = Path(sys.argv[2]).resolve()
OUT = Path(sys.argv[3]).resolve()
COMMIT = "5093e2af9db66567cba85caaff34220f1f8a0b35"
PREFIX = (
    "AQARION-QUANTARION-AI/research/"
    "boolean-hypercube-cyclic-support/audits/sixbit-exact/"
    "synthesis/2026-11-09/evidence-package/inputs/"
)
START = time.monotonic()
REPORT = {
    "status": "RUNNING",
    "commit": COMMIT,
    "started_utc": datetime.now(timezone.utc).isoformat(),
    "full_census_verified": False,
    "local_extension_completeness_verified": False,
    "promotion": False,
}

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def git(*args):
    result = subprocess.run(
        ["git", "-C", str(REPO),
         "-c", "core.fsmonitor=false", *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"),
        timeout=120,
        check=False,
    )
    need(
        result.returncode == 0,
        result.stdout.decode(errors="replace") +
        result.stderr.decode(errors="replace"),
    )
    return result.stdout

def modular_rank(rows, prime=1009):
    a = [[int(x) % prime for x in row] for row in rows]
    rank = 0
    for col in range(len(a[0])):
        found = next(
            (i for i in range(rank, len(a)) if a[i][col]),
            None,
        )
        if found is None:
            continue

        a[rank], a[found] = a[found], a[rank]
        inverse = pow(a[rank][col], -1, prime)
        a[rank] = [(x * inverse) % prime for x in a[rank]]

        for i in range(rank + 1, len(a)):
            factor = a[i][col]
            if factor:
                a[i] = [
                    (x - factor * y) % prime
                    for x, y in zip(a[i], a[rank])
                ]
        rank += 1
        if rank == len(a):
            break
    return rank

def image(direction, generator):
    return tuple(sorted(generator[x] for x in direction))

exit_code = 2

try:
    need(
        git("rev-parse", "HEAD").decode().strip() == COMMIT,
        "HEAD differs from the frozen checkpoint",
    )

    previous = json.loads((PREV / "REPORT.json").read_text())
    source = (PREV / "verifier.py").read_bytes()

    need(
        previous["status"] == "PASS_FOR_BOUNDED_VALIDATION_ONLY"
        and previous["commit"] == COMMIT,
        "Previous verifier receipt is not the expected passing run",
    )
    need(
        sha(source) == previous["verifier_sha256"],
        "Previous verifier source changed",
    )

    names = {"matrix", "rref"}
    functions = [
        node for node in ast.parse(source.decode()).body
        if isinstance(node, ast.FunctionDef) and node.name in names
    ]
    need(
        len(functions) == 2
        and {node.name for node in functions} == names
        and all(not node.decorator_list for node in functions),
        "Expected mathematical functions not found",
    )
    namespace = {"Fraction": Fraction, "itertools": itertools}
    exec(
        compile(
            ast.Module(body=functions, type_ignores=[]),
            str(PREV / "verifier.py"),
            "exec",
        ),
        namespace,
    )
    matrix = namespace["matrix"]
    rref = namespace["rref"]
    REPORT["rank_function_source_sha256"] = sha(source)
    (OUT / "reused-verifier.py").write_bytes(source)

    frozen = git("show", COMMIT + ":" + PREFIX + "sixflat-report.json")
    original = json.loads(frozen)
    (OUT / "FROZEN-SIXFLAT-REPORT.json").write_bytes(frozen)
    rows = original["rows"]
    need(len(rows) == 6, "Expected six frozen base rows")

    need(modular_rank([[0, 1], [1, 0]]) == 2,
         "Modular row-swap control failed")
    need(modular_rank([[1, 2], [2, 4]]) == 1,
         "Modular dependent-row control failed")
    need(modular_rank([[1009]]) == 0,
         "Modular bad-prime control failed")
    need(len(rref([[1009]])[1]) == 1,
         "Exact fallback control failed")

    print("ENUMERATING ALL THREE-DIMENSIONAL DIRECTIONS", flush=True)
    directions = set()

    for a, b, c in itertools.combinations(range(1, 64), 3):
        span = tuple(sorted({
            0, a, b, c, a ^ b, a ^ c, b ^ c, a ^ b ^ c
        }))
        if len(span) == 8:
            directions.add(span)

    need(len(directions) == 1395, "Direction count differs from 1395")
    print("DIRECTIONS ENUMERATED:", len(directions), flush=True)

    eligible = set()
    ranks = Counter()
    exact_fallbacks = 0

    for number, direction in enumerate(sorted(directions), 1):
        features = matrix(list(direction))
        rank = modular_rank(features)

        if rank < 8:
            rank = len(rref(features)[1])
            exact_fallbacks += 1

        ranks[rank] += 1
        if rank == 8:
            eligible.add(direction)

        if number % 200 == 0:
            print("DIRECTION RANKS CHECKED:", number, flush=True)

    need(len(eligible) == 1045, "Rank-eight count differs from 1045")

    # Root swap j: preserve bit j; XOR it into every other bit.
    generators = [
        tuple(
            x ^ (63 ^ (1 << j)) if (x >> j) & 1 else x
            for x in range(64)
        )
        for j in range(6)
    ]

    for generator in generators:
        need(sorted(generator) == list(range(64)),
             "Generator is not bijective")
        need(all(generator[generator[x]] == x for x in range(64)),
             "Generator is not an involution")

    print("RECONSTRUCTING SIX DIRECTION ORBITS", flush=True)
    covered = set()
    orbit_results = []

    for number, row in enumerate(rows, 1):
        need(row["row"] == number, "Unexpected frozen row order")
        seed = tuple(sorted(row["base_flat"]))
        need(seed in eligible, "Frozen base is not rank-eight")

        orbit = {seed}
        pending = [seed]

        while pending:
            direction = pending.pop()
            for generator in generators:
                transformed = image(direction, generator)
                if transformed not in orbit:
                    orbit.add(transformed)
                    pending.append(transformed)

        need(orbit <= eligible, "Orbit contains an ineligible direction")
        need(not (covered & orbit), "Direction orbits overlap")
        covered.update(orbit)

        flat_count = 8 * len(orbit)
        need(
            flat_count == row["flat_orbit_size"],
            "Affine-flat weight differs from frozen report",
        )
        orbit_results.append({
            "base_row": number,
            "base": list(seed),
            "directions": len(orbit),
            "affine_flats": flat_count,
        })
        print(
            f"PASS: BASE-{number}: "
            f"{len(orbit)} directions, {flat_count} affine flats",
            flush=True,
        )

    need(covered == eligible,
         "Six orbits do not exactly cover rank-eight directions")

    REPORT.update({
        "status": "PASS_FOR_DIRECTION_COVERAGE_ONLY",
        "all_three_dimensional_directions": len(directions),
        "feature_rank_distribution": dict(ranks),
        "rank_eight_directions": len(eligible),
        "exact_rank_fallbacks": exact_fallbacks,
        "six_orbits_disjoint": True,
        "six_orbits_cover_rank_eight_directions": True,
        "orbits": orbit_results,
        "limitations": [
            "Does not enumerate twelve-point extensions.",
            "Does not prove local-generator completeness.",
            "Does not independently certify the odd-twelve sector.",
            "Checks direction action and rank membership; does not "
            "supply a new general proof of rational circuit transport.",
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
            sha(path.read_bytes()) + "  " + path.name + "\n"
            for path in sorted(OUT.iterdir())
            if path.is_file() and path.name != "SHA256SUMS"
        )
    )

print("\n=== FINAL ===")
print("STATUS:", REPORT["status"])
print("RANK-EIGHT DIRECTIONS:", REPORT.get("rank_eight_directions"))
print("FULL CENSUS VERIFIED: FALSE")
print("LOCAL EXTENSION COMPLETENESS VERIFIED: FALSE")
print("RESULTS:", OUT)
print("NO STAGING, COMMIT, PUSH, OR PR")
print("PROMOTION: FALSE")
sys.exit(exit_code)
