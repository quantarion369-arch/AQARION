#!/usr/bin/env python3
"""Group SM003 mutants by their complete finite detection sets.

The script imports the repository's exact-rational mutations.py and uses
its existing case_values(), parts(), and mutant registries.

A signature is the complete set of enumerated (map, partition) cases that
detect a mutant. Equal detection counts do not imply equal signatures.

This is bounded computational evidence only. It does not prove universal
equivalence; the R:first / D:KP(I-P) equivalence is addressed separately
in SM003/RANK_IDENTITY.md.
"""
from future import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import platform
import sys
from pathlib import Path

HERE = Path(file).resolve().parent
MUTATIONS_PATH = HERE / "mutations.py"

spec = importlib.util.spec_from_file_location(
"sm003_mutations_for_signatures", MUTATIONS_PATH
)
if spec is None or spec.loader is None:
raise RuntimeError(f"Cannot load SM003 mutation engine: {MUTATIONS_PATH}")

sm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sm)

CANONICAL_MUTANTS = tuple((*sm.D_MUTANTS, *sm.R_MUTANTS))

def sha256_file(path: Path) -> str:
digest = hashlib.sha256()
with path.open("rb") as handle:
for chunk in iter(lambda: handle.read(1024 * 1024), b""):
digest.update(chunk)
return digest.hexdigest()

def case_id(n: int, transition, blocks) -> str:
"""Stable, readable identifier for a labelled enumeration case."""
normalized_blocks = [list(block) for block in blocks]
return json.dumps(
{
"n": n,
"transition": list(transition),
"partition": normalized_blocks,
},
sort_keys=True,
separators=(",", ":"),
)

def enumerate_detection_sets(max_n: int):
if not 1 <= max_n <= 5:
raise ValueError("--max-n must be in 1..5")

detected_cases = {mutant: [] for mutant in CANONICAL_MUTANTS}
cases_by_n = {}
total_cases = 0
theorem_mismatches = 0

for n in range(1, max_n + 1):
    partitions = list(sm.parts(n))
    cases_n = 0

    for transition in itertools.product(range(n), repeat=n):
        for partition in partitions:
            values = sm.case_values(transition, partition)
            cases_n += 1
            total_cases += 1

            if values["baseline_rank"] != values["graph_prediction"]:
                theorem_mismatches += 1

            identifier = case_id(n, transition, partition)
            detected = set(values["detected"])

            for mutant in CANONICAL_MUTANTS:
                if mutant in detected:
                    detected_cases[mutant].append(identifier)

    expected = n ** n * len(partitions)
    if cases_n != expected:
        raise AssertionError(
            f"n={n}: enumerated {cases_n} cases, expected {expected}"
        )

    cases_by_n[str(n)] = {
        "map_count": n ** n,
        "partition_count": len(partitions),
        "partition_map_pairs": cases_n,
        "expected_partition_map_pairs": expected,
    }

if theorem_mismatches:
    raise AssertionError(
        f"rank identity mismatches found: {theorem_mismatches}"
    )

return {
    "max_n": max_n,
    "total_cases": total_cases,
    "cases_by_n": cases_by_n,
    "detected_cases": detected_cases,
}

def group_signatures(detected_cases):
"""Group canonical mutants with identical complete detection sets."""
groups = {}
for mutant, cases in detected_cases.items():
# Cases are generated in a deterministic enumeration order.
signature_key = json.dumps(cases, separators=(",", ":"))
groups.setdefault(signature_key, []).append(mutant)

result = []
for signature_key, mutants in groups.items():
    cases = json.loads(signature_key)
    result.append(
        {
            "mutants": sorted(mutants),
            "detection_count": len(cases),
            "detection_set_sha256": hashlib.sha256(
                signature_key.encode("utf-8")
            ).hexdigest(),
            "detected_case_ids": cases,
        }
    )

result.sort(
    key=lambda item: (
        item["mutants"],
        item["detection_set_sha256"],
    )
)
return result

def build_report(max_n: int, include_case_ids: bool):
enumeration = enumerate_detection_sets(max_n)
signatures = group_signatures(enumeration["detected_cases"])

if not include_case_ids:
    for signature in signatures:
        signature.pop("detected_case_ids", None)

return {
    "schema": "AQ-SM003-DETECTION-SIGNATURES/1",
    "status": "PASS",
    "scope": {
        "n_min": 1,
        "n_max": max_n,
        "cases": enumeration["total_cases"],
        "cases_by_n": enumeration["cases_by_n"],
    },
    "method": (
        "Exact-rational mutations.py evaluation; group mutants by "
        "identical complete finite detection sets."
    ),
    "canonical_mutant_count": len(CANONICAL_MUTANTS),
    "signature_count": len(signatures),
    "signatures": signatures,
    "source_sha256": {
        "mutations.py": sha256_file(MUTATIONS_PATH),
        "manifest.json": sha256_file(HERE / "manifest.json"),
    },
    "environment": {
        "python": sys.version,
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
    },
    "limitations": [
        "Equal finite signatures establish equivalence only on this census.",
        "Different detection counts imply different signatures; equal counts do not imply equal signatures.",
        "The universal R:first / D:KP(I-P) result relies on the separate mathematical proof.",
        "This report does not certify Lean, a clean checkout, or a repository release.",
    ],
}

def main():
parser = argparse.ArgumentParser(description=doc)
parser.add_argument("--max-n", type=int, default=4)
parser.add_argument(
"--report",
type=Path,
help="Optional path for the JSON report; parent directories are created.",
)
parser.add_argument(
"--no-indices",
action="store_true",
help="Omit the full list of detected case IDs from each signature.",
)
args = parser.parse_args()

try:
    report = build_report(args.max_n, include_case_ids=not args.no_indices)
    output = json.dumps(report, indent=2, sort_keys=True) + "\n"
    sys.stdout.write(output)

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output, encoding="utf-8")

    return 0
except Exception as exc:
    failure = {
        "schema": "AQ-SM003-DETECTION-SIGNATURES/1",
        "status": "FAIL",
        "error": f"{type(exc).__name__}: {exc}",
    }
    output = json.dumps(failure, indent=2, sort_keys=True) + "\n"
    sys.stderr.write(output)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output, encoding="utf-8")
    return 1

if name == "main":
raise SystemExit(main())
