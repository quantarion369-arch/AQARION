from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from math import comb
import ast
import csv
import hashlib
import json
import platform

ROOT = Path(__file__).resolve().parent
RESEARCH = (
    Path.home() / "AQARION"
    / "AQARION-QUANTARION-AI/research/ordered-cycle-ratio-audit"
)
PARENTS = {
    "ratio-decision": (
        "79b143136ff778001603c805bd006d87ef2c8f7af5f04e650802e3f9a1e3b4d1",
        "c8ed537c602dac71ad16f3b668a5f2466446804b1ad6251a418024e0cd933724"
    ),
    "canonical-ratio-bridge": (
        "18dcc25d80132b1480f5f5d9c94f7645567196a3e41c42bce83640fb2f63274c",
        "686a851bccb7c433a7bd659e4feb89fee2927c74ca702dfa5bece7df939134ab"
    )
}

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read(path):
    need(path.is_file() and not path.is_symlink(), "Missing or linked input")
    return path.read_bytes()

def load_csv(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))

def floor_log(x, p):
    result = 0
    while x >= p:
        x //= p
        result += 1
    return result

def bounds(n, m):
    need(type(n) is int and type(m) is int and 1 <= m <= n,
         "Require integer 1<=m<=n")
    old = comb(n-1, m-1)
    d = n-m
    if d == 0:
        return old, 1
    deficit = sum(
        comb(d-1, j-1)
        for j in range(1, min(m, d)+1)
    )
    return old, min(old, deficit)

def save_csv(name, rows):
    path = ROOT / name
    with path.open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return sha(path.read_bytes())

source = Path(__file__).read_bytes()
bindings = {}
parent_sources = {}

for name, (source_hash, receipt_hash) in PARENTS.items():
    folder = RESEARCH / name
    raw_source = read(folder / "audit.py")
    raw_receipt = read(folder / "receipt.json")
    need(sha(raw_source) == source_hash, "Parent source differs")
    need(sha(raw_receipt) == receipt_hash, "Parent receipt differs")
    receipt = json.loads(raw_receipt)
    need(receipt["status"] == "PASS", "Parent is not PASS")
    need(receipt["source_sha256"] == source_hash, "Source binding differs")
    files = {"audit.py": source_hash, "receipt.json": receipt_hash}
    for filename, expected in receipt["table_sha256"].items():
        need(Path(filename).name == filename, "Unexpected table path")
        need(sha(read(folder / filename)) == expected, "Parent CSV differs")
        files[filename] = expected
    bindings[name] = files
    parent_sources[name] = raw_source

tree = ast.parse(parent_sources["ratio-decision"])
nodes = [
    node for node in tree.body
    if isinstance(node, ast.FunctionDef)
    and node.name == "interval_decision"
]
need(len(nodes) == 1, "Decision-function extraction differs")
namespace = {}
exec(
    compile(ast.Module(body=nodes, type_ignores=[]),
            "published-interval-decision", "exec"),
    namespace
)
decision = namespace["interval_decision"]

old_rows = load_csv(RESEARCH / "ratio-decision/ratio_interval_decisions.csv")
references = load_csv(
    RESEARCH / "canonical-ratio-bridge/canonical_ratio_bridge.csv"
)
need(len(old_rows) == 5700 and len(references) == 950,
     "Parent row count differs")

reference = {
    (int(r["n"]), int(r["m"]), int(r["p"])): r
    for r in references
}
need(len(reference) == 950, "Duplicate reference rows")
selected = [r for r in old_rows if r["partition_mode"] == "composition_bound"]
need(len(selected) == 2850, "Composition-mode count differs")

failures = []
results = []
profiles = {cap: Counter() for cap in (1, 2, 4)}
improvements = Counter()
early_improvements = Counter()
checked_pairs = set()
tighter = 0
seen = set()

print("RUNNING=deficit-bound reclassification of saved intervals", flush=True)

for row in selected:
    n, m, p, cap = (int(row[k]) for k in ("n", "m", "p", "cap"))
    key = (n, m, p, cap)
    need(key not in seen, "Duplicate decision row")
    seen.add(key)
    need(cap in profiles and row["status"] == "PASS", "Unexpected parent row")

    ref = reference[(n, m, p)]
    actual = int(ref["vp_R"])
    partition_count = int(ref["partition_count"])
    old_B, new_B = bounds(n, m)
    old_U = floor_log(old_B, p)
    new_U = floor_log(new_B, p)
    delta = old_U-new_U

    old_lower = int(row["ratio_lower_bound"])
    upper = (
        int(row["ratio_upper_bound"])
        if row["ratio_upper_bound"] != "" else None
    )
    lower = old_lower+delta
    old_decision = row["decision"]
    new_decision = decision(lower, upper)

    valid = (
        1 <= partition_count <= new_B <= old_B
        and delta >= 0
        and actual == int(row["reference_ratio_valuation"])
        and decision(old_lower, upper) == old_decision
        and lower <= actual
        and (upper is None or actual <= upper)
    )
    if new_decision == "NONINTEGRAL":
        valid = valid and actual < 0
    elif new_decision == "EQUALITY_EXCLUDED_POSITIVE":
        valid = valid and actual > 0
    elif new_decision != "INCONCLUSIVE":
        valid = False

    if old_decision in ("NONINTEGRAL", "EQUALITY_EXCLUDED_POSITIVE"):
        valid = valid and new_decision == old_decision

    additional = (
        old_decision == "INCONCLUSIVE"
        and new_decision == "EQUALITY_EXCLUDED_POSITIVE"
    )
    if additional:
        improvements[cap] += 1
        if row["arithmetic_status"] == "UNRESOLVED_AT_CAP":
            early_improvements[cap] += 1

    tighter += delta > 0
    checked_pairs.add((n, m))
    profiles[cap][new_decision] += 1
    if not valid:
        failures.append(["decision", n, m, p, cap])

    results.append({
        "n": n, "m": m, "p": p, "cap": cap,
        "old_integer_bound": old_B,
        "deficit_integer_bound": new_B,
        "old_partition_vp_upper": old_U,
        "new_partition_vp_upper": new_U,
        "old_ratio_lower": old_lower,
        "new_ratio_lower": lower,
        "ratio_upper": upper,
        "arithmetic_status": row["arithmetic_status"],
        "old_decision": old_decision,
        "new_decision": new_decision,
        "additional_positive_decision": additional,
        "reference_ratio_valuation": actual,
        "status": "PASS" if valid else "FAIL"
    })

boundary_controls = [
    (1, 1, 1), (10, 10, 1), (8, 1, 1), (5, 2, 3)
]
for n, m, expected in boundary_controls:
    if bounds(n, m)[1] != expected:
        failures.append(["bound_boundary", n, m])

print("RUNNING=size-certificate binomial boundary checks", flush=True)
size_rows = []
for d in range(1, 150):
    n = 4*d+1
    matching = comb(n-d, d)
    required = 4**d
    valid = matching >= required
    if not valid:
        failures.append(["size_boundary", n, d])
    size_rows.append({
        "deficit": d,
        "boundary_n": n,
        "matching_binomial": matching,
        "required_binomial_lower_bound": required,
        "ratio_lower_bound_at_least_two": valid,
        "status": "PASS" if valid else "FAIL"
    })

covered_pairs = sum(600-4*d for d in range(1, 150))
if len(results) != 2850 or len(checked_pairs) != 190:
    failures.append(["decision_domain_count"])
if covered_pairs != 44700 or len(size_rows) != 149:
    failures.append(["size_domain_count"])
if Path(__file__).read_bytes() != source:
    failures.append(["source_changed"])

tables = {
    "deficit_bound_decisions.csv":
        save_csv("deficit_bound_decisions.csv", results),
    "size_certificate_boundaries.csv":
        save_csv("size_certificate_boundaries.csv", size_rows)
}
report = {
    "status": "PASS" if not failures else "FAIL",
    "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    "python": platform.python_version(),
    "source_sha256": sha(source),
    "table_sha256": tables,
    "parent_hashes": bindings,
    "new_decision_comparisons": len(results),
    "distinct_partition_oracle_pairs": len(checked_pairs),
    "strict_exponent_improvements_across_cap_records": tighter,
    "profiles": {str(k): dict(v) for k, v in profiles.items()},
    "additional_positive_decisions": dict(improvements),
    "additional_positive_decisions_while_unresolved": dict(early_improvements),
    "boundary_controls": len(boundary_controls),
    "size_boundary_checks": len(size_rows),
    "size_region_pairs_through_600_by_monotonicity": covered_pairs,
    "size_checks_are_not_direct_ratio_evaluations": True,
    "size_region": "d>=1, n>=4*d+1",
    "size_region_is_case_A": True,
    "resolver_reexecuted": False,
    "stirling_tables_rebuilt": False,
    "partition_counts_used_only_as_bound_validation_oracles": True,
    "parent_top_level_audits_executed": False,
    "failures": failures,
    "formal_certification": "OPEN",
    "novelty_clearance": "OPEN",
    "global_classification": "OPEN",
    "production_integration": False,
    "promotion": False,
    "git_operations": 0
}
receipt_path = ROOT / "receipt.json"
with receipt_path.open("x", encoding="utf-8") as stream:
    json.dump(report, stream, indent=2, sort_keys=True)

print("STATUS=" + report["status"])
print("NEW_DECISION_COMPARISONS=" + str(len(results)))
print("PARTITION_ORACLE_PAIRS=" + str(len(checked_pairs)))
print("STRICT_EXPONENT_IMPROVEMENTS=" + str(tighter))
for cap in (1, 2, 4):
    print("PROFILE_CAP_" + str(cap) + "="
          + json.dumps(dict(profiles[cap]), sort_keys=True))
    print("ADDITIONAL_POSITIVE_CAP_" + str(cap) + "="
          + str(improvements[cap]))
    print("ADDITIONAL_EARLY_POSITIVE_CAP_" + str(cap) + "="
          + str(early_improvements[cap]))
print("BOUNDARY_CONTROLS=4")
print("SIZE_BOUNDARY_CHECKS=" + str(len(size_rows)))
print("SIZE_REGION_PAIRS_THROUGH_600=" + str(covered_pairs))
print("FAILURES=" + str(len(failures)))
print("SOURCE_SHA256=" + sha(source))
print("RECEIPT_SHA256=" + sha(receipt_path.read_bytes()))
print("EVIDENCE_DIRECTORY=" + str(ROOT))
print("RESOLVER_REEXECUTED=NO")
print("STIRLING_TABLES_REBUILT=NO")
print("CSV_DUMP=NO")
print("GIT_OPERATIONS=0")
print("PROMOTION=FALSE")
print("GLOBAL_CLASSIFICATION=OPEN")

if failures:
    raise SystemExit(1)
