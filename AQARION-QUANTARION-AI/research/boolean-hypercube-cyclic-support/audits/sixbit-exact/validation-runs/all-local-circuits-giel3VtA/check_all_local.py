#!/usr/bin/env python3
import ast
import hashlib
import itertools
import json
import math
import os
import re
import subprocess
import sys
import time
import traceback
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
PREV = Path(sys.argv[2]).resolve()
OUT = Path(sys.argv[3]).resolve()
COMMIT = "5093e2af9db66567cba85caaff34220f1f8a0b35"
SOURCE = (
    "AQARION-QUANTARION-AI/research/"
    "boolean-hypercube-cyclic-support/audits/sixbit-exact/"
    "synthesis/2026-11-09/evidence-package/inputs/"
    "reconciliation-report.json"
)
START = time.monotonic()
REPORT = {
    "status": "RUNNING",
    "commit": COMMIT,
    "started_utc": datetime.now(timezone.utc).isoformat(),
    "files": [],
    "records_verified": 0,
    "full_census_verified": False,
    "promotion": False,
}
RESULTS = []

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

exit_code = 2

try:
    need(
        git("rev-parse", "HEAD").decode().strip() == COMMIT,
        "HEAD differs from the frozen checkpoint",
    )

    previous = json.loads((PREV / "REPORT.json").read_text())
    verifier = (PREV / "verifier.py").read_bytes()

    need(
        previous["status"] == "PASS_FOR_BOUNDED_VALIDATION_ONLY",
        "Previous verifier did not pass",
    )
    need(previous["commit"] == COMMIT, "Previous commit mismatch")
    need(
        sha(verifier) == previous["verifier_sha256"],
        "Previous verifier source hash mismatch",
    )

    wanted = {"require", "matrix", "rref", "certificate"}
    parsed = ast.parse(verifier.decode())
    functions = [
        node for node in parsed.body
        if isinstance(node, ast.FunctionDef)
        and node.name in wanted
    ]
    need(
        len(functions) == 4
        and {node.name for node in functions} == wanted,
        "Expected mathematical functions not found",
    )
    need(
        all(not node.decorator_list for node in functions),
        "Unexpected function decorators",
    )

    namespace = {
        "Fraction": Fraction,
        "itertools": itertools,
        "math": math,
        "Counter": Counter,
    }
    module = ast.Module(body=functions, type_ignores=[])
    exec(compile(module, str(PREV / "verifier.py"), "exec"), namespace)
    check = namespace["certificate"]

    REPORT["reused_verifier_sha256"] = sha(verifier)
    (OUT / "reused-verifier.py").write_bytes(verifier)

    frozen = git("show", COMMIT + ":" + SOURCE)
    document = json.loads(frozen)
    (OUT / "FROZEN-RECONCILIATION-REPORT.json").write_bytes(frozen)

    inputs = document["inputs"]
    files = {}
    for original, expected in inputs.items():
        match = re.fullmatch(
            r"BASE-([1-6])-CIRCUITS\.jsonl",
            Path(original).name,
        )
        if match:
            base = int(match.group(1))
            need(base not in files, "Duplicate base-file reference")
            files[base] = (Path(original), expected)

    need(set(files) == set(range(1, 7)), "Six base files not found")

    expected_counts = {1: 0, 2: 8, 3: 56, 4: 24, 5: 48, 6: 24}
    expected_patterns = Counter()
    orbit_sizes = {}

    for entry in document["class_ledger"]:
        base = entry["base_row"]
        expected_patterns[(base, entry["pattern"])] += (
            entry["local_class_size"]
        )
        orbit = entry["flat_orbit_size"]
        need(
            base not in orbit_sizes or orbit_sizes[base] == orbit,
            "Inconsistent reported orbit size",
        )
        orbit_sizes[base] = orbit

    observed_patterns = Counter()
    input_snapshots = {}
    global_supports = set()
    total = 0

    for base in range(1, 7):
        path, expected = files[base]
        raw = path.read_bytes()
        need(sha(raw) == expected, "Input hash mismatch: " + str(path))
        input_snapshots[path] = expected

        seen = set()
        count = 0

        for line_number, line in enumerate(raw.splitlines(), 1):
            if not line.strip():
                continue

            record = json.loads(line)
            label = f"BASE-{base}, line {line_number}"
            need(
                type(record["base_row"]) is int
                and record["base_row"] == base,
                label + ": incorrect base-row label",
            )
            need(
                record["classification"] == "ODD_EIGHT_CIRCUIT",
                label + ": unexpected classification",
            )

            supplied = record["primitive_kernel"]
            checked = check(record["support"], supplied)

            need(
                math.gcd(*supplied) == 1,
                label + ": supplied kernel is not primitive",
            )
            computed = checked["primitive_kernel"]
            need(
                supplied == computed
                or supplied == [-v for v in computed],
                label + ": kernel differs beyond overall sign",
            )
            need(
                sum(v % 2 != 0 for v in computed) == 8,
                label + ": expected eight odd coefficients",
            )
            need(
                checked["pattern"] == record["pattern"],
                label + ": coefficient-pattern mismatch",
            )

            key = tuple(checked["canonical_support"])
            need(key not in seen, label + ": duplicate local support")
            seen.add(key)
            global_supports.add(key)
            observed_patterns[(base, checked["pattern"])] += 1

            checked["base_row"] = base
            checked["input_line"] = line_number
            RESULTS.append(checked)
            count += 1
            total += 1
            REPORT["records_verified"] = total

            if total % 8 == 0:
                print("RECORDS VERIFIED:", total, flush=True)

        need(
            count == expected_counts[base],
            f"BASE-{base}: unexpected record count {count}",
        )
        REPORT["files"].append({
            "base": base,
            "path": str(path),
            "sha256": expected,
            "records_verified": count,
            "within_base_duplicates": 0,
        })
        print(f"PASS: BASE-{base}: {count} records", flush=True)

    need(total == 160, "Expected 160 verified records")
    need(
        observed_patterns == expected_patterns,
        "Per-base pattern totals differ from the frozen class ledger",
    )

    weighted = Counter()
    for (base, pattern), count in observed_patterns.items():
        weighted[pattern] += count * orbit_sizes[base]

    need(
        dict(weighted) == document["weighted_pattern_counts"],
        "Reported-orbit weighted pattern arithmetic mismatch",
    )
    need(
        sum(weighted.values()) == document["weighted_total"] == 286720,
        "Reported-orbit weighted total mismatch",
    )

    for path, expected in input_snapshots.items():
        need(
            sha(path.read_bytes()) == expected,
            "Input changed during verification: " + str(path),
        )

    REPORT.update({
        "status": "PASS_FOR_ALL_160_PRESERVED_LOCAL_RECORDS",
        "per_base_pattern_totals_match": True,
        "reported_orbit_weighted_patterns": dict(weighted),
        "reported_orbit_weighted_total": sum(weighted.values()),
        "distinct_supports_across_local_files": len(global_supports),
        "orbit_sizes_independently_verified": False,
        "local_generator_completeness_verified": False,
        "odd_twelve_sector_verified": False,
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
    (OUT / "CHECKED-CIRCUITS.json").write_text(
        json.dumps(RESULTS, indent=2) + "\n"
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
print("LOCAL RECORDS VERIFIED:", REPORT["records_verified"])
print("FULL CENSUS VERIFIED: FALSE")
print("RESULTS:", OUT)
print("NO HISTORICAL GENERATOR EXECUTED")
print("NO STAGING, COMMIT, PUSH, OR PR")
print("PROMOTION: FALSE")
sys.exit(exit_code)
