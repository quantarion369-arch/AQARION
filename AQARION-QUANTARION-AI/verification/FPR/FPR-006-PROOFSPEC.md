AQ-FPR-006 — Proof Specification

5 October 2026

Statement

Let \sigma be a permutation of a finite set X, with disjoint cycles

[
C_1,\ldots,C_r,
\qquad |C_i|=c_i.
]

Let N(c_1,\ldots,c_r) denote the number of equivalence relations E on X satisfying

[
xEy\Longrightarrow \sigma(x)E\sigma(y).
]

Then

[
N(c_1,\ldots,c_r)

\sum_{\pi\in\Pi([r])}
\prod_{B\in\pi}
\left(
\sum_{d\mid g_B}d^{|B|-1}
\right),
]

where

[
g_B=\gcd{c_i:i\in B}.
]

Single-cycle lemma

For a cycle C_c, every invariant equivalence relation is of the form

[
x\sim y
\iff
x\equiv y\pmod d
]

for a unique divisor d\mid c.

Hence the number of invariant equivalence relations on C_c is

[
\tau(c).
]

Cycle-index relation

For an invariant equivalence E, define a relation on cycle indices by

[
i\sim_E j
\iff
\exists x\in C_i,\ y\in C_j,\ xEy.
]

This relation is an equivalence relation on [r].

Its equivalence classes are the blocks B of the outer partition.

Common-modulus lemma

Fix a block B containing k cycles.

The quotient induced by E on each participating cycle is a cycle of a common length d.

Therefore

[
d\mid c_i
]

for every i\in B, and hence

[
d\mid g_B.
]

Conversely, every divisor d\mid g_B gives admissible common quotient data.

Phase lemma

Fix d\mid g_B.

Choose coordinates

[
C_i\simeq\mathbb Z/c_i\mathbb Z.
]

An equivariant quotient map to the common d-cycle has the form

[
q_i(x)=x+\phi_i\pmod d.
]

Thus phase vectors lie in

[
(\mathbb Z/d\mathbb Z)^k.
]

Two phase vectors define the same equivalence relation precisely when they differ by a common diagonal translation.

Therefore the number of distinct phase classes is

[
\frac{d^k}{d}=d^{k-1}.
]

Hence

[
W(B)

\sum_{d\mid g_B}d^{|B|-1}.
]

Block independence

Different blocks of the cycle-index partition have disjoint supports.

Therefore their choices multiply:

[
N_\pi

\prod_{B\in\pi}W(B).
]

Summing over all set partitions gives

[
N(c_1,\ldots,c_r)

\sum_{\pi\in\Pi([r])}
\prod_{B\in\pi}W(B).
]

Evidence boundary

The underlying single-cycle congruence structure is classical.

The explicit weighted phase enumeration is retained as a proof candidate pending a complete formal proof and literature-priority determination.

Current status:

Mathematical status: proof candidate
Computational corroboration: PASS
External independent reproduction: NOT ESTABLISHED
Literature priority: OPEN
Lean: OPEN
C4: BLOCKED
Publication: BLOCKED
Promotion: BLOCKED
