#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
from math import isqrt
import csv
import hashlib
import io
import json
import platform
import sys
import traceback

ROOT = Path(__file__).resolve().parent
INPUT = Path.home() / "AQARION_AUDIT/cycle_ratio/3adic-parity.Jb4Pnm"
INPUT_SOURCE_HASH = (
    "8f2e34bd5d5d6221c527e9010a09db78ab3a035c847ece1951ff54daed5d954b"
)
INPUT_TABLE_HASH = (
    "5385ca83be27ba76c1cab9e011d25a2f48ebd273ee9f364b67828e98a0289a8c"
)
INPUT_RECEIPT_HASH = (
    "4a0ae4ce34b3c23716a691bd8fe7a25d56759249129998d2e7cc6915566865f8"
)
MAX_R = 6

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def v3(n):
    need(n > 0, "Valuation requires a positive integer")
    result = 0
    while n % 3 == 0:
        result += 1
        n //= 3
    return result

def vf(n):
    result = 0
    while n:
        n //= 3
        result += n
    return result

def partition_count(n, m):
    table = [[0]*(m+1) for _ in range(n+1)]
    table[0][0] = 1
    for total in range(1, n+1):
        for count in range(1, min(m, total)+1):
            table[total][count] = (
                table[total-1][count-1]
                + (table[total-count][count] if total >= count else 0)
            )
    return table[n][m]

def main():
    source = Path(__file__).read_bytes()

    source_raw = (INPUT / "audit.py").read_bytes()
    table_raw = (INPUT / "valuation_certificates.csv").read_bytes()
    receipt_raw = (INPUT / "receipt.json").read_bytes()

    need(sha(source_raw) == INPUT_SOURCE_HASH, "Input source changed")
    need(sha(table_raw) == INPUT_TABLE_HASH, "Input table changed")
    need(sha(receipt_raw) == INPUT_RECEIPT_HASH, "Input receipt changed")

    prior = json.loads(receipt_raw)
    need(prior["status"] == "PASS", "Input audit is not PASS")
    need(prior["source_sha256"] == INPUT_SOURCE_HASH, "Input source binding")
    need(prior["table_sha256"] == INPUT_TABLE_HASH, "Input table binding")

    previous_rows = list(csv.DictReader(io.StringIO(table_raw.decode())))
    reused = set()

    for row in previous_rows:
        n, m = int(row["N"]), int(row["m"])
        if n > 2*m:
            need(row["status"] == "PASS", "Reused certificate failed")
            need(int(row["observed_gap"]) > 0, "Reused gap not positive")
            need((n, m) not in reused, "Duplicate reused pair")
            reused.add((n, m))

    need(len(reused) == 816, "Reused Case B count differs")

    selected = {
        a*3**r: (a, r)
        for a in (1, 2)
        for r in range(1, MAX_R+1)
    }
    maximum = max(selected)
    width = (maximum-1)//2
    previous = [1] + [0]*width
    rows = []
    nonpositive = []
    newly_checked = set()

    for n in range(1, maximum+1):
        current = [0]*(width+1)

        for m in range(1, min(n, width)+1):
            current[m] = (
                (n-1)*previous[m] + previous[m-1]
            )

        if n in selected:
            a, r = selected[n]
            print("RUNNING=opposite-parity N=" + str(n), flush=True)

            for m in range(1, (n-1)//2+1):
                if (m-a) % 2 == 0:
                    continue

                ell = 1
                while m > a*3**ell-3:
                    ell += 1
                k = a*3**ell-m

                need(1 <= ell <= r, "Exponent translation")
                need(
                    3 <= k <= 2*a*3**(ell-1)+1 < a*3**ell
                    and k % 2 == 1,
                    "Odd-offset source hypotheses"
                )

                direct_vc = v3(current[m])
                formula_vc = (
                    a*(3**r-3**ell)//2
                    - (r-ell)*m
                    + 2*ell-1
                    - v3((k-1)//2)
                    + v3(k)
                )
                factorial_v = vf(n)-vf(m)
                gap = factorial_v-direct_vc
                simplified = (
                    (r-ell)*m + 1-ell
                    + vf(k-1) + v3(k-1)-v3(k)
                )

                need(direct_vc == formula_vc, "Stirling valuation mismatch")
                need(gap == simplified, "Simplified gap mismatch")

                partition_value = ""
                partition_valuation = ""
                if gap <= 0:
                    nonpositive.append([n, m, gap])
                    need((n, m, gap) == (9, 4, 0),
                         "Unexpected nonpositive gap")
                    partition_value = partition_count(n, m)
                    partition_valuation = v3(partition_value)
                    need(
                        partition_value == 6
                        and gap + partition_valuation > 0,
                        "Exceptional equality not excluded"
                    )

                newly_checked.add((n, m))
                rows.append({
                    "a": a, "r": r, "N": n, "m": m,
                    "ell": ell, "k": k,
                    "v3_stirling_direct": direct_vc,
                    "v3_stirling_formula": formula_vc,
                    "v3_factorial_quotient": factorial_v,
                    "gap": gap,
                    "partition_count_if_needed": partition_value,
                    "partition_valuation_if_needed": partition_valuation,
                    "equality_excluded": True,
                    "status": "PASS"
                })

        previous = current

    expected = {
        (n, m)
        for n in selected
        for m in range(1, (n-1)//2+1)
    }

    need(len(rows) == 813, "New comparison count differs")
    need(nonpositive == [[9, 4, 0]], "Exceptional gap list differs")
    need(not (reused & newly_checked), "Domains overlap")
    need(reused | newly_checked == expected, "Combined domain incomplete")
    need(len(expected) == 1629, "Combined Case B count differs")

    output_table = ROOT / "opposite_parity_certificates.csv"
    with output_table.open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    need(source == Path(__file__).read_bytes(), "Source changed during run")

    report = {
        "status": "PASS",
        "python": platform.python_version(),
        "executable": sys.executable,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": sha(source),
        "table_sha256": sha(output_table.read_bytes()),
        "input_receipt_sha256": INPUT_RECEIPT_HASH,
        "input_table_sha256": INPUT_TABLE_HASH,
        "source_theorem": "Qiu-Feng-Hong, arXiv:2109.13458v1, Theorem 1.1",
        "new_opposite_parity_checks": len(rows),
        "reused_same_parity_case_B_certificates": len(reused),
        "combined_case_B_pairs": len(expected),
        "nonpositive_basic_gaps": nonpositive,
        "exceptional_partition_count": 6,
        "all_checked_equalities_excluded": True,
        "scope": (
            "Finite validation of the source-dependent Case B "
            "classification for totals a*3^r; not arbitrary totals"
        ),
        "same_parity_audit_rerun": False,
        "global_ratio_classification": "OPEN",
        "git_operations": 0
    }

    receipt = ROOT / "receipt.json"
    with receipt.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)

    print("STATUS=PASS")
    print("NEW_OPPOSITE_PARITY_CHECKS=" + str(len(rows)))
    print("REUSED_CASE_B_CERTIFICATES=" + str(len(reused)))
    print("COMBINED_CASE_B_PAIRS=" + str(len(expected)))
    print("NONPOSITIVE_BASIC_GAPS=" + str(nonpositive))
    print("EXCEPTION_9_4=EXCLUDED_BY_PARTITION_VALUATION")
    print("SOURCE_SHA256=" + report["source_sha256"])
    print("TABLE_SHA256=" + report["table_sha256"])
    print("RECEIPT_SHA256=" + sha(receipt.read_bytes()))
    print("EVIDENCE_DIRECTORY=" + str(ROOT))
    print("GLOBAL_CLASSIFICATION=OPEN")
    print("NO_GIT_OPERATIONS")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        with (ROOT / "failure.json").open("x", encoding="utf-8") as stream:
            json.dump({
                "status": "FAIL",
                "source_sha256": sha(Path(__file__).read_bytes()),
                "traceback": traceback.format_exc()
            }, stream, indent=2)
        raise
