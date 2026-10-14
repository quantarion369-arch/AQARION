"""Known-answer evaluation harness for AQARION-RAG retrieval."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from retrieve import retrieve

MIN_SCORE = 2
NL = chr(10)

CASES = [
    {"id": "ledger-status", "query": "evidence ledger status partial",
     "expect_sha_prefix": "b1642c3", "expect_passage_contains": "PARTIAL LEDGER"},
    {"id": "ledger-purpose", "query": "claim-level evidence artifact hashes disposition",
     "expect_sha_prefix": "b1642c3", "expect_passage_contains": "artifact hashes"},
    {"id": "abstain-unknown-topic", "query": "quantum chromodynamics lattice gauge theory",
     "expect_abstain": True},
]

def run_eval():
    passed = failed = 0
    for case in CASES:
        results = retrieve(case["query"], top_k=3)
        hits = [r for r in results if r[0] >= MIN_SCORE]
        if case.get("expect_abstain"):
            if not hits:
                print("PASS  " + case["id"] + " (abstained correctly)")
                passed += 1
            else:
                print("FAIL  " + case["id"] + " (expected abstention, got " + str(len(hits)) + " hits)")
                failed += 1
            continue
        if not hits:
            print("FAIL  " + case["id"] + " (no hits above threshold)")
            failed += 1
            continue
        top = hits[0]
        sha_ok = top[2].startswith(case["expect_sha_prefix"])
        passage_ok = case["expect_passage_contains"].lower() in top[3].lower()
        if sha_ok and passage_ok:
            print("PASS  " + case["id"] + " (sha + passage matched)")
            passed += 1
        else:
            print("FAIL  " + case["id"] + " (sha_ok=" + str(sha_ok) + ", passage_ok=" + str(passage_ok) + ")")
            failed += 1
    print(NL + str(passed) + " passed, " + str(failed) + " failed out of " + str(len(CASES)))
    return failed == 0

if __name__ == "__main__":
    sys.exit(0 if run_eval() else 1)
