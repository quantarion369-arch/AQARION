
import csv
import hashlib
import json
import platform
import sys
import time
import traceback
from collections import Counter
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parent
PRIOR = Path("/root/aqarionz-sandbox/eight-state-multigroup-jla1t1yp")
T = (5, 6, 6, 5, 0, 2, 0, 2)
EXPECTED_GROUPS = {
    1: 1, 2: 127, 3: 966, 4: 1701,
    5: 1050, 6: 266, 7: 28, 8: 1,
}


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    (ROOT / name).write_text(
        json.dumps(value, indent=2, sort_keys=True) + chr(10)
    )


def partitions(prefix=(0,)):
    if len(prefix) == 8:
        yield prefix
    else:
        for label in range(max(prefix) + 2):
            yield from partitions(prefix + (label,))


def equivalent(labels, x, y):
    seen = set()
    while (x, y) not in seen:
        if labels[x] != labels[y]:
            return False
        seen.add((x, y))
        x, y = T[x], T[y]
    return True


save("status.json", {"complete": False})
started = time.monotonic()
checked = 0

try:
    manifest = PRIOR / "artifacts/SHA256SUMS"
    need(manifest.is_file(), "Prior artifact manifest missing")
    verified = set()
    for line in manifest.read_text().splitlines():
        expected, name = line.split(None, 1)
        name = name.lstrip("*")
        path = (manifest.parent / name).resolve()
        need(path.parent == manifest.parent.resolve(),
             "Unexpected manifest path")
        need(sha(path) == expected, "Prior checksum mismatch: " + name)
        verified.add(path.name)
    need("partitions.csv" in verified and "report.json" in verified,
         "Prior CSV or report is not covered by manifest")

    original_csv = PRIOR / "artifacts/partitions.csv"
    original_report = PRIOR / "artifacts/report.json"
    csv_data = original_csv.read_bytes()
    report_data = original_report.read_bytes()
    (ROOT / "production-partitions.csv").write_bytes(csv_data)
    (ROOT / "production-report.json").write_bytes(report_data)
    prior_report = json.loads(report_data)

    need(prior_report["result"] == "PASS", "Prior report is not PASS")
    need(tuple(prior_report["transition_map"]) == T, "Transition map differs")
    need(prior_report["partitions_checked"] == 4140, "Prior scope differs")
    save("input-hashes.json", {
        "source_receipt": str(PRIOR),
        "production_csv_sha256": hashlib.sha256(csv_data).hexdigest(),
        "production_report_sha256": hashlib.sha256(report_data).hexdigest(),
        "prior_artifact_manifest_sha256": sha(manifest),
    })

    records = list(csv.DictReader(csv_data.decode().splitlines()))
    labels_list = [
        tuple(json.loads(row["labels"])) for row in records
    ]
    canonical = set(partitions())
    need(len(records) == len(set(labels_list)) == len(canonical) == 4140,
         "Partition count or uniqueness mismatch")
    need(set(labels_list) == canonical, "Partition coverage mismatch")

    A = sp.zeros(8)
    for x, target in enumerate(T):
        A[target, x] = 1
    powers = [sp.eye(8)]
    for _ in range(7):
        powers.append(powers[-1] * A)

    distribution = Counter()
    groups_count = Counter()
    joint = Counter()
    maxima = {}
    fields = [
        "labels", "initial_groups", "independent_stable_classes",
        "independent_rank", "independent_gap",
        "production_stable_classes", "production_rank",
        "production_gap", "match",
    ]

    with (ROOT / "comparisons.csv").open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(fields)

        for record, labels in zip(records, labels_list):
            groups = sorted(set(labels))
            relation = [
                tuple(equivalent(labels, x, y) for y in range(8))
                for x in range(8)
            ]
            stable = len(set(relation))

            H = sp.Matrix([
                [int(label == group) for label in labels]
                for group in groups
            ])
            O = sp.Matrix.vstack(*[H * power for power in powers])
            rank = int(O.rank())
            gap = stable - rank
            expected = (
                int(record["stable_classes"]),
                int(record["observable_rank"]),
                int(record["gap"]),
            )
            observed = (stable, rank, gap)
            matches = observed == expected

            writer.writerow([
                json.dumps(labels), len(groups), stable, rank, gap,
                *expected, matches,
            ])
            if not matches:
                save("mismatch.json", {
                    "labels": labels,
                    "independent": observed,
                    "production": expected,
                    "behavioral_equivalence_rows": relation,
                })
                raise RuntimeError("Independent mismatch: " + repr(labels))

            k = len(groups)
            need(k == int(record["initial_groups"]),
                 "Initial group count differs")
            need(k <= rank <= stable <= 8, "Dimension bounds failed")
            distribution[gap] += 1
            groups_count[k] += 1
            joint[k, gap] += 1
            if k not in maxima or gap > maxima[k]["gap"]:
                maxima[k] = {"gap": gap, "labels": labels}
            checked += 1
            if checked % 250 == 0:
                print("PROGRESS:", checked, "/ 4140", flush=True)

    need(dict(groups_count) == EXPECTED_GROUPS, "Group totals differ")
    expected_distribution = {
        int(k): v for k, v in prior_report["distribution"].items()
    }
    need(dict(distribution) == expected_distribution,
         "Aggregate distribution differs")
    need(original_csv.read_bytes() == csv_data, "Prior CSV changed")
    need(original_report.read_bytes() == report_data, "Prior report changed")

    with (ROOT / "group-gap-counts.csv").open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["initial_groups", "gap", "count"])
        for (k, gap), count in sorted(joint.items()):
            writer.writerow([k, gap, count])

    binary = maxima[2]["gap"]
    multigroup = max(maxima[k]["gap"] for k in range(3, 9))
    report = {
        "result": "PASS",
        "transition_map": T,
        "partitions_checked": checked,
        "all_per_partition_results_match": True,
        "independent_behavioral_method": "pair trajectories until repeat",
        "independent_rank_method": "exact SymPy rank of stacked H*A**t",
        "production_evaluator_imported": False,
        "distribution": dict(sorted(distribution.items())),
        "maxima_by_groups": maxima,
        "best_binary_gap": binary,
        "best_multigroup_gap": multigroup,
        "python": platform.python_version(),
        "python_executable": sys.executable,
        "sympy": sp.__version__,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "scope": "one fixed map, all 4140 partitions; not all eight-state maps",
    }
    save("report.json", report)
    save("status.json", {"complete": True, "result": "PASS"})
    print("PASS: all 4140 per-partition results independently matched.")
    print("DISTRIBUTION:", dict(sorted(distribution.items())))
    print("BEST BINARY GAP:", binary)
    print("BEST MULTIGROUP GAP:", multigroup)

except Exception as error:
    save("status.json", {
        "complete": True, "result": "FAIL",
        "partitions_matched_before_failure": checked,
        "error": type(error).__name__ + ": " + str(error),
    })
    traceback.print_exc()
    sys.exit(1)
