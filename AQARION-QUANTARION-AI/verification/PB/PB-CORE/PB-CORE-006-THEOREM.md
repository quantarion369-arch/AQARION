# AQ-PB-CORE-006 — Aggregate Enumeration of Pullback-Fixed Equivalences

**Artifact ID:** AQ-PB-CORE-006  
**Date:** 2026-10-09  
**Status:** `P-CANDIDATE` — repository proof artifact, independent review, and Lean formalization remain open  
**Computational status:** `V-REPORTED` — repository-recorded exhaustive checks  
**Lean:** `OPEN`  
**C4:** `BLOCKED`  
**Publication:** `BLOCKED`  
**Promotion:** `FALSE`

---

## 1. Statement

Let (X) be a finite set with (|X|=n), and let

[
mathcal T_n={T:X\to X}
]

be the set of all labelled endofunctions on (X). There are (n^n) such maps.

For (Tinmathcal T_n), define

[
operatorname{Stab}(T)
=
{Einoperatorname{Eq}(X):T^*E=E},
]

the set of equivalence relations on (X) preserved by the pullback action of (T).

Define the aggregate

[
A_n
=
sum_{Tinmathcal T_n}
|operatorname{Stab}(T)|.
]

Let (p(k)) denote the number of integer partitions of (k).

The candidate closed formula is

[
\boxed{
A_n
=
sum_{k=1}^{n}
\binom{n}{k}
k!,p(k),k,n^{n-k-1}
}
]

with the endpoint (k=n) interpreted as

[
\boxed{
n!,p(n).
}
]

Equivalently,

[
\boxed{
A_n
=
n!
sum_{k=1}^{n}
\frac{k,p(k),n^{n-k-1}}{(n-k)!}.
}
]

All intermediate factorial ratios must be evaluated using exact integer arithmetic.

---

## 2. Dependency correction

This aggregate theorem does **not** require the PB-CORE-005 phase-orbit classification.

Its proof requires only:

1. Periodic-core reduction.
2. Enumeration of permutation/equivalence pairs on the periodic core.
3. Enumeration of rooted forests feeding the core.

The dependency graph is therefore:

[
\boxed{
\text{PB-001}

ightarrow
\text{PB-004}

ightarrow
\text{PB-006 aggregate enumeration}.
}
]

PB-CORE-005 is a separate structural refinement:

[
\boxed{
\text{PB-004}

ightarrow
\text{PB-005 phase classification}.
}
]

The phase theorem is not a prerequisite for the aggregate theorem.

---

## 3. Periodic-core reduction

Let

[
P=operatorname{Per}(T)
]

be the periodic core of (T), and let (|P|=k).

By PB-CORE-004,

[
\boxed{
operatorname{Stab}(T)
cong
operatorname{Con}(P,T|_P).
}
]

Since (T|_P) is a permutation of (P),

[
|operatorname{Stab}(T)|
=
|operatorname{Con}(P,T|_P)|.
]

Thus the contribution of (T) depends only on:

1. The size (k) of its periodic core.
2. The permutation (T|_P) on that core.
3. The rooted-forest structure of the transient vertices feeding the core.

---

## 4. Permutation/equivalence aggregate

Define

[
S_k
=
sum_{sigmain S_k}
|operatorname{Con}([k],sigma)|.
]

Equivalently, (S_k) counts pairs

[
(sigma,E)
]

where (sigmain S_k), (E) is an equivalence relation on ([k]), and (sigma(E)=E).

---

## 5. Fix an equivalence relation

Let (E) have block-size profile

[
1^{m_1}2^{m_2}cdots,
]

so that

[
sum_{sge1}s,m_s=k.
]

The number of set partitions of ([k]) with this profile is

[
\boxed{
\frac{k!}{prod_{sge1}(s!)^{m_s}m_s!}.
}
]

---

## 6. Count preserving permutations

A permutation preserves (E) exactly when it permutes blocks of equal size among themselves and permutes points independently within each block.

For blocks of size (s):

- The (m_s) blocks may be permuted in (m_s!) ways.
- Each block contributes (s!) internal permutations.

Therefore the number of permutations preserving (E) is

[
\boxed{
prod_{sge1}(s!)^{m_s}m_s!.
}
]

---

## 7. Derive (S_k)

For every fixed block-size profile,

[
\frac{k!}{prod_s(s!)^{m_s}m_s!}
cdot
prod_s(s!)^{m_s}m_s!
=
k!.
]

Hence every integer partition of (k) contributes exactly (k!) permutation/equivalence pairs.

Since there are (p(k)) integer partitions of (k),

[
\boxed{
S_k=k!,p(k).
}
]

This identity is independent of the finer cycle-phase classification of PB-CORE-005.

---

## 8. Count transient attachments

Fix a particular (k)-element periodic core (Psubset[n]).

The remaining (n-k) vertices are transient. Their functional graph is a directed rooted forest whose roots are the (k) prescribed periodic vertices.

For (k<n), the number of labelled rooted forests on ([n]) with prescribed root set (P) is

[
\boxed{
k,n^{n-k-1}.
}
]

For (k=n), there are no transient vertices, and the count is

[
\boxed{1.}
]

This is the classical fixed-root forest enumeration. No novelty claim is made for it.

---

## 9. Contribution by core size

There are

[
\binom{n}{k}
]

choices for the periodic vertex set.

For each such core:

- There are (k,n^{n-k-1}) transient rooted forests when (k<n), and (1) when (k=n).
- The permutation/equivalence aggregate on the core contributes (k!,p(k)).

Therefore the total contribution from maps whose periodic core has size (k) is

[
\boxed{
\binom{n}{k}
k!,p(k),k,n^{n-k-1}.
}
]

---

## 10. Aggregate formula

Summing over (1le kle n),

[
\boxed{
A_n
=
sum_{k=1}^{n}
\binom{n}{k}
k!,p(k),k,n^{n-k-1}.
}
]

Using

[
\binom{n}{k}k!
=
\frac{n!}{(n-k)!},
]

this becomes

[
\boxed{
A_n
=
n!
sum_{k=1}^{n}
\frac{k,p(k),n^{n-k-1}}{(n-k)!}.
}
]

---

## 11. Generating-function form

Let

[
P(z)=sum_{kge1}p(k)z^k
]

and let (T(z)) be the rooted-tree generating function satisfying

[
T(z)=ze^{T(z)}.
]

Then the corrected exponential generating function is

[
\boxed{
sum_{nge1}\frac{A_n}{n!}z^n
=
P(T(z)).
}
]

The coefficient extraction gives

[
[z^n]P(T(z))
=
sum_{k=1}^{n}
p(k)
\frac{k,n^{n-k-1}}{(n-k)!},
]

with the (k=n) endpoint contributing (p(n)). Multiplying by (n!) recovers the aggregate formula.

**Correction record:** an earlier draft used (P(T(z))-1). That form is incorrect. The correct right-hand side is (P(T(z))).

---

## 12. Small values

The first values are:

[
\begin{aligned}
A_1&=1,\\
A_2&=6,\\
A_3&=51,\\
A_4&=592,\\
A_5&=8{,}565,\\
A_6&=148{,}896,\\
A_7&=3{,}018{,}127,\\
A_8&=69{,}844{,}608,\\
A_9&=1{,}816{,}084{,}233,\\
A_{10}&=52{,}399{,}129{,}600,\\
A_{11}&=1{,}660{,}832{,}066{,}091,\\
A_{12}&=57{,}351{,}480{,}413{,}184.
end{aligned}
]

These are repository-reported reference values. Their inclusion here does not certify them; the arithmetic verifier must independently recompute them, and a direct finite-map census must independently corroborate them.

For example, at (n=6), there are

[
6^6=46{,}656
]

labelled maps, and the reported aggregate stable-equivalence count is

[
\boxed{148{,}896.}
]

---

## 13. Independent permutation check

The core identity

[
S_k=k!,p(k)
]

can be checked independently by enumerating permutations and their invariant equivalence relations.

For (kle6), this checks

[
1+2+6+24+120+720=873
]

permutations cumulatively.

The repository-recorded permutation verifier reports zero mismatches through (k=6). This is `V-REPORTED`, not a substitute for the analytic proof.

---

## 14. Relationship to PB-CORE-005

PB-CORE-005 proposes the finer formula

[
N(c_1,ldots,c_r)
=
sum_{piinPi([r])}
prod_{Binpi}
left(
sum_{dmid g_B}d^{|B|-1}

ight),
]

where

[
g_B=gcd(c_i:iin B).
]

That formula classifies individual permutation congruence structures by cycle lengths.

It is not needed for the aggregate identity

[
S_k=k!,p(k).
]

Therefore,

[
\boxed{
\text{PB-CORE-006 does not depend on completion of PB-CORE-005.}
}
]

---

## 15. Evidence status

| Component | Status |
|---|---|
| Periodic-core reduction | `P` — analytic derivation presented |
| Permutation-core pair count (S_k=k!p(k)) | `P` — analytic derivation presented |
| Fixed-root forest count | `P` — classical combinatorial result |
| Aggregate formula | `P-CANDIDATE` — pending independent review and repository-bound verification |
| Exhaustive map enumeration (nle7) | `V-REPORTED` |
| Permutation enumeration (kle6) | `V-REPORTED` |
| Lean formalization | `OPEN` |
| Independent external replay | `NOT ESTABLISHED HERE` |
| C4 | `BLOCKED` |
| Publication | `BLOCKED` |
| Promotion | `FALSE` |

---

## 16. Literature boundary

The ingredients used here are not claimed as novel.

Classical literature establishes substantial parts of the surrounding theory of unary and monounary algebras, invariant equivalence relations, and cyclic structures. Relevant work includes Berman’s results on congruence lattices of unary algebras, Ratanaprasert and Denecke’s study of invariant equivalence relations for finite unary operations, and Jakubíková-Studenovská and Janičková’s work on congruence lattices of connected monounary algebras.

The exact AQARION aggregate synthesis

[
A_n
=
sum_{k=1}^{n}
\binom{n}{k}
k!,p(k),k,n^{n-k-1}
]

was not located in the current literature search.

**Permitted statement:**

> No exact source for this aggregate formula was located in the current search pass.

**Prohibited statement:**

> This formula has never appeared before.

---

## 17. Formalization targets

The Lean development should prove the following independently.

### Permutation aggregate

```lean
theorem PB006_permutation_aggregate :
    ∑ σ : Equiv.Perm (Fin k),
      (InvariantEquiv σ).card
    =
    k! * Nat.PartitionNumber k := by
  sorry
```

The exact Lean encoding may differ, but the theorem must not depend on the PB-CORE-005 phase parameterization.

### Fixed-root forest factor

The second formal theorem should establish the fixed-root forest count:

[
k,n^{n-k-1}.
]

### Aggregate theorem

Only after both preceding results are formalized should the final aggregate theorem be assembled.

---

## 18. Certification boundary

This document does **not** claim:

- A Lean proof.
- An independently executed current-branch verifier run.
- C4 certification.
- Publication readiness.
- Promotion eligibility.

Current status:

[
\boxed{
\text{P-candidate}
quad
\text{V-reported}
quad
\text{Lean open}
quad
\text{C4 blocked}.
}
]

---

## 19. Research lanes

The research program should now be split into two independent theorem lanes.

### Lane A — Aggregate enumeration

[
\boxed{
\text{PB-004}

ightarrow
S_k=k!p(k)

ightarrow
\text{rooted forests}

ightarrow
A_n.
}
]

This is the shortest route to a closed aggregate theorem.

### Lane B — Structural cycle classification

[
\boxed{
\text{PB-004}

ightarrow
\text{cycle decomposition}

ightarrow
\text{phase torsors}

ightarrow
d^{k-1}

ightarrow
\text{weighted Bell formula}.
}
]

This is the deeper structural theorem.

Neither lane should be treated as formally complete until its own proof obligations close.
