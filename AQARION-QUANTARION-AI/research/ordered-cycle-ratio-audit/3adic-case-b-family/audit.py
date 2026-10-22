#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import json
import os

ROOT = Path(os.environ["WORK"])

def need(condition, message):
    if not condition:
        raise RuntimeError(message)

def v3(x):
    if x == 0:
        raise ValueError("v3(0) is undefined for this audit")
    x = abs(x)
    result = 0
    while x % 3 == 0:
        x //= 3
        result += 1
    return result

def digit_sum3(x):
    result = 0
    while x:
        result += x % 3
        x //= 3
    return result

def stirling1(n, k):
    # Unsigned c(n,k), exact integer recurrence.
    dp = [0] * (k + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        nxt = [0] * (k + 1)
        for j in range(1, min(i, k) + 1):
            nxt[j] = dp[j - 1] + (i - 1) * dp[j]
        dp = nxt
    return dp[k]

rows = []
for r in range(2, 7):
    n = 3**r
    m = 3**(r - 1) - 2
    d = n - m
    q = 3**(r - 1)

    c = stirling1(n, m)
    vc = v3(c)

    # Legendre: v3(n!/m!) = (d - s3(n) + s3(m))/2.
    vf = (d - digit_sum3(n) + digit_sum3(m)) // 2

    need(digit_sum3(n) == 1, "Digit sum of 3^r")
    need(digit_sum3(m) == 2*r - 3, "Digit sum of 3^(r-1)-2")
    need(vc == r, "Stirling valuation disagrees with theorem")
    need(vf == q + r - 1, "Factorial valuation disagrees with Legendre")
    need(vf > vc, "Necessary valuation obstruction failed")
    need(m < d, "Pair is not in Case B")

    rows.append({
        "r": r,
        "n": n,
        "m": m,
        "deficit": d,
        "v3_stirling_direct": vc,
        "v3_stirling_formula": r,
        "v3_factorial_ratio": vf,
        "valuation_gap": vf - vc,
        "case": "B",
        "status": "PASS",
    })

csv_path = ROOT / "caseB_3adic_family.csv"
with csv_path.open("x", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

source_path = Path(__file__)
source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
csv_hash = hashlib.sha256(csv_path.read_bytes()).hexdigest()

receipt = {
    "status": "PASS",
    "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    "source_sha256": source_hash,
    "table_sha256": csv_hash,
    "cases": len(rows),
    "direct_stirling_valuations": "PASS",
    "legendre_factorial_valuations": "PASS",
    "all_pairs_in_case_B": True,
    "global_ratio_classification": "OPEN",
    "git_operations": 0,
    "publication": "NOT PERFORMED",
}
receipt_path = ROOT / "receipt.json"
with receipt_path.open("x", encoding="utf-8") as f:
    json.dump(receipt, f, indent=2)

for row in rows:
    print(
        f"r={row['r']} n={row['n']} m={row['m']} "
        f"v3_c={row['v3_stirling_direct']} "
        f"v3_factorial={row['v3_factorial_ratio']} "
        f"gap={row['valuation_gap']} CASE_B=PASS"
    )

print("STATUS=PASS")
print("CASES=5")
print("SOURCE_SHA256=" + source_hash)
print("TABLE_SHA256=" + csv_hash)
print("RECEIPT_SHA256=" +
      hashlib.sha256(receipt_path.read_bytes()).hexdigest())
print("EVIDENCE_DIRECTORY=" + str(ROOT))
print("GLOBAL_CLASSIFICATION=OPEN")
print("PUBLICATION=NOT_PERFORMED")
