from pathlib import Path
from fractions import Fraction
from math import factorial
from datetime import datetime, timezone
import csv
import hashlib
import json
import platform

ROOT = Path(__file__).resolve().parent
PARENT = (
    Path.home() / "AQARION"
    / "AQARION-QUANTARION-AI/research"
    / "ordered-cycle-ratio-audit/polynomial-certificate-chain"
    / "polynomial-second-kind"
)
EXPECTED = {
    "audit.py": "57e6634d46c1059ca0f5e7ce4c5ff16b621344f2ef62529d77e528cfafa38588",
    "receipt.json": "d7b602fdd2ce26d609985dcc9f2f8f5f5699caf004cd40b58728e3673ab560f3",
    "polynomial_certificates.csv": "ec8a4a1723877364e8919bb208640093ee0a6bf82b09490f5019295bc0b1873c"
}

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def vi(x, p):
    need(x != 0, "Zero valuation requires separate handling")
    x = abs(x)
    result = 0
    while x % p == 0:
        result += 1
        x //= p
    return result

def vq(x, p):
    return vi(x.numerator, p)-vi(x.denominator, p)

source = Path(__file__).read_bytes()
for name, expected in EXPECTED.items():
    path = PARENT / name
    need(path.is_file() and not path.is_symlink(), "Missing or linked input")
    need(sha(path.read_bytes()) == expected, "Input hash differs: " + name)

parent_receipt = json.loads((PARENT / "receipt.json").read_bytes())
need(parent_receipt["status"] == "PASS", "Parent is not PASS")
need(
    parent_receipt["source_sha256"] == EXPECTED["audit.py"],
    "Parent source binding differs"
)
need(
    parent_receipt["table_sha256"]["polynomial_certificates.csv"]
    == EXPECTED["polynomial_certificates.csv"],
    "Parent polynomial binding differs"
)

with (PARENT / "polynomial_certificates.csv").open(
    newline="", encoding="utf-8"
) as stream:
    saved = list(csv.DictReader(stream))

index = {
    (row["polynomial"], int(row["n"]), int(row["k"]), int(row["p"])): row
    for row in saved
}
need(len(index) == len(saved) == 6300, "Parent domain count or duplicates differ")

NMAX = 21
primes = [2, 3, 5, 7, 11]
C = [[0]*(NMAX+1) for _ in range(NMAX+1)]
P = [[0]*(NMAX+1) for _ in range(NMAX+1)]
C[0][0] = 1
P[0][0] = 1

for n in range(1, NMAX+1):
    for m in range(1, n+1):
        C[n][m] = (n-1)*C[n-1][m]+C[n-1][m-1]
        P[n][m] = P[n-1][m-1]+P[n-m][m]

def partition_alternate(n, m):
    target = n-m
    dp = [0]*(target+1)
    dp[0] = 1
    for part in range(1, m+1):
        for total in range(part, target+1):
            dp[total] += dp[total-part]
    return dp[target]

rows = []
failures = []
pairs = 0
equalities = []

print("RUNNING=canonical ratio and auxiliary Q bridges", flush=True)

for n in range(3, NMAX+1):
    elementary = [Fraction(0) for _ in range(n)]
    elementary[0] = Fraction(1)
    for j in range(1, n):
        for k in range(j, 0, -1):
            elementary[k] += elementary[k-1]/j

    for m in range(2, n):
        pairs += 1
        E = elementary[m-1]
        partitions = P[n][m]
        R = Fraction(factorial(m)*C[n][m], factorial(n)*partitions)
        Q = Fraction(factorial(n), factorial(m)*C[n][m])

        identities_ok = (
            partitions == partition_alternate(n, m)
            and C[n][m] == factorial(n-1)*E
            and R == Fraction(factorial(m), n*partitions)*E
            and Q == Fraction(n, factorial(m))/E
            and R*Q*partitions == 1
        )
        if not identities_ok:
            failures.append(["pair_identity", n, m])
        if R == 1:
            equalities.append([n, m])

        for p in primes:
            saved_row = index[("x", n-1, m-1, p)]
            vE = vq(E, p)
            vP = vi(partitions, p)
            gap = (
                vi(factorial(n), p)
                - vi(factorial(m), p)
                - vi(C[n][m], p)
            )
            direct_R = vq(R, p)
            direct_Q = vq(Q, p)
            bridge_R = (
                vi(factorial(m), p)+vE-vi(n, p)-vP
            )
            bridge_Q = vi(n, p)-vi(factorial(m), p)-vE

            valid = (
                identities_ok
                and saved_row["status"] == "PASS"
                and int(saved_row["actual_valuation"]) == vE
                and direct_Q == bridge_Q == gap
                and direct_R == bridge_R == -gap-vP
            )
            if not valid:
                failures.append(["valuation_bridge", n, m, p])

            rows.append({
                "n": n, "m": m, "p": p,
                "partition_count": partitions,
                "E_numerator": E.numerator,
                "E_denominator": E.denominator,
                "Q_numerator": Q.numerator,
                "Q_denominator": Q.denominator,
                "R_numerator": R.numerator,
                "R_denominator": R.denominator,
                "vp_E": vE, "vp_partition": vP,
                "gap_G": gap, "vp_Q": direct_Q,
                "vp_R": direct_R,
                "canonical_bridge": bridge_R,
                "ratio_nonintegrality_witness": direct_R < 0,
                "ratio_equality_exclusion_witness": direct_R != 0,
                "status": "PASS" if valid else "FAIL"
            })

E52 = Fraction(25, 12)
Q52 = Fraction(6, 5)
R52 = Fraction(5, 12)
G52 = vi(factorial(5), 5)-vi(factorial(2), 5)-vi(C[5][2], 5)

controls = {
    "auxiliary_Q_is_not_canonical_R": Q52 != R52,
    "omitted_partition_factor_changes_ratio":
        Fraction(factorial(2)*C[5][2], factorial(5)) != R52,
    "wrong_gap_sign_rejected": vq(R52, 5) != G52,
    "positive_local_valuation_does_not_imply_integer":
        vq(E52, 5) > 0 and E52.denominator != 1
}
if not all(controls.values()):
    failures.append(["normalization_control"])
if pairs != 190 or len(rows) != 950:
    failures.append(["domain_count"])
if Path(__file__).read_bytes() != source:
    failures.append(["source_changed"])

table = ROOT / "canonical_ratio_bridge.csv"
with table.open("x", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

report = {
    "status": "PASS" if not failures else "FAIL",
    "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    "python": platform.python_version(),
    "source_sha256": sha(source),
    "table_sha256": {
        "canonical_ratio_bridge.csv": sha(table.read_bytes())
    },
    "parent_hashes": EXPECTED,
    "distinct_pair_identity_checks": pairs,
    "prime_pair_checks": len(rows),
    "normalization_controls": controls,
    "observed_equalities_in_tested_domain": equalities,
    "canonical_R": "m!*c(n,m)/(n!*P(n,m))",
    "auxiliary_Q": "n!/(m!*c(n,m))",
    "relation": "R*Q*P=1; vp(R)=-G-vp(P); vp(Q)=G",
    "failures": failures,
    "formal_certification": "OPEN",
    "novelty_clearance": "OPEN",
    "global_classification": "OPEN",
    "promotion": False,
    "git_operations": 0
}

receipt = ROOT / "receipt.json"
with receipt.open("x", encoding="utf-8") as stream:
    json.dump(report, stream, indent=2, sort_keys=True)

print("STATUS=" + report["status"])
print("DISTINCT_PAIR_IDENTITY_CHECKS=" + str(pairs))
print("PRIME_PAIR_BRIDGE_CHECKS=" + str(len(rows)))
print("NORMALIZATION_CONTROLS=" + str(sum(controls.values())) + "/4")
print("OBSERVED_EQUALITIES=" + json.dumps(equalities))
print("FAILURES=" + str(len(failures)))
print("SOURCE_SHA256=" + sha(source))
print("RECEIPT_SHA256=" + sha(receipt.read_bytes()))
print("EVIDENCE_DIRECTORY=" + str(ROOT))
print("CSV_DUMP=NO")
print("GIT_OPERATIONS=0")
print("PROMOTION=FALSE")
print("GLOBAL_CLASSIFICATION=OPEN")

if failures:
    raise SystemExit(1)
