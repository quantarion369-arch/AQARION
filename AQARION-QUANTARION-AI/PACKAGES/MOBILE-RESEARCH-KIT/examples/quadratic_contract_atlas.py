import argparse
import json
import sys
from pathlib import Path


def validate_modulus(q):
    if q < 2:
        raise ValueError("Modulus must be at least 2")


def exact_classifier(c, a, b, q):
    validate_modulus(q)
    return (
        b % q == 0
        and (c + a - 2) % q == 0
        and (2 * (c - 1)) % q == 0
    )


def strict_classifier(c, a, b, q):
    validate_modulus(q)
    return (
        (c - 1) % q == 0
        and (a - 1) % q == 0
        and b % q == 0
    )


def evaluate(c, a, b, q, domain):
    validate_modulus(q)
    comparisons = []
    first_failure = None

    for x in domain:
        reference = x * x + x
        candidate = c * x * x + a * x + b
        row = {
            "input": x,
            "reference_output": reference,
            "candidate_output": candidate,
            "reference_residue": reference % q,
            "candidate_residue": candidate % q,
        }
        comparisons.append(row)
        if (
            row["reference_residue"] != row["candidate_residue"]
            and first_failure is None
        ):
            first_failure = row.copy()

    return {
        "accepted": first_failure is None,
        "inputs_checked": len(comparisons),
        "first_counterexample": first_failure,
        "comparisons": comparisons,
    }


def replay_witness(c, a, b, q, witness):
    validate_modulus(q)
    if witness is None:
        return False

    x = witness["input"]
    reference = x * x + x
    candidate = c * x * x + a * x + b

    return (
        witness["reference_output"] == reference
        and witness["candidate_output"] == candidate
        and witness["reference_residue"] == reference % q
        and witness["candidate_residue"] == candidate % q
        and reference % q != candidate % q
    )


def analyze_candidate(c, a, b, q):
    complete = evaluate(c, a, b, q, range(q))
    three_point = evaluate(c, a, b, q, (0, 1, 2))
    exact = exact_classifier(c, a, b, q)
    strict = strict_classifier(c, a, b, q)
    accepted = complete["accepted"]
    witness = complete["first_counterexample"]

    return {
        "c": c,
        "a": a,
        "b": b,
        "complete_acceptance": accepted,
        "exact_acceptance": exact,
        "three_point_acceptance": three_point["accepted"],
        "strict_acceptance": strict,
        "primary_routes_agree": (
            accepted == exact == three_point["accepted"]
        ),
        "strict_false_rejection": accepted and not strict,
        "strict_false_acceptance": strict and not accepted,
        "first_counterexample": witness,
        "witness_replayed": (
            None if witness is None
            else replay_witness(c, a, b, q, witness)
        ),
        "equivalence_certificate": (
            complete["comparisons"] if accepted and not strict
            else None
        ),
    }


def build_report(moduli, bound):
    if bound < 0:
        raise ValueError("Coefficient bound must be nonnegative")
    if not moduli:
        raise ValueError("At least one modulus is required")
    for q in moduli:
        validate_modulus(q)

    moduli = sorted(set(moduli))
    summaries = []
    results = []
    values = range(-bound, bound + 1)

    for q in moduli:
        rows = [
            analyze_candidate(c, a, b, q)
            for c in values
            for a in values
            for b in values
        ]
        summaries.append({
            "modulus": q,
            "candidates": len(rows),
            "accepted": sum(row["complete_acceptance"] for row in rows),
            "primary_disagreements": sum(
                not row["primary_routes_agree"] for row in rows
            ),
            "strict_false_rejections": sum(
                row["strict_false_rejection"] for row in rows
            ),
            "strict_false_acceptances": sum(
                row["strict_false_acceptance"] for row in rows
            ),
            "failed_witness_replays": sum(
                row["witness_replayed"] is False for row in rows
            ),
        })
        results.append({"modulus": q, "candidates": rows})

    checks_passed = all(
        row["primary_disagreements"] == 0
        and row["strict_false_acceptances"] == 0
        and row["failed_witness_replays"] == 0
        for row in summaries
    )

    return {
        "kind": "quadratic_contract_atlas",
        "reference": "x*x + x",
        "candidate": "c*x*x + a*x + b",
        "coefficient_bound": bound,
        "moduli": moduli,
        "summaries": summaries,
        "results": results,
        "all_checks_passed": checks_passed,
        "scope": (
            "Complete residues, exact quadratic conditions, and three "
            "evaluation points are compared. Strict coefficient matching "
            "is an adversarial rule. False rejections by that rule are "
            "expected findings, not harness failures. This is not a "
            "general polynomial classifier or formal certification."
        ),
    }


def render_table(report):
    lines = [
        "# Quadratic Contract Atlas",
        "",
        "| q | Candidates | Accept | Primary disagreements | Strict false rejects | Strict false accepts | Failed replays |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in report["summaries"]:
        lines.append(
            "| {modulus} | {candidates} | {accepted} | "
            "{primary_disagreements} | {strict_false_rejections} | "
            "{strict_false_acceptances} | {failed_witness_replays} |"
            .format(**row)
        )
    lines.extend(["", report["scope"]])
    return chr(10).join(lines) + chr(10)


def main():
    parser = argparse.ArgumentParser(
        description="Compare polynomial coefficients with induced functions."
    )
    parser.add_argument(
        "--moduli", nargs="+", type=int, default=[2, 3, 4, 5, 6, 8]
    )
    parser.add_argument("--bound", type=int, default=3)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    if any(q < 2 for q in args.moduli):
        parser.error("Every modulus must be at least 2")
    if args.bound < 0:
        parser.error("--bound must be nonnegative")

    report = build_report(args.moduli, args.bound)
    code = 0 if report["all_checks_passed"] else 1
    report["exit_code"] = code
    report["exit_interpretation"] = (
        "0: primary routes agree and consistency checks pass; "
        "1: disagreement or consistency failure; "
        "2: invalid input or output failure."
    )
    table = render_table(report)

    try:
        args.output_dir.mkdir(parents=True, exist_ok=False)
        with (args.output_dir / "atlas.json").open(
            "x", encoding="utf-8"
        ) as handle:
            json.dump(report, handle, indent=2)
            handle.write(chr(10))
        with (args.output_dir / "atlas.md").open(
            "x", encoding="utf-8"
        ) as handle:
            handle.write(table)
    except OSError as error:
        print("QUADRATIC_ATLAS_ERROR=" + str(error), file=sys.stderr)
        return 2

    print(table, end="")
    print("ATLAS_DIRECTORY=" + str(args.output_dir.resolve()))
    print("QUADRATIC_ATLAS_EXIT=" + str(code))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
