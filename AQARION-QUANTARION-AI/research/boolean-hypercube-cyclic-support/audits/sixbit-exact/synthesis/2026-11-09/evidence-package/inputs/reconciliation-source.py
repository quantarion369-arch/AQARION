import collections
import hashlib
import itertools
import json
import os
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

import sympy as sp

OUT = Path(sys.argv[1]).resolve()
OUT.mkdir(exist_ok=False)

report = {
    "experiment": "SIX-FLAT-472-CLASS-RECONCILIATION",
    "started_utc": datetime.now(timezone.utc).isoformat(),
    "promotion": {"allowed": False},
    "status": "RUNNING",
    "inputs": {},
    "boundaries": [
        "This is class reconciliation, not another extension search.",
        "No explicit enumeration of every global support.",
        "Completeness depends on the six-flat replay and parity-flat reduction.",
        "Digest consistency is not external provenance authentication.",
        "No odd-twelve, combined 497056, Lean, CI or novelty certification."
    ]
}

tracked = {}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def read_bound(path):
    path = Path(path).expanduser().resolve()
    require(path.is_file(), "Missing input: " + str(path))
    raw = path.read_bytes()
    digest = sha_bytes(raw)
    if path in tracked:
        require(tracked[path] == digest, "Input changed: " + str(path))
    tracked[path] = digest
    report["inputs"][str(path)] = digest
    return raw


def load(path):
    return json.loads(read_bound(path).decode("utf-8"))


def image(support, transformation):
    return tuple(sorted(transformation[x] for x in support))


def parse_records(value):
    found = []

    def walk(obj):
        if isinstance(obj, list):
            if (
                len(obj) == 472
                and all(
                    isinstance(r, dict)
                    and "support" in r
                    and "primitive_kernel" in r
                    for r in obj
                )
            ):
                found.append(obj)
            else:
                for item in obj:
                    walk(item)
        elif isinstance(obj, dict):
            for item in obj.values():
                walk(item)

    walk(value)
    require(
        len(found) == 1,
        "Unsupported or ambiguous historical record schema"
    )
    return found[0]


try:
    home = Path.home()
    experiments = home / "AQARION-EXPERIMENTS"

    explicit = os.environ.get("SIX_FLAT_RUN", "").strip()
    if explicit:
        run = Path(explicit).expanduser().resolve()
    else:
        candidates = []
        for directory in experiments.glob("six-flat-independent.*"):
            path = directory / "results/REPORT.json"
            if not path.is_file():
                continue
            try:
                candidate = json.loads(path.read_text(encoding="utf-8"))
                if (
                    candidate.get("experiment")
                    == "SIX-FLAT-INDEPENDENT-TERMUX-REPLAY"
                    and candidate.get("status")
                    == "PASS_FOR_DECLARED_SCOPE"
                ):
                    candidates.append(directory.resolve())
            except Exception:
                continue

        require(
            len(candidates) == 1,
            "Expected exactly one completed six-flat replay. "
            "If several exist, set SIX_FLAT_RUN to the chosen execution directory."
        )
        run = candidates[0]

    print("SIX-FLAT EXECUTION:", run, flush=True)

    replay_report = load(run / "results/REPORT.json")
    require(
        replay_report["experiment"]
        == "SIX-FLAT-INDEPENDENT-TERMUX-REPLAY",
        "Wrong replay experiment"
    )
    require(
        replay_report["status"] == "PASS_FOR_DECLARED_SCOPE",
        "Six-flat replay has not passed"
    )
    require(
        replay_report["total_extensions"] == 2203740,
        "Unexpected replay extension count"
    )

    replay_source = read_bound(run / "replay.py")
    require(
        sha_bytes(replay_source) == replay_report["source_sha256"],
        "Replay source differs from recorded source"
    )

    pairs = list(itertools.combinations(range(6), 2))

    def feature(x):
        bits = [(x >> i) & 1 for i in range(6)]
        return (
            [1] + bits
            + [bits[i] * bits[j] for i, j in pairs]
        )

    A = sp.Matrix.hstack(
        *[sp.Matrix(feature(x)) for x in range(64)]
    )

    bases = [
        (0, 7, 25, 30, 42, 45, 51, 52),
        (0, 3, 5, 6, 9, 10, 12, 15),
        (0, 1, 6, 7, 10, 11, 12, 13),
        (0, 3, 5, 6, 24, 27, 29, 30),
        (0, 1, 6, 7, 26, 27, 28, 29),
        (0, 3, 12, 15, 21, 22, 25, 26)
    ]

    def root_swap(x, j):
        bits = [0] + [(x >> i) & 1 for i in range(6)]
        bits[0], bits[j] = bits[j], bits[0]
        return sum(
            (bits[i] ^ bits[0]) << (i - 1)
            for i in range(1, 7)
        )

    root_generators = [
        tuple(root_swap(x, j) for x in range(64))
        for j in range(1, 7)
    ]
    translation_generators = [
        tuple(x ^ (1 << j) for x in range(64))
        for j in range(6)
    ]

    print("CHECKING FEATURE-SPACE ACTION", flush=True)
    for generator in root_generators + translation_generators:
        require(
            sorted(generator) == list(range(64)),
            "Generator is not bijective"
        )
        require(
            A.col_join(A[:, list(generator)]).rank() == 22,
            "Generator does not preserve rational feature space"
        )

    def validate(record):
        support = record["support"]
        values = record["primitive_kernel"]

        require(
            isinstance(support, list)
            and isinstance(values, list)
            and len(support) == len(values) == 12,
            "Invalid support/kernel shape"
        )
        require(
            all(type(x) is int and 0 <= x < 64 for x in support),
            "Invalid support point"
        )
        require(len(set(support)) == 12, "Repeated support point")
        require(
            all(type(v) is int and v != 0 for v in values),
            "Invalid kernel coefficient"
        )

        import math
        require(
            math.gcd(*[abs(v) for v in values]) == 1,
            "Nonprimitive kernel"
        )

        matrix = A[:, support]
        require(
            matrix * sp.Matrix(values) == sp.zeros(22, 1),
            "Exact kernel identity failed"
        )
        require(matrix.rank() == 11, "Circuit rank is not eleven")

        odd = tuple(sorted(
            x for x, value in zip(support, values)
            if value % 2
        ))
        require(len(odd) == 8, "Odd support is not eight points")

        origin = odd[0]
        direction = {x ^ origin for x in odd}
        require(
            all(x ^ y in direction for x in direction for y in direction),
            "Odd support is not an affine flat"
        )
        require(
            A[:, list(odd)].rank() == 8,
            "Odd flat rank is not eight"
        )

        counts = collections.Counter(abs(v) for v in values)
        pattern = " ".join(
            f"{v}^{counts[v]}" for v in sorted(counts)
        )
        return tuple(sorted(support)), odd, pattern

    rows = replay_report["rows"]
    require(len(rows) == 6, "Expected six replay rows")

    local_sets = []
    local_patterns = []

    print("READING AND CHECKING REPLAY CIRCUITS", flush=True)
    for number, base in enumerate(bases, 1):
        row = rows[number - 1]
        require(row["row"] == number, "Replay row order differs")
        require(
            tuple(row["base_flat"]) == base,
            "Replay base differs"
        )

        raw = read_bound(
            run / "results" / f"BASE-{number}-CIRCUITS.jsonl"
        )
        require(
            sha_bytes(raw) == row["circuit_file_sha256"],
            "Replay circuit file hash mismatch"
        )

        records = [
            json.loads(line)
            for line in raw.decode("utf-8").splitlines()
            if line.strip()
        ]

        supports = set()
        patterns = {}

        for record in records:
            support, odd, pattern = validate(record)
            require(odd == base, "Local circuit has wrong odd flat")
            require(support not in supports, "Duplicate local support")
            supports.add(support)
            patterns[support] = pattern

        require(
            len(supports) == row["accepted"],
            "Local accepted count differs from report"
        )

        local_sets.append(supports)
        local_patterns.append(patterns)

        print(
            "BASE", number, "VALID CIRCUITS:", len(supports),
            flush=True
        )

    require(
        sum(map(len, local_sets)) == 160,
        "Local circuit total is not 160"
    )

    # Each stored transporter maps a canonical base direction
    # to the direction serving as its dictionary key.
    transporters = {}
    direction_sizes = []

    for index, base in enumerate(bases):
        identity = tuple(range(64))
        mappings = {base: identity}
        pending = [base]

        while pending:
            direction = pending.pop()
            current = mappings[direction]
            for generator in root_generators:
                transformed = image(direction, generator)
                if transformed not in mappings:
                    mappings[transformed] = tuple(
                        generator[current[x]] for x in range(64)
                    )
                    pending.append(transformed)

        for direction, mapping in mappings.items():
            require(
                direction not in transporters,
                "Canonical direction orbits overlap"
            )
            inverse = [0] * 64
            for x, y in enumerate(mapping):
                inverse[y] = x
            transporters[direction] = (index, tuple(inverse))

        direction_sizes.append(len(mappings))

    require(
        len(transporters) == 1045,
        "Direction-transporter coverage differs"
    )

    masks = [0] + [1 << j for j in range(6)]

    def linear_image(x, rows):
        return sum(
            ((x & row).bit_count() % 2) << j
            for j, row in enumerate(rows)
        )

    class_for_local_support = {}
    class_ledger = []

    print("RECONSTRUCTING LOCAL STABILIZER CLASSES", flush=True)

    for index, base in enumerate(bases):
        supports = local_sets[index]
        flat_weight = 8 * direction_sizes[index]

        require(
            flat_weight == rows[index]["flat_orbit_size"],
            "Recomputed flat weight differs"
        )

        if not supports:
            continue

        stabilizer = set()
        for permutation in itertools.permutations(range(7)):
            linear_rows = tuple(
                masks[permutation[j]] ^ masks[permutation[0]]
                for j in range(1, 7)
            )
            if tuple(sorted(
                linear_image(x, linear_rows) for x in base
            )) != base:
                continue

            for translation in base:
                stabilizer.add(tuple(
                    linear_image(x, linear_rows) ^ translation
                    for x in range(64)
                ))

        require(
            len(stabilizer) * flat_weight == 322560,
            "Flat orbit-stabilizer identity failed"
        )

        unseen = set(supports)

        while unseen:
            representative = min(unseen)
            members = {
                image(representative, g) for g in stabilizer
            }

            require(
                members <= supports,
                "Replay accepted set is not stabilizer-closed"
            )
            require(
                members <= unseen,
                "Local classes overlap"
            )

            patterns = {
                local_patterns[index][support]
                for support in members
            }
            require(len(patterns) == 1, "Pattern varies inside class")

            class_id = len(class_ledger) + 1
            for support in members:
                class_for_local_support[(index, support)] = class_id

            circuit_stabilizer = sum(
                image(representative, g) == representative
                for g in stabilizer
            )
            require(
                len(members) * circuit_stabilizer == len(stabilizer),
                "Circuit orbit-stabilizer identity failed"
            )

            class_ledger.append({
                "class_id": class_id,
                "base_row": index + 1,
                "representative": representative,
                "pattern": next(iter(patterns)),
                "local_class_size": len(members),
                "flat_orbit_size": flat_weight,
                "circuit_stabilizer_order": circuit_stabilizer,
                "full_orbit_size": flat_weight * len(members)
            })
            unseen -= members

    historical = (
        home / "AQARION/AQARION-QUANTARION-AI"
        / "research/boolean-hypercube-cyclic-support"
        / "audits/sixbit-exact/experiments"
        / "ODD-EIGHT-QUOTIENT-008/run-tQhJSezz"
        / "REPRESENTATIVE-CIRCUITS.json"
    )

    raw = read_bound(historical)
    require(
        sha_bytes(raw)
        == "fd85dd9977c015efde2a22c8e9b52eefff210970ec7858fd9294cb2fb13647d1",
        "Historical input differs from pinned digest"
    )

    records = parse_records(json.loads(raw.decode("utf-8")))
    historical_supports = set()
    class_hits = collections.Counter()
    assignments = []

    print("TRANSPORTING THE 472 HISTORICAL RECORDS", flush=True)

    for number, record in enumerate(records, 1):
        support, odd, pattern = validate(record)
        require(
            support not in historical_supports,
            "Duplicate historical support"
        )
        historical_supports.add(support)

        origin = odd[0]
        direction = tuple(sorted(x ^ origin for x in odd))
        require(
            direction in transporters,
            "Historical odd-flat direction not in eligible universe"
        )

        index, inverse = transporters[direction]
        normalized = tuple(sorted(
            inverse[x ^ origin] for x in support
        ))
        normalized_odd = tuple(sorted(
            inverse[x ^ origin] for x in odd
        ))
        require(
            normalized_odd == bases[index],
            "Transporter sends odd support to wrong base"
        )

        key = (index, normalized)
        require(
            key in class_for_local_support,
            "Historical circuit is absent from replayed local family"
        )

        class_id = class_for_local_support[key]
        require(
            pattern == class_ledger[class_id - 1]["pattern"],
            "Transported coefficient pattern differs"
        )

        class_hits[class_id] += 1
        assignments.append({
            "historical_record": number,
            "class_id": class_id,
            "base_row": index + 1,
            "normalized_support": normalized
        })

        if number % 25 == 0:
            print("HISTORICAL RECORDS CHECKED:", number, "/ 472",
                  flush=True)

    missing_classes = [
        row["class_id"] for row in class_ledger
        if class_hits[row["class_id"]] == 0
    ]

    for row in class_ledger:
        row["historical_record_hits"] = class_hits[row["class_id"]]

    weighted_patterns = collections.Counter()
    for row in class_ledger:
        weighted_patterns[row["pattern"]] += row["full_orbit_size"]

    report.update({
        "six_flat_execution": str(run),
        "historical_records_checked": len(records),
        "direction_transporters": len(transporters),
        "derived_circuit_class_count": len(class_ledger),
        "class_ledger": class_ledger,
        "historically_unrepresented_classes": missing_classes,
        "weighted_pattern_counts": dict(weighted_patterns),
        "weighted_total": sum(weighted_patterns.values()),
        "all_historical_records_in_replayed_family": True
    })

    (OUT / "ASSIGNMENTS.json").write_text(
        json.dumps(assignments, indent=2, sort_keys=True) + "\n",
        encoding="utf-8"
    )

    require(
        not missing_classes,
        "Historical 472 records do not cover every replayed class"
    )
    require(
        sum(weighted_patterns.values()) == 286720,
        "Class-based weighted total differs"
    )

    report["status"] = "PASS_FOR_DECLARED_CLASS_RECONCILIATION"

except Exception as error:
    report["status"] = "FAIL"
    report["error"] = str(error)
    traceback.print_exc()

finally:
    changed = []
    for path, digest in tracked.items():
        if not path.is_file() or sha_bytes(path.read_bytes()) != digest:
            changed.append(str(path))

    report["inputs_changed_during_run"] = changed
    if changed:
        report["status"] = "FAIL"
        report["input_change_error"] = changed

    report["source_sha256"] = sha_bytes(
        Path(__file__).read_bytes()
    )
    report["finished_utc"] = datetime.now(timezone.utc).isoformat()

    (OUT / "REPORT.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8"
    )

    files = sorted(
        p for p in OUT.iterdir()
        if p.is_file() and p.name != "SHA256SUMS"
    )
    (OUT / "SHA256SUMS").write_text(
        "".join(
            sha_bytes(p.read_bytes()) + "  " + p.name + "\n"
            for p in files
        ),
        encoding="utf-8"
    )

    print("\n=== FINAL ===", flush=True)
    print("STATUS:", report["status"])
    print(
        "HISTORICAL RECORDS:",
        report.get("historical_records_checked", "NOT COMPLETED")
    )
    print(
        "DERIVED CIRCUIT CLASSES:",
        report.get("derived_circuit_class_count", "NOT COMPLETED")
    )
    print(
        "UNREPRESENTED CLASSES:",
        report.get("historically_unrepresented_classes", "NOT COMPLETED")
    )
    print(
        "WEIGHTED PATTERNS:",
        report.get("weighted_pattern_counts")
    )
    print("WEIGHTED TOTAL:", report.get("weighted_total"))
    print("REPORT:", OUT / "REPORT.json")
    print("PROMOTION: FALSE")

sys.exit(
    0 if report["status"]
    == "PASS_FOR_DECLARED_CLASS_RECONCILIATION"
    else 1
)
