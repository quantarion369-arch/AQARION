#!/usr/bin/env python3
from pathlib import Path
from collections import Counter, defaultdict
from fractions import Fraction as F
from datetime import datetime, timezone
import csv
import hashlib
import io
import json
import platform
import sys
import traceback

INPUT = Path.home() / "AQARION_AUDIT/cycle_ratio/joint-incidence.lLjYiR"
RECEIPT_HASH = (
    "9ba116540c801153d70f34c12ed360ef21a670298e2f6b859d6d0f16d856ad20"
)
SOURCE_HASH = (
    "9eb24246c9d4e7e801b7b0013285626b2cc843d3a197f691e7651c3418f0151c"
)

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def factor(coefficients):
    quotient = []
    previous = 0
    for value in coefficients:
        current = value - previous
        need(current >= 0, "Negative coefficient in positive quotient")
        quotient.append(current)
        previous = current
    need(previous == 0, "Polynomial is not divisible by 1+s")
    return quotient[:-1]

def main():
    root = Path(__file__).resolve().parent
    receipt_raw = (INPUT / "receipt.json").read_bytes()
    need(sha(receipt_raw) == RECEIPT_HASH, "Input receipt hash mismatch")
    original = json.loads(receipt_raw)

    need(original["status"] == "PASS", "Input audit did not pass")
    need(original["source_sha256"] == SOURCE_HASH, "Input source binding")
    need(sha((INPUT / "audit.py").read_bytes()) == SOURCE_HASH,
         "Input source changed")

    for name, metadata in original["artifacts"].items():
        data = (INPUT / name).read_bytes()
        need(sha(data) == metadata["sha256"], "Input artifact changed: " + name)
        need(len(data) == metadata["bytes"], "Input artifact size: " + name)

    raw = (INPUT / "joint_coefficients.csv").read_bytes()
    rows = list(csv.DictReader(io.StringIO(raw.decode())))
    need(len(rows) == 582, "Unexpected joint coefficient row count")

    joint = defaultdict(Counter)
    seen = set()

    for row in rows:
        n, m, k, q, count = (
            int(row[name]) for name in ("n", "m", "K", "Q", "count")
        )
        key = (n, m, k, q)
        need(key not in seen, "Duplicate coefficient")
        seen.add(key)
        beta = n-k-m+q
        need(beta == int(row["beta1"]), "Incidence index mismatch")
        need(q == int(row["beta0"]), "Component index mismatch")
        need(beta >= 0 and count > 0, "Invalid coefficient")
        joint[n, m][k, q] += count

    need(
        set(joint) == {
            (n, m) for n in range(1, 11) for m in range(1, n+1)
        },
        "Input parameter domain differs"
    )

    quotient_rows = []
    statistics = []
    off_diagonal = fixed_q_checks = strict_checks = 0

    for (n, m), poly in sorted(joint.items()):
        beta_counts = Counter()
        by_q = defaultdict(Counter)

        for (k, q), count in poly.items():
            beta = n-k-m+q
            beta_counts[beta] += count
            by_q[q][beta] += count

        mass = sum(beta_counts.values())
        mean = F(sum(b*v for b, v in beta_counts.items()), mass)
        variance = (
            F(sum(b*b*v for b, v in beta_counts.items()), mass)
            - mean*mean
        )
        d = n-m

        if d == 0:
            need(beta_counts == {0: mass}, "Diagonal support")
            need(variance == 0, "Diagonal variance")
            continue

        off_diagonal += 1
        coefficients = [beta_counts[b] for b in range(d+1)]
        quotient = factor(coefficients)
        need(2*sum(quotient) == mass, "Orbit-count normalization")
        need(sum((-1)**b*v for b, v in beta_counts.items()) == 0,
             "Parity imbalance")

        quotient_rows.append(dict(
            n=n, m=m, Q="ALL",
            coefficients=json.dumps(coefficients),
            quotient=json.dumps(quotient)
        ))

        for q, counts in sorted(by_q.items()):
            coefficients_q = [counts[b] for b in range(d+1)]
            quotient_q = factor(coefficients_q)
            need(
                sum((-1)**b*v for b, v in counts.items()) == 0,
                "Fixed-Q parity imbalance"
            )
            fixed_q_checks += 1
            quotient_rows.append(dict(
                n=n, m=m, Q=q,
                coefficients=json.dumps(coefficients_q),
                quotient=json.dumps(quotient_q)
            ))

        need(variance >= F(1, 4), "Variance floor")
        if d == 1:
            need(variance == F(1, 4), "Deficit-one variance")
        else:
            need(variance > F(1, 4), "Strict variance inequality")
            strict_checks += 1

        statistics.append(dict(
            n=n, m=m, deficit=d, pairs=mass,
            mean_beta1=str(mean),
            variance_beta1=str(variance),
            involution_orbits=mass//2,
            status="PASS"
        ))

    negative_controls = 0
    for invalid in ([1, 2], [2, 1, 1]):
        try:
            factor(invalid)
        except RuntimeError:
            negative_controls += 1
        else:
            raise RuntimeError("Invalid factorization was accepted")

    need(
        off_diagonal == 45
        and fixed_q_checks == 137
        and strict_checks == 36
        and negative_controls == 2,
        "Acceptance counts differ"
    )

    artifacts = {}
    for name, records in (
        ("factorizations.csv", quotient_rows),
        ("statistics.csv", statistics),
    ):
        with (root / name).open("x", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(records[0]))
            writer.writeheader()
            writer.writerows(records)
        data = (root / name).read_bytes()
        artifacts[name] = {
            "rows": len(records),
            "bytes": len(data),
            "sha256": sha(data)
        }

    report = {
        "status": "PASS",
        "python": platform.python_version(),
        "executable": sys.executable,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": sha(Path(__file__).read_bytes()),
        "input_receipt_sha256": RECEIPT_HASH,
        "input_coefficient_sha256": sha(raw),
        "off_diagonal_factorizations": off_diagonal,
        "fixed_Q_factorizations": fixed_q_checks,
        "strict_variance_checks_deficit_ge_2": strict_checks,
        "negative_controls_detected": negative_controls,
        "artifacts": artifacts,
        "scope": (
            "Finite verification of positive 1+s factorization and "
            "incidence-variance classification against preserved joint data"
        ),
        "direct_involution_enumeration_performed_here": False,
        "joint_audit_rerun": False,
        "global_ratio_classification": "OPEN",
        "git_operations": 0
    }

    output = root / "receipt.json"
    with output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)

    print("STATUS=PASS")
    print("INPUT_RECEIPT_AND_ARTIFACTS=PASS")
    print("OFF_DIAGONAL_FACTORIZATIONS=" + str(off_diagonal))
    print("FIXED_Q_FACTORIZATIONS=" + str(fixed_q_checks))
    print("STRICT_VARIANCE_CHECKS=" + str(strict_checks))
    print("NEGATIVE_CONTROLS_DETECTED=" + str(negative_controls))
    print("SOURCE_SHA256=" + report["source_sha256"])
    print("RECEIPT_SHA256=" + sha(output.read_bytes()))
    print("EVIDENCE_DIRECTORY=" + str(root))
    print("NO_JOINT_RERUN_NO_GIT_OPERATIONS")
    print("GLOBAL_CLASSIFICATION=OPEN")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        failure = {
            "status": "FAIL",
            "source_sha256": sha(Path(__file__).read_bytes()),
            "traceback": traceback.format_exc()
        }
        with (
            Path(__file__).resolve().parent / "failure.json"
        ).open("x", encoding="utf-8") as stream:
            json.dump(failure, stream, indent=2)
        raise
