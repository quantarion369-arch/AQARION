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

## Provenance correction and actual-source check (2026-10-14)

This entry supersedes the provenance wording in the earlier verification
thread; the original numerical results remain unchanged.

### Corrections
- "Three independent checks" overstated independence: some checks share
  implementations and oracle components.
- The original xcheck.py run tested a reconstructed implementation,
  not the production source.
- The unittest suite used the reconstructed implementation and shared
  components; it was not a third independent implementation.

### Actual production-source cross-check
- Execution: user ran the path-specific loader in the local Termux checkout.
- Source:
  AQARION-QUANTARION-AI/verification/defect-transport/closure_profile.py
- Source SHA-256:
  e97325fedd0ee6a5d9223003b857358ce5ba303c483603b36215eb233f115db1
- Method: explicitly load the source above, then run dt_check/xcheck.py
  against the independent prof.profile oracle.
- Domain: every map and set partition for 1 <= n <= 4.
- Result: 3,984 cases; zero profile/linear-cost mismatches;
  zero implementation self-check failures; reported runtime 9 seconds.
- Scope: finite-domain agreement for the identified production source.
  Not a general correctness proof, a replay of larger reported searches,
  or machine-checked theorem verification.

## Closure-cost proof and audit artifacts

See research/closure-cost/:
- THEOREM.md: general bound, equality criterion, binary characterization.
- AUDIT.md: evidence attribution, counts, witnesses, and limitations.
- check_actual_source.py: production-source replay harness.
- actual-source-n4.txt: captured local replay output.

Paper proof is not machine-checked; novelty is not established.
Claude's complete extended-search artifacts remain pending export.

## Closure-cost equality extension — local replay complete

**Status:** Local semantic replay complete on seeds 0 and 1; pushed in commit `1dfd095`.

The corrected all-k equality checker passed locally on both seeds. Both runs reproduced the reported counts exactly: 166,484 exhaustive n<=5 cases per seed, 43,488 attained per seed, matching random, construction, and empty-profile results, with all assertions passing.

**Dependency qualification:** local `prof.py` is a compatible reconstruction, not the Claude-reported dependency (`829be3fc…`). This is a semantic replay, not a hash-verified byte-for-byte replay.

**Theorem status:** paper-level proof complete; exact exhaustive n<=5, sampled n in {8,9}, construction, and empty-profile checks passed locally. Not Lean-formalized and not independently formally reviewed.

**Artifacts:** `extensions/closure-cost-equality/replay/` and `extensions/closure-cost-equality/local-dependency/`.

## Stability-notions clarification — accepted

**Status:** Accepted as a framework correction and case verification.

1. `D=(I-P)KP=0` is forward stability, not commutation: it does not imply `[K,P]=0`.
2. Forward-stable partitions are closed under join and meet. The transitive-closure argument is valid; 18,737 random non-bijective n=6 checks provide independent randomized corroboration, not exhaustive proof.
3. Kaprekar’s many forward-stable partitions versus one pullback-stable partition is consistent with its non-invertibility. Pullback stability is a distinct, stronger condition.

**Label:** mathematical clarification plus independent randomized/case verification; not a new all-systems theorem.
