from pathlib import Path
from datetime import datetime, timezone
import ast
import csv
import hashlib
import json
import platform

ROOT = Path(__file__).resolve().parent
KERNEL_DIR = (
    Path.home() / "AQARION"
    / "AQARION-QUANTARION-AI/research/ordered-cycle-ratio-audit"
    / "modular-cancellation-lift"
)
EXPECTED = {
    "audit.py": "f2183c83034ad7a2cf7e093060300bf9e2ebf0bfc6244e1f5ebeaa3b9562479d",
    "receipt.json": "352dbd57c4961a73f490e1cb0bebecfef5c39954a6adb4aee2036528e5765410",
    "lifted_tied_zero_cases.csv": "15154a2df583e27afcc6a272f1e92264667bc90fc3498a060e9ffe2f52ab9ed2",
    "telescoping_structural_checks.csv": "9dedf5ef4855996d729eaec17c5ffaa48da464bd0c2b278ba431c42227f498e5"
}

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

source = Path(__file__).read_bytes()
for name, expected in EXPECTED.items():
    path = KERNEL_DIR / name
    need(path.is_file() and not path.is_symlink(), "Invalid parent file")
    need(sha(path.read_bytes()) == expected, "Parent hash differs: " + name)

parent = json.loads((KERNEL_DIR / "receipt.json").read_bytes())
need(parent["status"] == "PASS", "Parent is not PASS")
need(parent["source_sha256"] == EXPECTED["audit.py"], "Source binding differs")
for name, expected in parent["table_sha256"].items():
    need(EXPECTED.get(name) == expected, "Parent table binding differs")

tree = ast.parse((KERNEL_DIR / "audit.py").read_bytes())
wanted = {"need", "vp", "scaled"}
nodes = [
    node for node in tree.body
    if isinstance(node, ast.FunctionDef) and node.name in wanted
]
need(len(nodes) == 3 and {node.name for node in nodes} == wanted,
     "Kernel extraction differs")

namespace = {}
module = ast.Module(body=nodes, type_ignores=[])
exec(compile(module, str(KERNEL_DIR / "audit.py"), "exec"), namespace)
kernel = namespace["scaled"]

def invalid(reason):
    return {"status": "INVALID", "reason": reason}

def validate(values, k, p, precision):
    if type(values) not in (list, tuple) or len(values) > 64:
        return "unsupported_denominator_sequence"
    if any(type(x) is not int or x <= 0 or x.bit_length() > 64
           for x in values):
        return "unsupported_denominator"
    if type(k) is not int or not 0 <= k <= len(values):
        return "invalid_degree"
    if type(p) is not int or not 2 <= p <= 97:
        return "unsupported_prime"
    if any(p % d == 0 for d in range(2, int(p**0.5)+1)):
        return "composite_modulus_base"
    if type(precision) is not int or not 1 <= precision <= 32:
        return "unsupported_precision"
    return None

def independent_weight(values, k, p):
    weights = []
    for value in values:
        w = 0
        while value % p == 0:
            value //= p
            w += 1
        weights.append(w)
    return sum(sorted(weights, reverse=True)[:k])

def at_precision(values, k, p, precision):
    reason = validate(values, k, p, precision)
    if reason:
        return invalid(reason)

    try:
        weights, residues = kernel(values, p, precision, max_k=k)
        W, residue = weights[k], residues[k]
        if type(W) is not int or W != independent_weight(values, k, p):
            return invalid("weight_invariant")
        if type(residue) is not int or not 0 <= residue < p**precision:
            return invalid("residue_invariant")
    except Exception as error:
        return invalid("kernel_exception:" + type(error).__name__)

    result = {
        "status": "UNRESOLVED_AT_CAP",
        "precision": precision,
        "max_weight_W": W,
        "normalized_residue": residue,
        "cancellation_depth": None,
        "first_nonzero_precision": None,
        "valuation": None,
        "lower_bound": precision-W
    }

    if residue:
        depth = 0
        unit = residue
        while unit % p == 0:
            unit //= p
            depth += 1
        result.update({
            "status": "RESOLVED",
            "cancellation_depth": depth,
            "first_nonzero_precision": depth+1,
            "valuation": depth-W,
            "lower_bound": None
        })
    return result

def resolve(values, k, p, cap):
    reason = validate(values, k, p, cap)
    if reason:
        return invalid(reason)

    precision = 1
    previous = None
    while True:
        result = at_precision(values, k, p, precision)
        if result["status"] == "INVALID":
            return result
        if previous is not None:
            consistent = (
                result["max_weight_W"] == previous["max_weight_W"]
                and result["normalized_residue"] % p**previous["precision"]
                == previous["normalized_residue"]
            )
            if not consistent:
                return invalid("cross_precision_inconsistency")
        if result["status"] == "RESOLVED" or precision == cap:
            return result
        previous = result
        precision = min(2*precision, cap)

def verify_claim(values, k, p, precision, claim):
    actual = at_precision(values, k, p, precision)
    if actual["status"] == "INVALID":
        return actual
    same = (
        type(claim) is dict
        and set(claim) == set(actual)
        and all(
            type(claim[key]) is type(actual[key])
            and claim[key] == actual[key]
            for key in actual
        )
    )
    return actual if same else invalid("certificate_mismatch")

records = []
failures = []

def record(label, group, actual, passed):
    records.append({
        "label": label,
        "group": group,
        "actual_status": actual["status"],
        "passed": passed,
        "actual_result": json.dumps(actual, sort_keys=True)
    })
    if not passed:
        failures.append(label)

values32 = [i*(i+1) for i in range(1, 33)]
values64 = [i*(i+1) for i in range(1, 65)]

cases = [
    ("unit", [1,2,3], 1, 3, 1, "RESOLVED", -1, None),
    ("tie_cap1", [1,2,3], 2, 2, 1, "UNRESOLVED_AT_CAP", None, 0),
    ("tie_cap2", [1,2,3], 2, 2, 2, "RESOLVED", 0, None),
    ("depth2_cap2", [1,2,3,4], 1, 5, 2, "UNRESOLVED_AT_CAP", None, 2),
    ("depth2_cap3", [1,2,3,4], 1, 5, 3, "RESOLVED", 2, None),
    ("depth10_cap9", values32, 1, 2, 9, "UNRESOLVED_AT_CAP", None, 4),
    ("depth10_cap10", values32, 1, 2, 10, "UNRESOLVED_AT_CAP", None, 5),
    ("depth10_cap11", values32, 1, 2, 11, "RESOLVED", 5, None),
    ("empty_degree_zero", [], 0, 2, 1, "RESOLVED", 0, None),
    ("depth12_cap12", values64, 1, 2, 12, "UNRESOLVED_AT_CAP", None, 6),
    ("depth12_cap13", values64, 1, 2, 13, "RESOLVED", 6, None)
]

print("RUNNING=resolver status and cap-boundary tests", flush=True)
for label, values, k, p, cap, status, valuation, lower in cases:
    result = resolve(values, k, p, cap)
    passed = (
        result["status"] == status
        and result.get("valuation") == valuation
        and result.get("lower_bound") == lower
    )
    record(label, "resolver_behavior", result, passed)

bad_inputs = [
    ("zero_denominator", [0], 1, 2, 2),
    ("negative_denominator", [-1], 1, 2, 2),
    ("float_denominator", [1.5], 1, 2, 2),
    ("boolean_denominator", [True], 1, 2, 2),
    ("composite_prime", [1], 1, 4, 2),
    ("prime_below_two", [1], 1, 1, 2),
    ("boolean_prime", [1], 1, True, 2),
    ("negative_degree", [1], -1, 2, 2),
    ("degree_too_large", [1], 2, 2, 2),
    ("zero_cap", [1], 1, 2, 0),
    ("boolean_cap", [1], 1, 2, True),
    ("too_many_terms", [1]*65, 1, 2, 2),
    ("oversized_denominator", [2**65], 1, 2, 2),
    ("unsupported_prime", [1], 1, 101, 2),
    ("unsupported_cap", [1], 1, 2, 33)
]
for label, values, k, p, cap in bad_inputs:
    result = resolve(values, k, p, cap)
    record(label, "invalid_input", result, result["status"] == "INVALID")

good = at_precision([1,2,3], 2, 2, 2)
zero = at_precision([1,2,3], 2, 2, 1)
for label, precision, claim in (
    ("valid_resolved_claim", 2, good),
    ("valid_unresolved_claim", 1, zero)
):
    result = verify_claim([1,2,3], 2, 2, precision, claim)
    record(label, "valid_claim", result, result == claim)

mutations = [
    ("wrong_scale", "max_weight_W", 2),
    ("wrong_residue", "normalized_residue", 3),
    ("noncanonical_residue", "normalized_residue", 6),
    ("wrong_precision", "precision", 3),
    ("wrong_valuation", "valuation", 1),
    ("wrong_status", "status", "UNRESOLVED_AT_CAP"),
    ("boolean_scale", "max_weight_W", True)
]
for label, field, value in mutations:
    claim = dict(good)
    claim[field] = value
    result = verify_claim([1,2,3], 2, 2, 2, claim)
    record(label, "corrupted_claim", result, result["status"] == "INVALID")

claim = dict(good)
del claim["valuation"]
result = verify_claim([1,2,3], 2, 2, 2, claim)
record("missing_field", "corrupted_claim", result, result["status"] == "INVALID")

claim = dict(good)
claim["unjustified_proof"] = True
result = verify_claim([1,2,3], 2, 2, 2, claim)
record("extra_field", "corrupted_claim", result, result["status"] == "INVALID")

claim = dict(zero)
claim["status"] = "RESOLVED"
claim["valuation"] = 0
result = verify_claim([1,2,3], 2, 2, 1, claim)
record("exactness_claim_from_zero", "corrupted_claim",
       result, result["status"] == "INVALID")

need(Path(__file__).read_bytes() == source, "Adapter source changed")

table = ROOT / "resolver_contract_tests.csv"
with table.open("x", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(records[0]))
    writer.writeheader()
    writer.writerows(records)

spec_lines = [
    "# Bounded modular resolver research contract",
    "",
    "Supported inputs: at most 64 positive integer denominators,",
    "each at most 64 bits; prime p between 2 and 97;",
    "integer degree from zero through sequence length;",
    "precision or adaptive cap from 1 through 32.",
    "",
    "RESOLVED: nonzero normalized residue determines exact valuation.",
    "UNRESOLVED_AT_CAP: zero residue supplies only precision-W lower bound.",
    "INVALID: unsupported input, invariant failure, or claim mismatch.",
    "",
    "Arithmetic uses unchanged function definitions extracted from",
    "the hash-verified published modular-lifting source.",
    "The original module top-level audit is not executed.",
    "",
    "Claim verification recomputes the declared fixed-precision result.",
    "It does not establish identity of an untrusted remote runtime.",
    "No claim of production integration or formal certification is made."
]
spec = ROOT / "SPEC.md"
with spec.open("x", encoding="utf-8") as stream:
    stream.write(chr(10).join(spec_lines)+chr(10))

report = {
    "status": "PASS" if not failures else "FAIL",
    "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    "python": platform.python_version(),
    "source_sha256": sha(source),
    "kernel_parent_hashes": EXPECTED,
    "kernel_functions": ["need", "vp", "scaled"],
    "extraction_mode": "unchanged function AST definitions only",
    "original_top_level_audit_executed": False,
    "test_count": len(records),
    "resolver_behavior_tests": len(cases),
    "invalid_input_tests": len(bad_inputs),
    "valid_claim_tests": 2,
    "corrupted_claim_tests": 10,
    "failures": failures,
    "files": {
        table.name: sha(table.read_bytes()),
        spec.name: sha(spec.read_bytes())
    },
    "production_integration": False,
    "formal_certification": "OPEN",
    "novelty_clearance": "OPEN",
    "promotion": False,
    "git_operations": 0
}
receipt = ROOT / "receipt.json"
with receipt.open("x", encoding="utf-8") as stream:
    json.dump(report, stream, indent=2, sort_keys=True)

print("STATUS=" + report["status"])
print("KERNEL_PARENT_BINDINGS=PASS")
print("UNCHANGED_KERNEL_FUNCTIONS=3")
print("ORIGINAL_TOP_LEVEL_AUDIT_EXECUTED=NO")
print("RESOLVER_BEHAVIOR_TESTS=" + str(len(cases)))
print("INVALID_INPUTS_REJECTED=" + str(sum(
    row["passed"] for row in records if row["group"] == "invalid_input"
)))
print("VALID_CLAIMS_ACCEPTED=" + str(sum(
    row["passed"] for row in records if row["group"] == "valid_claim"
)))
print("CORRUPTED_CLAIMS_REJECTED=" + str(sum(
    row["passed"] for row in records if row["group"] == "corrupted_claim"
)))
print("TOTAL_TESTS=" + str(len(records)))
print("FAILURES=" + str(len(failures)))
print("SOURCE_SHA256=" + sha(source))
print("RECEIPT_SHA256=" + sha(receipt.read_bytes()))
print("EVIDENCE_DIRECTORY=" + str(ROOT))
print("CSV_DUMP=NO")
print("GIT_OPERATIONS=0")
print("PRODUCTION_INTEGRATION=NO")
print("PROMOTION=FALSE")

if failures:
    raise SystemExit(1)
