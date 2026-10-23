from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import json
import platform
import sys

ROOT = Path(__file__).resolve().parent

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def v3(x):
    need(x > 0, "Valuation input must be positive")
    result = 0
    while x % 3 == 0:
        result += 1
        x //= 3
    return result

def vf(x):
    result = 0
    while x:
        x //= 3
        result += x
    return result

def partitions(n, m):
    table = [[0]*(m+1) for _ in range(n+1)]
    table[0][0] = 1
    for total in range(1, n+1):
        for parts in range(1, min(total, m)+1):
            table[total][parts] = (
                table[total-1][parts-1]
                + (table[total-parts][parts] if total >= parts else 0)
            )
    return table[n][m]

def save_csv(name, rows):
    path = ROOT / name
    with path.open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return sha(path.read_bytes())

source_bytes = Path(__file__).read_bytes()
selected = {
    a*3**r+1: (a, r)
    for a in (1, 2)
    for r in range(1, 7)
}
same_rows = []
opposite_rows = []
previous = [1]
transfer_checks = 0
step_checks = 0

for n in range(1, max(selected)+1):
    current = [0]*(n+1)
    for M in range(1, n+1):
        current[M] = (
            (n-1)*(previous[M] if M < len(previous) else 0)
            + previous[M-1]
        )

    if n in selected:
        a, r = selected[n]
        N = n-1
        print("RUNNING=adjacent-total n=" + str(n), flush=True)

        for u in range(1, N-1):
            if (u-a) % 2 == 0:
                step_checks += 1
                need(
                    v3(previous[u+2])-v3(previous[u]) >= -2*r+2,
                    "Step bound failed at " + str((N, u))
                )

        for M in range(1, n):
            if (M-a) % 2 == 0:
                transfer_checks += 1
                need(
                    v3(current[M])
                    == r+v3(M+1)+v3(previous[M]),
                    "Complementary transfer failed at " + str((n, M))
                )

        for M in range(2, n):
            if (M-n) % 2:
                continue
            m = M-1
            base_v = v3(previous[m])
            shifted_v = v3(current[M])
            gap = vf(n)-vf(M)-shifted_v
            need(base_v == shifted_v, "Same-parity transfer failed")

            if a == 1 and m == 1:
                ell = ""
                k = ""
                predicted = r
            else:
                ell = 1
                while m > a*3**ell-2:
                    ell += 1
                k = a*3**ell-m
                need(
                    1 <= ell <= r
                    and k % 2 == 0
                    and 2 <= k <= 2*a*3**(ell-1)+1 < a*3**ell,
                    "Even-offset hypotheses failed"
                )
                predicted = 1+(r-ell)*m+vf(k)-v3(k-1)

            need(gap == predicted and gap > 0, "Same-parity gap failed")
            same_rows.append({
                "a": a, "r": r, "n": n, "M": M,
                "base_N": N, "base_m": m,
                "ell": ell, "k": k,
                "base_stirling_v3": base_v,
                "shifted_stirling_v3": shifted_v,
                "gap": gap, "predicted_gap": predicted,
                "status": "PASS"
            })

        for M in range(2, (n-1)//2+1):
            if (M-n) % 2 == 0:
                continue
            base_v = v3(previous[M])
            shifted_v = v3(current[M])
            excess = shifted_v-r-base_v
            gap = vf(n)-vf(M)-shifted_v
            need(excess == v3(M+1), "Cancellation formula failed")

            partition_value = ""
            partition_v = ""
            full_gap = ""
            if gap <= 0:
                need((n, M, gap) == (7, 2, 0), "Unexpected exception")
                partition_value = partitions(n, M)
                partition_v = v3(partition_value)
                full_gap = gap+partition_v
                need(
                    partition_value == 3 and full_gap == 1,
                    "Exceptional exclusion failed"
                )

            opposite_rows.append({
                "a": a, "r": r, "n": n, "M": M,
                "residue_mod3": M % 3,
                "base_stirling_v3": base_v,
                "shifted_stirling_v3": shifted_v,
                "excess_over_base_plus_r": excess,
                "gap": gap,
                "partition_count_if_needed": partition_value,
                "partition_v3_if_needed": partition_v,
                "full_gap_if_evaluated": full_gap,
                "equality_excluded": True,
                "status": "PASS"
            })

    previous = current

need(len(same_rows) == 1629, "Same-parity count differs")
need(len(opposite_rows) == 810, "Complementary count differs")
need(transfer_checks == 1641, "Transfer count differs")
need(step_checks == 1629, "Step count differs")

exceptions = [
    [row["n"], row["M"], row["gap"]]
    for row in opposite_rows if row["gap"] <= 0
]
need(exceptions == [[7, 2, 0]], "Exception list differs")
need(Path(__file__).read_bytes() == source_bytes, "Source changed")

table_hashes = {
    "same_parity_certificates.csv":
        save_csv("same_parity_certificates.csv", same_rows),
    "complementary_case_B_certificates.csv":
        save_csv("complementary_case_B_certificates.csv", opposite_rows)
}

receipt = {
    "status": "PASS",
    "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    "python": platform.python_version(),
    "executable": sys.executable,
    "source_sha256": sha(source_bytes),
    "table_sha256": table_hashes,
    "same_parity_rows": len(same_rows),
    "complementary_case_B_rows": len(opposite_rows),
    "full_complementary_transfer_checks": transfer_checks,
    "valuation_step_checks": step_checks,
    "nonpositive_complementary_case_B_gaps": exceptions,
    "exception_partition_count": 3,
    "exception_partition_valuation": 1,
    "exception_full_gap": 1,
    "scope": "Finite exact diagnostics for n=a*3^r+1, a=1,2, r=1,...,6",
    "M_equals_1_boundary_in_csv_tables": False,
    "proof_included": False,
    "formal_certification": "OPEN",
    "novelty_clearance": "OPEN",
    "global_classification": "OPEN",
    "promotion": False,
    "git_operations_by_audit": 0,
    "prior_print_only_diagnostics_recomputed_for_preservation": True
}
with (ROOT / "receipt.json").open("x", encoding="utf-8") as stream:
    json.dump(receipt, stream, indent=2, sort_keys=True)

print("AUDIT_STATUS=PASS")
print("SAME_PARITY_ROWS=1629")
print("COMPLEMENTARY_CASE_B_ROWS=810")
print("FULL_TRANSFER_CHECKS=1641")
print("VALUATION_STEP_CHECKS=1629")
print("EXCEPTION_7_2=RESOLVED")
print("CSV_DUMP=NO")
