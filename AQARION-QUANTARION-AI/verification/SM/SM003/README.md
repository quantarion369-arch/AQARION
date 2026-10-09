
## SM003 — AQ-SM-003-MATRIX

**Formulas:**
- Rank: `rank(D) = k - c` where k=|partition|, c=components of image graph
- Energy: `||D||² = Σ m(|B|-m)/(|B||B'|)` (exact Fraction required, // fails 75%)

**Evidence:**
- n=3,4 quick: 3975 cases BAD=0
- n=3,4,5 full: 166475 cases BAD=0 exact, 125348 BAD with integer division
- n=6 f0=0: 1,578,528 cases
- Total: 1,745,003
- Ground truth: `matrix_rank((I-P)KP, tol=1e-9)` + `Fraction`

**Mutants — 11 distinct (12 raw IDs):**
- D-level 6: K^T, [K,P], (I-P)K, PKP, (I-P)K^T, KP(I-P)
- R-level 5 clusters: ignore+preimage (ONE cluster, kill set 1664 identical at n<=4), c, k-c-1, first, c-only-variant
- Note: `ignore isolated == preimage graph` at n<=4 exhaustive

**Witness Suite W-AQ001-MIN (2 instances, bounded [V] n<=4):**
- W1: f=(0,0,2) partition {0,2},{1} — kills 9
- W2: f=(0,0,1) partition {0,2},{1} — kills 3 additional
- Requires: non_injective_f=true, unreached_block=true, non_constant_f=true, non_singleton_block=true
- Covers: M-AQ001-v1 (11 mutants) at n<=4
- Caveat: Does NOT cover BRT incidence mutation

**Open Items:**
- All-n equivalence for ignore==preimage — KEEP OPEN (only n<=4 proven)
- BRT incidence mutation — must run verification/BRT/brt_mutation.py
- Lean formalization — separate from [V]

**Workflow:**
`.github/workflows/sm003-verify.yml` — green 21s

**Status:** Two findings ready for ledger as bounded computational results. Repository-suite coverage OPEN until BRT exercised.
