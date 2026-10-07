import argparse
import json


def reference(x):
    return x * x + x


def subtract_mutation(x):
    return x * x - x


def offset_mutation(x):
    return x * x + x + 1


def check_contract(candidate, contract, domain):
    if contract not in {"equality", "parity"}:
        raise ValueError("Unknown contract: " + repr(contract))

    checked = 0
    for x in domain:
        expected = reference(x)
        actual = candidate(x)
        checked += 1

        if contract == "equality":
            accepted = actual == expected
        elif contract == "parity":
            accepted = actual % 2 == expected % 2

        if not accepted:
            return {
                "accepted_on_tested_domain": False,
                "evidence_status": "counterexample_found",
                "inputs_checked": checked,
                "first_counterexample": {
                    "input": x,
                    "reference_output": expected,
                    "candidate_output": actual,
                    "reference_parity": expected % 2,
                    "candidate_parity": actual % 2,
                },
            }

    if checked == 0:
        return {
            "accepted_on_tested_domain": None,
            "evidence_status": "no_evidence",
            "inputs_checked": 0,
            "first_counterexample": None,
        }

    return {
        "accepted_on_tested_domain": True,
        "evidence_status": "accepted_on_tested_domain",
        "inputs_checked": checked,
        "first_counterexample": None,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Compare output equality with parity preservation."
    )
    parser.add_argument("--radius", type=int, default=20)
    args = parser.parse_args()
    if args.radius < 1:
        parser.error("--radius must be at least 1")

    domain = range(-args.radius, args.radius + 1)
    fixtures = [
        ("reference", reference, "equality", True),
        ("reference", reference, "parity", True),
        ("subtract_mutation", subtract_mutation, "equality", False),
        ("subtract_mutation", subtract_mutation, "parity", True),
        ("offset_mutation", offset_mutation, "equality", False),
        ("offset_mutation", offset_mutation, "parity", False),
    ]

    results = []
    for name, candidate, contract, expected_acceptance in fixtures:
        result = check_contract(candidate, contract, domain)
        result.update({
            "candidate": name,
            "contract": contract,
            "expected_acceptance": expected_acceptance,
            "expectation_matched": (
                result["accepted_on_tested_domain"]
                == expected_acceptance
            ),
        })
        results.append(result)

    expectations_met = all(
        result["expectation_matched"] for result in results
    )
    report = {
        "kind": "contract_collision_experiment",
        "domain": {
            "minimum": -args.radius,
            "maximum": args.radius,
            "size": len(domain),
        },
        "reference_expression": "x*x + x",
        "candidate_expressions": {
            "reference": "x*x + x",
            "subtract_mutation": "x*x - x",
            "offset_mutation": "x*x + x + 1",
        },
        "results": results,
        "all_fixture_expectations_met": expectations_met,
        "scope": (
            "Finite-domain experiment. Acceptance is not a universal "
            "proof. Equality and parity are separate contracts."
        ),
        "exit_interpretation": (
            "0 means fixture expectations matched; "
            "2 means a fixture expectation failed."
        ),
    }
    print(json.dumps(report, indent=2))
    return 0 if expectations_met else 2


if __name__ == "__main__":
    raise SystemExit(main())
