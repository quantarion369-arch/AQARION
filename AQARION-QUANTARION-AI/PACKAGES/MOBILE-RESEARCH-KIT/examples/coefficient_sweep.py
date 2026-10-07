import argparse
import json
import sys
from pathlib import Path


def evaluate(a, b, radius):
    first_equality_failure = None
    first_parity_failure = None
    checked = 0

    for x in range(-radius, radius + 1):
        expected = x * x + x
        actual = x * x + a * x + b
        checked += 1

        if actual != expected and first_equality_failure is None:
            first_equality_failure = {
                "input": x,
                "reference_output": expected,
                "candidate_output": actual,
            }

        if (
            actual % 2 != expected % 2
            and first_parity_failure is None
        ):
            first_parity_failure = {
                "input": x,
                "reference_output": expected,
                "candidate_output": actual,
                "reference_parity": expected % 2,
                "candidate_parity": actual % 2,
            }

    equality = first_equality_failure is None
    parity = first_parity_failure is None

    if equality and parity:
        classification = "both"
    elif equality:
        classification = "equality_only"
    elif parity:
        classification = "parity_only"
    else:
        classification = "neither"

    return {
        "a": a,
        "b": b,
        "inputs_checked": checked,
        "equality_accepted": equality,
        "parity_accepted": parity,
        "classification": classification,
        "first_equality_counterexample": first_equality_failure,
        "first_parity_counterexample": first_parity_failure,
    }


def build_report(radius, bound):
    rows = [
        evaluate(a, b, radius)
        for a in range(-bound, bound + 1)
        for b in range(-bound, bound + 1)
    ]
    counts = {
        category: sum(
            row["classification"] == category for row in rows
        )
        for category in (
            "both", "equality_only", "parity_only", "neither"
        )
    }
    return {
        "kind": "coefficient_contract_sweep",
        "reference_expression": "x*x + x",
        "candidate_expression": "x*x + a*x + b",
        "domain": {
            "minimum": -radius,
            "maximum": radius,
            "size": 2 * radius + 1,
        },
        "coefficient_bounds": {
            "minimum": -bound,
            "maximum": bound,
        },
        "candidate_count": len(rows),
        "classification_counts": counts,
        "results": rows,
        "scope": (
            "All selected candidates were evaluated on the stated "
            "finite domain. This report alone is not a universal proof."
        ),
    }


def render_table(report):
    lines = [
        "# Coefficient Contract Sweep",
        "",
        "Reference: x*x + x",
        "Candidate: x*x + a*x + b",
        "",
        "| a | b | Equality | Parity | Classification |",
        "|---:|---:|---|---|---|",
    ]
    for row in report["results"]:
        lines.append(
            "| {a} | {b} | {equality} | {parity} | {category} |".format(
                a=row["a"],
                b=row["b"],
                equality="pass" if row["equality_accepted"] else "fail",
                parity="pass" if row["parity_accepted"] else "fail",
                category=row["classification"],
            )
        )
    lines.extend(["", report["scope"]])
    return chr(10).join(lines) + chr(10)


def main():
    parser = argparse.ArgumentParser(
        description="Sweep polynomial candidates against two contracts."
    )
    parser.add_argument("--radius", type=int, default=20)
    parser.add_argument("--bound", type=int, default=2)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    if args.radius < 1:
        parser.error("--radius must be at least 1")
    if args.bound < 0:
        parser.error("--bound must be nonnegative")

    report = build_report(args.radius, args.bound)
    report_text = json.dumps(report, indent=2) + chr(10)
    table_text = render_table(report)

    try:
        args.output_dir.mkdir(parents=True, exist_ok=False)
        report_path = args.output_dir / "report.json"
        table_path = args.output_dir / "table.md"

        with report_path.open("x", encoding="utf-8") as handle:
            handle.write(report_text)
        with table_path.open("x", encoding="utf-8") as handle:
            handle.write(table_text)

    except OSError as error:
        print("SWEEP_ERROR=" + str(error), file=sys.stderr)
        return 2

    print(
        "CLASSIFICATION_COUNTS="
        + json.dumps(report["classification_counts"], sort_keys=True)
    )
    print("CANDIDATE_COUNT=" + str(report["candidate_count"]))
    print("REPORT_FILE=" + str(report_path.resolve()))
    print("TABLE_FILE=" + str(table_path.resolve()))
    print(table_text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
