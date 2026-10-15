import json, sys

oracle = {
    "required_content_fragments": [
        "oc(T) witness rank check",
        "counterexample",
        "invalid",
        "unrefuted"
    ],
    "decisive_title": "Evidence ledger",
    "must_rank_in_top_k": 3,
    "required_scope_fragment": "witness-level for oc(T)"
}

observed = json.load(open("real_retrieval_ec05_real.json"))
retrieved_text = " ".join(p[3] for p in observed)
failures = []

for frag in oracle["required_content_fragments"]:
    if frag not in retrieved_text:
        failures.append("MISSING: " + frag[:40])

top_titles = [p[1] for p in observed[:oracle["must_rank_in_top_k"]]]
if not any(oracle["decisive_title"] in t for t in top_titles):
    failures.append("DECISIVE_PASSAGE_NOT_IN_TOP_K")

if oracle["required_scope_fragment"] not in retrieved_text:
    failures.append("SCOPE_QUALIFIER_NOT_RETRIEVED")

print(json.dumps({
    "fixture": "EC-05-REAL-001",
    "layer": "RETRIEVAL_ONLY",
    "failures": failures,
    "pass": not failures,
    "top_score": observed[0][0] if observed else None
}, indent=2))
sys.exit(0 if not failures else 1)
