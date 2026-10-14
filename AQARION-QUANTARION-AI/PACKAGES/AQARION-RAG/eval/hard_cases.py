"""Near-miss eval cases for AQARION-RAG retrieval."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from retrieve import retrieve

MIN_SCORE = 2

HARD_CASES = [
    {"id": "lean-formalization-status",
     "query": "Lean formalization status closure cost",
     "expect_contains": "Not Lean-formalized"},
    {"id": "independence-qualifier",
     "query": "three independent checks independence",
     "expect_contains": "overstated independence"},
    {"id": "hard-abstain-unrelated-math",
     "query": "Riemann hypothesis zeta function zeros",
     "expect": "abstain"},
]

def run_hard():
    passed = 0
    failed = 0
    for case in HARD_CASES:
        results = retrieve(case["query"], top_k=3)
        hits = [r for r in results if r[0] >= MIN_SCORE]
        if case.get("expect") == "abstain":
            ok = not hits
            note = "abstained" if ok else "should have abstained"
        else:
            ok = any(case["expect_contains"].lower() in r[3].lower()
                     for r in hits)
            if ok:
                note = "found qualified passage"
            else:
                note = "missed qualified passage"
        tag = "PASS" if ok else "FAIL"
        print(tag + "  " + case["id"] + " (" + note + ")")
        if ok:
            passed += 1
        else:
            failed += 1
    print("")
    print(str(passed) + " passed, " + str(failed) + " failed of " + str(len(HARD_CASES)))
    return failed == 0

if __name__ == "__main__":
    sys.exit(0 if run_hard() else 1)
