"""Full per-mutant detection sets over all (map, partition) cases n<=MAXN; reports set equality, not just counts."""
import hashlib, itertools, json, sys
import mutations as M
MAXN = int(sys.argv[1]) if len(sys.argv) > 1 else 4
names = (*M.D_MUTANTS, *M.R_MUTANTS)
S = {n: set() for n in names}; idx = 0
for n in range(1, MAXN + 1):
    for t in itertools.product(range(n), repeat=n):
        for b in M.parts(n):
            for m in M.case_values(t, b)["detected"]: S[m].add(idx)
            idx += 1
total = idx
groups = {}
for n in names: groups.setdefault(tuple(sorted(S[n])), []).append(n)
rep = {"scope": f"n=1..{MAXN}", "total_cases": total,
       "per_mutant": {n: {"detected_cases": len(S[n]),
                          "sha256_of_sorted_case_indices": hashlib.sha256(json.dumps(sorted(S[n])).encode()).hexdigest()} for n in names},
       "named_mutants_detected": sum(1 for n in names if S[n]), "named_valid_mutants": len(names),
       "distinct_detection_signatures": len(groups),
       "signature_groups": [{"members": g, "detected_cases": len(k)} for k, g in groups.items()],
       "degenerate_behaviour": {"D:KP(I-P)": "always-accepting zero-test (P(I-P)=0)", "R:first": "always predicts rank 0 (singleton groups)"},
       "case_indices": {n: sorted(S[n]) for n in names},
       "note": "Case index = enumeration order over n, map, partition. Reconstructed engine, not repo file."}
json.dump(rep, open("detection_signatures_n4.json", "w"), indent=1)
print(json.dumps({k: rep[k] for k in ("scope","total_cases","named_mutants_detected","named_valid_mutants","distinct_detection_signatures")}))
for g in rep["signature_groups"]: print(g)
