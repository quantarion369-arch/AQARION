AQARION LEAN THEOREM TARGETS

Status

OPEN — TARGET SPECIFICATION ONLY

No theorem in this document is certified merely because its statement appears here.

---

TARGET ORDER

JS-02 — Finite Kernel Equality

Given finite X, T:X\to X, and equivalence E:

[
T(x)ET(y)\Rightarrow xEy
]

implies

[
\ker(q_E\circ T)=E.
]

This is the first formalization target.

---

JS-03 — Quotient Injectivity

Define

[
\bar T_E([x])=[T(x)].
]

Prove:

[
\bar T_E([x])=\bar T_E([y])
\Rightarrow
[x]=[y].
]

---

JS-04 — Finite Quotient Permutation

Use finite cardinality to prove:

[
\bar T_E
]

is bijective.

---

JS-G01 — Simple Incidence Relation

For E,F, define:

[
[A]_E\sim[B]_F
\iff
A\cap B\ne\varnothing.
]

Do not use a point-indexed multigraph as the canonical object.

The theorem concerns the simple incidence relation.

---

JS-G02 — Join Components

Prove that the connected-component equivalence induced by the incidence graph equals:

[
E\vee F.
]

---

JS-G03 — Incidence Automorphism

Given quotient permutations

[
\bar T_E,\bar T_F,
]

prove that

[
(A,B)\mapsto
(\bar T_E(A),\bar T_F(B))
]

is an automorphism of the finite incidence relation.

---

JS-11 — Finite Join Stability

Conclude:

[
T^{-1}(E)\subseteq E
\land
T^{-1}(F)\subseteq F
\Longrightarrow
T^{-1}(E\vee F)\subseteq E\vee F.
]

---

FORBIDDEN FORMALIZATION SHORTCUTS

Do not:

- omit the finite hypothesis;
- use "sorry";
- hide the finite cardinality argument;
- import a theorem equivalent to the target without recording it;
- replace the theorem with exhaustive computation;
- weaken the statement simply to obtain compilation;
- use a multigraph where a simple incidence relation is required.

---

BUILD EVIDENCE

A formalization receipt must identify:

repository revision
Lean version
toolchain
lake version
target theorem
imports
build command
build result
sorry/admit audit
axiom audit

A successful build is formalization evidence.

It is not by itself a repository-wide certification.
