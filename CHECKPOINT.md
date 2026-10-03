AQARION Research Direction

Public Checkpoint — Executable Evidence Infrastructure

Checkpoint date: 2026-09-30
Repository audited: "JASKSG9/Aqarion-Quantarion-AI"
Audited revision: "ce96ae26e57e4806ad8e9f490866c0d48c737a54"
Governance: C4 BLOCKED · Promotion FALSE

---

1. Current research thesis

AQARION is being developed as:

«Executable evidence infrastructure for mathematical and computational research.»

The central object is not a PASS flag and not an AI-generated conclusion.

The central object is a research claim with an auditable evidence state:

[
\text{CLAIM}
\rightarrow
\text{FORMALIZATION}
\rightarrow
\text{COMPUTATION}
\rightarrow
\text{ATTACK}
\rightarrow
\text{REPRODUCTION}
\rightarrow
\text{PROVENANCE}
\rightarrow
\text{DISPOSITION}.
]

---

2. Mathematical research spine

The current principal mathematical program is the pullback operator

[
T^*E(x,y)\iff E(Tx,Ty).
]

The established direct node is pullback preservation of intersections.

The next structural target is finite reflection:

[
T^*E\subseteq E
\quad\Longrightarrow\quad
T^*E=E
]

for finite X and equivalence relation E.

The intended proof proceeds by counting fibers of

[
x\mapsto [T(x)]_E.
]

The resulting quotient action is a permutation.

This provides a structural route toward Join-Stability.

---

3. Join-Stability structural hypothesis

For finite X, if

[
T^*E=E
\qquad\text{and}\qquad
T^*F=F,
]

then T induces permutations on the E- and F-class sets.

Construct the bipartite incidence graph whose left vertices are E-classes, whose right vertices are F-classes, and whose edges are the realized pairs

[
([x]_E,[x]_F).
]

The connected components of this graph correspond to the classes of

[
E\vee F.
]

The induced quotient permutations act injectively on the finite realized edge set and therefore bijectively.

This gives a candidate structural proof of

[
\boxed{
T^*(E\vee F)=E\vee F
}
]

for finite X.

This is a theorem-design result, not yet a formal certification.

---

4. Infinite boundary

The finite hypothesis is structurally meaningful.

For

[
X=\mathbb N,\qquad T(n)=n+1,
]

let E have nontrivial class {0,2}, with all other points singleton, and let F have nontrivial class {0,3}, with all other points singleton.

Then E and F are individually pullback-stable, while

[
2;(E\vee F);3
]

through the boundary point 0, but

[
1\not(E\vee F)2.
]

Since

[
T(1)=2,\qquad T(2)=3,
]

we obtain

[
T^*(E\vee F)\subsetneq E\vee F.
]

This identifies the infinite obstruction as an image/range-gap phenomenon.

---

5. Independent finite computation

An independent exhaustive computation over n=5 examined:

- all 5^5=3125 deterministic maps;
- all 52 set partitions;
- 8,565 stable equivalence relations;
- 24,475 unordered stable pairs.

No Join-Stability counterexample was found.

This is computational corroboration only.

It is not a proof and is not a promotion event.

---

6. Live repository findings

The current repository contains:

Aqarion-Lean/AqarionLean/Pullback.lean
Aqarion-Lean/Pending/PullbackStableJoin.lean
Aqarion-Lean/Pending/Pullback-StableJoin-Surjective.lean
Aqarion-Lean/Pending/pullback_equivgen_subset.lean
Aqarion-Lean/Killed/PullbackStableEquivGen.lean

It also contains:

verification/brt-validation.py
verification/brt-cases.json

Therefore older statements that these source artifacts were entirely absent are superseded by the current repository state.

---

7. Live BRT integration defects

The current BRT validator expects a case containing:

T
partition = list of blocks

while the current BRT corpus supplies:

transition
partition = block labels

Therefore the validator and corpus are not currently schema-compatible.

The current BRT workflow also references a root-level:

verify.sh

which is not present at the audited revision.

The workflow is additionally configured around "master", while the repository default branch is "main".

These are evidence-plumbing defects.

They do not establish that the BRT mathematics is false.

---

8. Mutation-testing finding

The current NC-02 mutation replaces an incidence matrix by its transpose and compares matrix rank.

Because

[
\operatorname{rank}(A)=\operatorname{rank}(A^T),
]

this mutation cannot be killed by the selected rank oracle.

NC-02 is therefore classified as:

[
\boxed{\text{DEAD MUTATION}}
]

and should not be counted as successful adversarial coverage until replaced by a semantically distinguishable mutant.

---

9. Exact verification primitive boundary

The local "exact_proper.py" checkpoint demonstrates a useful execution/comparison primitive.

Its correct semantic interpretation is:

«declared recomputation + Python equality + declared invariant checks.»

It should not yet be treated as a mathematical exactness primitive.

In particular:

- "frozen=True" does not make nested dictionaries immutable;
- Python "==" is not a canonical mathematical equality system;
- deterministic execution is caller responsibility;
- invariant adequacy is outside the primitive's authority.

Repository integration and mathematical certification remain separate.

---

10. Evidence taxonomy

AQARION should distinguish at least:

IDEA
FORMALIZED
COMPUTED
REPLAYED
INDEPENDENTLY VERIFIED
FORMALLY CHECKED
WITHDRAWN
REFUTED
CERTIFICATION ELIGIBLE
PROMOTED

Transitions between these states must be evidence-driven.

An AI-generated assertion must never itself constitute the transition.

---

11. Scientific-agent direction

AQARION's emerging AI research question is:

«Can an AI agent maintain epistemic discipline while conducting a mathematical or computational investigation?»

Relevant capabilities include:

- correct scope handling;
- counterexample search;
- distinction between finite evidence and universal proof;
- mutation resistance;
- independent reproduction;
- provenance preservation;
- appropriate uncertainty;
- withdrawal after failed reproduction;
- recognition that green CI is not a theorem.

This direction is complementary to current scientific-agent benchmarks rather than a replacement for them.

---

12. Current status

Research object| Status
Pullback meet| DIRECT LEAN RESULT
Pullback equivalence preservation| NEXT FORMAL NODE
Finite reflection| THEOREM DESIGN READY
Quotient permutation lemma| THEOREM DESIGN READY
Join incidence-permutation argument| THEOREM DESIGN READY
Infinite boundary counterexample| CONSTRUCTED
Finite n=5 exhaustive corroboration| PASS / COMPUTATIONAL
Join-Stability formal proof| OPEN
Join-Stability promotion| FALSE
BRT exact kernel| PRESENT
BRT corpus integration| BROKEN
BRT workflow binding| BROKEN
NC-02 mutation| DEAD / REPLACE
C4| BLOCKED

---

13. Research principle

AQARION does not ask the repository to make a claim appear true.

It asks the repository to make the claim survive attempts to make it false.

The intended progression is:

[
\boxed{
\text{interesting}
\rightarrow
\text{precise}
\rightarrow
\text{computable}
\rightarrow
\text{attackable}
\rightarrow
\text{reproducible}
\rightarrow
\text{formally checkable}
\rightarrow
\text{appropriately classified}.
}
]

No promotion is implied by this checkpoint.

---

AQ-PB-CORE-004 — Stable Equivalence/Core Congruence Classification

Date: October 3, 2026

Status

PROVED

Computational audit: PASS for every finite map on sets of size n\le5.

Exhaustive maps checked:

[
1+4+27+256+3125=3413.
]

No counterexample found.

The mathematical classification is proved independently of the computation.

Definitions

Let T:X\to X be a map on a finite set.

Let

[
P=\operatorname{Per}(T)
]

be the eventual periodic set. Choose h\ge0 such that

[
T^h(X)=P.
]

Then T|_P is a permutation.

For an equivalence relation E on X, define

[
T^*E=T^{-1}(E)

{(x,y):T(x)\mathrel E T(y)}.
]

Define

[
\operatorname{Stab}(T)

{E\in\operatorname{Eq}(X):T^*E=E}.
]

Define

[
\operatorname{Con}(P,T|_P)

{F\in\operatorname{Eq}(P):
xFy\Rightarrow T(x)F T(y)}.
]

Theorem

Restriction to the eventual periodic core induces an order-lattice isomorphism

[
\boxed{
\rho:\operatorname{Stab}(T)
\overset{\cong}{\longrightarrow}
\operatorname{Con}(P,T|_P)
}
]

given by

[
\rho(E)=E|_P.
]

Its inverse is

[
\boxed{
\operatorname{Ext}(F)

{(x,y):
T^h(x)\mathrel F T^h(y)}.
}
]

The extension is independent of the chosen sufficiently large h.

Proof

For F\in\operatorname{Con}(P,T|_P), invariance under the permutation T|_P gives

[
uFv
\iff
T(u)F T(v)
]

for all u,v\in P.

Hence the relation

[
x\operatorname{Ext}(F)y
\iff
T^h(x)F T^h(y)
]

is independent of increasing h, is an equivalence relation, and satisfies

[
T^*\operatorname{Ext}(F)=\operatorname{Ext}(F).
]

Its restriction to P is F.

Conversely, if E\in\operatorname{Stab}(T), then

[
E=T^*E,
]

so

[
xEy
\iff
T(x)E T(y).
]

Iterating,

[
xEy
\iff
T^h(x)E T^h(y).
]

Since T^h(X)=P,

[
E=\operatorname{Ext}(E|_P).
]

Thus restriction and extension are inverse bijections.

Both preserve refinement order. Therefore they form an order isomorphism and consequently preserve meet and join.

Exhaustive computational audit

For every map T:X\to X with 1\le |X|\le5, all equivalence relations were enumerated.

Aggregate counts:

n| maps| stable equivalences| core congruences
1| 1| 1| 1
2| 4| 6| 6
3| 27| 51| 51
4| 256| 592| 592
5| 3125| 8565| 8565

The restriction map was tested for both surjectivity and injectivity for every map. No failure occurred.

Evidence classification

[T] The classification theorem follows directly from the finite eventual-core property and the equality T^*E=E.

[C2] Exhaustive computational confirmation for all maps through n=5.

The computation is corroboration, not the proof.

Scope restriction

The theorem is established only for finite deterministic maps.

It does not establish any analogous result for arbitrary infinite dynamical systems.

It also does not imply the false pullback-distributivity identity

[
T^{-1}(E\vee F)

T^{-1}(E)\vee T^{-1}(F).
]

That separate statement remains REFUTED.

Research consequence

The transient portion of a finite deterministic system introduces no independent freedom into a pullback-fixed equivalence relation.

The complete lattice of such relations is determined by the congruence lattice of the eventual permutation core.
