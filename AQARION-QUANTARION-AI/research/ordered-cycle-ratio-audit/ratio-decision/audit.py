from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from math import comb, factorial
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
    "resolver-contract": (
        "a8a8188143099b7060b9b1f03b52afa8ab2bc74a80759a7ea568419e713a5d84",
        "8384f5bce432d6548f6f8925d2ab5278b06dc9c62ef773c6d895a14fe8775563",
        "files"
    ),
    "modular-cancellation-lift": (
        "f2183c83034ad7a2cf7e093060300bf9e2ebf0bfc6244e1f5ebeaa3b9562479d",
        "352dbd57c4961a73f490e1cb0bebecfef5c39954a6adb4aee2036528e5765410",
        "table_sha256"
    ),
    "canonical-ratio-bridge": (
        "18dcc25d80132b1480f5f5d9c94f7645567196a3e41c42bce83640fb2f63274c",
        "686a851bccb7c433a7bd659e4feb89fee2927c74ca702dfa5bece7df939134ab",
        "table_sha256"
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

source = Path(__file__).read_bytes()
bindings = {}
parent_sources = {}

for name, (source_hash, receipt_hash, table_field) in PARENTS.items():
    folder = RESEARCH / name
    raw_source = read(folder / "audit.py")
    raw_receipt = read(folder / "receipt.json")
    need(sha(raw_source) == source_hash, "Parent source differs: " + name)
    need(sha(raw_receipt) == receipt_hash, "Parent receipt differs: " + name)
    receipt = json.loads(raw_receipt)
    need(receipt["status"] == "PASS", "Parent is not PASS")
    need(receipt["source_sha256"] == source_hash, "Source binding differs")
    files = {"audit.py": source_hash, "receipt.json": receipt_hash}
    for filename, expected in receipt[table_field].items():
        need(Path(filename).name == filename, "Unexpected parent path")
        need(sha(read(folder / filename)) == expected, "Parent file differs")
        files[filename] = expected
    bindings[name] = files
    parent_sources[name] = raw_source

def extract(raw, names, namespace, filename):
    tree = ast.parse(raw)
    nodes = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name in names
    ]
    need(len(nodes) == len(names), "Function extraction differs")
    need({node.name for node in nodes} == set(names), "Function names differ")
    module = ast.Module(body=nodes, type_ignores=[])
    exec(compile(module, filename, "exec"), namespace)

ns = {}
extract(
    parent_sources["modular-cancellation-lift"],
    {"need", "vp", "scaled"}, ns, "published-modular-kernel"
)
ns["kernel"] = ns["scaled"]
extract(
    parent_sources["resolver-contract"],
    {"invalid", "validate", "independent_weight", "at_precision", "resolve"},
    ns, "published-resolver-functions"
)
resolver = ns["resolve"]

reference_path = RESEARCH / "canonical-ratio-bridge/canonical_ratio_bridge.csv"
with reference_path.open(newline="", encoding="utf-8") as stream:
    references = list(csv.DictReader(stream))

keys = {(int(r["n"]), int(r["m"]), int(r["p"])) for r in references}
need(len(keys) == len(references) == 950, "Reference domain differs")
need(all(r["status"] == "PASS" for r in references), "Reference row failed")

def vp(x, p):
    need(x > 0, "Positive input required")
    result = 0
    while x % p == 0:
        result += 1
        x //= p
    return result

def floor_log(x, p):
    result = 0
    while x >= p:
        x //= p
        result += 1
    return result

partition_cache = {}
def partition_count(n, m):
    key = (n, m)
    if key not in partition_cache:
        target = n-m
        dp = [0]*(target+1)
        dp[0] = 1
        for part in range(1, m+1):
            for total in range(part, target+1):
                dp[total] += dp[total-part]
        partition_cache[key] = dp[target]
    return partition_cache[key]

def interval_decision(lower, upper):
    if type(lower) is not int:
        return "INVALID"
    if upper is not None and type(upper) is not int:
        return "INVALID"
    if upper is not None and lower > upper:
        return "INVALID"
    if upper is not None and upper < 0:
        return "NONINTEGRAL"
    if lower > 0:
        return "EQUALITY_EXCLUDED_POSITIVE"
    return "INCONCLUSIVE"

arithmetic_cache = {}
def decide(n, m, p, cap, mode):
    if (
        type(n) is not int or type(m) is not int
        or not 1 <= m <= n <= 65
        or mode not in ("exact_partition", "composition_bound")
    ):
        return {"decision": "INVALID", "reason": "unsupported_ratio_input"}

    key = (n, m, p, cap)
    if key not in arithmetic_cache:
        arithmetic_cache[key] = resolver(list(range(1, n)), m-1, p, cap)
    arithmetic = arithmetic_cache[key]
    if arithmetic["status"] == "INVALID":
        return {"decision": "INVALID", "reason": arithmetic["reason"]}

    offset = vp(factorial(m), p)-vp(n, p)

    if mode == "exact_partition":
        partition_v = vp(partition_count(n, m), p)
        partition_lower = partition_upper = partition_v
    else:
        partition_lower = 0
        partition_upper = floor_log(comb(n-1, m-1), p)

    if arithmetic["status"] == "RESOLVED":
        base = offset+arithmetic["valuation"]
        lower = base-partition_upper
        upper = base-partition_lower
    else:
        lower = offset+arithmetic["lower_bound"]-partition_upper
        upper = None

    return {
        "decision": interval_decision(lower, upper),
        "arithmetic_status": arithmetic["status"],
        "ratio_lower_bound": lower,
        "ratio_upper_bound": upper,
        "partition_evaluated": mode == "exact_partition",
        "arithmetic": arithmetic
    }

rows = []
failures = []
profiles = {}
early = Counter()

print("RUNNING=canonical ratio interval decisions", flush=True)

for cap in (1, 2, 4):
    for mode in ("exact_partition", "composition_bound"):
        profile = Counter()
        for ref in references:
            n, m, p = (int(ref[field]) for field in ("n", "m", "p"))
            result = decide(n, m, p, cap, mode)
            actual = int(ref["vp_R"])
            arithmetic = result.get("arithmetic", {})
            lower = result.get("ratio_lower_bound")
            upper = result.get("ratio_upper_bound")
            decision = result["decision"]

            valid = decision != "INVALID"
            if valid:
                valid = lower <= actual and (upper is None or actual <= upper)
                if decision == "NONINTEGRAL":
                    valid = valid and actual < 0
                if decision == "EQUALITY_EXCLUDED_POSITIVE":
                    valid = valid and actual > 0
                if arithmetic["status"] == "RESOLVED":
                    valid = valid and arithmetic["valuation"] == int(ref["vp_E"])
                else:
                    valid = valid and arithmetic["lower_bound"] <= int(ref["vp_E"])

                if mode == "exact_partition":
                    valid = valid and partition_count(n, m) == int(ref["partition_count"])
                else:
                    valid = valid and (
                        int(ref["partition_count"]) <= comb(n-1, m-1)
                        and result["partition_evaluated"] is False
                    )

            if not valid:
                failures.append(["decision", n, m, p, cap, mode])

            profile[decision] += 1
            if (
                result.get("arithmetic_status") == "UNRESOLVED_AT_CAP"
                and decision in ("NONINTEGRAL", "EQUALITY_EXCLUDED_POSITIVE")
            ):
                early[(cap, mode)] += 1

            rows.append({
                "n": n, "m": m, "p": p, "cap": cap,
                "partition_mode": mode,
                "arithmetic_status": result.get("arithmetic_status"),
                "decision": decision,
                "ratio_lower_bound": lower,
                "ratio_upper_bound": upper,
                "reference_ratio_valuation": actual,
                "partition_evaluated": result.get("partition_evaluated"),
                "status": "PASS" if valid else "FAIL"
            })
        profiles[str((cap, mode))] = dict(profile)

interval_cases = [
    (-2, -1, "NONINTEGRAL"),
    (-1, 1, "INCONCLUSIVE"),
    (0, 0, "INCONCLUSIVE"),
    (1, 1, "EQUALITY_EXCLUDED_POSITIVE"),
    (1, None, "EQUALITY_EXCLUDED_POSITIVE"),
    (0, None, "INCONCLUSIVE"),
    (-1, None, "INCONCLUSIVE"),
    (1, 0, "INVALID"),
    (True, None, "INVALID"),
    (0, False, "INVALID")
]
interval_results = []
for lower, upper, expected in interval_cases:
    actual = interval_decision(lower, upper)
    interval_results.append({
        "lower": lower, "upper": upper,
        "expected": expected, "actual": actual,
        "passed": actual == expected
    })
if not all(item["passed"] for item in interval_results):
    failures.append(["interval_control"])

fixtures = [
    (5, 2, 5, 1, "exact_partition", "UNRESOLVED_AT_CAP", "INCONCLUSIVE"),
    (5, 2, 5, 2, "exact_partition", "UNRESOLVED_AT_CAP", "EQUALITY_EXCLUDED_POSITIVE"),
    (5, 2, 5, 2, "composition_bound", "UNRESOLVED_AT_CAP", "EQUALITY_EXCLUDED_POSITIVE"),
    (3, 2, 2, 1, "exact_partition", "RESOLVED", "INCONCLUSIVE"),
    (5, 2, 2, 1, "composition_bound", "RESOLVED", "NONINTEGRAL")
]
fixture_results = []
for n, m, p, cap, mode, status, decision in fixtures:
    actual = decide(n, m, p, cap, mode)
    passed = (
        actual.get("arithmetic_status") == status
        and actual["decision"] == decision
    )
    fixture_results.append({
        "n": n, "m": m, "p": p, "cap": cap,
        "mode": mode, "passed": passed, "actual": actual
    })
    if not passed:
        failures.append(["normalization_fixture", n, m, p, cap, mode])

if len(rows) != 5700:
    failures.append(["comparison_count"])
if Path(__file__).read_bytes() != source:
    failures.append(["source_changed"])

table = ROOT / "ratio_interval_decisions.csv"
with table.open("x", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

report = {
    "status": "PASS" if not failures else "FAIL",
    "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    "python": platform.python_version(),
    "source_sha256": sha(source),
    "table_sha256": {"ratio_interval_decisions.csv": sha(table.read_bytes())},
    "parent_hashes": bindings,
    "comparison_count": len(rows),
    "profiles": profiles,
    "early_decisions": {
        str(key): value for key, value in sorted(early.items())
    },
    "interval_controls": interval_results,
    "normalization_fixtures": fixture_results,
    "bound_mode_evaluates_partition_count": False,
    "reference_values_choose_precision": False,
    "original_parent_top_level_audits_executed": False,
    "failures": failures,
    "scope": "Finite canonical-ratio decision layer using published resolver functions",
    "formal_certification": "OPEN",
    "novelty_clearance": "OPEN",
    "global_classification": "OPEN",
    "production_integration": False,
    "promotion": False,
    "git_operations": 0
}
receipt = ROOT / "receipt.json"
with receipt.open("x", encoding="utf-8") as stream:
    json.dump(report, stream, indent=2, sort_keys=True)

print("STATUS=" + report["status"])
print("RATIO_DECISION_COMPARISONS=" + str(len(rows)))
print("INTERVAL_CONTROLS=" + str(sum(x["passed"] for x in interval_results)) + "/10")
print("NORMALIZATION_FIXTURES=" + str(sum(x["passed"] for x in fixture_results)) + "/5")
for key, profile in profiles.items():
    print("PROFILE=" + key + " " + json.dumps(profile, sort_keys=True))
print("EARLY_DECISIONS=" + json.dumps(report["early_decisions"], sort_keys=True))
print("FAILURES=" + str(len(failures)))
print("SOURCE_SHA256=" + sha(source))
print("RECEIPT_SHA256=" + sha(receipt.read_bytes()))
print("EVIDENCE_DIRECTORY=" + str(ROOT))
print("CSV_DUMP=NO")
print("GIT_OPERATIONS=0")
print("PRODUCTION_INTEGRATION=NO")
print("PROMOTION=FALSE")
print("GLOBAL_CLASSIFICATION=OPEN")

if failures:
    raise SystemExit(1)
