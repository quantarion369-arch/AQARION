#!/usr/bin/env python3
"""Wire retrieve() to assess() for EC-04/EC-05.

Retrieval gate: decisive passage must appear in top-k.
Assessment: runs on fixture-defined structured witnesses.
Fail-closed: missing/broken witness data yields OPEN + reason.
"""
import json, sys
from retrieve import retrieve
from assess import assess, READINGS, make_claim, W

STABLE = READINGS["bounded_orbit"]

def retrieval_gate(passages, required_fragments, top_k=3):
    """Return (ok, failures). Decisive content must be in top-k."""
    failures = []
    top = passages[:top_k]
    top_text = " ".join(p[3] for p in top)
    for frag in required_fragments:
        if frag not in top_text:
            failures.append("NOT_IN_TOP_K: " + frag[:40])
    return (len(failures) == 0), failures

def run_fixture(name, query, claim, witnesses, expected,
                required_fragments, top_k=3):
    passages = retrieve(query, top_k=top_k)
    gate_ok, gate_failures = retrieval_gate(
        passages, required_fragments, top_k)
    verdict, decisive = assess(claim, witnesses)
    result = {
        "fixture": name,
        "retrieval_gate": "PASS" if gate_ok else "FAIL",
        "gate_failures": gate_failures,
        "retrieved_titles": [p[1] for p in passages[:top_k]],
        "top_score": passages[0][0] if passages else None,
        "logical_assessment": verdict,
        "decisive_record_ids": decisive,
        "expected": expected,
        "assessment_pass": verdict == expected,
    }
    result["overall"] = ("PASS" if gate_ok and
                         verdict == expected else "FAIL")
    return result

if __name__ == "__main__":
    univ = make_claim("EC-04 universal", lambda w: True, STABLE)
    lt1 = make_claim(
        "EC-05 scoped", lambda w: -2 <= w["c"] <= 0.25, STABLE)

    ec04 = run_fixture(
        "EC-04-WIRED",
        "oc(T) witness counterexample invalid rank-0 audit unrefuted",
        univ,
        [W("EC04:E-003", 0.5, "unstable")],
        "REFUTED",
        ["oc(T) witness rank check"])

    ec05 = run_fixture(
        "EC-05-WIRED",
        "oc(T) witness counterexample invalid rank-0 audit unrefuted",
        lt1,
        [W("EC05:E-003", 1.5, "unstable")],
        "OPEN",
        ["oc(T) witness rank check"])

    for r in (ec04, ec05):
        print(json.dumps(r, indent=2))
    ok = all(r["overall"] == "PASS" for r in (ec04, ec05))
    sys.exit(0 if ok else 1)
