# SM003 / BRT Refactor — Delta Summary

**Pinned base commit:** `20e7447b93ae356fb8c3a937cce56573909b0a84`
**Prepared:** 2026-10-09
**Disposition:** `PATCH_PREPARED / NOT_YET_APPLIED`

## Files changed

| File | Nature of change | Semantic effect |
|---|---|---|
| `SM/SM003/manifest.json` | Rewrite | Version 2.0 → 2.1; commit placeholder removed; `domain_verified` splits historical vs new scope; explicit mutant IDs added; witness suite added |
| `SM/SM003/README.md` | Rewrite | Stale workflow claim removed; exact-vs-float contradiction resolved; new scope table added |
| `SM/SM003/mutations.py` | Rewrite | NumPy `matrix_rank(tol=1e-9)` → `fractions.Fraction` Gauss-Jordan; six D-level matrix mutants added; graph mutants retained; `R:c-only-variant` marked `INVALID_MUTANT`; outcome vocabulary `DETECTED`/`NOT_DETECTED`/`NOT_RUN`/`INVALID_MUTANT` |
| `SM/SM003/test_sm003.py` | New | Partition counts; rank identity edge cases; alternative outcomes present; label permutation invariance; census completion check |
| `BRT/brt_mutation.py` | Rewrite | Obsolete "killed/survived" vocabulary → `DETECTED`/`NOT_DETECTED`; input validation added; exit code 1 on failure |
| `BRT/test_brt_validation.py` | New | Semantic controls; isolated vertices; noninjective map; label invariance; invalid-input rejection; case corpus; state-graph alternative detection on two witnesses |

## Files unchanged

| File | Reason |
|---|---|
| `BRT/brt_validation.py` | Already uses exact `Fraction`; correct as-is |
| `BRT/brt_cases.json` | Corpus is valid; unchanged |
| `BRT/README.md` | Only the mutation-terminology line is patched |
| `SM/SM003/rank.py` | Historical float-based reference — should be moved to `historical/` in a subsequent commit |
| `SM/SM003/frobenius.py` | Historical float-based reference — should be moved to `historical/` in a subsequent commit |

## Suggested commit split

Apply as four separate commits, in order:

1. **Patch A — manifest scope fix only.** `3,975 → 3,984`; remove placeholder. Smallest, cleanest.
2. **Patch B — `mutations.py` rewrite.** Exact arithmetic + six D-level mutants.
3. **Patch C — `README.md` + `manifest.json` reconciliation.** Remove stale workflow claim.
4. **Patch D — BRT terminology + tests.** `DETECTED`/`NOT_DETECTED`; regression tests.

## Non-goals

This patch does **not**:

- verify the repository's original `mutations.py` correctness;
- run GitHub Actions;
- close the SM003 claim;
- touch PB, D22, or the partition-koopman experiment;
- certify the BRT workflow;
- formalize anything in Lean;
- promote any evidence class.
