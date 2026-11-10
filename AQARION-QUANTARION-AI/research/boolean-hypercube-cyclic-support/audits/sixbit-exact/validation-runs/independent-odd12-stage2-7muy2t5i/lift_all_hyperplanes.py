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
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

REPO = Path(sys.argv[1]).resolve()
PREV = Path(sys.argv[2]).resolve()
OUT = Path(sys.argv[3]).resolve()
COMMIT = "5093e2af9db66567cba85caaff34220f1f8a0b35"
HISTORICAL = (
    "AQARION-QUANTARION-AI/research/"
    "boolean-hypercube-cyclic-support/audits/sixbit-exact/"
    "synthesis/2026-11-09/evidence-package/inputs/odd12-report.json"
)
START = time.monotonic()
REPORT = {
    "status": "RUNNING",
    "experiment": "DIRECT_ALL_126_HYPERPLANES",
    "commit": COMMIT,
    "started_utc": datetime.now(timezone.utc).isoformat(),
    "source_sha256": hashlib.sha256(
        Path(__file__).read_bytes()
    ).hexdigest(),
    "full_census_verified": False,
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

def binary_rank(values):
    pivots = {}
    for value in values:
        while value:
            bit = value.bit_length() - 1
            if bit in pivots:
                value ^= pivots[bit]
            else:
                pivots[bit] = value
                break
    return len(pivots)

exit_code = 2

try:
    need(
        git("rev-parse", "HEAD").decode().strip() == COMMIT,
        "Unexpected HEAD",
    )

    input_hashes = {}
    for line in (PREV / "SHA256SUMS").read_text().splitlines():
        expected, name = line.split("  ", 1)
        rel = PurePosixPath(name)
        need(
            not rel.is_absolute() and ".." not in rel.parts,
            "Unsafe Stage 1 manifest path",
        )
        path = PREV / name
        need(sha(path.read_bytes()) == expected,
             "Stage 1 artifact mismatch: " + name)
        input_hashes[name] = expected

    previous = json.loads((PREV / "REPORT.json").read_text())
    need(
        previous["status"] == "PASS_FOR_FIVEBIT_CANDIDATE_LAYER",
        "Stage 1 did not pass",
    )

    source = (PREV / "reconstruct.py").read_bytes()
    need(
        sha(source) == previous["source_sha256"],
        "Stage 1 source hash mismatch",
    )

    functions = [
        node for node in ast.parse(source.decode()).body
        if isinstance(node, ast.FunctionDef)
        and node.name == "eliminate"
    ]
    need(
        len(functions) == 1 and not functions[0].decorator_list,
        "Expected integer-elimination function not found",
    )
    namespace = {"math": math, "need": need}
    exec(
        compile(
            ast.Module(body=functions, type_ignores=[]),
            str(PREV / "reconstruct.py"),
            "exec",
        ),
        namespace,
    )
    eliminate = namespace["eliminate"]

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

    base = []
    seen_base = set()

    with (PREV / "RANK11-KERNELS.jsonl").open() as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            support = record["support"]
            kernel = record["primitive_kernel"]

            need(
                len(support) == 12
                and all(type(x) is int and 0 <= x < 32
                        for x in support)
                and support == sorted(set(support)),
                "Malformed base support",
            )
            need(
                len(kernel) == 12
                and all(type(v) is int and v != 0 and v % 2
                        for v in kernel)
                and math.gcd(*kernel) == 1,
                "Malformed base kernel",
            )
            key = tuple(support)
            need(key not in seen_base, "Duplicate base support")
            seen_base.add(key)

            rows = [[row[x] for x in support] for row in features]
            need(len(eliminate(rows)[1]) == 11,
                 "Base rank recheck failed")
            need(
                all(
                    sum(c * value for c, value in zip(kernel, row))
                    == 0
                    for row in rows
                ),
                "Base kernel identity failed",
            )
            need(
                binary_rank([x ^ support[0] for x in support]) == 5,
                "Base affine dimension is not five",
            )

            counts = Counter(map(abs, kernel))
            pattern = " ".join(
                f"{v}^{counts[v]}" for v in sorted(counts)
            )
            base.append((support, kernel, pattern))

    need(len(base) == 3808, "Expected 3808 base circuits")
    print("BASE RANKS AND IDENTITIES RECHECKED:", len(base), flush=True)

    frozen = git("show", COMMIT + ":" + HISTORICAL)
    historical = json.loads(frozen)
    (OUT / "FROZEN-ODD12-REPORT.json").write_bytes(frozen)

    families = defaultdict(set)
    seen_global = set()
    cases = []
    tested = 0

    for normal in range(1, 64):
        pivot = normal.bit_length() - 1
        free_bits = [i for i in range(6) if i != pivot]

        for parity in (0, 1):
            lift = []
            pivot_values = []

            for y in range(32):
                x = sum(
                    ((y >> j) & 1) << bit
                    for j, bit in enumerate(free_bits)
                )
                value = parity ^ ((x & normal).bit_count() % 2)
                pivot_values.append(value)
                lift.append(x | (value << pivot))

            accepted = Counter()

            for support, kernel, pattern in base:
                tested += 1

                # Free-coordinate identities were checked above.
                # Check the pivot and its five pairwise products.
                if sum(
                    c * pivot_values[y]
                    for y, c in zip(support, kernel)
                ):
                    continue

                if any(
                    sum(
                        c * pivot_values[y] * ((y >> j) & 1)
                        for y, c in zip(support, kernel)
                    )
                    for j in range(5)
                ):
                    continue

                points = bytes(sorted(lift[y] for y in support))
                need(
                    all(
                        (x & normal).bit_count() % 2 == parity
                        for x in points
                    ),
                    "Lifted hyperplane equation failed",
                )
                need(
                    points not in seen_global,
                    "Duplicate support across hyperplane reconstruction",
                )
                seen_global.add(points)
                families[pattern].add(points)
                accepted[pattern] += 1

            cases.append({
                "normal": normal,
                "parity": parity,
                "counts": dict(accepted),
            })

        if normal % 7 == 0 or normal == 63:
            print(
                "HYPERPLANES CHECKED:", 2 * normal,
                "UNIQUE SUPPORTS:", len(seen_global),
                flush=True,
            )

    need(len(cases) == 126, "Wrong hyperplane count")
    need(tested == 126 * 3808, "Wrong candidate-test count")

    counts = {pattern: len(values)
              for pattern, values in families.items()}
    digests = {}

    for pattern, values in sorted(families.items()):
        ordered = sorted(values)
        raw = b"".join(ordered)
        digests[pattern] = sha(raw)

        # Fixed-width records: twelve unsigned bytes per support.
        (OUT / ("SUPPORTS-" + pattern + ".bin")).write_bytes(raw)

    need(
        counts == historical["global_pattern_counts"],
        "Pattern counts differ from frozen report",
    )
    need(
        digests == historical["support_set_sha256"],
        "Canonical support-set hashes differ from frozen report",
    )
    need(
        len(seen_global)
        == historical["odd_support_twelve_sector_count"]
        == 210336,
        "Odd-twelve total mismatch",
    )

    for name, expected in input_hashes.items():
        need(
            sha((PREV / name).read_bytes()) == expected,
            "Stage 1 artifact changed during this run: " + name,
        )
    need(
        sha(Path(__file__).read_bytes()) == REPORT["source_sha256"],
        "Stage 2 source changed during execution",
    )

    REPORT.update({
        "status": "PASS_FOR_DIRECT_ODD12_RECONSTRUCTION",
        "base_circuits_rechecked": len(base),
        "hyperplanes_visited": len(cases),
        "lift_candidates_tested": tested,
        "distinct_sixbit_supports": len(seen_global),
        "global_pattern_counts": counts,
        "support_set_sha256": digests,
        "historical_support_hashes_match": True,
        "stage1_input_hashes": input_hashes,
        "hyperplane_cases": cases,
        "support_file_format": (
            "Concatenated 12-byte sorted supports; records ordered "
            "lexicographically. Each byte is a point in 0..63."
        ),
        "rank_certificate": (
            "Each base support has exact rank eleven. Projection "
            "to the five free coordinates supplies the lifted "
            "rank lower bound. The checked full-support kernel "
            "supplies the matching upper bound and minimality."
        ),
        "limitations": [
            "General odd-twelve coverage remains conditional on "
            "the cited classical binary-support theorem.",
            "Six-bit ranks are certified by projection and kernel, "
            "not separately eliminated for every lifted support.",
            "Does not establish odd-eight local-search completeness.",
            "Not a full census proof, Lean proof, or novelty certification.",
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
print("SUPPORTS:", REPORT.get("distinct_sixbit_supports"))
print("PATTERN COUNTS:", REPORT.get("global_pattern_counts"))
print("HISTORICAL HASHES MATCH:",
      REPORT.get("historical_support_hashes_match", False))
print("FULL CENSUS VERIFIED: FALSE")
print("RESULTS:", OUT)
print("NO STAGING, COMMIT, PUSH, OR PR")
print("PROMOTION: FALSE")
sys.exit(exit_code)
