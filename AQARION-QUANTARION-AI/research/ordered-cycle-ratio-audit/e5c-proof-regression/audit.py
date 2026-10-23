from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction
from math import factorial
from collections import Counter
import csv
import hashlib
import json
import platform

ROOT = Path(__file__).resolve().parent
NMAX = 48

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

source = Path(__file__).read_bytes()
C = [[0]*(NMAX+1) for _ in range(NMAX+1)]
P = [[0]*(NMAX+1) for _ in range(NMAX+1)]
C[0][0] = 1
P[0][0] = 1

for n in range(1, NMAX+1):
    for m in range(1, n+1):
        C[n][m] = (n-1)*C[n-1][m]+C[n-1][m-1]
        P[n][m] = P[n-1][m-1]+P[n-m][m]

ordinary = [0]*(NMAX+1)
ordinary[0] = 1
for part in range(1, NMAX+1):
    for total in range(part, NMAX+1):
        ordinary[total] += ordinary[total-part]

def R(n, m):
    need(1 <= m <= n <= NMAX, "Ratio input outside table")
    return Fraction(
        factorial(m)*C[n][m],
        factorial(n)*P[n][m]
    )

def partitions(total, minimum=1):
    if total == 0:
        yield ()
        return
    for part in range(minimum, total+1):
        for tail in partitions(total-part, part):
            yield (part,)+tail

def falling(x, degree):
    result = 1
    for j in range(degree):
        result *= x-j
    return result

coefficients = {}
for d in range(1, 13):
    coefficients[d] = []
    for partition in partitions(d):
        denominator = 1
        for j, multiplicity in Counter(partition).items():
            denominator *= (j+1)**multiplicity * factorial(multiplicity)
        coefficients[d].append((len(partition), denominator))

def F(n, d):
    need(n >= 2*d, "Polynomial-to-ratio comparison requires n>=2d")
    return sum(
        (
            Fraction(falling(n-d, degree), denominator)
            for degree, denominator in coefficients[d]
        ),
        Fraction(0)
    )

def closed(n, d):
    if d == 1:
        return Fraction(n-1, 2)
    if d == 2:
        return Fraction((n-2)*(3*n-1), 48)
    if d == 3:
        return Fraction(n*(n-1)*(n-3), 144)
    if d == 4:
        return Fraction(
            (n-4)*(15*n**3-30*n**2+5*n+2),
            28800
        )
    raise ValueError("Closed form supplied only for deficits 1..4")

def A(d):
    need(1 <= 2*d <= NMAX, "A(d) requires Stirling row 2*d")
    return Fraction(
        factorial(d)*C[2*d][d],
        factorial(2*d)
    )

records = []
failures = []
counts = Counter()

def record(group, label, passed, left="", right=""):
    counts[group] += 1
    records.append({
        "group": group,
        "label": label,
        "left": str(left),
        "right": str(right),
        "status": "PASS" if passed else "FAIL"
    })
    if not passed:
        failures.append({"group": group, "label": label})

print("RUNNING=cycle polynomials and quantitative monotonicity", flush=True)

for d in range(1, 13):
    record(
        "cycle_type_count", str(d),
        len(coefficients[d]) == ordinary[d],
        len(coefficients[d]), ordinary[d]
    )

    for n in range(2*d, 4*d+1):
        exact = R(n, n-d)
        polynomial = F(n, d)
        record(
            "cycle_polynomial", str((n, d)),
            polynomial == ordinary[d]*exact,
            polynomial, ordinary[d]*exact
        )
        if d <= 4:
            formula = closed(n, d)
            record(
                "closed_form", str((n, d)),
                formula == exact, formula, exact
            )
            if d >= 2:
                incorrect = exact*factorial(d)
                record(
                    "extra_factorial_rejection", str((n, d)),
                    incorrect != exact, incorrect, exact
                )

    for n in range(2*d, 4*d):
        difference = R(n+1, n+1-d)-R(n, n-d)
        lower = Fraction(1, (d+1)*ordinary[d])
        record(
            "monotonic_increment", str((n, d)),
            difference >= lower, difference, lower
        )

print("RUNNING=induction bases and coefficient inequalities", flush=True)

base_values = {}
for d in range(5, 10):
    value = A(d)
    base_values[str(d)] = {
        "A": str(value),
        "partition_count": ordinary[d],
        "boundary_ratio": str(value/ordinary[d])
    }
    record(
        "induction_base", str(d),
        value > ordinary[d], value, ordinary[d]
    )

for a in range(1, 7):
    for b in range(a, 7):
        left = A(a+b)
        right = A(a)*A(b)
        record(
            "coefficient_supermultiplicativity", str((a, b)),
            left >= right, left, right
        )

for d in range(10, 20):
    first = A(d)
    second = A(5)*A(d-5)
    third = ordinary[5]*ordinary[d-5]
    fourth = ordinary[d]
    valid = first >= second > third > fourth
    record(
        "induction_chain", str(d), valid,
        str((first, second)), str((third, fourth))
    )

for n, expected in ((4, Fraction(1,4)), (5, Fraction(5,12))):
    actual = R(n, n-3)
    invalid_extension = closed(n, 3)
    record(
        "domain_control", str((n, n-3)),
        actual == expected and invalid_extension != expected,
        actual, invalid_extension
    )

for n in (1, 2, 3, 10, 48):
    record("diagonal", str(n), R(n, n) == 1, R(n, n), 1)

print("RUNNING=finite Case A sign regression", flush=True)
below_one = {(2,1), (4,2), (5,3), (6,3), (8,4)}

for n in range(1, NMAX+1):
    for m in range((n+1)//2, n):
        value = R(n, m)
        observed = (value > 1)-(value < 1)
        expected = (
            -1 if (n, m) in below_one
            else 0 if (n, m) == (3, 2)
            else 1
        )
        record(
            "case_A_sign", str((n, m)),
            observed == expected, observed, expected
        )

expected_counts = {
    "cycle_type_count": 12,
    "cycle_polynomial": 168,
    "closed_form": 24,
    "monotonic_increment": 156,
    "extra_factorial_rejection": 21,
    "induction_base": 5,
    "coefficient_supermultiplicativity": 21,
    "induction_chain": 10,
    "domain_control": 2,
    "diagonal": 5,
    "case_A_sign": 576
}
if dict(counts) != expected_counts or len(records) != 1000:
    failures.append({"group": "accounting", "label": "count_mismatch"})
if Path(__file__).read_bytes() != source:
    failures.append({"group": "integrity", "label": "source_changed"})

table = ROOT / "e5c_regression_checks.csv"
with table.open("x", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(records[0]))
    writer.writeheader()
    writer.writerows(records)

notes_lines = [
    "# E5C Case A proof notes",
    "",
    "Canonical ratio: R(n,m)=m!*c(n,m)/(n!*P(n,m)).",
    "Off-diagonal Case A: 1<=m<n<=2m; d=n-m>=1; n>=2d.",
    "Only in this domain is P(n,n-d)=p(d) used.",
    "",
    "Cycle types with sum(j*b_j)=d and ell=sum(b_j) give",
    "F_d(n)=p(d)*R(n,n-d)",
    "=sum((n-d)_falling_ell / product((j+1)^b_j*b_j!)).",
    "",
    "The identity (x+1)_falling_ell-x_falling_ell",
    "=ell*x_falling_(ell-1), together with positive coefficients,",
    "gives F_d(n+1)-F_d(n)>=1/(d+1).",
    "Thus R increases strictly at fixed d for n>=2d.",
    "",
    "Let A_d=[z^(2d)](-log(1-z))^d.",
    "Nonnegative coefficient convolution gives A_(a+b)>=A_a*A_b.",
    "Five exact bases d=5,...,9 satisfy A_d>p(d).",
    "",
    "External dependency: Bessenrodt-Ono, Theorem 2.1,",
    "Maximal Multiplicative Properties of Partitions.",
    "For a,b>=2 and a+b>9, p(a)*p(b)>p(a+b).",
    "Source: https://uva.theopenscholar.com/files/ken-ono/files/149_8.pdf",
    "",
    "For d>=10, use a=5,b=d-5 and induction:",
    "A_d>=A_5*A_(d-5)>p(5)*p(d-5)>p(d).",
    "This proves R(2d,d)>1 for d>=5; monotonicity extends it.",
    "",
    "Deficits 1,...,4 are handled by the recorded closed forms.",
    "Case A below-one exceptions:",
    "(2,1),(4,2),(5,3),(6,3),(8,4).",
    "Only off-diagonal Case A equality: (3,2).",
    "Every diagonal has R(n,n)=1.",
    "",
    "The argument is derived and depends on the cited theorem.",
    "Finite tests corroborate it; they do not prove the external",
    "partition inequality or provide Lean certification.",
    "No arbitrary-total Case B classification is asserted.",
    "Novelty clearance and formal certification remain OPEN."
]
notes = ROOT / "PROOF_NOTES.md"
with notes.open("x", encoding="utf-8") as stream:
    stream.write(chr(10).join(notes_lines)+chr(10))

report = {
    "status": "PASS" if not failures else "FAIL",
    "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    "python": platform.python_version(),
    "source_sha256": sha(source),
    "files": {
        table.name: sha(table.read_bytes()),
        notes.name: sha(notes.read_bytes())
    },
    "maximum_stirling_order": NMAX,
    "test_count": len(records),
    "test_groups": dict(counts),
    "induction_base_values": base_values,
    "external_theorem": {
        "authors": "Christine Bessenrodt and Ken Ono",
        "title": "Maximal Multiplicative Properties of Partitions",
        "reference": "Theorem 2.1",
        "strict_specialization": "a,b>=2 and a+b>9"
    },
    "external_theorem_proved_by_this_script": False,
    "proof_scope": "Off-diagonal Case A, with diagonal controls",
    "case_B_classification": "OPEN",
    "formal_certification": "OPEN",
    "novelty_clearance": "OPEN",
    "production_integration": False,
    "promotion": False,
    "git_operations": 0,
    "failures": failures
}
receipt = ROOT / "receipt.json"
with receipt.open("x", encoding="utf-8") as stream:
    json.dump(report, stream, indent=2, sort_keys=True)

print("STATUS=" + report["status"])
print("E5C_REGRESSION_CHECKS=" + str(len(records)))
for group, count in counts.items():
    print(group.upper() + "=" + str(count))
print("FAILURES=" + str(len(failures)))
print("SOURCE_SHA256=" + sha(source))
print("RECEIPT_SHA256=" + sha(receipt.read_bytes()))
print("EVIDENCE_DIRECTORY=" + str(ROOT))
print("CSV_DUMP=NO")
print("GIT_OPERATIONS=0")
print("FORMAL_CERTIFICATION=OPEN")
print("PROMOTION=FALSE")
print("GLOBAL_CLASSIFICATION=OPEN")

if failures:
    raise SystemExit(1)
