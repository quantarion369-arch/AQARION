# Supplementary verification for the Project 2 proof draft

This directory preserves newer local evidence beside, not inside, the earlier review commit.

* m2-direct-homology-QQ: Macaulay2 1.24.11 computed positive homology of the supplied complex over QQ.
* second-impl-components: a differently implemented, column-oriented replay of the nine integral component certificates.
* second-impl-divisor: a differently implemented replay of the 835-degree divisor-complex certificates.
* lean-arithmetic-kernel: 20 arithmetic lemmas compiled under Lean v4.35.0-rc4 without Mathlib.
* lean-generated-submonoid: an inductive-closure theorem Gen <-> Feasible compiled under the same pinned compiler.

Scope limits: the Macaulay2 run is over QQ only. The Lean files formalize the integer
semigroup-generation lemma only, not the real-cone, canonical-module, divisor-homology
or resolution theorems. No external peer review, novelty claim or all-field Lean proof
is made. The earlier theorem status remains DRAFT_REQUIRING_REVIEW.
