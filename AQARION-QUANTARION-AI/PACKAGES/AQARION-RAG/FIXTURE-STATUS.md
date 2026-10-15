# Fixture Status — Single Source of Truth

## Baseline (Termux, observed 2026-10-14)
- Unit: 9/9 PASS (pytest: claims, graph, retrieve, supersedes)
- Eval: 3/3 PASS + bm25-ranks-relevant-first
- Env: Termux Android, Python 3.13

## Pilot fixtures
- EC-05-REAL-001 v0.1.0 refutation_handling: RETRIEVAL_VERIFIED (Termux)
  - Corpus: REAL evidence ledger @ b1642c3392bfee54d4d7854b3dc6d8b53f4f58b2
  - Query: "oc(T) witness counterexample invalid rank-0 audit unrefuted"
  - Result: PASS — decisive passage rank #1 (score 9), scope qualifier co-retrieved
  - Scope: RETRIEVAL_ONLY — assessment layer not yet built
  - Validator: validate_ec05_real.py (comparison-harness, real output)

- EC-04-001 v0.1.1: DRAFT — ORACLE BLOCKED_PENDING_VALIDATION
- EC-05-001 (synthetic) v0.1.0: DRAFT — LOGIC_CONTRACT_VALIDATED (simulated only)
- EC-07A, EC-07B, EC-08, EC-14, EC-17: NOT STARTED

## Lock criteria
[ ] witness validity independently validated with receipt
[ ] claim ID + version both checked
[ ] retrieval from actual returned IDs
[ ] fallback OPEN/NOT_ASSESSED, never SUPPORTED
[ ] mutations executed, raw logs saved
[ ] Termux real run + Claude sandbox agree, James adjudicates
