AQ-PB-CORE-005 — CYCLE-ORBIT CLASSIFICATION

Artifact ID: AQ-PB-CORE-005
Title: Cycle-Orbit Classification of Invariant Equivalence Relations
Status: "[P-CANDIDATE]" structural theorem · "[V]" computational support · "[L]" OPEN · "C4 BLOCKED"

---

1. Purpose

This artifact isolates the remaining structural problem after periodic-core reduction.

PB-CORE-004 establishes

[
\operatorname{Stab}(T)
\cong
\operatorname{Con}(\operatorname{Per}(T),T|_{\operatorname{Per}(T)}).
]

Therefore the remaining problem is purely a finite permutation problem.

Let the periodic core consist of r cycles with lengths

[
c_1,\ldots,c_r.
]

The objective is to classify all equivalence relations invariant under the permutation.

The primary candidate theorem is a bijection between:

1. invariant equivalence relations joining a specified connected collection of cycles; and
2. a divisor d\mid\gcd(c_1,\ldots,c_k) together with a relative phase orbit in

[
(\mathbb Z/d)^k/\Delta_d.
]

The corresponding local count is

[
d^{k-1}.
]

This artifact deliberately treats that classification as a candidate theorem, not as a formally closed theorem.

---

2. Cycle model

For a cycle of length c, identify its points with

[
\mathbb Z/c\mathbb Z
]

and let the permutation act by

[
x\mapsto x+1.
]

For k cycles with lengths

[
c_1,\ldots,c_k,
]

write the points as

[
(i,a),
\qquad
1\le i\le k,
\quad
a\in\mathbb Z/c_i\mathbb Z.
]

The permutation is

[
\sigma(i,a)=(i,a+1).
]

---

3. Local connected-block classification candidate

Consider an invariant equivalence relation \theta whose quotient identifies the k cycles into one connected component at the cycle-index level.

The candidate classification is:

[
\boxed{
\theta
\longleftrightarrow
\left(
d,
[\phi]
\right)
}
]

where

[
d\mid\gcd(c_1,\ldots,c_k)
]

and

[
[\phi]\in(\mathbb Z/d)^k/\Delta_d.
]

Here

[
\Delta_d

{(a,\ldots,a):a\in\mathbb Z/d\mathbb Z}
]

is the diagonal subgroup.

---

4. Why the divisor condition appears

If a connected invariant equivalence relation identifies cycles of lengths

[
c_1,\ldots,c_k,
]

then the induced permutation on the common quotient component has some cycle length d.

Every original cycle maps equivariantly onto that quotient cycle.

Therefore

[
d\mid c_i
]

for every i.

Hence

[
\boxed{
d\mid\gcd(c_1,\ldots,c_k).
}
]

Conversely, if

[
d\mid c_i
]

for every i, each cycle admits an equivariant quotient map onto C_d.

---

5. Phase parameters

For cycle i, choose an equivariant map

[
\phi_i:C_{c_i}\to C_d.
]

After identifying the cycles with additive cyclic groups, every such map has the form

[
\phi_i(a)=a+t_i\pmod d
]

for some

[
t_i\in\mathbb Z/d\mathbb Z.
]

Thus a connected system of k cycles has phase vector

[
(t_1,\ldots,t_k)\in(\mathbb Z/d)^k.
]

Changing the origin of the common quotient by s\in\mathbb Z/d\mathbb Z replaces every phase by

[
(t_1+s,\ldots,t_k+s).
]

Therefore the intrinsic parameter is the diagonal orbit

[
\boxed{
[(t_1,\ldots,t_k)]
\in
(\mathbb Z/d)^k/\Delta_d.
}
]

---

6. Candidate local count

The diagonal action is free.

Therefore

[
\left|
(\mathbb Z/d)^k/\Delta_d
\right|

\frac{d^k}{d}

d^{k-1}.
]

Thus the candidate number of invariant connected equivalence structures for fixed d is

[
\boxed{
d^{k-1}.
}
]

Summing over all admissible quotient cycle lengths gives

[
\boxed{
\sum_{d\mid\gcd(c_1,\ldots,c_k)}
d^{k-1}.
}
]

---

7. Important sign convention

The canonical phase convention is

[
\phi_i(a)=a+t_i\pmod d.
]

If the reference point on the quotient is 0, then

[
(i,a)\sim(1,0)
]

corresponds to

[
a+t_i\equiv0\pmod d,
]

so

[
t_i\equiv-a\pmod d.
]

Thus the inverse parameter extracted from an equivalence relation is

[
\boxed{
t_i=-a_i.
}
]

For d=2, this sign disappears because

[
-a=a\pmod2.
]

The sign must not be silently omitted when generalizing to d\ge3.

---

8. Candidate bijection theorem

Candidate Theorem

Let

[
c_1,\ldots,c_k\ge1.
]

For invariant equivalence relations that connect exactly these k cycles, there is a bijection

[
\boxed{
\left{
\text{connected invariant equivalence relations}
\right}
\cong
\bigsqcup_{d\mid\gcd(c_1,\ldots,c_k)}
(\mathbb Z/d)^k/\Delta_d.
}
]

Consequently,

[
\boxed{
#{\text{connected invariant relations}}

\sum_{d\mid\gcd(c_1,\ldots,c_k)}
d^{k-1}.
}
]

---

9. Required proof obligations

The candidate theorem is not promoted to "[P]" until all of the following are established.

9.1 Extraction

Given an invariant connected equivalence relation \theta, construct:

[
d
]

and

[
[(t_1,\ldots,t_k)].
]

9.2 Divisor condition

Prove

[
d\mid c_i
]

for every i.

9.3 Phase existence

Prove that each cycle admits a phase parameter relative to a reference cycle.

9.4 Phase uniqueness

Prove that the phase is unique modulo the common diagonal shift.

9.5 Reconstruction

Show that the extracted d and phase orbit reconstruct the complete equivalence relation.

9.6 Injectivity

Two parameter pairs producing the same equivalence relation must differ only by the diagonal action.

9.7 Surjectivity

Every admissible parameter pair produces an invariant equivalence relation.

9.8 Assembly

Combine connected cycle blocks over set partitions of the cycle-index set.

---

10. Small exact examples

One cycle

For one cycle of length m,

[
\boxed{
|\operatorname{Con}(C_m)|=\tau(m).
}
]

This is classical.

---

Two cycles

For cycles of lengths m,n,

[
\boxed{
\tau(m)+\tau(n)+
\sum_{d\mid\gcd(m,n)}d.
}
]

The first two terms correspond to keeping the cycles separate.

The final term counts connected identifications.

---

Examples

(2,2)

[
\tau(2)+\tau(2)+
(1+2)

2+2+3

7. 

]

(2,3)

[
2+2+1=5.
]

(2,4)

[
2+3+(1+2)=8.
]

The value 9 previously considered for (2,4) is incorrect.

---

11. General cycle-assembly formula

Let the permutation have cycle lengths

[
c_1,\ldots,c_r.
]

For a set partition

[
\pi\in\Pi([r]),
]

each block B\in\pi represents a collection of cycles that are connected in the quotient.

Define

[
g_B

\gcd(c_i:i\in B).
]

The candidate number of structures associated with B is

[
\sum_{d\mid g_B}d^{|B|-1}.
]

Therefore the global candidate formula is

[
\boxed{
N(c_1,\ldots,c_r)

\sum_{\pi\in\Pi([r])}
\prod_{B\in\pi}
\left(
\sum_{d\mid g_B}d^{|B|-1}
\right).
}
]

This formula is a candidate theorem until the local bijection and assembly are formally proved.

---

12. Identity-core check

If every cycle has length 1, then

[
g_B=1
]

for every block.

Hence

[
\sum_{d\mid1}d^{|B|-1}=1.
]

Therefore

[
N(1,\ldots,1)

|\Pi([r])|

B_r,
]

the Bell number.

This agrees with the fact that the identity permutation preserves every equivalence relation.

---

13. Computational evidence

Repository-reported exhaustive permutation verification supports the candidate formula.

The cumulative number of permutations through n=6 is

[
1+2+6+24+120+720

873. 

]

The recorded permutation verifier reports zero mismatches through n=6.

The later cycle-type computations also report the corresponding formula checks through larger cycle-size bounds.

These are evidence of computational agreement.

They do not replace the missing general proof.

---

14. Local Lean status

A local d=2,k=2 relation has been constructed in the PB006 audit.

The relation is

[
p\sim_t q
\iff
p_2+\operatorname{phase}_t(p_1)
\equiv
q_2+\operatorname{phase}_t(q_1)
\pmod2.
]

The local construction establishes:

- reflexivity;
- symmetry;
- transitivity;
- Setoid construction;
- distinction of t=0 and t=1.

The next missing formal step is the converse:

[
\boxed{
\text{every admissible invariant relation on }C_2\sqcup C_2
\text{ is one of the two phase relations}.
}
]

---

15. Required local staircase

The formalization should proceed in this order:

[
\boxed{
(2,2)
\rightarrow
(k,2)
\rightarrow
(2,d)
\rightarrow
(k,d)
\rightarrow
d^{k-1}.
}
]

The first nontrivial boundary is:

[
\boxed{
\mathcal C_{2,2}

{
\operatorname{phaseSetoid}_2(0),
\operatorname{phaseSetoid}_2(1)
}.
}
]

---

16. Evidence status

Claim| Status
Single-cycle divisor classification| "[P]" classical
Two-cycle gcd synchronization| "[P]" classical
General phase-orbit parametrization| "[P-CANDIDATE]"
Local d^{k-1} count| "[P-CANDIDATE]"
Global weighted Bell formula| "[P-CANDIDATE]"
Permutation enumeration through n=6| "[V]" repository-recorded
Local d=2,k=2 construction| "[P-CANDIDATE]" until Lean compile
General Lean theorem| "[O]"
Literature priority| "[R] OPEN"
C4| "BLOCKED"
Publication| "BLOCKED"
Promotion| "FALSE"

---

17. Literature boundary

The following surrounding ingredients are classical:

- congruence lattices of unary algebras;
- congruence relations of monounary algebras;
- periodic/cyclic decomposition;
- invariant equivalence relations of finite unary operations;
- divisor structure on a cycle;
- gcd synchronization between cycles.

Relevant literature includes:

Joel Berman, On the congruence lattices of unary algebras, 1972.

C. Ratanaprasert and K. Denecke, Unary operations with long pre-periods, Discrete Mathematics 308 (2008), 4998–5005.

D. Jakubíková-Studenovská and L. Janičková, Congruence lattices of connected monounary algebras, Algebra Universalis 81 (2020), Article 54.

The current search did not establish priority for the exact multi-cycle phase-orbit formulation

[
(\mathbb Z/d)^k/\Delta_d
]

or for the exact weighted Bell assembly formula.

Therefore the permitted wording is:

«No exact source for the specific phase-orbit parametrization was located in the current search pass.»

The following claims are prohibited:

«“This is novel.”»

«“No one has proved this before.”»

«“AQARION discovered the phase classification.”»

---

18. Final status

[
\boxed{
\text{PB-CORE-005 = STRUCTURAL THEOREM CANDIDATE}
}
]

It is not formally closed.

It is not C4-certified.

It is not publication-certified.

It is not promoted beyond "[P-CANDIDATE]".

The correct next proof target is the local converse/surjectivity theorem, beginning with k=d=2.
