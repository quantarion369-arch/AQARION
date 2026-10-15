#!/usr/bin/env python3
import hashlib, json, re, sys
from retrieve import retrieve

B = chr(92)
C = re.compile(B + "bc" + B + "s*=" + B + "s*(-?" + B + "d+(?:" + B + "." + B + "d+)?)"+ B + "b", re.I)
FAM = re.compile(B + "bquadratic" + B + "b", re.I)
LAB = re.compile(B + "b(stable|unstable)" + B + "b", re.I)

def extract_diagnostic(text):
    if not FAM.search(text):
        return None, "missing_family_marker"
    m = C.search(text)
    if not m:
        return None, "missing_parameter_c"
    labels = {x.lower() for x in LAB.findall(text)}
    if not labels:
        return None, "missing_stability_label"
    if len(labels) != 1:
        return None, "conflicting_stability_labels"
    return {
        "family": "quadratic",
        "c": float(m.group(1)),
        "reported_label": labels.pop(),
        "verification_status": "SYNTACTIC_CANDIDATE_ONLY",
    }, None

def extract(text):
    return extract_diagnostic(text)[0]

def run(query, top_k=3):
    candidates, skipped, retrieved = [], [], 0
    for score, doc, sha, passage in retrieve(query, top_k=top_k):
        retrieved += 1
        psha = hashlib.sha256(passage.encode("utf-8")).hexdigest()
        provenance = {
            "doc": doc,
            "commit_sha": sha,
            "retrieval_score": score,
            "passage_sha256": psha,
            "passage": passage,
        }
        candidate, reason = extract_diagnostic(passage)
        if candidate is None:
            skipped.append({**provenance, "skip_reason": reason})
            continue
        candidate["id"] = doc + ":" + psha[:12]
        candidate["provenance"] = provenance
        candidates.append(candidate)
    return {
        "search_completed": True,
        "status": "CANDIDATES_FOUND" if candidates else "NO_CANDIDATES",
        "query": query,
        "top_k": top_k,
        "retrieved_count": retrieved,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "skipped_count": len(skipped),
        "skipped": skipped,
        "limitations": [
            "Corpus is limited to the pinned manifest.",
            "Extraction is syntactic, not semantic verification.",
            "Reported labels are claims, not verified conclusions.",
            "Zero candidates does not establish or refute a claim.",
        ],
    }

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        assert extract_diagnostic("quadratic c = 0.5 unstable")[0]["c"] == 0.5
        assert extract_diagnostic("quadratic c = 0.2 stable unstable")[1] == "conflicting_stability_labels"
        assert extract_diagnostic("quadratic unstable")[1] == "missing_parameter_c"
        assert extract_diagnostic("c = 0.5 unstable")[1] == "missing_family_marker"
        assert extract_diagnostic("quadratic c = 0.5")[1] == "missing_stability_label"
        print("SELF_TEST=PASS")
        sys.exit(0)
    query = " ".join(sys.argv[1:]).strip()
    if not query:
        print("ERROR: provide a retrieval query", file=sys.stderr)
        sys.exit(2)
    try:
        result = run(query)
    except Exception as exc:
        print(json.dumps({"search_completed": False, "status": "ERROR", "error_type": type(exc).__name__, "error": str(exc)}, indent=2))
        sys.exit(1)
    print(json.dumps(result, indent=2))
