import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
import subprocess

def partitions(n):
    for labels in itertools.product(range(n), repeat=n):
        if labels[0] != 0:
            continue
        maximum = 0
        for value in labels[1:]:
            if value > maximum + 1:
                break
            maximum = max(maximum, value)
        else:
            yield [
                [x for x in range(n) if labels[x] == j]
                for j in range(maximum + 1)
            ]

rows, failures = [], []
first_mutant_detection = None
for n, expected in [(1, 1), (2, 8), (3, 135), (4, 3840)]:
    cases = mismatches = detections = 0
    for blocks in partitions(n):
        owner = {x: j for j, b in enumerate(blocks) for x in b}
        scale = math.lcm(*(len(b) for b in blocks))
        P = [
            [
                scale // len(blocks[owner[x]])
                if owner[x] == owner[y] else 0
                for y in range(n)
            ]
            for x in range(n)
        ]
        for T in itertools.product(range(n), repeat=n):
            KP = [P[T[x]][:] for x in range(n)]
            numerator = [
                [
                    scale * KP[x][y]
                    - sum(P[x][z] * KP[z][y] for z in range(n))
                    for y in range(n)
                ]
                for x in range(n)
            ]
            energy = Fraction(
                sum(v * v for row in numerator for v in row),
                scale ** 4
            )
            formula, mutant = Fraction(0), 0
            for b in blocks:
                for j, c in enumerate(blocks):
                    m = sum(owner[T[x]] == j for x in b)
                    top = m * (len(b) - m)
                    bottom = len(b) * len(c)
                    formula += Fraction(top, bottom)
                    mutant += top // bottom
            cases += 1
            if energy != formula:
                mismatches += 1
                failures.append({
                    "n": n, "T": T, "blocks": blocks,
                    "energy": str(energy), "formula": str(formula)
                })
            if energy != mutant:
                detections += 1
                if first_mutant_detection is None:
                    first_mutant_detection = {
                        "n": n, "T": T, "blocks": blocks,
                        "exact_energy": str(energy),
                        "floor_mutant": mutant
                    }
    rows.append({
        "n": n, "cases": cases, "expected_cases": expected,
        "energy_mismatches": mismatches,
        "floor_mutant_detections": detections
    })
    print(rows[-1], flush=True)

passed = (
    not failures
    and all(r["cases"] == r["expected_cases"] for r in rows)
    and first_mutant_detection is not None
)
here = Path(__file__).resolve().parent
report = {
    "claim": "SM003 exact Frobenius-energy cross-check",
    "tested_commit": subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True
    ).strip(),
    "arithmetic": "integer-scaled matrix plus Fraction",
    "production_imports": False,
    "rows": rows,
    "failures": failures,
    "first_floor_mutant_detection": first_mutant_detection,
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "status": "PASS" if passed else "FAIL"
}
(here / "report.json").write_text(json.dumps(report, indent=2))
print("EXACT_ENERGY_STATUS:", report["status"])
print("REPORT:", here / "report.json")
raise SystemExit(0 if passed else 1)
