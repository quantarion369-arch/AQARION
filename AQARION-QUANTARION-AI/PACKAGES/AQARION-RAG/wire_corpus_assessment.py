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
    query = " ".join(sys.argv[1:]).strip() or "quadratic map c unstable"
    result = extract_run(query, top_k=5)
    candidates = result["candidates"]
    witnesses = [to_assess_witness(c) for c in candidates]
    assessments = {}
    for reading in READINGS:
        claim = make_claim("universal " + reading + " stability", lambda w: True, READINGS[reading])
        verdict, decisive = assess(claim, witnesses)
        assessments[reading] = {
            "verdict": verdict,
            "decisive_candidate_ids": decisive,
        }
    output = {
        "search_completed": result["search_completed"],
        "candidate_count": len(candidates),
        "assessments": assessments,
        "candidates": candidates,
        "limitations": [
            "Assessment recomputes the conclusion from c; reported labels are not trusted.",
            "Extraction remains syntactic; semantic binding is a known limitation.",
            "A REFUTED verdict depends only on recomputed counterexamples, not corpus labels.",
        ],
    }
    print(json.dumps(output, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
