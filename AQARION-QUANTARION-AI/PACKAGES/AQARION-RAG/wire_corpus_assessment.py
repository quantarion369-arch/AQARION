#!/usr/bin/env python3
import json, sys
from extract_witness import run as extract_run
from assess import READINGS, make_claim, assess

def to_assess_witness(candidate):
    return {
        "id": candidate["id"],
        "family": candidate["family"],
        "c": candidate["c"],
        "label": candidate["reported_label"],
    }

def main():
    query = " ".join(sys.argv[1:]).strip() or "quadratic map c stable unstable"
    args = sys.argv[1:]
    top_k = 5
    if '--top-k' in args:
        top_k = int(args[args.index('--top-k') + 1])
        args = args[:args.index('--top-k')] + args[args.index('--top-k') + 2:]
    query = " ".join(args).strip() or "quadratic map c stable unstable"
    result = extract_run(query, top_k=top_k)
    candidates = result["candidates"]
    witnesses = [to_assess_witness(c) for c in candidates]

    claims = {
        "universal_bounded_orbit": make_claim(
            "universal bounded-orbit stability",
            lambda w: True,
            READINGS["bounded_orbit"],
        ),
        "universal_attracting_fixed_point": make_claim(
            "universal attracting-fixed-point stability",
            lambda w: True,
            READINGS["attracting_fixed_point"],
        ),
        "scoped_bounded_orbit": make_claim(
            "bounded-orbit stability for -2 <= c <= 0.25",
            lambda w: -2 <= w["c"] <= 0.25,
            READINGS["bounded_orbit"],
        ),
        "scoped_attracting_fixed_point": make_claim(
            "attracting-fixed-point stability for -2 <= c <= 0.25",
            lambda w: -2 <= w["c"] <= 0.25,
            READINGS["attracting_fixed_point"],
        ),
    }

    assessments = {}
    for name, claim in claims.items():
        verdict, decisive = assess(claim, witnesses)
        assessments[name] = {
            "verdict": verdict,
            "decisive_candidate_ids": decisive,
        }

    output = {
        "search_completed": result["search_completed"],
        "candidate_count": len(candidates),
        "retrieved_count": result["retrieved_count"],
        "top_k": top_k,
        "assessments": assessments,
        "candidates": candidates,
        "limitations": [
            "Assessment recomputes the conclusion from c; reported labels are not trusted.",
            "Extraction remains syntactic; semantic binding is a known limitation.",
            "Finite witnesses cannot establish a universal or scoped universal claim.",
        ],
    }
    print(json.dumps(output, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
