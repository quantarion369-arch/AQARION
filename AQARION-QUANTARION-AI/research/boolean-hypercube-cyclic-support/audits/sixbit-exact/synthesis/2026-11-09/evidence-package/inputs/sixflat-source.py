import collections
import hashlib
import itertools as it
import json
import math
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import sympy as sp

OUT = Path(sys.argv[1]).resolve()
OUT.mkdir(exist_ok=False)
started = time.time()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


report = {
    "experiment": "SIX-FLAT-INDEPENDENT-TERMUX-REPLAY",
    "started_utc": datetime.now(timezone.utc).isoformat(),
    "source_sha256": sha(__file__),
    "python": sys.version,
    "numpy": np.__version__,
    "sympy": sp.__version__,
    "rows": [],
    "status": "RUNNING",
    "promotion": {"allowed": False},
    "boundaries": [
        "No original search program or retained circuit list imported.",
        "No direct historical global-support-set comparison.",
        "Parity-flat reduction and symmetry validity remain mathematical dependencies.",
        "No odd-twelve or combined 497056 certification.",
        "No Lean, CI, novelty or publication certification."
    ]
}

try:
    pairs = list(it.combinations(range(6), 2))

    def feature(x):
        bits = [(x >> i) & 1 for i in range(6)]
        return [1] + bits + [
            bits[i] * bits[j] for i, j in pairs
        ]

    A = sp.Matrix.hstack(
        *[sp.Matrix(feature(x)) for x in range(64)]
    )
    require(A.rank() == 22, "Feature matrix rank is not 22")

    extensions = np.array(
        list(it.combinations(range(56), 4)),
        dtype=np.int16
    )
    require(len(extensions) == 367290, "Wrong extension universe")

    determinant_terms = [
        (
            permutation,
            (-1) ** sum(
                permutation[i] > permutation[j]
                for i in range(4)
                for j in range(i + 1, 4)
            )
        )
        for permutation in it.permutations(range(4))
    ]

    bases = [
        (0, 7, 25, 30, 42, 45, 51, 52),
        (0, 3, 5, 6, 9, 10, 12, 15),
        (0, 1, 6, 7, 10, 11, 12, 13),
        (0, 3, 5, 6, 24, 27, 29, 30),
        (0, 1, 6, 7, 26, 27, 28, 29),
        (0, 3, 12, 15, 21, 22, 25, 26)
    ]

    expected_patterns = [
        {},
        {"1^7 2^4 3^1": 8},
        {
            "1^7 2^4 3^1": 8,
            "1^8 2^4": 36,
            "1^6 2^4 3^2": 12
        },
        {
            "1^7 2^4 3^1": 8,
            "1^8 2^4": 12,
            "1^6 2^4 3^2": 4
        },
        {
            "1^7 2^4 3^1": 8,
            "1^8 2^4": 32,
            "1^6 2^4 3^2": 8
        },
        {"1^8 2^4": 24}
    ]

    def root_swap(x, j):
        bits = [0] + [(x >> i) & 1 for i in range(6)]
        bits[0], bits[j] = bits[j], bits[0]
        return sum(
            (bits[i] ^ bits[0]) << (i - 1)
            for i in range(1, 7)
        )

    generators = [
        tuple(root_swap(x, j) for x in range(64))
        for j in range(1, 7)
    ]

    print("CHECKING CUT-ACTION GENERATORS", flush=True)
    for generator in generators:
        require(
            sorted(generator) == list(range(64)),
            "Generator is not bijective"
        )
        require(
            A.col_join(A[:, list(generator)]).rank() == 22,
            "Generator changes rational feature space"
        )

    def direction_orbit(seed):
        found = {tuple(seed)}
        pending = list(found)
        while pending:
            direction = pending.pop()
            for generator in generators:
                transformed = tuple(sorted(
                    generator[x] for x in direction
                ))
                if transformed not in found:
                    found.add(transformed)
                    pending.append(transformed)
        return found

    weighted = collections.Counter()
    seen_directions = set()
    local_count = 0
    deletion_checks = 0

    for number, base in enumerate(bases, 1):
        base_started = time.time()
        print("\nBASE", number, "/ 6:", list(base), flush=True)

        AB = A[:, list(base)]
        require(AB.rank() == 8, "Base rank is not eight")

        left_nullspace = AB.T.nullspace()
        L = sp.Matrix.vstack(*[
            (
                vector * sp.ilcm(*[value.q for value in vector])
            ).T
            for vector in left_nullspace
        ])
        require(
            L.rank() == 14 and L * AB == sp.zeros(14, 8),
            "Invalid quotient map"
        )

        Q = L * A
        outside = [x for x in range(64) if x not in base]

        q = np.array(
            Q[:, outside].tolist(),
            dtype=np.int64
        ) % 1009
        gram = (q.T @ q) % 1009
        blocks = gram[
            extensions[:, :, None],
            extensions[:, None, :]
        ]

        determinants = np.zeros(len(extensions), dtype=np.int64)

        for permutation, sign in determinant_terms:
            product = np.ones(len(extensions), dtype=np.int64)
            for j in range(4):
                product = (
                    product * blocks[:, j, permutation[j]]
                ) % 1009
            determinants = (
                determinants + sign * product
            ) % 1009

        pending = np.flatnonzero(determinants == 0)
        counts = collections.Counter({
            "QUOTIENT_RANK_4": int((determinants != 0).sum())
        })

        print(
            "MODULAR FULL-RANK CERTIFICATES:",
            counts["QUOTIENT_RANK_4"],
            "EXACT FALLBACKS:", len(pending),
            flush=True
        )

        pivot_rows = list(AB.T.rref()[1])
        R = AB[pivot_rows, :].inv() * A[pivot_rows, :]

        accepted = []
        patterns = collections.Counter()

        for progress, position in enumerate(pending, 1):
            extra = [
                outside[int(i)] for i in extensions[position]
            ]
            nullspace = Q[:, extra].nullspace()
            quotient_rank = 4 - len(nullspace)

            if quotient_rank != 3:
                counts[f"QUOTIENT_RANK_{quotient_rank}"] += 1

            else:
                vector = nullspace[0]
                coefficients = (
                    list(-R[:, extra] * vector) + list(vector)
                )

                if any(value == 0 for value in coefficients):
                    counts["ZERO_COEFFICIENT"] += 1

                else:
                    denominator = sp.ilcm(*[
                        value.q for value in coefficients
                    ])
                    values = [
                        int(value * denominator)
                        for value in coefficients
                    ]
                    divisor = math.gcd(*map(abs, values))
                    values = [value // divisor for value in values]

                    ordered = sorted(zip(list(base) + extra, values))
                    support = [x for x, value in ordered]
                    values = [value for x, value in ordered]

                    if values[0] < 0:
                        values = [-value for value in values]

                    matrix = A[:, support]
                    require(
                        matrix * sp.Matrix(values) == sp.zeros(22, 1),
                        "Exact kernel identity failed"
                    )
                    require(
                        matrix.rank() == 11,
                        "Accepted circuit rank differs from eleven"
                    )

                    for removed in range(12):
                        keep = [
                            j for j in range(12) if j != removed
                        ]
                        require(
                            matrix[:, keep].rank() == 11,
                            "Deletion-rank check failed"
                        )
                        deletion_checks += 1

                    odd_support = tuple(
                        x for x, value in zip(support, values)
                        if value % 2
                    )
                    classification = (
                        "ODD_EIGHT_CIRCUIT"
                        if odd_support == base
                        else "OTHER_FULL_SUPPORT_CIRCUIT"
                    )
                    counts[classification] += 1

                    multiplicities = collections.Counter(
                        abs(value) for value in values
                    )
                    pattern = " ".join(
                        f"{value}^{multiplicities[value]}"
                        for value in sorted(multiplicities)
                    )
                    patterns[pattern] += 1

                    accepted.append({
                        "base_row": number,
                        "support": support,
                        "primitive_kernel": values,
                        "classification": classification,
                        "pattern": pattern
                    })

            if progress % 1000 == 0:
                print(
                    "EXACT FALLBACKS:",
                    progress, "/", len(pending),
                    flush=True
                )

        require(
            sum(counts.values()) == 367290,
            "Case accounting does not reconcile"
        )
        require(
            counts.get("OTHER_FULL_SUPPORT_CIRCUIT", 0) == 0,
            "Unexpected full-support sector"
        )

        orbit = direction_orbit(base)
        require(
            not seen_directions.intersection(orbit),
            "Direction orbits overlap"
        )
        seen_directions.update(orbit)
        flat_weight = 8 * len(orbit)

        for pattern, count in patterns.items():
            weighted[pattern] += flat_weight * count

        accepted.sort(key=lambda record: record["support"])
        circuit_file = OUT / f"BASE-{number}-CIRCUITS.jsonl"
        circuit_file.write_text(
            "".join(
                json.dumps(record, sort_keys=True) + "\n"
                for record in accepted
            ),
            encoding="utf-8"
        )

        supports = sorted(
            record["support"] for record in accepted
        )
        canonical_digest = hashlib.sha256(
            json.dumps(
                supports, separators=(",", ":")
            ).encode("utf-8")
        ).hexdigest()

        row = {
            "row": number,
            "base_flat": base,
            "cases_visited": 367290,
            "counts": dict(counts),
            "patterns": dict(patterns),
            "accepted": len(accepted),
            "exact_fallbacks": len(pending),
            "flat_orbit_size": flat_weight,
            "weighted_contribution": flat_weight * len(accepted),
            "circuit_file_sha256": sha(circuit_file),
            "canonical_support_sha256": canonical_digest,
            "matches_previous_sandbox_patterns": (
                dict(patterns) == expected_patterns[number - 1]
            ),
            "seconds": time.time() - base_started
        }

        report["rows"].append(row)
        local_count += len(accepted)

        (OUT / "PROGRESS.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8"
        )

        print("COUNTS:", dict(counts), flush=True)
        print("PATTERNS:", dict(patterns), flush=True)
        print(
            "FLAT ORBIT:", flat_weight,
            "CONTRIBUTION:", row["weighted_contribution"],
            flush=True
        )

    require(
        len(seen_directions) == 1045,
        "Eligible-direction total differs from 1045"
    )
    require(
        all(
            row["matches_previous_sandbox_patterns"]
            for row in report["rows"]
        ),
        "Replay disagrees with sandbox pattern counts"
    )
    require(
        dict(weighted) == {
            "1^7 2^4 3^1": 44800,
            "1^8 2^4": 201600,
            "1^6 2^4 3^2": 40320
        },
        "Weighted pattern totals disagree"
    )

    report.update({
        "status": "PASS_FOR_DECLARED_SCOPE",
        "total_extensions": 2203740,
        "local_circuits": local_count,
        "exact_deletion_checks": deletion_checks,
        "rank_eight_directions": len(seen_directions),
        "weighted_pattern_counts": dict(weighted),
        "weighted_odd_eight_total": sum(weighted.values())
    })

except Exception as error:
    report["status"] = "FAIL"
    report["error"] = str(error)
    traceback.print_exc()

finally:
    report["finished_utc"] = datetime.now(timezone.utc).isoformat()
    report["elapsed_seconds"] = time.time() - started

    (OUT / "REPORT.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8"
    )

    files = sorted(
        path for path in OUT.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    (OUT / "SHA256SUMS").write_text(
        "".join(
            sha(path) + "  " + path.name + "\n"
            for path in files
        ),
        encoding="utf-8"
    )

    print("\n=== FINAL ===", flush=True)
    print("STATUS:", report["status"])
    print("TOTAL EXTENSIONS:", report.get("total_extensions"))
    print("LOCAL CIRCUITS:", report.get("local_circuits"))
    print("DELETION CHECKS:", report.get("exact_deletion_checks"))
    print("WEIGHTED PATTERNS:", report.get("weighted_pattern_counts"))
    print("ODD-EIGHT TOTAL:", report.get("weighted_odd_eight_total"))
    print("REPORT:", OUT / "REPORT.json")
    print("PROMOTION: FALSE")

sys.exit(
    0 if report["status"] == "PASS_FOR_DECLARED_SCOPE"
    else 1
)
