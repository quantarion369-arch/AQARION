
# PB-CORE-005 — Cycle-Orbit Classification

**Program:** AQARION / Quantarion-AI  
**Lane:** PB — finite pullback and eventual-core structure  
**Artifact:** PB-CORE-005-CYCLE-ORBIT-CLASSIFICATION.md  
**Status:** corrected consolidated research document  
**Promotion:** not authorized  
**Lean status:** open; no Lean certification is claimed by this document  
**Publication status:** blocked pending completion of the stated proof and reproducibility obligations

---

## 1. Scope and evidence discipline

This document studies congruence relations preserved by a finite self-map and the reduction of that problem to the eventual periodic core. It then records cycle-level classification results and a proposed global counting formula.

The document distinguishes the following evidence categories:

- **[P]** — mathematical proof supplied in this document.
- **[V-recorded]** — computational result reported by the repository; not represented here as a fresh execution.
- **[P-CANDIDATE]** — a proposed classification or formula whose full proof obligations remain open.
- **[L-open]** — formalization or Lean verification remains outstanding.
- **[R]** — research context or a direction requiring further investigation.

A computational match does not substitute for a proof. A written proof does not establish that a Lean project builds. A candidate formula is not a certified theorem merely because its small cases agree.

The correction policy is strict: contradictions in earlier versions are resolved in favor of the mathematically correct statements below. In particular, the two-cycle example for lengths \(2\) and \(4\) has value \(9\), not \(8\).

---

## 2. Basic definitions

Let \(X\) be a set and let \(T:X\to X\).

For an equivalence relation \(E\) on \(X\), define its pullback under \(T\) by

\[
T^*E
=
\{(x,y)\in X^2:T(x)\mathrel E T(y)\}.
\]

Call \(E\) **forward invariant** when

\[
x\mathrel E y
\implies
T(x)\mathrel E T(y),
\]

equivalently,

\[
E\subseteq T^*E.
\]

Call \(E\) **pullback-stable** when

\[
T^*E\subseteq E.
\]

Call \(E\) **exactly invariant** when

\[
T^*E=E.
\]

These are different conditions in general. The direction of each inclusion must be retained in every theorem statement.

For a self-map \(T\), write

\[
\operatorname{Con}(X,T)
=
\{E:E\text{ is an equivalence relation on }X
\text{ and }E\subseteq T^*E\}.
\]

Thus \(\operatorname{Con}(X,T)\) denotes the forward-invariant equivalence relations, or congruences of the unary algebra \((X,T)\).

The periodic core is

\[
P=\operatorname{Per}(T)
=\{x\in X:\exists m\geq 1,\ T^m(x)=x\}.
\]

When \(X\) is finite, \(P\) is nonempty if \(X\) is nonempty, \(T(P)=P\), and the restriction

\[
\sigma=T|_P:P\to P
\]

is a permutation.

---

## 3. Finite pullback rigidity

### Theorem PB-005-T1 — finite pullback rigidity

Let \(X\) be finite, let \(E\) be an equivalence relation on \(X\), and let \(T:X\to X\). If

\[
T^*E\subseteq E,
\]

then

\[
\boxed{T^*E=E.}
\]

Consequently, on a finite set, pullback-stability of an equivalence relation implies exact invariance.

### Proof

Let \(\pi:X\to X/E\) be the quotient map. By definition,

\[
x\mathrel E y
\iff
\pi(x)=\pi(y).
\]

Therefore

\[
x\mathrel{T^*E}y
\iff
\pi(T(x))=\pi(T(y)),
\]

so \(T^*E\) is the kernel equivalence relation of \(\pi\circ T\).

The assumption \(T^*E\subseteq E\) means that every \(T^*E\)-class is contained in an \(E\)-class. Hence the map

\[
X/(T^*E)\longrightarrow X/E,
\qquad
[x]_{T^*E}\longmapsto [x]_E
\]

is well-defined and surjective. It follows that

\[
|X/(T^*E)|\geq |X/E|.
\]

On the other hand, the number of equivalence classes of \(T^*E\) equals the size of the image of \(\pi\circ T\):

\[
|X/(T^*E)|
=
|\operatorname{im}(\pi\circ T)|
\leq |X/E|.
\]

Thus

\[
|X/(T^*E)|=|X/E|.
\]

The natural surjection between these finite quotient sets is therefore bijective. Its fibers cannot merge distinct \(T^*E\)-classes, so the two kernel relations coincide:

\[
T^*E=E.
\]

This proves the theorem. \(\square\)

### Scope limitation

Finiteness is essential to this argument. The corresponding assertion is false for arbitrary infinite sets.

---

## 4. Infinite counterexample

Let

\[
X=\mathbb N=\{0,1,2,\ldots\},
\qquad T(n)=n+1.
\]

Define \(E\) to have the single nonsingleton class \(\{0,1\}\), with every \(n\geq2\) in its own singleton class.

Then

\[
T(0)=1,\qquad T(1)=2.
\]

Since \(1\not\mathrel E2\), the pair \((0,1)\) does not belong to \(T^*E\). All other distinct pairs are also excluded from \(T^*E\). Therefore

\[
T^*E=\Delta_X,
\]

where \(\Delta_X\) is equality. But

\[
\Delta_X\subsetneq E.
\]

Hence

\[
T^*E\subsetneq E.
\]

This is an infinite counterexample to pullback rigidity without finiteness. It also identifies exactly where the finite quotient-cardinality argument ceases to apply.

---

## 5. Reduction to the eventual periodic core

### Theorem PB-005-T2 — eventual-core correspondence

Let \(X\) be finite and \(T:X\to X\). Put

\[
P=\operatorname{Per}(T).
\]

Choose \(h\geq0\) large enough that

\[
T^h(X)=P.
\]

Let

\[
\sigma=T|_P.
\]

Then restriction to \(P\) induces a bijection

\[
\boxed{
\operatorname{Con}(X,T)
\cong
\operatorname{Con}(P,\sigma).
}
\]

More explicitly, if \(E\in\operatorname{Con}(X,T)\), its restriction \(F=E|_P\) determines \(E\) uniquely by

\[
\boxed{
x\mathrel E y
\iff
T^h(x)\mathrel F T^h(y).
}
\]

### Proof

First, let \(E\in\operatorname{Con}(X,T)\). Since \(E\) is forward invariant, every iterate \(T^j\) preserves \(E\). In particular,

\[
x\mathrel E y
\implies
T^h(x)\mathrel E T^h(y).
\]

Thus the restriction \(F=E|_P\) controls every pair in \(E\) through its image under \(T^h\).

Because \(T^h(X)=P\), the map \(T^h:X\to P\) is surjective. For \(u,v\in P\), forward invariance gives

\[
u\mathrel Fv
\implies
\sigma(u)\mathrel F\sigma(v).
\]

Hence \(F\in\operatorname{Con}(P,\sigma)\).

Conversely, suppose \(F\in\operatorname{Con}(P,\sigma)\). Define a relation \(E_F\) on \(X\) by

\[
x\mathrel{E_F}y
\iff
T^h(x)\mathrel F T^h(y).
\]

As the inverse image of an equivalence relation under a map, \(E_F\) is an equivalence relation. To show forward invariance, assume \(x\mathrel{E_F}y\). Then

\[
T^h(x)\mathrel F T^h(y).
\]

Forward invariance of \(F\) under \(\sigma\) yields

\[
\sigma(T^h(x))
\mathrel F
\sigma(T^h(y)).
\]

Since \(T\) commutes with its iterates and \(T^h(x),T^h(y)\in P\),

\[
T^h(T(x))\mathrel F T^h(T(y)).
\]

Thus \(T(x)\mathrel{E_F}T(y)\), proving \(E_F\in\operatorname{Con}(X,T)\).

Finally, \(T^h\) acts as a permutation iterate on \(P\), so \(T^h|_P\) is bijective. Its inverse preserves \(F\) because a congruence for a permutation is also invariant under its inverse: on a finite set, forward invariance under a permutation implies exact invariance by Theorem PB-005-T1. Therefore the restriction of \(E_F\) to \(P\) is precisely \(F\).

The two constructions are inverse bijections. \(\square\)

### Consequence

The finite congruence problem for an arbitrary self-map reduces to the congruence problem for a permutation on its periodic core. The transient trees affect how the core relation is pulled back, but introduce no additional independent choice of congruence.

---

## 6. Cycle decomposition

Let the permutation \(\sigma\) on \(P\) have disjoint cycles

\[
C_1,\ldots,C_r
\]

of lengths

\[
m_1,\ldots,m_r.
\]

Then

\[
|P|=m_1+\cdots+m_r.
\]

An equivalence relation \(F\) on \(P\) is a congruence precisely when

\[
x\mathrel Fy
\implies
\sigma(x)\mathrel F\sigma(y).
\]

By finite pullback rigidity, this condition is equivalent to

\[
x\mathrel Fy
\iff
\sigma(x)\mathrel F\sigma(y).
\]

Thus congruences on the periodic core are exactly the equivalence relations invariant under simultaneous application of the permutation.

This statement is proved. A full closed-form classification and count for arbitrary cycle type is a separate claim and must not be inferred merely from this equivalence.

---

## 7. One-cycle classification

Consider a single cycle of length \(m\), identified with the cyclic group

\[
\mathbb Z/m\mathbb Z
\]

and acted on by translation \(x\mapsto x+1\).

### Theorem PB-005-T3 — congruences on a single cycle

Every invariant equivalence relation on a single cycle is determined by a subgroup of \(\mathbb Z/m\mathbb Z\). Consequently, such relations are in bijection with the positive divisors of \(m\), and the number of them is

\[
\boxed{\tau(m)},
\]

where \(\tau(m)\) denotes the number of positive divisors of \(m\).

### Proof

Let \(F\) be an equivalence relation invariant under translation. Define

\[
H=\{a\in\mathbb Z/m\mathbb Z:a\mathrel F0\}.
\]

Since \(F\) is invariant under translation, \(a\mathrel F0\) implies that all translates of this pair remain related. In particular, translating by \(-a\) gives \(0\mathrel F(-a)\), and symmetry gives \((-a)\mathrel F0\). Thus \(H\) is closed under additive inverses.

If \(a,b\in H\), then \(a\mathrel F0\) and \(b\mathrel F0\). Translating the latter relation by \(a\) gives \(a+b\mathrel Fa\). Combining with \(a\mathrel F0\), transitivity gives \(a+b\mathrel F0\). Hence \(a+b\in H\).

Therefore \(H\) is a subgroup. Translation invariance also gives

\[
x\mathrel Fy
\iff
x-y\in H.
\]

Conversely, every subgroup \(H\leq\mathbb Z/m\mathbb Z\) defines an invariant equivalence relation by this formula.

The subgroups of a finite cyclic group are in bijection with the divisors of \(m\). Their number is \(\tau(m)\). \(\square\)

---

## 8. Multiple-cycle phase relations: precise candidate statement

For two disjoint cycles of lengths \(m,n\), write their phases as

\[
\mathbb Z/m\mathbb Z
\quad\text{and}\quad
\mathbb Z/n\mathbb Z.
\]

An invariant equivalence relation that connects the two cycles must be compatible with the simultaneous shift

\[
(a,b)\longmapsto(a+1,b+1).
\]

For \(k\) labeled cycles of lengths \(m_1,\ldots,m_k\), the phase tuple lies in

\[
G=\prod_{i=1}^{k}\mathbb Z/m_i\mathbb Z.
\]

Simultaneous application of the permutation corresponds to translation by

\[
\delta=(1,\ldots,1)\in G.
\]

A proposed description of connected cross-cycle relations in terms of phase orbits and stabilizer subgroups must explicitly account for:

1. the subgroup generated by \(\delta\);
2. the kernel of the phase representation;
3. the individual cycle stabilizers;
4. compatibility with equivalence-relation transitivity;
5. possible multiple connections between cycle pairs;
6. overcounting when the same equivalence relation admits multiple descriptions.

For equal cycle lengths \(d\), a useful candidate phase space is

\[
(\mathbb Z/d\mathbb Z)^k/\langle(1,\ldots,1)\rangle.
\]

This quotient describes phase tuples modulo a common shift. It is a natural organizing device, but its existence alone does not prove that arbitrary invariant equivalence relations are classified bijectively by subgroups or orbits in this quotient.

**Status:** [P-CANDIDATE]. A complete classification theorem requires an explicit construction in both directions and a proof of uniqueness. No general classification or counting formula is certified here solely on the basis of this candidate description.

---

## 9. Global cycle-assembly count: corrected formula

Let \(A_n\) denote the total number of pairs

\[
(T,E)
\]

where \(T:[n]\to[n]\) is a self-map and \(E\in\operatorname{Con}([n],T)\). Equivalently,

\[
A_n
=
\sum_{T:[n]\to[n]}
|\operatorname{Con}([n],T)|.
\]

Every finite functional digraph decomposes into a rooted forest feeding into a permutation on its periodic vertices.

Let \(k\) be the number of periodic vertices. The periodic restriction is a permutation of those \(k\) labeled vertices. Let

\[
p(k)
\]

denote the integer partition function, and define the aggregate permutation count

\[
S_k
=
\sum_{\sigma\in S_k}
|\operatorname{Con}([k],\sigma)|.
\]

The proposed cycle-assembly identity is

\[
\boxed{S_k=k!\,p(k).}
\]

The corresponding global formula is

\[
\boxed{
A_n
=
\sum_{k=1}^{n-1}
\binom nk
k\,n^{\,n-k-1}\,k!\,p(k)
+
n!\,p(n).
}
\]

Equivalently,

\[
\boxed{
A_n
=
n!\sum_{k=1}^{n-1}
\frac{k\,p(k)\,n^{\,n-k-1}}{(n-k)!}
+
n!\,p(n).
}
\]

The final term is a separate endpoint term. It must not be written as though the factor \(n^{n-k-1}\) could be used unchanged at \(k=n\): that would introduce the exponent \(-1\) and would not express the correct forest count.

### 9.1 Rooted-forest factor

For \(1\leq k<n\), the number of rooted forests on \(n\) labeled vertices with a specified set of \(k\) roots, in which every component contains exactly one root, is

\[
F(n,k)=k\,n^{\,n-k-1}.
\]

For \(k=n\), every vertex is a root and there are no nonroot vertices to attach, so

\[
F(n,n)=1.
\]

This endpoint is handled separately in the global sum.

### 9.2 Aggregate permutation identity

The proposed identity

\[
S_k=k!\,p(k)
\]

is a statement about the sum of congruence counts over all permutations of a labeled \(k\)-element set. It is not a claim that every individual permutation has exactly \(p(k)\) congruences.

A proof must group permutations by cycle type and establish that the sum of the invariant-equivalence counts over each cycle type, weighted by the number of permutations of that type, yields the stated aggregate.

The cycle type is indexed by an integer partition \(\lambda\vdash k\). If \(a_j\) is the number of parts of size \(j\), the number of permutations of type \(\lambda\) is

\[
\frac{k!}{\prod_{j\geq1}j^{a_j}a_j!}.
\]

The full proof must evaluate the congruence count for each type and show that the resulting sum is \(k!p(k)\). A list of small numerical agreements is not a substitute for that derivation.

**Evidence status:** [P-CANDIDATE] for the global assembly unless the complete cycle-type sum proof and all required lemmas are supplied in the formal verification artifact. Do not upgrade the formula's status on the basis of the table below alone.

---

## 10. Correct exact examples

For a single cycle of length \(m\), the count is \(\tau(m)\).

For two cycles of lengths \(m,n\), the recorded candidate formula is

\[
C(m,n)
=
\tau(m)\tau(n)
+
\sum_{d\mid\gcd(m,n)}d.
\]

Here \(\tau\) is the divisor-counting function. The sum ranges over the positive divisors of \(\gcd(m,n)\).

Under this formula, the following examples are arithmetically correct:

| Cycle lengths | Calculation | Value |
|---|---:|---:|
| \((2,2)\) | \(2\cdot2+(1+2)\) | \(7\) |
| \((2,3)\) | \(2\cdot2+1\) | \(5\) |
| \((3,3)\) | \(2\cdot2+(1+3)\) | \(8\) |
| \((2,4)\) | \(2\cdot3+(1+2)\) | \(9\) |
| \((4,4)\) | \(3\cdot3+(1+2+4)\) | \(16\) |

These are examples of the two-cycle candidate formula. They do not, by themselves, prove it for all \(m,n\), nor do they establish the general \(k\)-cycle formula.

### Identity permutation on three points

The identity permutation on three points has five equivalence relations, corresponding to the five set partitions of a three-element set. Thus

\[
|\operatorname{Con}([3],\operatorname{id})|
=
B_3
=
5,
\]

where \(B_3\) is the third Bell number.

This is a useful independent boundary check: when every point is a fixed point, every equivalence relation is invariant.

---

## 11. Computational evidence recorded by the repository

The following results are recorded in the PB research artifacts. They are reproduced as repository claims, not as assertions of fresh execution in this editing pass.

- The repository reports finite-map and finite-permutation checks for the stated congruence and restriction/extension identities.
- The repository reports small-case checks for the cycle-level and aggregate-count formulas.
- The repository's broader checkpoint records exhaustive permutation checks through \(n=7\), with additional random permutation checks at \(n=8,9,10\).
- The checkpoint records a brute-force extension attempt at \(n=12\) that timed out; it does not record a successful result for that attempt.

For every reported computational result, a release-quality receipt should identify:

1. the exact source commit;
2. the exact source file hashes;
3. the test command and environment;
4. the generated output;
5. the number of cases executed;
6. the expected and observed values;
7. the manifest hash;
8. the distinction between a completed run, a timeout, and an unexecuted test.

A receipt with `source_hash: null` or `manifest_hash: null` does not cryptographically bind the reported results to a specific source artifact and manifest.

No result is promoted to [V] merely because it appears in this document.

---

## 12. Literature and novelty boundary

Congruences of unary algebras, invariant equivalence relations, and functional digraphs are established mathematical subjects. Relevant literature recorded for this research includes:

- Joel Berman, “On the congruence lattices of unary algebras” (1972).
- C. Ratanaprasert and K. Denecke, “Unary operations with long pre-periods,” *Discrete Mathematics* 308 (2008), 4998–5005.
- D. Jakubíková-Studenovská and L. Janičková, “Congruence lattices of connected monounary algebras,” *Algebra Universalis* 81 (2020), Article 54.

These references are research context, not a claim that each formula in this document appears in those works. Conversely, absence of a matching formula in an incomplete literature search does not establish novelty or priority.

Any publication claim about the phase-orbit formulation or the aggregate identity must be preceded by a literature review that compares exact definitions, hypotheses, statements, and proofs.

---

## 13. Theorem and obligation ledger

| ID | Claim | Evidence status | Remaining obligation |
|---|---|---|---|
| PB-005-T1 | Finite pullback rigidity | [P] | Formalize and verify in Lean |
| PB-005-T2 | Eventual-core correspondence | [P] | Formalize and verify in Lean |
| PB-005-T3 | Single-cycle divisor classification | [P] | Formalize and verify in Lean |
| PB-005-C1 | Two-cycle count formula | [P-CANDIDATE] | Complete general proof and independent verification |
| PB-005-C2 | General phase-orbit classification | [P-CANDIDATE] | Prove existence, completeness, and uniqueness |
| PB-005-C3 | Aggregate identity \(S_k=k!p(k)\) | [P-CANDIDATE] unless its full cycle-type proof is supplied | Complete the cycle-type sum proof |
| PB-005-C4 | Global formula for \(A_n\) | [P-CANDIDATE] pending the aggregate identity and assembly proof | Prove the forest/permutation decomposition and verify the formal statement |
| PB-005-V1 | Repository-reported finite checks | [V-recorded] | Reproduce from pinned source and environment |
| PB-005-L1 | Lean certification | [L-open] | Complete formalization and build |
| PB-005-R1 | Novelty/priority of phase classification | [R] | Complete comparative literature review |

---

## 14. Corrected research conclusion

The finite pullback-rigidity theorem, the reduction to the eventual periodic core, and the single-cycle divisor classification are supported by explicit mathematical proofs in this document.

The two-cycle count, general phase-orbit classification, aggregate permutation identity, and global total-count formula are kept at candidate status unless and until their complete proofs and verification obligations are met. Repository-reported computations remain recorded evidence rather than fresh certification.

The immediate mathematical target is a complete proof of the cycle-type aggregate

\[
S_k=k!\,p(k),
\]

including the exact invariant-equivalence count for each permutation cycle type. Only after that proof is established should the global forest-assembly formula be promoted. Lean formalization, reproducible computation, hash-bound receipts, and literature review remain separate gates.

**Final status:** corrected mathematical document; no claim of fresh execution, Lean completion, source modification, or publication approval is made here.
