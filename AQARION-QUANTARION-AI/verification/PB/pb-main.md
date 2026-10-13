AQARION-QUANTARION-AI/DOCS/THEOREMS/PB-CORE-006.md
```

This is the canonical document. Keep `PB-001.md` and the Gate 2 mutation document separate.

***

# AQ-PB-CORE-006 — Aggregate Enumeration of Pullback-Fixed Equivalences

**Artifact ID:** `AQ-PB-CORE-006`  
**Date:** 2026-10-12  
**Mathematical status:** Candidate formula; general derivation presented; independent proof review pending  
**Computational status:** Reported finite checks; repository-bound replay not established by this document  
**Lean status:** OPEN  
**C4:** BLOCKED  
**Publication:** BLOCKED  
**Promotion:** NOT AUTHORIZED

***

## 1. Statement

Let $$X_n=\{0,\ldots,n-1\}$$. Let $$\mathcal T_n$$ be the set of all maps $$T:X_n\to X_n$$. There are $$n^n$$ such maps.

For $$T\in\mathcal T_n$$, define

$$
\operatorname{Stab}(T)
=
\left\{
E\in\operatorname{Eq}(X_n):
T^*E=E
\right\},
$$

where the pullback is defined by

$$
x\mathrel{T^*E}y
\iff
T(x)\mathrel{E}T(y).
$$

Define the aggregate

$$
A_n
=
\sum_{T\in\mathcal T_n}
\left|\operatorname{Stab}(T)\right|.
$$

Let $$p(k)$$ denote the number of integer partitions of $$k$$.

**Candidate closed formula:**

$$
\boxed{
A_n
=
\sum_{k=1}^{n}
\binom{n}{k}
k n^{n-k-1}
k!\,p(k)
}
$$

with the $$k=n$$ summand interpreted as

$$
\binom{n}{n}n!\,p(n)=n!\,p(n).
$$

Equivalently,

$$
\boxed{
A_n
=
n!
\sum_{k=1}^{n}
\frac{k\,p(k)\,n^{n-k-1}}{(n-k)!}.
}
$$

For $$k=n$$, use the original summand $$n!\,p(n)$$; do not interpret $$n^{-1}$$ literally.

***

## 2. Dependency structure

This aggregate theorem does **not** require PB-CORE-005’s phase-orbit classification.

Its proof route requires only:

1. Periodic-core reduction.
2. Enumeration of permutation/equivalence pairs on the periodic core.
3. Enumeration of rooted forests feeding the core.

```text
DEPENDENCY LANES
------------------------------------------------------------
Lane A — Aggregate enumeration

PB-001 -> PB-004 -> S_k = k! p(k)
                 -> rooted forests
                 -> A_n

Lane B — Structural cycle classification

PB-001 -> PB-004 -> cycle decomposition
                 -> phase torsors
                 -> d^(k-1)
                 -> weighted Bell formula
------------------------------------------------------------
```

PB-CORE-005 is a separate structural refinement. It is not a prerequisite for the aggregate identity.

***

## 3. Periodic-core reduction

Let

$$
P=\operatorname{Per}(T)
$$

be the set of periodic points of $$T$$. By PB-CORE-004,

$$
\operatorname{Stab}(T)
\cong
\operatorname{Con}(P,T|_P).
$$

Let $$|P|=k$$. Then $$T|_P$$ is a permutation of $$P$$. Therefore,

$$
\left|\operatorname{Stab}(T)\right|
=
\left|\operatorname{Con}(P,T|_P)\right|.
$$

Thus the contribution of $$T$$ depends on:

1. The size $$k$$ of its periodic core.
2. The permutation $$T|_P$$ on that core.
3. The rooted forest structure feeding into the core.

***

## 4. Permutation/equivalence pairs

Define

$$
S_k
=
\sum_{\sigma\in S_k}
\left|\operatorname{Con}([k],\sigma)\right|,
$$

where $$\operatorname{Con}([k],\sigma)$$ is the set of equivalence relations $$E$$ on $$[k]$$ satisfying

$$
\sigma(E)=E.
$$

Equivalently,

$$
S_k
=
\left|
\left\{
(\sigma,E):
\sigma\in S_k,\;
E\in\operatorname{Eq}([k]),\;
\sigma(E)=E
\right\}
\right|.
$$

**Claim:**

$$
\boxed{
S_k=k!\,p(k).
}
$$

***

## 5. Counting by block-size profile

Fix an equivalence relation $$E$$ on $$[k]$$. Let its block-size profile be

$$
1^{m_1}2^{m_2}\cdots,
$$

where there are $$m_s$$ blocks of size $$s$$, and

$$
\sum_s s\,m_s=k.
$$

The number of set partitions of $$[k]$$ with this profile is

$$
\boxed{
\frac{k!}{\prod_s (s!)^{m_s}m_s!}.
}
$$

A permutation preserves $$E$$ exactly when it permutes blocks of equal size and independently permutes elements within each block.

For blocks of size $$s$$:

- The $$m_s$$ blocks may be permuted in $$m_s!$$ ways.
- Each block contributes $$s!$$ internal permutations.

Therefore, the number of permutations preserving a fixed partition with this profile is

$$
\boxed{
\prod_s (s!)^{m_s}m_s!.
}
$$

Multiplying,

$$
\frac{k!}{\prod_s (s!)^{m_s}m_s!}
\cdot
\prod_s (s!)^{m_s}m_s!
=
k!.
$$

Thus every block-size profile contributes exactly $$k!$$ permutation/equivalence pairs.

There are $$p(k)$$ integer partitions of $$k$$, hence $$p(k)$$ block-size profiles. Therefore,

$$
\boxed{
S_k=k!\,p(k).
}
$$

Equivalence relations on a finite set correspond exactly to set partitions of that set. [1271][1272]

***

## 6. Transient attachments

Fix a particular $$k$$-element periodic core $$P\subseteq X_n$$.

The remaining $$n-k$$ vertices are transient. Their functional graph consists of directed rooted trees whose roots are the $$k$$ prescribed periodic vertices.

For $$k<n$$, the number of labeled rooted forests on $$[n]$$ with prescribed root set $$P$$ is

$$
\boxed{
k n^{n-k-1}.
}
$$

For $$k=n$$, there are no transient vertices, so the count is $$1$$.

This is the classical specified-root forest enumeration. It is not claimed as an AQARION result.

***

## 7. Contribution of a fixed core size

There are

$$
\binom{n}{k}
$$

choices for the periodic vertex set.

For each such core:

- There are $$k n^{n-k-1}$$ transient rooted forests when $$k<n$$.
- There is $$1$$ transient forest when $$k=n$$.
- The permutation/equivalence pairs on the core contribute $$k!\,p(k)$$.

Therefore, the total contribution from maps whose periodic core has size $$k$$ is

$$
\boxed{
\binom{n}{k}
k n^{n-k-1}
k!\,p(k)
}
$$

for $$k<n$$, and

$$
\boxed{
n!\,p(n)
}
$$

for $$k=n$$.

Summing over $$1\le k\le n$$ gives the aggregate formula.

***

## 8. Generating function

Define

$$
P(z)=\sum_{k\ge1}p(k)z^k,
$$

and let $$T(z)$$ be the rooted-tree generating function

$$
T(z)=ze^{T(z)}.
$$

Then

$$
\boxed{
\sum_{n\ge1}\frac{A_n}{n!}z^n
=
P(T(z)).
}
$$

This follows by expanding the aggregate formula and applying Lagrange inversion.

**Correction:** an earlier draft stated

$$
\sum_{n\ge1}\frac{A_n}{n!}z^n
=
P(T(z))-1.
$$

That expression is incorrect. Since $$A_1=1$$, the left-hand side has constant term $$0$$. But $$P(T(z))-1$$ has constant term $$-1$$. The corrected identity above has the correct constant term and linear term.

***

## 9. Small values

The first values are:

$$
\begin{aligned}
A_1&=1,\\
A_2&=6,\\
A_3&=51,\\
A_4&=592,\\
A_5&=8{,}565,\\
A_6&=148{,}896.
\end{aligned}
$$

These agree with repository-recorded exhaustive map enumeration on the stated tested scope.

```text
AGGREGATE VALUES
------------------------------------------------------------
n     A_n
------------------------------------------------------------
1     1
2     6
3     51
4     592
5     8,565
6     148,896
------------------------------------------------------------
```

The number of maps is $$n^n$$. For $$n=6$$,

$$
6^6=46{,}656.
$$

The reported total stable-equivalence count is

$$
\boxed{148{,}896.}
$$

***

## 10. Independent permutation aggregate

The core identity

$$
S_k=k!\,p(k)
$$

can be checked independently.

For $$k\le6$$,

$$
\sum_{k=1}^{6}k!
=
1+2+6+24+120+720
=
873
$$

permutations are checked cumulatively.

The repository-recorded permutation verifier reports zero mismatches through $$k=6$$.

This is **reported computational evidence**, not a substitute for the analytic proof.

***

## 11. Relationship to PB-CORE-005

PB-CORE-005 proposes the finer formula

$$
N(c_1,\ldots,c_r)
=
\sum_{\pi\in\Pi([r])}
\prod_{B\in\pi}
\left(
\sum_{d\mid g_B}d^{|B|-1}
\right),
$$

where

$$
g_B=\gcd(c_i:i\in B).
$$

That formula classifies individual permutation congruence structures by cycle lengths.

It is not needed for the aggregate identity

$$
S_k=k!\,p(k).
$$

Therefore,

$$
\boxed{
\text{PB-CORE-006 does not depend on completion of PB-CORE-005.}
}
$$

***

## 12. Why the aggregate identity is natural

For each equivalence relation $$E$$, the permutations preserving $$E$$ are exactly the automorphisms of the corresponding set partition.

For a block-size profile $$\lambda\vdash k$$,

$$
\#\{\text{partitions of profile }\lambda\}
\times
\#\{\text{permutations preserving one such partition}\}
=
k!.
$$

Since there are $$p(k)$$ integer-partition profiles,

$$
S_k=k!\,p(k).
$$

This identity is independent of the finer cycle-phase classification.

***

## 13. Evidence status

| Component | Status |
|---|---|
| Periodic-core reduction | Analytic derivation presented; independent review pending |
| Permutation-core pair count $$S_k=k!\,p(k)$$ | Analytic derivation presented; independent review pending |
| Fixed-root forest count | Classical combinatorial result |
| Aggregate formula | Candidate until repository proof artifact is independently reviewed |
| Exhaustive map enumeration $$n\le7$$ | Reported; repository-bound replay not established here |
| Permutation enumeration $$k\le6$$ | Reported; repository-bound replay not established here |
| Generating function | Corrected expression presented; independent review pending |
| Lean formalization | OPEN |
| Independent external replay | NOT ESTABLISHED HERE |
| C4 | BLOCKED |
| Publication | BLOCKED |
| Promotion | NOT AUTHORIZED |

***

## 14. Literature boundary

The ingredients used here are not claimed as novel.

Classical literature establishes substantial parts of the surrounding theory of unary and monounary algebras, invariant equivalence relations, rooted forests, functional graphs, and cyclic structures.

In particular:

- Rooted-forest enumeration includes the specified-root formula $$k n^{n-k-1}$$.
- Functional graphs decompose into cycles with rooted trees feeding into cycles.
- Lagrange inversion is a standard tool for extracting coefficients from implicitly defined generating functions.
- Berman established foundational results on congruence lattices of unary algebras.
- Ratanaprasert and Denecke studied invariant equivalence relations for finite unary operations with long pre-periods.
- Jakubíková-Studenovská and Janičková studied congruence lattices of connected monounary algebras.

The exact AQARION aggregate synthesis

$$
A_n
=
\sum_{k=1}^{n}
\binom{n}{k}
k n^{n-k-1}
k!\,p(k)
$$

was not located in the current literature search.

**Permitted statement:**

> No exact source for this aggregate formula was located in the current search pass.

**Prohibited statement:**

> This formula has never appeared before.

***

## 15. Formalization target

The Lean development should prove the following independently:

```lean
theorem PB006_permutation_aggregate
    (k : ℕ) :
    ∑ σ : Equiv.Perm (Fin k),
      Fintype.card { E : EquivalenceRelation (Fin k) |
        ∀ x y : Fin k,
          (E x y ↔ E (σ x) (σ y)) } =
    k.factorial * Nat.PartitionNumber k := by
  sorry
```

The exact Lean encoding may differ. The theorem must not depend on PB-CORE-005’s phase parameterization.

The second formal theorem should establish the fixed-root forest factor. Only after both are formalized should the final aggregate theorem be assembled.

Lean’s `theorem` command requires a proposition after the colon and a proof after `:=`; `sorry` marks an incomplete proof and must not be treated as verification. [1259]

***

## 16. Certification boundary

This document does **not** claim:

- A completed Lean proof.
- A no-sorry Lean build.
- An independently executed current-branch verifier run.
- A repository-bound replay certificate.
- C4 certification.
- Publication readiness.
- Research promotion.

Current disposition:

$$
\boxed{
[P\text{-candidate}]
\quad
[V\text{-reported}]
\quad
[L\text{-open}]
\quad
C4\text{ BLOCKED}.
}
$$

***

## 17. Final research consequence

The research program should remain split into two independent theorem lanes:

```text
LANE A — AGGREGATE ENUMERATION
------------------------------------------------------------
PB-001
  -> PB-004
  -> S_k = k! p(k)
  -> rooted forests
  -> A_n
------------------------------------------------------------

LANE B — STRUCTURAL CYCLE CLASSIFICATION
------------------------------------------------------------
PB-001
  -> PB-004
  -> cycle decomposition
  -> phase torsors
  -> d^(k-1)
  -> weighted Bell formula
------------------------------------------------------------
```

Lane A is the shortest route to a closed aggregate theorem.

Lane B is the deeper structural theorem.

Neither should be treated as formally complete until its own proof obligations close.

***

## Gate 2 — Semantic gcd-to-lcm mutation

**Purpose:** test whether the Lean development rejects a mathematically incorrect replacement of a gcd-based quantity by an lcm-based quantity.

This is a **semantic mutation gate**, not a compilation-only gate.

### Baseline

The intended implementation uses:

```lean
listGcd b
```

For witness

$$
b=,[2][4]
$$

the intended value is

$$
\gcd(2,4)=2.
$$

The corresponding witness values are

$$
W=5,
\qquad
f_2=9.
$$

### Mutation

Replace

```lean
listGcd b
```

with

```lean
b.foldl Nat.lcm 1
```

For $$b=$$, the mutated value is[2][4]

$$
\operatorname{lcm}(2,4)=4.
$$

The mutated witness gives

$$
W=7,
\qquad
f_2=13.
$$

Therefore, the mutation changes the mathematical result.

### Required execution

```bash
cd ~/aqarion-lean/AQFPR006

# Baseline
lake build
BASELINE_BUILD_EXIT=$?

# Apply semantic mutation
sed -i 's/listGcd b/b.foldl Nat.lcm 1/' AQFPR006/Basic.lean

lake build
MUTATION_BUILD_EXIT=$?

# Restore
sed -i 's/b.foldl Nat.lcm 1/listGcd b/' AQFPR006/Basic.lean

lake build
RESTORED_BUILD_EXIT=$?
```

Lean provides `Nat.gcd` and `Nat.lcm`; their definitions and basic properties are part of the standard library. [1255][1257]

### Expected disposition

A valid gate requires:

```text
BASELINE_BUILD_EXIT   = 0
MUTATION_BUILD_EXIT   = 1
RESTORED_BUILD_EXIT   = 0
```

and a semantic witness equivalent to:

```text
MUTATION_WITNESS:
input=[2,4]
expected_gcd_result=9
mutated_lcm_result=13
different=true
```

### Interpretation

| Outcome | Meaning |
|---|---|
| PASS | All three build conditions hold, and the mutation is rejected because it changes the theorem-level result. |
| FAIL | The mutated implementation compiles and passes the relevant theorem/check despite producing incorrect lcm semantics. |
| INCONCLUSIVE | Compilation status is unavailable, the wrong source file was mutated, or the witness does not establish that the mutation changes the verified result. |

A successful baseline build alone is insufficient. A successful mutation rejection demonstrates that the formal development is sensitive to the semantic distinction

$$
\gcd(2,4)\ne\operatorname{lcm}(2,4).
$$

No PASS is asserted by this document until the three runtime exit statuses and the witness are actually observed.

Citations:
[1] 26.9 Integer Partitions: Restricted Number and Part Size https://dlmf.nist.gov/26.9
[2] [PDF] Set Partitions and Other Bell Number Enumerated Objects https://cs.uwaterloo.ca/journals/JIS/VOL26/Beyene/beyene13.pdf
[3] [PDF] BALLS INTO BOXES 1. partitions of sets 1.1. Equivalence relations ... https://people.math.sc.edu/laszlo/Twelvefold.pdf
[4] Partition of a set - Wikipedia https://en.wikipedia.org/wiki/Partition_of_a_set
