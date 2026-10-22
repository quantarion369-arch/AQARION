#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import json
import platform
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parent
MAX_R = 6

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def v3(x):
    need(x > 0, "Valuation requires a positive integer")
    value = 0
    while x % 3 == 0:
        value += 1
        x //= 3
    return value

def v3_factorial(n):
    value = 0
    while n:
        n //= 3
        value += n
    return value

def digit_sum3(n):
    value = 0
    while n:
        value += n % 3
        n //= 3
    return value

def main():
    started = time.monotonic()
    source = Path(__file__).read_bytes()
    selected = {
        a * 3**r: (a, r)
        for a in (1, 2)
        for r in range(1, MAX_R + 1)
    }

    rows = []
    summaries = []
    case_b_checks = 0
    elementary_cases = 0
    previous = [1]

    for n in range(1, max(selected) + 1):
        current = [0] * (n + 1)

        for m in range(1, n + 1):
            current[m] = (
                (n - 1) * (
                    previous[m] if m < len(previous) else 0
                )
                + previous[m - 1]
            )

        if n in selected:
            a, r = selected[n]
            print(
                "RUNNING=a=" + str(a)
                + " r=" + str(r)
                + " N=" + str(n),
                flush=True
            )

            count = 0
            minimum_gap = None

            for m in range(1, n):
                if (m - a) % 2:
                    continue

                ell = 1
                while m > a * 3**ell - 2:
                    ell += 1

                k = a * 3**ell - m
                elementary = a == 1 and m == 1

                need(1 <= ell <= r, "Invalid exponent translation")
                need(k >= 2 and k % 2 == 0, "Invalid even offset")

                if elementary:
                    elementary_cases += 1
                else:
                    need(
                        2 <= k <= 2*a*3**(ell - 1) + 1
                        < a*3**ell,
                        "Written source-theorem hypotheses fail"
                    )

                direct_vc = v3(current[m])
                factorial_v = v3_factorial(n) - v3_factorial(m)

                formula_vc = (
                    a * (3**r - 3**ell) // 2
                    - (r - ell) * m
                    + ell - 1
                    - v3(k)
                )

                predicted_gap = (
                    1 + (r - ell) * m + v3_factorial(k)
                )
                observed_gap = factorial_v - direct_vc

                need(
                    digit_sum3(m)
                    == a - 1 + 2*ell - digit_sum3(k - 1),
                    "Digit-complement identity"
                )
                need(
                    direct_vc == formula_vc,
                    "Direct Stirling/source-formula mismatch"
                )
                need(
                    observed_gap == predicted_gap,
                    "Exact valuation-gap identity"
                )
                need(observed_gap > 0, "No valuation obstruction")

                if elementary:
                    need(
                        direct_vc == v3_factorial(n - 1),
                        "Elementary c(N,1) identity"
                    )
                    need(observed_gap == r, "Elementary gap")

                in_case_b = n > 2*m
                case_b_checks += in_case_b
                count += 1

                minimum_gap = (
                    observed_gap
                    if minimum_gap is None
                    else min(minimum_gap, observed_gap)
                )

                rows.append({
                    "a": a,
                    "r": r,
                    "N": n,
                    "m": m,
                    "ell": ell,
                    "k": k,
                    "elementary_boundary": elementary,
                    "v3_stirling_direct": direct_vc,
                    "v3_stirling_formula": formula_vc,
                    "v3_factorial_quotient": factorial_v,
                    "observed_gap": observed_gap,
                    "predicted_gap": predicted_gap,
                    "case_B": in_case_b,
                    "status": "PASS"
                })

            summaries.append({
                "a": a,
                "r": r,
                "N": n,
                "comparisons": count,
                "minimum_gap": minimum_gap
            })

        previous = current

    need(len(rows) == 1629, "Comparison count differs")
    need(case_b_checks == 816, "Case B count differs")
    need(elementary_cases == MAX_R, "Elementary boundary count")

    table = ROOT / "valuation_certificates.csv"
    with table.open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    need(
        source == Path(__file__).read_bytes(),
        "Source changed during execution"
    )

    receipt = {
        "audit": "3adic_same_parity_valuation_gap",
        "status": "PASS",
        "python": platform.python_version(),
        "executable": sys.executable,
        "termux_executable_path_detected":
            "com.termux" in sys.executable,
        "completed_at_utc":
            datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "source_sha256": hashlib.sha256(source).hexdigest(),
        "table_sha256":
            hashlib.sha256(table.read_bytes()).hexdigest(),
        "source_theorem": {
            "authors": ["Min Qiu", "Yulu Feng", "Shaofang Hong"],
            "identifier": "arXiv:2109.13458v1",
            "theorem": "Theorem 1.1, even-offset case",
            "elementary_boundary":
                "a=1,m=1 checked directly using c(N,1)=(N-1)!"
        },
        "maximum_r": MAX_R,
        "maximum_N": max(selected),
        "comparisons": len(rows),
        "case_B_comparisons": case_b_checks,
        "elementary_boundary_comparisons": elementary_cases,
        "failures": 0,
        "summaries": summaries,
        "gap_identity": "1+(r-ell)*m+v3(k!)",
        "scope":
            "Finite verification of a literature-dependent infinite "
            "same-parity exclusion theorem",
        "global_ratio_classification": "OPEN",
        "git_operations": 0
    }

    output = ROOT / "receipt.json"
    with output.open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, indent=2)

    print("STATUS=PASS")
    print("SAME_PARITY_COMPARISONS=" + str(len(rows)))
    print("CASE_B_COMPARISONS=" + str(case_b_checks))
    print("ELEMENTARY_BOUNDARY_CHECKS=" + str(elementary_cases))
    print("VALUATION_GAP_FAILURES=0")
    print("SOURCE_SHA256=" + receipt["source_sha256"])
    print("TABLE_SHA256=" + receipt["table_sha256"])
    print(
        "RECEIPT_SHA256="
        + hashlib.sha256(output.read_bytes()).hexdigest()
    )
    print("EVIDENCE_DIRECTORY=" + str(ROOT))
    print("GLOBAL_CLASSIFICATION=OPEN")
    print("NO_GIT_OPERATIONS")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        failure = {
            "status": "FAIL",
            "source_sha256": hashlib.sha256(
                Path(__file__).read_bytes()
            ).hexdigest(),
            "traceback": traceback.format_exc()
        }
        with (ROOT / "failure.json").open(
            "x", encoding="utf-8"
        ) as stream:
            json.dump(failure, stream, indent=2)
        raise
