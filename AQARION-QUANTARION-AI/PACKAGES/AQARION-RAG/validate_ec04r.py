import json, sys

def validate_retrieval(observed_passages, oracle):
    failures = []
    retrieved_text = " ".join(p[3] for p in observed_passages)
    for required in oracle["required_content_fragments"]:
        if required not in retrieved_text:
            failures.append("REQUIRED_CONTENT_NOT_RETRIEVED: " + required[:50])
    top_titles = [p[1] for p in observed_passages[:oracle["must_rank_in_top_k"]]]
    if not any(oracle["decisive_title"] in t for t in top_titles):
        failures.append("DECISIVE_PASSAGE_NOT_IN_TOP_K")
    return failures

oracle = {
    "required_content_fragments": ["Q3", "c=0.5", "unstable"],
    "decisive_title": "Evidence ledger",
    "must_rank_in_top_k": 3
}

observed = json.load(open("real_retrieval_ec04.json"))
failures = validate_retrieval(observed, oracle)
print(json.dumps({"failures": failures, "pass": not failures}, indent=2))
sys.exit(0 if not failures else 1)
