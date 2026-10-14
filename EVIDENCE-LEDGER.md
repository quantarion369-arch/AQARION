# AQARION Evidence Ledger

Status: PLACEHOLDER — navigation stub. Content pending.

## Purpose

This ledger will record claim-level evidence: exact statement, hypotheses,
declared domain, evidence type, execution records, artifact hashes,
independent reconstruction status, and disposition.

## Currently verified claims (repository-level)

| Claim | Evidence type | Test artifact |
|---|---|---|
| rank((I-P_j)KP_j) = dim W_{j+1} - dim W_j | [V] | test_closure_profile.py |
| c_lin <= c_part | [V] | test_partition_repair.py |
| Defect-rank profile does not determine c_part | [V] + hand verification | test_profile_separation.py |
| SM003 bounded census replay | [V], clean-checkout | SM003 replay receipt |

This stub is not itself a complete evidence record. Full per-claim entries
with hashes, receipts, and scope statements are pending.

## Verification thread — oc(T) witness, product bound, repo cross-check (2026-10-14)

**Status:** ALL VERIFIED — three independent checks, all clean.

### 1. oc(T) witness rank check
- Witness: T=(0,1,0), Π={{0,1},{2}}, n=3
- Method: exact rational computation of D=(I-P_Π)KP_Π, pure Python (no sympy)
- Result: D = zero matrix, rank 0 — defect vanishes on V_Π
- Conclusion: "counterexample" in independent_exhaustive_check.py is invalid;
  Claude's rank-0 audit confirmed. oc(T) unrefuted at this witness.

### 2. Product bound C ≤ s-k ≤ k(∏(1+δ_j)-1)
- Method: independent oracle (prof.py), exhaustive over all maps and
  restricted-growth partitions, n≤4
- Result: 3984 cases, 0 violations
- Tightness: bound attained at T=(0,0,1,1), Π={{0,2},{1,3}} (s-k = k(2-1) = 2)
- Negative control: off-by-one bound correctly rejected
- Cross-check: unittest file (test_profile_partition_bound.py) independently
  re-derives same result — 4 tests ok, 1 skipped (n=5 deep test, optional)

### 3. Repo-vs-oracle cross-check
- Method: xcheck.py comparing closure_profile_repo.closure_profile against
  independent prof.profile oracle, exhaustive n≤4
- Result: 3984 cases, 0 profile mismatches, 0 repo self-check failures
  (increment identity, monotonicity, telescoping sum all hold)
- Conclusion: repo implementation validated against independent oracle.

### Scope qualifier
All results are exhaustive for n≤4 (and witness-level for oc(T) at n=3).
Full oc(T) claim for all (T,Π) still requires the general argument or
broader census. n=5 deep test (162,500 cases) available via AQ_DEEP=1,
not yet run — non-blocking.

### Next (held)
- Claude/GPT defect-transport blocker fixes
- Product bound test integration into main repo test suite
- Split-signature invariant research
