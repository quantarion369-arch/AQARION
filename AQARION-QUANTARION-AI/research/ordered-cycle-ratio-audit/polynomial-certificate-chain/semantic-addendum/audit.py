from pathlib import Path
from fractions import Fraction
from math import comb, factorial
from datetime import datetime, timezone
import csv
import hashlib
import json
import platform

ROOT = Path(__file__).resolve().parent
PARENT = Path.home() / "AQARION_AUDIT/cycle_ratio/polynomial-second-kind.0pdqA2"
EXPECTED_HASHES = {
    "audit.py": "57e6634d46c1059ca0f5e7ce4c5ff16b621344f2ef62529d77e528cfafa38588",
    "receipt.json": "d7b602fdd2ce26d609985dcc9f2f8f5f5699caf004cd40b58728e3673ab560f3",
    "polynomial_certificates.csv": "ec8a4a1723877364e8919bb208640093ee0a6bf82b09490f5019295bc0b1873c",
    "second_kind_certificates.csv": "8b21dc05f3d753e802625cc30535aafb4c6108f09b6ebcb4adbf7b5ea0405262"
}

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def vp(x, p):
    need(x != 0, "Zero valuation requires separate handling")
    x = abs(x)
    result = 0
    while x % p == 0:
        result += 1
        x //= p
    return result

def load_csv(name):
    with (PARENT / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))

source = Path(__file__).read_bytes()
for name, expected in EXPECTED_HASHES.items():
    path = PARENT / name
    need(path.is_file() and not path.is_symlink(), "Missing or linked input")
    need(sha(path.read_bytes()) == expected, "Parent hash differs: " + name)

parent_receipt = json.loads((PARENT / "receipt.json").read_bytes())
need(parent_receipt["status"] == "PASS", "Parent is not PASS")
need(
    parent_receipt["source_sha256"] == EXPECTED_HASHES["audit.py"],
    "Parent source binding differs"
)
for name in ("polynomial_certificates.csv", "second_kind_certificates.csv"):
    need(
        parent_receipt["table_sha256"][name] == EXPECTED_HASHES[name],
        "Parent table binding differs"
    )

poly_rows = load_csv("polynomial_certificates.csv")
second_rows = load_csv("second_kind_certificates.csv")
primes = [2, 3, 5, 7, 11]
polynomials = {
    "x": lambda x: x,
    "x2": lambda x: x*x,
    "x2_plus_1": lambda x: x*x+1,
    "x_times_xplus1": lambda x: x*(x+1),
    "2x_plus_1": lambda x: 2*x+1,
    "x2_minus_x_plus_1": lambda x: x*x-x+1
}

expected_poly = {}
checks = []
failures = []
print("RUNNING=exact normalized residue checks", flush=True)

for name, f in polynomials.items():
    values = []
    elementary = [Fraction(1)]
    for n in range(1, 21):
        values.append(f(n))
        elementary.append(Fraction(0))
        for k in range(n, 0, -1):
            elementary[k] += elementary[k-1]/values[-1]
        for p in primes:
            weights = sorted((vp(x, p) for x in values), reverse=True)
            for k in range(1, n+1):
                L = sum(weights[:k])
                exact = elementary[k]
                normalized = exact * p**L
                need(normalized.denominator % p != 0,
                     "Normalization failed to produce a p-integral value")
                residue = (
                    normalized.numerator
                    * pow(normalized.denominator, -1, p)
                ) % p
                actual = vp(exact.numerator, p)-vp(exact.denominator, p)
                strict = k == n or weights[k-1] > weights[k]
                mode = (
                    "strict" if strict
                    else "tied_nonzero" if residue
                    else "tied_zero"
                )
                expected_poly[(name, n, k, p)] = {
                    "polynomial": name, "n": str(n), "k": str(k),
                    "p": str(p), "top_weight_sum": str(L),
                    "normalized_residue": str(residue),
                    "actual_valuation": str(actual), "mode": mode,
                    "nonintegrality_certified": str(bool(residue and L > 0)),
                    "status": "PASS"
                }

def poly_key(row):
    return (
        row["polynomial"], int(row["n"]),
        int(row["k"]), int(row["p"])
    )

def poly_valid(row):
    try:
        return row == expected_poly[poly_key(row)]
    except (KeyError, ValueError, TypeError):
        return False

def poly_domain_valid(rows):
    try:
        return (
            len(rows) == len(expected_poly)
            and {poly_key(row) for row in rows} == set(expected_poly)
        )
    except (KeyError, ValueError, TypeError):
        return False

if not poly_domain_valid(poly_rows):
    failures.append("polynomial domain mismatch")

for index, row in enumerate(poly_rows):
    valid = poly_valid(row)
    if not valid:
        failures.append("polynomial row " + str(index))
    key = poly_key(row)
    expected = expected_poly[key]
    checks.append({
        "family": "reciprocal_polynomial",
        "key": str(key),
        "observed_residue": row["normalized_residue"],
        "expected_residue": expected["normalized_residue"],
        "expected_valuation": expected["actual_valuation"],
        "status": "PASS" if valid else "FAIL"
    })

print("RUNNING=second-kind exact and lifted-modulus checks", flush=True)
S = [[0]*13 for _ in range(1251)]
S[0][0] = 1
for n in range(1, 1251):
    for k in range(1, min(n, 12)+1):
        S[n][k] = k*S[n-1][k]+S[n-1][k-1]

expected_second = {}
exact_identity_checks = 0
lifted_checks = 0
period_checks = 0

for n in range(1, 41):
    for k in range(1, min(n, 12)+1):
        fact = factorial(k)
        exact = fact*S[n][k]
        alternate = sum(
            (-1)**(k-j)*comb(k, j)*j**n
            for j in range(k+1)
        )
        exact_identity_checks += 1
        if exact != alternate:
            failures.append("exact inclusion-exclusion " + str((n, k)))

        for p in primes:
            modulus = p**3
            exponent = vp(fact, p)
            lifted_modulus = p**(3+exponent)
            lifted = sum(
                (-1)**(k-j)*comb(k, j)*pow(j, n, lifted_modulus)
                for j in range(k+1)
            ) % lifted_modulus

            need(lifted % p**exponent == 0, "Lifted divisibility failed")
            recovered = (
                (lifted // p**exponent)
                * pow(fact // p**exponent, -1, modulus)
            ) % modulus

            lifted_checks += 1
            if recovered != S[n][k] % modulus:
                failures.append("lifted recovery " + str((n, k, p)))

            periods = True
            for t in range(1, min(3, n)+1):
                mod = p**t
                period = (p-1)*p**(t-1)
                periods = periods and (
                    fact*S[n][k]-fact*S[n+period][k]
                ) % mod == 0
                period_checks += 1

            expected_second[(n, k, p)] = {
                "n": str(n), "k": str(k), "p": str(p),
                "modulus": str(modulus),
                "factorial_times_S_residue": str(exact % modulus),
                "factorial_times_S_valuation": str(vp(exact, p)),
                "period_checks_pass": str(periods),
                "status": "PASS" if periods else "FAIL"
            }

def second_key(row):
    return int(row["n"]), int(row["k"]), int(row["p"])

def second_valid(row):
    try:
        return row == expected_second[second_key(row)]
    except (KeyError, ValueError, TypeError):
        return False

try:
    second_domain_ok = (
        len(second_rows) == len(expected_second)
        and {second_key(row) for row in second_rows} == set(expected_second)
    )
except (KeyError, ValueError, TypeError):
    second_domain_ok = False

if not second_domain_ok:
    failures.append("second-kind domain mismatch")

for index, row in enumerate(second_rows):
    valid = second_valid(row)
    if not valid:
        failures.append("second-kind row " + str(index))
    key = second_key(row)
    expected = expected_second[key]
    checks.append({
        "family": "second_kind",
        "key": str(key),
        "observed_residue": row["factorial_times_S_residue"],
        "expected_residue": expected["factorial_times_S_residue"],
        "expected_valuation": expected["factorial_times_S_valuation"],
        "status": "PASS" if valid else "FAIL"
    })

controls = []

def mutation(label, validator, original, field, value):
    changed = dict(original)
    changed[field] = value
    controls.append({
        "label": label,
        "rejected": not validator(changed)
    })

unit_row = next(
    row for row in poly_rows
    if int(row["p"]) >= 3 and int(row["normalized_residue"]) != 0
)
tie_row = next(row for row in poly_rows if row["mode"] == "tied_zero")

mutation(
    "wrong_nonzero_leading_unit", poly_valid, unit_row,
    "normalized_residue",
    "2" if unit_row["normalized_residue"] == "1" else "1"
)
mutation(
    "wrong_top_weight", poly_valid, unit_row,
    "top_weight_sum", str(int(unit_row["top_weight_sum"])+1)
)
mutation(
    "wrong_polynomial_valuation", poly_valid, unit_row,
    "actual_valuation", str(int(unit_row["actual_valuation"])+1)
)
mutation(
    "false_tie_nonintegrality", poly_valid, tie_row,
    "nonintegrality_certified", "True"
)
mutation("wrong_polynomial_status", poly_valid, unit_row, "status", "FAIL")

second = second_rows[0]
mutation(
    "wrong_modulus", second_valid, second,
    "modulus", str(int(second["p"])**2)
)
mutation(
    "wrong_second_kind_residue", second_valid, second,
    "factorial_times_S_residue",
    str((int(second["factorial_times_S_residue"])+1) % int(second["modulus"]))
)
mutation(
    "wrong_second_kind_valuation", second_valid, second,
    "factorial_times_S_valuation",
    str(int(second["factorial_times_S_valuation"])+1)
)
mutation(
    "wrong_period_flag", second_valid, second,
    "period_checks_pass", "False"
)
mutation("wrong_second_kind_status", second_valid, second, "status", "FAIL")

controls.append({
    "label": "missing_polynomial_row",
    "rejected": not poly_domain_valid(poly_rows[:-1])
})
controls.append({
    "label": "duplicate_replaces_polynomial_row",
    "rejected": not poly_domain_valid(poly_rows[:-1]+[poly_rows[0]])
})

if len(controls) != 12 or not all(c["rejected"] for c in controls):
    failures.append("negative control failure")

if (
    len(checks), exact_identity_checks, lifted_checks, period_checks
) != (8370, 414, 2070, 6190):
    failures.append("check count mismatch")

if Path(__file__).read_bytes() != source:
    failures.append("source changed during run")

table = ROOT / "semantic_checks.csv"
with table.open("x", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(checks[0]))
    writer.writeheader()
    writer.writerows(checks)

report = {
    "status": "PASS" if not failures else "FAIL",
    "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    "python": platform.python_version(),
    "source_sha256": sha(source),
    "table_sha256": {"semantic_checks.csv": sha(table.read_bytes())},
    "parent_hashes": EXPECTED_HASHES,
    "polynomial_rows_verified": len(poly_rows),
    "second_kind_rows_verified": len(second_rows),
    "exact_inclusion_exclusion_checks": exact_identity_checks,
    "lifted_modulus_recovery_checks": lifted_checks,
    "recurrence_period_comparisons": period_checks,
    "negative_controls": controls,
    "failures": failures,
    "scope": "Finite semantic checks of existing saved certificates",
    "polynomial_nonintegrality_target": "reciprocal symmetric sums, not canonical ratio",
    "periodicity_target": "factorial(k)*S(n,k), not minimum periods of S",
    "formal_certification": "OPEN",
    "novelty_clearance": "OPEN",
    "promotion": False,
    "git_operations": 0
}

receipt = ROOT / "receipt.json"
with receipt.open("x", encoding="utf-8") as stream:
    json.dump(report, stream, indent=2, sort_keys=True)

print("STATUS=" + report["status"])
print("EXACT_LEADING_RESIDUE_CHECKS=" + str(len(poly_rows)))
print("SECOND_KIND_SAVED_ROWS_VERIFIED=" + str(len(second_rows)))
print("EXACT_INCLUSION_EXCLUSION_CHECKS=" + str(exact_identity_checks))
print("LIFTED_MODULUS_RECOVERY_CHECKS=" + str(lifted_checks))
print("RECURRENCE_PERIOD_COMPARISONS=" + str(period_checks))
print("NEGATIVE_CONTROLS_REJECTED=" + str(sum(c["rejected"] for c in controls)))
print("FAILURES=" + str(len(failures)))
print("SOURCE_SHA256=" + sha(source))
print("RECEIPT_SHA256=" + sha(receipt.read_bytes()))
print("EVIDENCE_DIRECTORY=" + str(ROOT))
print("CSV_DUMP=NO")
print("GIT_OPERATIONS=0")
print("PROMOTION=FALSE")

if failures:
    raise SystemExit(1)
