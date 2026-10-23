from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import json
import platform
import sys

ROOT = Path(__file__).resolve().parent

def sha(data):
    return hashlib.sha256(data).hexdigest()

def vp(x, p):
    if x <= 0:
        raise ValueError("Valuation input must be positive")
    result = 0
    while x % p == 0:
        result += 1
        x //= p
    return result

def vf(n, p):
    result = 0
    while n:
        n //= p
        result += n
    return result

def is_prime(p):
    if type(p) is not int or p < 2:
        return False
    d = 2
    while d*d <= p:
        if p % d == 0:
            return False
        d += 1
    return True

def accepts(n, m, p, r, gap):
    if not all(type(x) is int for x in (n, m, p, r, gap)):
        return False
    if m < 2 or n <= 2*m or r < 1 or not is_prime(p):
        return False
    q = p**r
    if not (m-1)*q <= n-1 < m*q:
        return False
    predicted = vp(n, p)-vp(m, p)+(m-1)*r
    return gap == predicted and gap > 0

def save_csv(name, rows):
    path = ROOT / name
    with path.open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return sha(path.read_bytes())

source = Path(__file__).read_bytes()
primes = [p for p in range(2, 161) if is_prime(p)]
powers = []
for p in primes:
    q = p
    r = 1
    while q <= 160:
        powers.append((q, p, r))
        q *= p
        r += 1
powers.sort()

step_primes = [2, 3, 5, 7, 11, 13, 17, 19]
selected = {}
for p in step_primes:
    for a in range(1, p):
        r = 1
        while a*p**r <= 600:
            selected.setdefault(a*p**r, []).append((p, a, r))
            r += 1

certificate_rows = []
step_rows = []
failures = []
counterexamples = []
pairs_examined = 0
witness_checks = 0
previous = [1]

print("RUNNING=exact recurrence through n=600", flush=True)

for n in range(1, 601):
    current = [0]*(n+1)
    for m in range(1, n+1):
        current[m] = (
            (n-1)*(previous[m] if m < len(previous) else 0)
            + previous[m-1]
        )

    if 5 <= n <= 160:
        for m in range(2, (n-1)//2+1):
            pairs_examined += 1
            witnesses = []
            for q, p, r in powers:
                if (n-1)//q != m-1:
                    continue
                witness_checks += 1
                predicted = vp(n, p)-vp(m, p)+(m-1)*r
                actual = vf(n, p)-vf(m, p)-vp(current[m], p)
                valid = (
                    actual == predicted
                    and accepts(n, m, p, r, predicted)
                )
                if not valid:
                    failures.append({
                        "kind": "certificate_mismatch",
                        "n": n, "m": m, "p": p, "r": r,
                        "actual": actual, "predicted": predicted
                    })
                witnesses.append((p, r, q, predicted, actual, valid))

            if witnesses:
                p, r, q, predicted, actual, valid = witnesses[0]
                certificate_rows.append({
                    "n": n, "m": m, "p": p, "r": r, "q": q,
                    "predicted_gap": predicted,
                    "direct_gap": actual,
                    "witness_count": len(witnesses),
                    "status": "PASS" if valid else "FAIL"
                })

    if n in selected:
        for p, a, r in selected[n]:
            stride = p-1
            bound = -stride*(r-1)
            for u in range(a, n-stride+1, stride):
                left = vp(current[u], p)
                right = vp(current[u+stride], p)
                difference = right-left
                slack = difference-bound
                row = {
                    "p": p, "a": a, "r": r, "N": n,
                    "u": u, "next_u": u+stride,
                    "left_vp": left, "right_vp": right,
                    "difference": difference,
                    "candidate_bound": bound,
                    "slack": slack,
                    "counterexample": slack < 0
                }
                step_rows.append(row)
                if slack < 0:
                    counterexamples.append(row)

    previous = current

negative_cases = [
    (15, 4, 4, 1, 4),
    (15, 4, 2, 0, 4),
    (15, 4, 2, 1, 4),
    (15, 4, 2, 2, 5),
    (8, 4, 2, 1, 1)
]
negative_rejections = sum(not accepts(*case) for case in negative_cases)
if not accepts(15, 4, 2, 2, 4):
    failures.append({"kind": "positive_control_rejected"})
if negative_rejections != len(negative_cases):
    failures.append({"kind": "negative_control_accepted"})

false_stride_two_difference = vp(1, 5)-vp(35, 5)
if false_stride_two_difference != -1:
    failures.append({"kind": "false_stride_two_control_failed"})

expected_counts = (
    pairs_examined == 6162
    and len(certificate_rows) == 1800
    and witness_checks == 4568
    and len(step_rows) == 2894
)
if not expected_counts:
    failures.append({"kind": "domain_count_mismatch"})

if Path(__file__).read_bytes() != source:
    failures.append({"kind": "source_changed_during_execution"})

table_hashes = {
    "prime_power_certificates.csv":
        save_csv("prime_power_certificates.csv", certificate_rows),
    "generalized_step_search.csv":
        save_csv("generalized_step_search.csv", step_rows)
}

report = {
    "status": "PASS" if not failures else "FAIL",
    "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    "python": platform.python_version(),
    "executable": sys.executable,
    "source_sha256": sha(source),
    "table_sha256": table_hashes,
    "certificate_pair_domain": "5<=n<=160, 2<=m<n/2",
    "pairs_examined": pairs_examined,
    "pairs_with_witness": len(certificate_rows),
    "individual_witness_checks": witness_checks,
    "negative_controls_rejected": negative_rejections,
    "negative_controls_total": len(negative_cases),
    "false_stride_two_extension_rejected": True,
    "step_search_domain": {
        "primes": step_primes,
        "N_limit": 600,
        "N": "a*p^r",
        "a": "1<=a<=p-1",
        "r": "r>=1",
        "u": "u congruent to a modulo p-1"
    },
    "step_comparisons": len(step_rows),
    "step_counterexamples": counterexamples,
    "general_step_conjecture": "UNPROVED",
    "failures": failures,
    "proof_formally_certified": False,
    "novelty_clearance": "OPEN",
    "global_classification": "OPEN",
    "promotion": False,
    "git_operations": 0
}

receipt = ROOT / "receipt.json"
with receipt.open("x", encoding="utf-8") as stream:
    json.dump(report, stream, indent=2, sort_keys=True)

print("STATUS=" + report["status"])
print("PAIRS_EXAMINED=" + str(pairs_examined))
print("PAIRS_WITH_CERTIFICATE=" + str(len(certificate_rows)))
print("INDIVIDUAL_WITNESS_CHECKS=" + str(witness_checks))
print("NEGATIVE_CONTROLS_REJECTED=" + str(negative_rejections))
print("STEP_COMPARISONS=" + str(len(step_rows)))
print("STEP_COUNTEREXAMPLES=" + str(len(counterexamples)))
print("GENERAL_STEP_CONJECTURE=UNPROVED")
print("SOURCE_SHA256=" + sha(source))
print("RECEIPT_SHA256=" + sha(receipt.read_bytes()))
print("EVIDENCE_DIRECTORY=" + str(ROOT))
print("CSV_DUMP=NO")
print("GIT_OPERATIONS=0")
print("PROMOTION=FALSE")
print("GLOBAL_CLASSIFICATION=OPEN")

if failures:
    raise SystemExit(1)
