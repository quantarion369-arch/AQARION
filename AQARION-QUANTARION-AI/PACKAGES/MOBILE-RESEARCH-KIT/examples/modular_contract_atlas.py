import argparse
import json
import sys
from pathlib import Path


def classify(a, b, q):
    if q < 2:
        raise ValueError("Modulus must be at least 2")
    return (a - 1) % q == 0 and b % q == 0


def observe(a, b, q, domain):
    if q < 2:
        raise ValueError("Modulus must be at least 2")

    seen = set()
    first_failure = None
    checked = 0

    for x in domain:
        reference = x * x + x
        candidate = x * x + a * x + b
        checked += 1
        seen.add(x % q)

        if candidate % q != reference % q and first_failure is None:
            first_failure = {
                "input": x,
                "reference_output": reference,
                "candidate_output": candidate,
                "reference_residue": reference % q,
                "candidate_residue": candidate % q,
            }

    return {
        "accepted_on_checked_domain": first_failure is None,
        "inputs_checked": checked,
        "residues_covered": len(seen),
        "complete_residue_coverage": len(seen) == q,
        "first_counterexample": first_failure,
    }


def negative_controls(q):
    fixtures = [
        ("ignores_constant", 1, 1, lambda a, b: (a - 1) % q == 0),
        ("ignores_slope", 0, 0, lambda a, b: b % q == 0),
        ("uses_or", 1, 1,
         lambda a, b: (a - 1) % q == 0 or b % q == 0),
    ]
    results = []
    for name, a, b, faulty in fixtures:
        observed = observe(a, b, q, range(q))
        actual = observed["accepted_on_checked_domain"]
        prediction = faulty(a, b)
        results.append({
            "faulty_classifier": name,
            "a": a,
            "b": b,
            "faulty_prediction": prediction,
            "observed_acceptance": actual,
            "detected": prediction != actual,
            "first_counterexample": observed["first_counterexample"],
        })
    return results


def build_report(moduli, bound, sample_radius):
    if bound < 0 or sample_radius < 0:
        raise ValueError("Bounds must be nonnegative")
    if not moduli or any(q < 2 for q in moduli):
        raise ValueError("Provide moduli of at least 2")

    moduli = sorted(set(moduli))
    rows = []
    summaries = []
    controls = []

    for q in moduli:
        accepted = 0
        disagreements = 0
        sample_false_acceptances = 0

        for a in range(-bound, bound + 1):
            for b in range(-bound, bound + 1):
                complete = observe(a, b, q, range(q))
                sampled = observe(
                    a, b, q,
                    range(-sample_radius, sample_radius + 1),
                )
                predicted = classify(a, b, q)
                actual = complete["accepted_on_checked_domain"]
                agreement = predicted == actual
                false_acceptance = (
                    sampled["accepted_on_checked_domain"] and not actual
                )

                accepted += int(actual)
                disagreements += int(not agreement)
                sample_false_acceptances += int(false_acceptance)

                rows.append({
                    "modulus": q,
                    "a": a,
                    "b": b,
                    "classifier_acceptance": predicted,
                    "complete_observation": complete,
                    "sample_observation": sampled,
                    "routes_agree": agreement,
                    "sample_false_acceptance": false_acceptance,
                })

        q_controls = negative_controls(q)
        controls.append({
            "modulus": q,
            "results": q_controls,
        })
        summaries.append({
            "modulus": q,
            "candidates": (2 * bound + 1) ** 2,
            "accepted": accepted,
            "rejected": (2 * bound + 1) ** 2 - accepted,
            "route_disagreements": disagreements,
            "sample_false_acceptances": sample_false_acceptances,
            "negative_controls_detected": sum(
                item["detected"] for item in q_controls
            ),
        })

    return {
        "kind": "modular_contract_atlas",
        "reference": "x*x + x",
        "candidate": "x*x + a*x + b",
        "coefficient_bound": bound,
        "sample_radius": sample_radius,
        "moduli": moduli,
        "summaries": summaries,
        "results": rows,
        "negative_controls": controls,
        "all_routes_agree": all(row["routes_agree"] for row in rows),
        "all_negative_controls_detected": all(
            item["detected"]
            for group in controls
            for item in group["results"]
        ),
        "scope": (
            "Complete-residue evaluation and coefficient classification "
            "are compared for the selected polynomial family. Sampled "
            "acceptance is reported separately. This is not formal "
            "certification or a general polynomial classifier."
        ),
    }


def render_table(report):
    lines = [
        "# Modular Contract Atlas",
        "",
        "| q | Candidates | Accept | Reject | Disagreements | Sample false accepts | Controls detected |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in report["summaries"]:
        lines.append(
            "| {modulus} | {candidates} | {accepted} | {rejected} | "
            "{route_disagreements} | {sample_false_acceptances} | "
            "{negative_controls_detected}/3 |".format(**row)
        )
    lines.extend(["", report["scope"]])
    return chr(10).join(lines) + chr(10)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--moduli", nargs="+", type=int, default=[2, 3, 4, 5, 6]
    )
    parser.add_argument("--bound", type=int, default=5)
    parser.add_argument("--sample-radius", type=int, default=0)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    if any(q < 2 for q in args.moduli):
        parser.error("Every modulus must be at least 2")
    if args.bound < 0 or args.sample_radius < 0:
        parser.error("Bounds must be nonnegative")

    report = build_report(
        args.moduli, args.bound, args.sample_radius
    )
    code = 0 if (
        report["all_routes_agree"]
        and report["all_negative_controls_detected"]
    ) else 1

    report["exit_code"] = code
    report["exit_interpretation"] = (
        "0: routes agree and negative controls detected; "
        "1: disagreement or missed control; "
        "2: invalid CLI input or output failure."
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
        print("ATLAS_ERROR=" + str(error), file=sys.stderr)
        return 2

    print(table, end="")
    print("ATLAS_DIRECTORY=" + str(args.output_dir.resolve()))
    print("ATLAS_EXIT=" + str(code))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
