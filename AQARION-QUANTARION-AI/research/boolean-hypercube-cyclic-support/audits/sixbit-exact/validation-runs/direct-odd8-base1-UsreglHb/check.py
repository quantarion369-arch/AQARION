import hashlib
import itertools
import json
import math
import os
import subprocess
import sys
import time
import traceback
from pathlib import Path

import sympy as sp

REPO = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
COMMIT = "5093e2af9db66567cba85caaff34220f1f8a0b35"
PREFIX = (
    "AQARION-QUANTARION-AI/research/"
    "boolean-hypercube-cyclic-support/audits/sixbit-exact/"
    "synthesis/2026-11-09/evidence-package/inputs/"
)
START = time.monotonic()
BASE = (0, 7, 25, 30, 42, 45, 51, 52)
REPORT = {
    "experiment": "DIRECT_FULL_MATRIX_ODD8_BASE1",
    "status": "RUNNING",
    "commit": COMMIT,
    "base": BASE,
    "full_census_verified": False,
    "promotion": False,
}

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def frozen(name):
    result = subprocess.run(
        ["git", "-C", str(REPO),
         "-c", "core.fsmonitor=false",
         "show", COMMIT + ":" + PREFIX + name],
        env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"),
        capture_output=True,
        timeout=120,
        check=False,
    )
    need(
        result.returncode == 0,
        result.stderr.decode(errors="replace")
    )
    return result.stdout

def modular_rank(rows, prime=1009):
    a = [row[:] for row in rows]
    rank = 0

    for col in range(12):
        pivot = next(
            (i for i in range(rank, len(a))
             if a[i][col] % prime),
            None,
        )
        if pivot is None:
            continue

        a[rank], a[pivot] = a[pivot], a[rank]
        inverse = pow(a[rank][col] % prime, -1, prime)

        for j in range(col, 12):
            a[rank][j] = a[rank][j] * inverse % prime

        for i in range(rank + 1, len(a)):
            factor = a[i][col] % prime
            if factor:
                for j in range(col + 1, 12):
                    a[i][j] = (
                        a[i][j] - factor * a[rank][j]
                    ) % prime
                a[i][col] = 0

        rank += 1
        if rank == 12:
            return rank

    return rank

exit_code = 2

try:
    source_raw = frozen("sixflat-source.py")
    report_raw = frozen("sixflat-report.json")

    need(
        sha(source_raw)
        == "04e9bd88f44cb75d8cbab8e683de05c1"
           "4b39bbf8de64072bfa6a12c8ba655b8a",
        "Frozen source pin mismatch"
    )
    need(
        sha(report_raw)
        == "59fe9ea76d765ff8455033baf59a28328"
           "bd0a6d032387a679806123aa901e80e",
        "Frozen report pin mismatch"
    )

    historical = json.loads(report_raw)
    row = historical["rows"][0]
    need(tuple(row["base_flat"]) == BASE, "Wrong base")
    need(row["accepted"] == 0, "Expected empty retained list")

    # Previously recovered retained execution; read only.
    retained = (
        Path.home() / "AQARION-EXPERIMENTS"
        / "six-flat-independent.6tHXV6wT/results"
        / "BASE-1-CIRCUITS.jsonl"
    )
    retained_raw = retained.read_bytes()
    need(
        sha(retained_raw) == row["circuit_file_sha256"],
        "Retained circuit-file hash mismatch"
    )
    retained_records = [
        json.loads(line)
        for line in retained_raw.decode().splitlines()
        if line.strip()
    ]
    expected = {
        tuple(record["support"]) for record in retained_records
    }
    need(not expected, "Base 1 retained support set is not empty")

    REPORT["frozen_report_sha256"] = sha(report_raw)
    REPORT["retained_circuit_file_sha256"] = sha(retained_raw)
    REPORT["source_sha256"] = sha(Path(__file__).read_bytes())

    pairs = list(itertools.combinations(range(6), 2))
    features = []
    for x in range(64):
        bits = [(x >> i) & 1 for i in range(6)]
        features.append(
            [1] + bits + [bits[i] * bits[j] for i, j in pairs]
        )

    base_rows = [
        [features[x][r] for x in BASE] for r in range(22)
    ]
    need(sp.Matrix(base_rows).rank() == 8, "Base rank is not eight")

    control = [
        [int(i == j) for j in range(12)]
        for i in range(22)
    ]
    need(modular_rank(control) == 12, "Rank control failed")
    control[11] = [0] * 12
    need(modular_rank(control) == 11, "Deficiency control failed")

    outside = [x for x in range(64) if x not in BASE]
    found = set()
    visited = 0
    full_rank = 0
    fallbacks = 0
    rank11_full_support = 0

    print("BASE 1: DIRECT FULL-MATRIX ENUMERATION", flush=True)
    print("EXPECTED EXTENSIONS:", math.comb(56, 4), flush=True)

    for extra in itertools.combinations(outside, 4):
        visited += 1
        support = BASE + extra
        rows = [
            base_rows[r] + [features[x][r] for x in extra]
            for r in range(22)
        ]

        if modular_rank(rows) == 12:
            full_rank += 1
        else:
            fallbacks += 1
            matrix = sp.Matrix(rows)
            kernel = matrix.nullspace()

            if len(kernel) == 1:
                vector = kernel[0]
                if all(value != 0 for value in vector):
                    rank11_full_support += 1
                    denominator = sp.ilcm(
                        *[value.q for value in vector]
                    )
                    values = [int(value * denominator)
                              for value in vector]
                    divisor = math.gcd(*map(abs, values))
                    values = [value // divisor for value in values]

                    need(
                        matrix * sp.Matrix(values) == sp.zeros(22, 1),
                        "Exact kernel identity failed"
                    )

                    odd = tuple(sorted(
                        x for x, value in zip(support, values)
                        if value % 2
                    ))
                    if odd == BASE:
                        key = tuple(sorted(support))
                        need(key not in found, "Duplicate support")
                        found.add(key)

        if visited % 25000 == 0:
            print(
                "VISITED:", visited,
                "EXACT FALLBACKS:", fallbacks,
                "ACCEPTED:", len(found),
                "SECONDS:", round(time.monotonic() - START, 1),
                flush=True
            )

    need(visited == 367290, "Incomplete extension universe")
    need(full_rank + fallbacks == visited, "Accounting mismatch")
    need(found == expected, "Support set differs from retained list")
    need(
        sha(retained.read_bytes()) == sha(retained_raw),
        "Retained input changed during execution"
    )

    REPORT.update({
        "status": "PASS_FOR_BASE1_LOCAL_COMPLETENESS",
        "extensions_visited": visited,
        "modular_full_rank_rejections": full_rank,
        "exact_fallbacks": fallbacks,
        "rank11_full_support_candidates": rank11_full_support,
        "accepted_odd_eight_circuits": len(found),
        "support_set_matches_retained": True,
        "limitations": [
            "Checks Base 1 only.",
            "Uses SymPy exact nullspaces for modular deficiencies.",
            "Does not certify the other five local lists.",
            "Does not certify the combined census."
        ],
    })
    exit_code = 0

except Exception:
    REPORT["status"] = "FAIL_OR_BLOCKED"
    REPORT["error"] = traceback.format_exc()
    print(REPORT["error"], flush=True)

finally:
    REPORT["elapsed_seconds"] = round(time.monotonic() - START, 3)
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
print("EXTENSIONS:", REPORT.get("extensions_visited"))
print("ACCEPTED:", REPORT.get("accepted_odd_eight_circuits"))
print("SUPPORT SET MATCH:",
      REPORT.get("support_set_matches_retained", False))
print("RESULTS:", OUT)
print("OTHER FIVE BASES VERIFIED: FALSE")
print("FULL CENSUS VERIFIED: FALSE")
print("NO STAGING, COMMIT, PUSH, OR PR")
sys.exit(exit_code)
