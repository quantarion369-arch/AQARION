#!/usr/bin/env python3
import hashlib
import itertools
import json
import math
import os
import platform
import subprocess
import sys
import time
import traceback
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path, PurePosixPath

REPO = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
COMMIT = "5093e2af9db66567cba85caaff34220f1f8a0b35"
DELIVERY = (
    "AQARION-QUANTARION-AI/research/"
    "boolean-hypercube-cyclic-support/audits/sixbit-exact/"
    "synthesis/2026-11-09"
)
ENV = dict(
    os.environ,
    GIT_OPTIONAL_LOCKS="0",
    GIT_TERMINAL_PROMPT="0",
)
START = time.monotonic()
SNAPSHOT = {}
SOURCE_HASH = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
REPORT = {
    "status": "RUNNING",
    "commit": COMMIT,
    "started_utc": datetime.now(timezone.utc).isoformat(),
    "python": sys.version,
    "platform": platform.platform(),
    "verifier_sha256": SOURCE_HASH,
    "tests": [],
    "full_census_verified": False,
    "promotion": False,
}

def require(ok, message):
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
        env=ENV,
        timeout=120,
        check=False,
    )
    require(
        result.returncode == 0,
        "Git failed: " + " ".join(args) + "\n" +
        result.stdout.decode(errors="replace") +
        result.stderr.decode(errors="replace"),
    )
    return result.stdout

def frozen(path):
    return git("show", COMMIT + ":" + path)

def matrix(support):
    rows = [[1] * len(support)]
    rows += [
        [(x >> i) & 1 for x in support]
        for i in range(6)
    ]
    rows += [
        [((x >> i) & 1) * ((x >> j) & 1) for x in support]
        for i, j in itertools.combinations(range(6), 2)
    ]
    return rows

def rref(rows):
    a = [[Fraction(x) for x in row] for row in rows]
    pivots = []
    for col in range(len(a[0])):
        row = len(pivots)
        found = next(
            (i for i in range(row, len(a)) if a[i][col]),
            None,
        )
        if found is None:
            continue
        a[row], a[found] = a[found], a[row]
        pivot = a[row][col]
        a[row] = [x / pivot for x in a[row]]
        for i in range(len(a)):
            if i != row and a[i][col]:
                factor = a[i][col]
                a[i] = [
                    x - factor * y
                    for x, y in zip(a[i], a[row])
                ]
        pivots.append(col)
        if len(pivots) == len(a):
            break
    return a, pivots

def certificate(support, supplied=None):
    require(
        isinstance(support, list) and len(support) == 12,
        "Expected twelve support points",
    )
    require(
        all(type(x) is int and 0 <= x < 64 for x in support),
        "Support points must be integers in 0..63",
    )
    require(len(set(support)) == 12, "Repeated support point")

    a = matrix(support)
    reduced, pivots = rref(a)
    require(len(pivots) == 11, "Support rank is not eleven")

    free = next(i for i in range(12) if i not in pivots)
    vector = [Fraction(0)] * 12
    vector[free] = Fraction(1)

    for row, col in enumerate(pivots):
        vector[col] = -reduced[row][free]

    denominator = math.lcm(*(v.denominator for v in vector))
    vector = [int(v * denominator) for v in vector]
    divisor = math.gcd(*vector)
    require(divisor != 0, "Zero kernel")
    vector = [v // divisor for v in vector]

    if next(v for v in vector if v) < 0:
        vector = [-v for v in vector]

    require(all(vector), "Kernel is not full-support")
    require(
        all(
            sum(x * y for x, y in zip(row, vector)) == 0
            for row in a
        ),
        "Exact kernel identity failed",
    )

    deletion_ranks = [
        len(rref([row[:i] + row[i+1:] for row in a])[1])
        for i in range(12)
    ]
    require(deletion_ranks == [11] * 12, "Deletion rank failed")

    if supplied is not None:
        require(
            len(supplied) == 12
            and all(type(v) is int and v != 0 for v in supplied),
            "Invalid supplied kernel",
        )
        require(
            all(
                sum(x * y for x, y in zip(row, supplied)) == 0
                for row in a
            ),
            "Supplied kernel identity failed",
        )

    counts = Counter(map(abs, vector))
    return {
        "support": support,
        "canonical_support": sorted(support),
        "rank_Q": 11,
        "primitive_kernel": vector,
        "pattern": " ".join(
            f"{v}^{counts[v]}" for v in sorted(counts)
        ),
        "deletion_ranks": deletion_ranks,
    }

def must_reject(support, kernel=None):
    try:
        certificate(support, kernel)
    except RuntimeError:
        return
    raise RuntimeError("Negative control was incorrectly accepted")

def integrity():
    require(
        git("rev-parse", "--show-toplevel").decode().strip()
        == str(REPO),
        "Unexpected repository root",
    )
    require(
        git("rev-parse", "HEAD").decode().strip() == COMMIT,
        "Unexpected HEAD",
    )

    manifest_name = DELIVERY + "/DELIVERY-SHA256SUMS"
    manifest = frozen(manifest_name)
    entries = []
    seen = set()

    for line in manifest.decode().splitlines():
        if not line.strip():
            continue
        expected, name = line.split("  ", 1)
        rel = PurePosixPath(name)
        require(
            len(expected) == 64
            and all(c in "0123456789abcdef" for c in expected),
            "Invalid manifest digest",
        )
        require(
            not rel.is_absolute()
            and ".." not in rel.parts
            and name not in seen,
            "Unsafe or duplicate manifest path",
        )
        seen.add(name)
        entries.append((DELIVERY + "/" + name, expected))

    require(len(entries) == 26, "Expected 26 manifest entries")
    entries.append((manifest_name, sha(manifest)))

    for name, expected in entries:
        raw = frozen(name)
        require(sha(raw) == expected, "Committed hash mismatch: " + name)
        path = REPO / name
        require(
            not path.is_symlink()
            and path.resolve().is_relative_to(REPO),
            "Unsafe evidence path",
        )
        require(
            path.read_bytes() == raw,
            "Local evidence differs from checkpoint: " + name,
        )
        SNAPSHOT[name] = expected

    return {"verified_files": len(entries)}

def controls():
    seed = [0,1,2,3,4,5,6,8,9,10,12,15]
    good = certificate(seed)

    must_reject(seed[:-1])
    must_reject(seed[:-1] + [seed[0]])
    must_reject(seed[:-1] + [64])

    bad_kernel = list(good["primitive_kernel"])
    bad_kernel[0] += 1
    must_reject(seed, bad_kernel)

    require(
        len(rref([[0, 1], [1, 0]])[1]) == 2,
        "Row-swap control failed",
    )
    require(
        len(rref([[1, 2, 3], [2, 4, 6]])[1]) == 1,
        "Dependent-row control failed",
    )
    return {
        "valid_circuit_accepted": True,
        "invalid_inputs_rejected": 4,
        "linear_algebra_controls": 2,
    }

def representatives():
    document = json.loads(frozen(
        DELIVERY +
        "/evidence-package/inputs/reconciliation-report.json"
    ))
    ledger = document["class_ledger"]
    require(len(ledger) == 14, "Expected fourteen representatives")

    checked = []
    seen = set()

    for record in ledger:
        result = certificate(record["representative"])
        require(
            result["pattern"] == record["pattern"],
            "Coefficient pattern differs from preserved report",
        )
        key = tuple(result["canonical_support"])
        require(key not in seen, "Duplicate representative")
        seen.add(key)
        result["class_id"] = record["class_id"]
        checked.append(result)

    for support in (
        [0,1,2,4,8,15,16,23,27,29,30,31],
        [0,1,2,4,8,15,48,55,59,61,62,63],
    ):
        result = certificate(support)
        require(
            result["pattern"] == "1^10 3^2",
            "Odd-twelve seed pattern mismatch",
        )
        result["kind"] = "explicit_odd_twelve_seed"
        checked.append(result)

    (OUT / "CIRCUIT-CERTIFICATES.json").write_text(
        json.dumps(checked, indent=2) + "\n"
    )
    return {
        "preserved_representatives_checked": 14,
        "explicit_odd_twelve_seeds_checked": 2,
        "census_completeness_checked": False,
    }

def unchanged():
    require(len(SNAPSHOT) == 27, "Initial integrity test incomplete")
    for name, expected in SNAPSHOT.items():
        require(
            sha((REPO / name).read_bytes()) == expected,
            "Evidence changed during run: " + name,
        )
    require(
        sha(Path(__file__).read_bytes()) == SOURCE_HASH,
        "Verifier source changed during run",
    )
    return {"evidence_files_unchanged": 27}

def run_test(name, operation):
    print("RUN:", name, flush=True)
    started = time.monotonic()
    try:
        details = operation()
    except Exception as exc:
        REPORT["tests"].append({
            "test": name,
            "status": "FAIL",
            "error": str(exc),
            "traceback": traceback.format_exc(),
        })
        print("FAIL:", name, "-", exc, flush=True)
        raise

    REPORT["tests"].append({
        "test": name,
        "status": "PASS_WITHIN_SCOPE",
        "seconds": round(time.monotonic() - started, 3),
        "details": details,
    })
    print("PASS:", name, flush=True)

exit_code = 2
try:
    run_test("frozen_delivery_integrity", integrity)
    run_test("checker_positive_and_negative_controls", controls)
    run_test("selected_exact_circuit_checks", representatives)
    run_test("final_evidence_integrity", unchanged)
    REPORT["status"] = "PASS_FOR_BOUNDED_VALIDATION_ONLY"
    exit_code = 0
except Exception:
    REPORT["status"] = "FAIL_OR_BLOCKED"
    REPORT["fatal_traceback"] = traceback.format_exc()
finally:
    REPORT["elapsed_seconds"] = round(time.monotonic() - START, 3)
    REPORT["finished_utc"] = datetime.now(timezone.utc).isoformat()
    (OUT / "REPORT.json").write_text(
        json.dumps(REPORT, indent=2) + "\n"
    )
    (OUT / "SHA256SUMS").write_text(
        "".join(
            sha(p.read_bytes()) + "  " + p.name + "\n"
            for p in sorted(OUT.iterdir())
            if p.is_file() and p.name != "SHA256SUMS"
        )
    )

print("\n=== FINAL ===")
print("STATUS:", REPORT["status"])
print("RESULTS:", OUT)
print("FULL CENSUS VERIFIED: FALSE")
print("NO STAGING, COMMIT, PUSH, OR PR")
print("PROMOTION: FALSE")
sys.exit(exit_code)
