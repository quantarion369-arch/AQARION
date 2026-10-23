from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import csv
import hashlib
import json
import platform

ROOT = Path(__file__).resolve().parent
PARENT = (
    Path.home() / "AQARION"
    / "AQARION-QUANTARION-AI/research/ordered-cycle-ratio-audit"
    / "polynomial-certificate-chain/polynomial-second-kind"
)
INPUT_HASHES = {
    "audit.py": "57e6634d46c1059ca0f5e7ce4c5ff16b621344f2ef62529d77e528cfafa38588",
    "receipt.json": "d7b602fdd2ce26d609985dcc9f2f8f5f5699caf004cd40b58728e3673ab560f3",
    "polynomial_certificates.csv": "ec8a4a1723877364e8919bb208640093ee0a6bf82b09490f5019295bc0b1873c"
}

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def vp(x, p):
    need(x > 0, "Positive valuation input required")
    result = 0
    while x % p == 0:
        result += 1
        x //= p
    return result

def scaled(values, p, precision, max_k=None):
    modulus = p**precision
    weights = [0]
    residues = [1]
    limit = len(values) if max_k is None else max_k
    for value in values:
        w = vp(value, p)
        inverse = pow(value // p**w, -1, modulus)
        new_weights = []
        new_residues = []
        for k in range(min(len(weights), limit)+1):
            candidates = []
            if k < len(weights):
                candidates.append(weights[k])
            if k:
                candidates.append(w+weights[k-1])
            top = max(candidates)
            residue = 0
            if k < len(weights):
                residue += (
                    pow(p, top-weights[k], modulus)*residues[k]
                )
            if k:
                residue += (
                    pow(p, top-w-weights[k-1], modulus)
                    * inverse * residues[k-1]
                )
            new_weights.append(top)
            new_residues.append(residue % modulus)
        weights, residues = new_weights, new_residues
    return weights, residues

def save_csv(name, rows):
    path = ROOT / name
    with path.open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return sha(path.read_bytes())

source = Path(__file__).read_bytes()
for name, expected in INPUT_HASHES.items():
    path = PARENT / name
    need(path.is_file() and not path.is_symlink(), "Missing or linked input")
    need(sha(path.read_bytes()) == expected, "Input changed: " + name)

parent_receipt = json.loads((PARENT / "receipt.json").read_bytes())
need(parent_receipt["status"] == "PASS", "Parent is not PASS")
need(parent_receipt["source_sha256"] == INPUT_HASHES["audit.py"],
     "Parent source binding differs")
need(
    parent_receipt["table_sha256"]["polynomial_certificates.csv"]
    == INPUT_HASHES["polynomial_certificates.csv"],
    "Parent CSV binding differs"
)

with (PARENT / "polynomial_certificates.csv").open(
    newline="", encoding="utf-8"
) as stream:
    saved = list(csv.DictReader(stream))

selected = [row for row in saved if row["mode"] == "tied_zero"]
need(len(saved) == 6300 and len(selected) == 2212, "Input count differs")
keys = {
    (row["polynomial"], row["n"], row["k"], row["p"])
    for row in selected
}
need(len(keys) == len(selected), "Duplicate selected rows")

functions = {
    "x": lambda x: x,
    "x2": lambda x: x*x,
    "x2_plus_1": lambda x: x*x+1,
    "x_times_xplus1": lambda x: x*(x+1),
    "2x_plus_1": lambda x: 2*x+1,
    "x2_minus_x_plus_1": lambda x: x*x-x+1
}
failures = []
lift_rows = []
depths = Counter()
cache = {}

print("RUNNING=preserved modular lifting at precision 9", flush=True)
for row in selected:
    name = row["polynomial"]
    N, k, p = (int(row[field]) for field in ("n", "k", "p"))
    key = (name, N, p)
    if key not in cache:
        values = [functions[name](i) for i in range(1, N+1)]
        cache[key] = scaled(values, p, 9)
    weights, residues = cache[key]
    W, residue = weights[k], residues[k]
    depth = vp(residue, p) if residue else None
    valuation = depth-W if depth is not None else None
    reference = int(row["actual_valuation"])
    valid = (
        row["status"] == "PASS"
        and W == int(row["top_weight_sum"])
        and residue % p == 0
        and depth is not None
        and valuation == reference
    )
    if not valid:
        failures.append(["lift", name, N, k, p])
    if depth is not None:
        depths[depth] += 1
    lift_rows.append({
        "polynomial": name, "N": N, "k": k, "p": p,
        "max_weight_W": W,
        "evaluated_precision": 9,
        "normalized_residue": residue,
        "cancellation_depth": depth,
        "first_nonzero_precision": depth+1 if depth is not None else "",
        "computed_valuation": valuation,
        "saved_reference_valuation": reference,
        "status": "PASS" if valid else "FAIL"
    })

expected_depths = {
    1: 1441, 2: 451, 3: 165, 4: 79,
    5: 54, 6: 15, 7: 4, 8: 3
}
if dict(depths) != expected_depths:
    failures.append(["finite_depth_profile_differs"])

print("RUNNING=telescoping structural checks", flush=True)
structural_rows = []
for N in range(1, 65):
    values = [i*(i+1) for i in range(1, N+1)]
    for p in (2, 3, 5, 7, 11):
        weights, residues = scaled(values, p, 16, max_k=1)
        W, residue = weights[1], residues[1]
        closed_W = 0
        power = p
        while power <= N+1:
            closed_W += 1
            power *= p
        v_next = vp(N+1, p)
        expected_depth = closed_W+vp(N, p)-v_next
        expected_residue = (
            pow(p, closed_W-v_next, p**16)
            * N * pow((N+1)//p**v_next, -1, p**16)
        ) % (p**16)
        depth = vp(residue, p) if residue else None
        valid = (
            W == closed_W
            and residue == expected_residue
            and depth == expected_depth
        )
        if not valid:
            failures.append(["telescoping", N, p])
        structural_rows.append({
            "N": N, "p": p, "k": 1,
            "max_weight_W": W,
            "evaluated_precision": 16,
            "normalized_residue": residue,
            "computed_depth": depth,
            "closed_form_depth": expected_depth,
            "closed_form_valuation": vp(N, p)-v_next,
            "status": "PASS" if valid else "FAIL"
        })

values32 = [i*(i+1) for i in range(1, 33)]
w9, a9 = scaled(values32, 2, 9, max_k=1)
w16, a16 = scaled(values32, 2, 16, max_k=1)
depth_control = (
    w9[1] == w16[1] == 5
    and a9[1] == 0
    and a16[1] != 0
    and vp(a16[1], 2) == 10
)
if not depth_control:
    failures.append(["depth_ten_precision_control"])
if len(structural_rows) != 320:
    failures.append(["structural_count"])
if Path(__file__).read_bytes() != source:
    failures.append(["source_changed"])

tables = {
    "lifted_tied_zero_cases.csv":
        save_csv("lifted_tied_zero_cases.csv", lift_rows),
    "telescoping_structural_checks.csv":
        save_csv("telescoping_structural_checks.csv", structural_rows)
}
report = {
    "status": "PASS" if not failures else "FAIL",
    "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    "python": platform.python_version(),
    "source_sha256": sha(source),
    "table_sha256": tables,
    "parent_hashes": INPUT_HASHES,
    "lifted_rows": len(lift_rows),
    "resolved_rows": sum(row["cancellation_depth"] is not None for row in lift_rows),
    "evaluated_precision": 9,
    "cancellation_depth_profile": dict(depths),
    "telescoping_checks": len(structural_rows),
    "depth_ten_precision_control": depth_control,
    "exact_rational_arithmetic_used": False,
    "reference_valuations_used_to_choose_precision": False,
    "failures": failures,
    "scope": "Finite modular lifting plus telescoping closed-form checks",
    "universal_finite_depth_bound_claimed": False,
    "canonical_ratio_certificates_added": False,
    "formal_certification": "OPEN",
    "novelty_clearance": "OPEN",
    "global_classification": "OPEN",
    "promotion": False,
    "git_operations_by_audit": 0
}
receipt = ROOT / "receipt.json"
with receipt.open("x", encoding="utf-8") as stream:
    json.dump(report, stream, indent=2, sort_keys=True)

print("AUDIT_STATUS=" + report["status"])
print("LIFTED_ROWS=" + str(len(lift_rows)))
print("RESOLVED_ROWS=" + str(report["resolved_rows"]))
print("MAX_OBSERVED_DEPTH=" + str(max(depths) if depths else -1))
print("TELESCOPING_CHECKS=" + str(len(structural_rows)))
print("DEPTH_TEN_CONTROL=" + ("PASS" if depth_control else "FAIL"))
print("FAILURES=" + str(len(failures)))
print("SOURCE_SHA256=" + sha(source))
print("RECEIPT_SHA256=" + sha(receipt.read_bytes()))
print("EVIDENCE_DIRECTORY=" + str(ROOT))
print("CSV_DUMP=NO")

if failures:
    raise SystemExit(1)
