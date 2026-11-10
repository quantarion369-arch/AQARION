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
from pathlib import Path, PurePosixPath

import sympy as sp

REPO = Path(sys.argv[1]).resolve()
PREV = Path(sys.argv[2]).resolve()
OUT = Path(sys.argv[3]).resolve()
COMMIT = "5093e2af9db66567cba85caaff34220f1f8a0b35"
PREFIX = (
    "AQARION-QUANTARION-AI/research/"
    "boolean-hypercube-cyclic-support/audits/sixbit-exact/"
    "synthesis/2026-11-09/evidence-package/inputs/"
)
RETAINED = (
    Path.home() / "AQARION-EXPERIMENTS"
    / "six-flat-independent.6tHXV6wT/results"
)
START = time.monotonic()
REPORT = {
    "experiment": "DIRECT_FULL_MATRIX_ODD8_BASES_2_TO_6",
    "status": "RUNNING",
    "commit": COMMIT,
    "full_census_verified": False,
    "promotion": False,
    "completed_bases": [],
}
tracked = {}

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def bound(path):
    raw = path.read_bytes()
    digest = sha(raw)
    if path in tracked:
        need(tracked[path] == digest, "Input changed: " + str(path))
    tracked[path] = digest
    return raw

def frozen(name):
    result = subprocess.run(
        ["git", "-C", str(REPO),
         "-c", "core.fsmonitor=false",
         "show", COMMIT + ":" + PREFIX + name],
        env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"),
        capture_output=True, timeout=120, check=False,
    )
    need(result.returncode == 0,
         result.stderr.decode(errors="replace"))
    return result.stdout

exit_code = 2

try:
    manifest = {}
    for line in bound(PREV / "SHA256SUMS").decode().splitlines():
        expected, name = line.split("  ", 1)
        rel = PurePosixPath(name)
        need(not rel.is_absolute() and ".." not in rel.parts,
             "Unsafe pilot manifest path")
        manifest[name] = expected

    for name in ("check.py", "REPORT.json"):
        need(name in manifest, "Pilot manifest missing " + name)
        need(sha(bound(PREV / name)) == manifest[name],
             "Pilot artifact mismatch: " + name)

    pilot = json.loads(bound(PREV / "REPORT.json"))
    need(pilot["status"] == "PASS_FOR_BASE1_LOCAL_COMPLETENESS",
         "Pilot did not pass")
    need(pilot["extensions_visited"] == 367290,
         "Pilot extension count differs")
    need(pilot["support_set_matches_retained"] is True,
         "Pilot support comparison did not pass")

    pilot_source = bound(PREV / "check.py")
    need(sha(pilot_source) == pilot["source_sha256"],
         "Pilot source/report mismatch")

    nodes = [
        node for node in ast.parse(pilot_source.decode()).body
        if isinstance(node, ast.FunctionDef)
        and node.name == "modular_rank"
    ]
    need(len(nodes) == 1 and not nodes[0].decorator_list,
         "Expected pilot rank function not found")
    namespace = {}
    exec(
        compile(ast.Module(body=nodes, type_ignores=[]),
                "verified-pilot-modular-rank", "exec"),
        namespace,
    )
    modular_rank = namespace["modular_rank"]

    report_raw = frozen("sixflat-report.json")
    need(
        sha(report_raw)
        == "59fe9ea76d765ff8455033baf59a28328"
           "bd0a6d032387a679806123aa901e80e",
        "Frozen report pin mismatch"
    )
    frozen_report = json.loads(report_raw)
    rows = frozen_report["rows"]
    need(len(rows) == 6, "Expected six frozen rows")

    REPORT["source_sha256"] = sha(bound(Path(__file__)))
    REPORT["pilot_source_sha256"] = sha(pilot_source)
    REPORT["frozen_report_sha256"] = sha(report_raw)

    pairs = list(itertools.combinations(range(6), 2))
    features = []
    for x in range(64):
        bits = [(x >> i) & 1 for i in range(6)]
        features.append(
            [1] + bits
            + [bits[i] * bits[j] for i, j in pairs]
        )

    control = [
        [int(i == j) for j in range(12)]
        for i in range(22)
    ]
    need(modular_rank(control) == 12, "Rank-12 control failed")
    control[11] = [0] * 12
    need(modular_rank(control) == 11, "Rank-11 control failed")

    # Bind every retained comparison file before starting searches.
    expected_sets = {}
    for number in range(2, 7):
        row = rows[number - 1]
        need(row["row"] == number, "Frozen row order differs")
        raw = bound(RETAINED / f"BASE-{number}-CIRCUITS.jsonl")
        need(sha(raw) == row["circuit_file_sha256"],
             "Retained file mismatch for base " + str(number))
        records = [
            json.loads(line) for line in raw.decode().splitlines()
            if line.strip()
        ]
        supports = [
            tuple(sorted(record["support"])) for record in records
        ]
        expected = set(supports)
        need(len(expected) == len(supports) == row["accepted"],
             "Retained count/uniqueness mismatch")
        expected_sets[number] = expected

    for number in range(2, 7):
        base_start = time.monotonic()
        row = rows[number - 1]
        base = tuple(row["base_flat"])
        need(len(base) == len(set(base)) == 8,
             "Malformed base")
        base_rows = [
            [features[x][r] for x in base] for r in range(22)
        ]
        need(sp.Matrix(base_rows).rank() == 8,
             "Base rank is not eight")
        outside = [x for x in range(64) if x not in base]

        found = set()
        found_records = []
        visited = full_rank = fallbacks = full_support = 0

        print("\nBASE", number, "DIRECT ENUMERATION", flush=True)

        for extra in itertools.combinations(outside, 4):
            visited += 1
            support = base + extra
            matrix_rows = [
                base_rows[r] + [features[x][r] for x in extra]
                for r in range(22)
            ]

            if modular_rank(matrix_rows) == 12:
                full_rank += 1
            else:
                fallbacks += 1
                matrix = sp.Matrix(matrix_rows)
                kernel = matrix.nullspace()

                if len(kernel) == 1 and all(v != 0 for v in kernel[0]):
                    full_support += 1
                    vector = kernel[0]
                    denominator = sp.ilcm(*[v.q for v in vector])
                    values = [int(v * denominator) for v in vector]
                    divisor = math.gcd(*map(abs, values))
                    values = [v // divisor for v in values]

                    need(
                        matrix * sp.Matrix(values) == sp.zeros(22, 1),
                        "Exact kernel identity failed"
                    )
                    odd = {
                        x for x, value in zip(support, values)
                        if value % 2
                    }

                    if odd == set(base):
                        ordered = sorted(zip(support, values))
                        key = tuple(x for x, _ in ordered)
                        coeff = [v for _, v in ordered]
                        if coeff[0] < 0:
                            coeff = [-v for v in coeff]
                        need(key not in found, "Duplicate support")
                        found.add(key)
                        found_records.append({
                            "support": key,
                            "primitive_kernel": coeff,
                        })

            if visited % 50000 == 0:
                print(
                    "BASE:", number, "VISITED:", visited,
                    "EXACT:", fallbacks, "ACCEPTED:", len(found),
                    "SECONDS:",
                    round(time.monotonic() - base_start, 1),
                    flush=True,
                )

        need(visited == 367290, "Incomplete extension enumeration")
        need(full_rank + fallbacks == visited, "Accounting failure")

        support_raw = b"".join(bytes(s) for s in sorted(found))
        (OUT / f"BASE-{number}-SUPPORTS.bin").write_bytes(support_raw)
        with (OUT / f"BASE-{number}-CIRCUITS.jsonl").open("w") as f:
            for record in sorted(
                found_records, key=lambda record: record["support"]
            ):
                f.write(json.dumps(record, sort_keys=True) + "\n")

        missing = expected_sets[number] - found
        unexpected = found - expected_sets[number]
        receipt = {
            "base_row": number,
            "extensions_visited": visited,
            "modular_full_rank_rejections": full_rank,
            "exact_fallbacks": fallbacks,
            "rank11_full_support_candidates": full_support,
            "accepted_odd_eight_circuits": len(found),
            "support_set_sha256": sha(support_raw),
            "missing_retained_supports": sorted(missing),
            "unexpected_supports": sorted(unexpected),
            "support_set_matches_retained": not missing and not unexpected,
            "elapsed_seconds": round(time.monotonic() - base_start, 3),
        }
        (OUT / f"BASE-{number}-REPORT.json").write_text(
            json.dumps(receipt, indent=2) + "\n"
        )
        REPORT["completed_bases"].append(receipt)

        need(not missing and not unexpected,
             "Support-set mismatch for base " + str(number))
        print("PASS: BASE", number, "SUPPORTS:", len(found), flush=True)

    for path, digest in tracked.items():
        need(path.is_file() and sha(path.read_bytes()) == digest,
             "Tracked input changed: " + str(path))

    REPORT["status"] = "PASS_FOR_BASES_2_TO_6_LOCAL_COMPLETENESS"
    REPORT["accepted_total_bases_2_to_6"] = sum(
        row["accepted_odd_eight_circuits"]
        for row in REPORT["completed_bases"]
    )
    REPORT["inputs_unchanged"] = True
    exit_code = 0

except Exception:
    REPORT["status"] = "FAIL_OR_BLOCKED"
    REPORT["error"] = traceback.format_exc()
    print(REPORT["error"], flush=True)

finally:
    REPORT["elapsed_seconds"] = round(time.monotonic() - START, 3)
    REPORT["tracked_inputs"] = {
        str(path): digest for path, digest in tracked.items()
    }
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
print("BASES COMPLETED:", len(REPORT["completed_bases"]))
print("ACCEPTED:", REPORT.get("accepted_total_bases_2_to_6"))
print("RESULTS:", OUT)
print("FULL CENSUS VERIFIED: FALSE")
print("NO HISTORICAL GENERATOR EXECUTED")
print("NO STAGING, COMMIT, PUSH, OR PR")
print("PROMOTION: FALSE")
sys.exit(exit_code)
