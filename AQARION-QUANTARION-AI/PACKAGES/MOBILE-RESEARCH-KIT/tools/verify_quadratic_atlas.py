#!/usr/bin/env python3
"""Recompute saved quadratic-atlas evidence using only the standard library."""

import argparse
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def _verify(report):
    require(
        report["kind"] == "quadratic_contract_atlas",
        "unexpected report kind",
    )

    require(
        report["reference"] == "x*x + x",
        "unexpected reference contract",
    )
    require(
        report["candidate"] == "c*x*x + a*x + b",
        "unexpected candidate contract",
    )

    bound = report["coefficient_bound"]
    require(
        type(bound) is int and bound >= 0,
        "invalid coefficient bound",
    )

    moduli = report["moduli"]
    require(
        isinstance(moduli, list) and bool(moduli),
        "invalid moduli",
    )
    require(
        all(type(q) is int and q >= 2 for q in moduli),
        "invalid modulus",
    )
    require(
        len(set(moduli)) == len(moduli),
        "duplicate moduli",
    )

    groups = report["results"]
    require(
        [group["modulus"] for group in groups] == moduli,
        "modulus groups mismatch",
    )

    expected_triples = {
        (c, a, b)
        for c in range(-bound, bound + 1)
        for a in range(-bound, bound + 1)
        for b in range(-bound, bound + 1)
    }

    totals = {
        "cases": 0,
        "accepted": 0,
        "rejection_witnesses": 0,
        "equivalence_comparisons": 0,
    }
    summaries = []

    for group in groups:
        q = group["modulus"]
        rows = group["candidates"]
        triples = [(row["c"], row["a"], row["b"]) for row in rows]

        require(
            all(type(v) is int for triple in triples for v in triple),
            f"q={q}: noninteger coefficient",
        )
        require(
            len(triples) == len(expected_triples),
            f"q={q}: candidate count mismatch",
        )
        require(
            set(triples) == expected_triples,
            f"q={q}: missing or duplicate candidates",
        )

        accepted_count = 0
        false_rejections = 0
        false_acceptances = 0

        for row in rows:
            c, a, b = row["c"], row["a"], row["b"]
            label = f"q={q}, coefficients=({c},{a},{b})"

            comparisons = []
            for x in range(q):
                reference = x*x + x
                candidate = c*x*x + a*x + b
                comparisons.append({
                    "input": x,
                    "reference_output": reference,
                    "candidate_output": candidate,
                    "reference_residue": reference % q,
                    "candidate_residue": candidate % q,
                })

            failures = [
                item for item in comparisons
                if item["reference_residue"] != item["candidate_residue"]
            ]
            accepted = not failures
            exact = (
                b % q == 0
                and (c + a - 2) % q == 0
                and (2 * (c - 1)) % q == 0
            )
            strict = (
                c % q == 1 % q
                and a % q == 1 % q
                and b % q == 0
            )
            three_point = all(
                (c*x*x + a*x + b) % q == (x*x + x) % q
                for x in (0, 1, 2)
            )
            false_rejection = accepted and not strict
            false_acceptance = strict and not accepted

            require(
                accepted == exact == three_point,
                f"{label}: recomputed primary disagreement",
            )

            expected_flags = {
                "complete_acceptance": accepted,
                "exact_acceptance": exact,
                "three_point_acceptance": three_point,
                "strict_acceptance": strict,
                "primary_routes_agree": True,
                "strict_false_rejection": false_rejection,
                "strict_false_acceptance": false_acceptance,
            }
            for field, expected in expected_flags.items():
                require(
                    row[field] is expected,
                    f"{label}: {field} mismatch",
                )

            witness = failures[0] if failures else None
            require(
                row["first_counterexample"] == witness,
                f"{label}: counterexample mismatch",
            )
            require(
                row["witness_replayed"] is (True if failures else None),
                f"{label}: witness replay status mismatch",
            )

            certificate = comparisons if false_rejection else None
            require(
                row["equivalence_certificate"] == certificate,
                f"{label}: equivalence comparison mismatch",
            )

            accepted_count += int(accepted)
            false_rejections += int(false_rejection)
            false_acceptances += int(false_acceptance)
            totals["cases"] += 1
            totals["accepted"] += int(accepted)
            totals["rejection_witnesses"] += int(bool(failures))
            totals["equivalence_comparisons"] += int(false_rejection)

        summaries.append({
            "modulus": q,
            "candidates": len(rows),
            "accepted": accepted_count,
            "primary_disagreements": 0,
            "strict_false_rejections": false_rejections,
            "strict_false_acceptances": false_acceptances,
            "failed_witness_replays": 0,
        })

    require(report["summaries"] == summaries, "summary mismatch")
    return totals


def verify(report):
    try:
        return _verify(report)
    except (KeyError, TypeError, IndexError) as error:
        raise ValueError(f"malformed report: {error}") from error


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()

    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
        totals = verify(report)
    except (OSError, ValueError, RecursionError) as error:
        parser.exit(
            1,
            "VERIFICATION_FAILED: " + str(error) + chr(10),
        )

    names = {
        "cases": "CASES_RECOMPUTED",
        "accepted": "ACCEPTED_CASES",
        "rejection_witnesses": "REJECTION_WITNESSES_REPLAYED",
        "equivalence_comparisons": "EQUIVALENCE_COMPARISONS_REPLAYED",
    }
    for key, name in names.items():
        print(f"{name}={totals[key]}")
    print("SAVED_QUADRATIC_EVIDENCE_REPLAY_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
