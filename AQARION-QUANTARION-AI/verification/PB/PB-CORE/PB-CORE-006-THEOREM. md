AQ-PB-CORE-006 — AGGREGATE ENUMERATION OF PULLBACK-FIXED EQUIVALENCES

Artifact ID: AQ-PB-CORE-006
Status: "[P-CANDIDATE]" until repository proof artifact and formal verification are closed
Computational status: "[V]" repository-recorded exhaustive checks
Lean: "[O]" OPEN
C4: BLOCKED
Publication: BLOCKED
Promotion: FALSE

---

1. Statement

For a finite set X with

[
|X|=n,
]

let

[
\mathcal T_n

{T:X\to X}.
]

For each T, define

[
\operatorname{Stab}(T)

{E\in\operatorname{Eq}(X):T^*E=E}.
]

Define the aggregate

[
A_n

\sum_{T\in\mathcal T_n}
|\operatorname{Stab}(T)|.
]

Let p(k) denote the number of integer partitions of k.

The candidate closed formula is

[
\boxed{
A_n

\sum_{k=1}^{n}
\binom nk
k,n^{,n-k-1}
k!,p(k),
}
]

with the k=n term interpreted as

[
n!,p(n).
]

Equivalently,

[
\boxed{
A_n

n!
\sum_{k=1}^{n}
\frac{k,p(k),n^{,n-k-1}}
{(n-k)!}.
}
]

---

2. Critical dependency correction

This aggregate theorem does not require the PB-CORE-005 phase-orbit classification.

The proof requires only:

1. periodic-core reduction;
2. enumeration of permutation/equivalence pairs on the core;
3. enumeration of rooted forests feeding the core.

Thus the dependency graph is

[
\boxed{
\text{PB-001}
\rightarrow
\text{PB-004}
\rightarrow
\text{PB-006 aggregate enumeration}.
}
]

PB-CORE-005 is a separate structural refinement:

[
\text{PB-004}
\rightarrow
\text{PB-005 phase classification}.
]

The phase theorem is therefore not a prerequisite for the aggregate theorem.

---

3. Periodic-core reduction

Let

[
P=\operatorname{Per}(T).
]

By PB-CORE-004,

[
\boxed{
\operatorname{Stab}(T)
\cong
\operatorname{Con}(P,T|_P).
}
]

Let

[
|P|=k.
]

Then T|_P is a permutation of P.

Therefore

[
|\operatorname{Stab}(T)|

|\operatorname{Con}(P,T|_P)|.
]

Thus the contribution of T depends only on:

1. the size k of its periodic core;
2. the permutation on that core.

---

4. Counting permutation/equivalence pairs

Define

[
S_k

\sum_{\sigma\in S_k}
|\operatorname{Con}([k],\sigma)|.
]

We now derive S_k without using PB-CORE-005.

Instead of fixing \sigma, count pairs

[
(\sigma,E)
]

where

[
E\in\operatorname{Eq}([k])
]

and

[
\sigma(E)=E.
]

---

5. Fix an equivalence relation

Let E have block-size profile

[
1^{m_1}2^{m_2}\cdots.
]

Thus

[
\sum_s s,m_s=k.
]

The number of set partitions of [k] having this profile is

[
\boxed{
\frac{k!}
{\prod_s (s!)^{m_s}m_s!}.
}
]

---

6. Count permutations preserving that equivalence

A permutation preserves E exactly when it permutes the E-blocks among blocks of equal size and independently permutes the points inside every block.

For blocks of size s:

- the m_s blocks can be permuted in m_s! ways;
- each block contributes s! internal permutations.

Therefore the number of permutations preserving E is

[
\boxed{
\prod_s (s!)^{m_s}m_s!.
}
]

---

7. Multiply

For every fixed block-size profile,

[
\frac{k!}
{\prod_s (s!)^{m_s}m_s!}
\cdot
\prod_s(s!)^{m_s}m_s!

k!.
]

Therefore every integer partition of k contributes exactly k! pairs.

The number of integer partitions of k is p(k).

Hence

[
\boxed{
S_k=k!,p(k).
}
]

This is the required permutation-core aggregate.

---

8. Counting transient attachments

Fix a particular k-element periodic core P.

The remaining

[
n-k
]

vertices are transient.

Their functional graph consists of directed rooted trees whose roots are the k prescribed periodic vertices.

For k<n, the number of labeled rooted forests on [n] with prescribed root set P is

[
\boxed{
k,n^{,n-k-1}.
}
]

For k=n, there are no transient vertices and the number is

[
1.
]

This is the classical fixed-root forest enumeration.

No novelty claim is made for this enumeration.

---

9. Contribution of a fixed core size

There are

[
\binom nk
]

choices for the periodic vertex set.

For each such core:

[
k,n^{,n-k-1}
]

choices of transient rooted forest, for k<n.

The sum over all permutation/equivalence pairs on the core contributes

[
k!p(k).
]

Therefore the total contribution from maps whose periodic core has size k is

[
\boxed{
\binom nk
k,n^{,n-k-1}
k!p(k).
}
]

---

10. Summation

Summing over

[
1\le k\le n
]

gives

[
\boxed{
A_n

\sum_{k=1}^{n}
\binom nk
k,n^{,n-k-1}
k!p(k).
}
]

Using

[
\binom nk k!

\frac{n!}{(n-k)!},
]

we obtain

[
\boxed{
A_n

n!
\sum_{k=1}^{n}
\frac{k,p(k),n^{,n-k-1}}
{(n-k)!}.
}
]

This is the aggregate enumeration formula.

---

11. Small values

The first values are:

[
A_1=1,
]

[
A_2=6,
]

[
A_3=51,
]

[
A_4=592,
]

[
A_5=8565,
]

[
A_6=148896.
]

These agree with the repository-recorded exhaustive map enumeration.

The number of maps is

[
n^n.
]

For n=6,

[
6^6=46656.
]

The reported total stable-equivalence count is

[
\boxed{
148896.
}
]

---

12. Independent permutation aggregate

The core identity

[
S_k=k!p(k)
]

can itself be checked independently.

For k\le6,

[
\sum_{k=1}^{6} k!

1+2+6+24+120+720

873
]

permutations are checked cumulatively.

The repository-recorded permutation verifier reports zero mismatches through k=6.

This is "[V]", not a substitute for the analytic proof.

---

13. Relationship to PB-CORE-005

PB-CORE-005 proposes the finer formula

[
N(c_1,\ldots,c_r)

\sum_{\pi\in\Pi([r])}
\prod_{B\in\pi}
\left(
\sum_{d\mid g_B}
d^{|B|-1}
\right),
]

where

[
g_B=\gcd(c_i:i\in B).
]

That formula classifies individual permutation congruence structures by cycle lengths.

It is not needed for the aggregate identity

[
S_k=k!p(k).
]

Therefore:

[
\boxed{
\text{PB-CORE-006 does not depend on completion of PB-CORE-005.}
}
]

---

14. Why the aggregate identity is natural

There is a direct combinatorial explanation.

For each equivalence relation E, the permutations preserving E are exactly the automorphisms of the corresponding set partition.

For a block-size profile \lambda\vdash k,

[
#{\text{partitions of profile }\lambda}
\times
#{\text{permutations preserving one such partition}}

k!.
]

Since there are p(k) possible integer-partition profiles,

[
S_k=k!p(k).
]

The identity is therefore independent of the finer cycle-phase classification.

---

15. Evidence status

Component| Status
Periodic-core reduction| "[P]"
Permutation-core pair count S_k=k!p(k)| "[P]" analytic derivation
Fixed-root forest count| "[P]" classical combinatorial result
Aggregate formula| "[P-CANDIDATE]" until repository proof artifact is independently reviewed
Exhaustive map enumeration n\le7| "[V-REPORTED]"
Permutation enumeration| "[V-REPORTED]"
Lean formalization| "[O]"
Independent external replay| "NOT ESTABLISHED HERE"
C4| "BLOCKED"
Publication| "BLOCKED"
Promotion| "FALSE"

---

16. Literature boundary

The ingredients used here are not claimed as novel.

Classical literature establishes substantial parts of the surrounding theory of unary and monounary algebras, invariant equivalence relations, and cyclic structures.

In particular:

- Berman established foundational results on congruence lattices of unary algebras.
- Ratanaprasert and Denecke studied invariant equivalence relations for finite unary operations with long pre-periods.
- Jakubíková-Studenovská and Janičková studied congruence lattices of connected monounary algebras.

The exact AQARION aggregate synthesis

[
A_n

\sum_{k=1}^{n}
\binom nk
k,n^{,n-k-1}
k!p(k)
]

was not located in the current literature search.

That does not establish priority.

Permitted statement:

«No exact source for this aggregate formula was located in the current search pass.»

Prohibited statement:

«This formula has never appeared before.»

---

17. Formalization target

The Lean development should prove the following independently:

THEOREM PB006_PERMUTATION_AGGREGATE
  :
  ∑ σ : Equiv.Perm (Fin k),
      card (InvariantEquiv σ)
  =
  k! * Nat.PartitionNumber k

The exact Lean encoding may differ.

The theorem should not depend on the PB-CORE-005 phase parameterization.

The second formal theorem should then establish the fixed-root forest factor.

Only after both are formalized should the final aggregate theorem be assembled.

---

18. Certification boundary

This document does not claim a Lean proof.

This document does not claim an independently executed current-branch verifier run.

This document does not claim C4 certification.

Current status:

[
\boxed{
[P\text{-candidate}]
\quad
[V\text{-reported}]
\quad
[L\text{-open}]
\quad
C4\text{ BLOCKED}.
}
]

---

19. Final research consequence

The research program should now be split into two independent theorem lanes:

Lane A — Aggregate enumeration

[
\boxed{
\text{PB-004}
\rightarrow
S_k=k!p(k)
\rightarrow
\text{rooted forests}
\rightarrow
A_n.
}
]

Lane B — Structural cycle classification

[
\boxed{
\text{PB-004}
\rightarrow
\text{cycle decomposition}
\rightarrow
\text{phase torsors}
\rightarrow
d^{k-1}
\rightarrow
\text{weighted Bell formula}.
}
]

Lane A is the shortest route to a new closed mathematical theorem.

Lane B is the deeper structural theorem.

Neither should be allowed to masquerade as formally complete until its own proof obligations close.
