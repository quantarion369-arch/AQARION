AQARION — Evidence-First Research Intelligence

5 October 2026

""C3" (https://img.shields.io/badge/C3-OPEN-yellow)"
""C4" (https://img.shields.io/badge/C4-BLOCKED-red)"
""Lean" (https://img.shields.io/badge/Lean-OPEN-lightgrey)"
""SDS-002" (https://img.shields.io/badge/SDS--002-QUARANTINED-orange)"
""Publication" (https://img.shields.io/badge/publication-BLOCKED-red)"
""Promotable" (https://img.shields.io/badge/promotable-false-lightgrey)"

AQARION is an evidence-first research and verification corpus for finite dynamical systems, invariant quotients, operator defects, permutation/block-structure mathematics, and formalizable computational mathematics.

The repository is governed as an auditable research record, not as an oracle of mathematical truth.

Its central rule is:

[
\boxed{
\text{Do not promote a result beyond what its evidence establishes.}
}
]

A result may execute successfully and still test the wrong claim.

A result may reproduce successfully and still use the wrong specification.

A result may have a matching hash and still have incorrect provenance.

A formal proof may compile and still prove a proposition different from the intended research claim.

Therefore AQARION keeps the following layers separate:

[
\boxed{
\text{specification}
\neq
\text{execution}
\neq
\text{inference}
\neq
\text{formal proof}
\neq
\text{provenance}
}
]

---

Research Standard

Every significant research claim should answer:

- What exactly is being claimed?
- Which definitions are frozen?
- Which conventions are frozen?
- What source artifact defines the claim?
- What implementation was actually executed?
- What domain was actually tested?
- Was the computation independently reconstructed?
- Is the second route genuinely independent?
- Were negative controls used?
- Were known mutations detected?
- What remains unproved?
- What remains open?
- What is blocked from promotion?
- What provenance connects the claim to the evidence?

AQARION preserves corrections, failed approaches, counterexamples, incomplete formalizations, and superseded claims because those records explain how the present result was established.

A killed claim is not erased.

A failed computation is not hidden.

An open proof obligation is not converted into a theorem by repetition.

---

Evidence Vocabulary

AQARION uses explicit evidence classes.

Label| Meaning
"[D]"| DEFINED
"[V]"| VERIFIED COMPUTATION
"[P]"| PROVED
"[PV]"| PROVED + VERIFIED
"[C]"| CONJECTURE
"[R]"| RESEARCH
"[F]"| REFUTED / KILLED
"[Q]"| QUARANTINED

These labels are not interchangeable.

In particular:

computed              ≠ verified
verified              ≠ proved
finite exhaustive     ≠ universal theorem
different programs    ≠ automatic independence
public artifact       ≠ certification
policy PASS           ≠ mathematical truth
Lean source           ≠ Lean proof
matching output       ≠ provenance equivalence
repository existence  ≠ reproduction

The strongest permissible statement is determined by the actual evidence available.

---

Governance State

Layer| Current state
C3| OPEN
C4| BLOCKED
Lean| OPEN
SDS-002| QUARANTINED
Publication| BLOCKED
Promotion| BLOCKED
Promotable| false

These states are governance states.

They are not mathematical conclusions.

Adding a computation, receipt, repository file, or policy check does not automatically change them.

---

Provenance Principle

AQARION distinguishes the following objects:

CLAIM
SPECIFICATION
SOURCE
IMPLEMENTATION
FIXTURE
EXECUTION
OUTPUT
COMPARISON
INDEPENDENCE
FORMAL STATUS
DRIFT

A valid reproduction requires an explicit relationship between the claim, specification, implementation, execution, and output.

An independent reproduction requires an independently justified basis.

A second script that repeats the same semantic construction is not automatically independent.

A copied file is not an independent implementation.

A matching result is not proof of equivalence between sources.

A repository path is not evidence that the claimed artifact was actually executed.

---

Verification Boundary

The current research verification surface is organized under:

AQARION-QUANTARION-AI/
└── verification/

This is the current canonical research-side verification namespace.

Research verification artifacts must be referenced by their actual live paths.

Documentation must not invent a second filesystem hierarchy merely because an older README described one.

The repository therefore does not currently treat the historical top-level paths

verification/manifest.json
verification/run-all.py
verification/replay-harness.py
verification/provenance.py
verification/repo_self_audit.py

as a live canonical verification boundary.

Their absence is not silently converted into PASS.

---

Verification-Boundary Migration

Earlier repository documentation described a top-level verification system under:

verification/

with a manifest, runner, replay harness, provenance tooling, mutation suite, and additional verification packages.

The live research corpus subsequently developed its verification surface under:

AQARION-QUANTARION-AI/verification/

The older documentation is therefore treated as historical repository-boundary documentation, not as a declaration that those paths currently exist.

This distinction is intentional.

AQARION does not restore obsolete infrastructure merely to make a historical README appear internally consistent.

The current rule is:

[
\boxed{
\text{live filesystem} >
\text{stale path description}
}
]

when determining whether an executable artifact presently exists.

Historical documentation may remain relevant for provenance, but it must not be cited as current execution evidence unless the corresponding artifact is recoverable and its revision is established.

---

FPR Research Line

The invariant-partition enumeration work is currently represented by:

AQARION-QUANTARION-AI/
└── verification/
    └── FPR/
        └── fpr_enumerator.py

The principal artifact is:

AQ-FPR-006
Invariant Partition Enumerator under a Permutation

The formula implemented is

[
W(B)

\sum_{d\mid\gcd(c_i:i\in B)}
d^{|B|-1},
]

and

[
N(\lambda)

\sum_{\pi\in\Pi([r])}
\prod_{B\in\pi}W(B).
]

Here the c_i are the cycle lengths of the permutation and B is a block of the partition of the cycle index set.

The mathematical derivation and the computational implementation must remain separate evidence objects.

The executable implementation also contains a direct invariant-partition enumeration route used as a computational oracle.

That route provides useful independent algorithmic corroboration.

It does not by itself establish external independent reproduction.

---

FPR Evidence Status

Current safe ledger:

AQ-FPR-006

Claim
-----
Invariant-partition count for a finite permutation cycle type.

Formula
-------
N(λ)
=
Σ_{π ∈ Π([r])}
  Π_{B ∈ π}
    Σ_{d | gcd(c_i : i ∈ B)}
      d^(|B|-1)

Mathematical status
-------------------
Analytically derived / proof candidate.

Computational route
-------------------
Formula evaluation.

Computational oracle
--------------------
Direct invariant-partition enumeration.

Finite support
--------------
Cycle types n ≤ 7.

Independence
------------
Independent computational route within the artifact:
YES.

External independent reproduction
----------------------------------
NOT ESTABLISHED.

Literature priority
-------------------
OPEN.

Lean
----
OPEN.

C4
--
BLOCKED.

Publication
-----------
BLOCKED.

Promotion
---------
BLOCKED.

The executable artifact must not print or be documented as having stronger evidence than this ledger supports.

---

FPR Direct Enumeration

The FPR implementation uses two conceptually different routes.

Formula route

The formula computes

[
N(\lambda)

\sum_{\pi}
\prod_{B\in\pi}
\left(
\sum_{d\mid g_B}d^{|B|-1}
\right).
]

Direct enumeration route

The oracle constructs a canonical permutation of the specified cycle type and enumerates set partitions using restricted-growth-string representation.

A partition is counted exactly when its blocks are mapped to blocks by the permutation.

Thus the computational comparison is:

[
\boxed{
N_{\mathrm{formula}}(\lambda)

N_{\mathrm{direct}}(\lambda)
}
]

over the declared finite domain.

This is computational evidence.

It is not a substitute for the mathematical derivation.

---

FPR Two-Power Family

For the cycle type consisting of m cycles of length 2,

[
W_j=1+2^{j-1}.
]

The corresponding exponential generating function is

[
\boxed{
\sum_{m\ge0}N_m\frac{z^m}{m!}

\exp\left(
e^z+\frac12e^{2z}-\frac32
\right).
}
]

The initial values are

[
\boxed{
N_0=1,\quad
N_1=2,\quad
N_2=7,\quad
N_3=31,\quad
N_4=164,\quad
N_5=999,\quad
N_6=6841.
}
]

The earlier sequence

[
1,1,3,10,53,\ldots
]

is not the correct sequence for this family.

That discrepancy is retained as a correction in the research record.

---

PB Cycle-Orbit Classification

The broader permutation/block line contains the cycle-orbit classification artifact:

AQARION-QUANTARION-AI/
└── verification/
    └── PB/
        └── PB-CORE/
            └── PB-CORE-005_CYCLE_ORBIT_CLASSIFICATION.md

The classification uses the same structural formula:

[
N(m_1,\ldots,m_s)

\sum_{\pi\in\Pi([s])}
\prod_{B\in\pi}
\left(
\sum_{d\mid g_B}
d^{|B|-1}
\right),
]

where

[
g_B=\gcd{m_i:i\in B}.
]

The phase interpretation is:

- choose a partition of the participating cycles;
- choose a common quotient cycle length d;
- require d\mid g_B;
- choose phase labels in (\mathbb Z/d\mathbb Z)^{|B|};
- quotient by the common diagonal phase;
- obtain d^{|B|-1} phase choices.

This gives the weighted Bell-type assembly formula.

---

PB Corrections

The PB research record explicitly preserves corrected values.

In particular:

[
N(3,3)=8,
]

not 10, and

[
N(2,4)=9,
]

not 7.

Additional corrected finite values include:

[
N(1,1,2)=7,
]

[
N(1,1,3)=7,
]

[
N(1,2,2)=12,
]

[
N(1,2,3)=10.
]

These corrections are part of the audit trail.

They are not to be silently removed from historical records.

---

PB Sanity Anchors

For a single cycle,

[
N(m)=\tau(m).
]

For the identity permutation on r points,

[
N(1^r)=B_r,
]

where B_r is the r-th Bell number.

For two cycles,

[
N(m,n)

\tau(m)\tau(n)
+
\sigma(\gcd(m,n)),
]

where

[
\sigma(k)=\sum_{d\mid k}d.
]

These provide useful low-dimensional sanity checks for the general formula.

---

FPR and PB Relationship

AQ-FPR-006 should not be treated as an isolated enumeration script.

Its formula is structurally connected to the PB cycle-orbit classification:

finite permutation
       │
       ▼
cycle decomposition
       │
       ▼
cycle-index partition
       │
       ▼
common quotient modulus
       │
       ▼
phase degrees of freedom
       │
       ▼
weighted Bell assembly
       │
       ▼
invariant-partition count

This relationship is evidence of mathematical coherence between the research artifacts.

It is not, by itself, proof that every surrounding conjecture in the PB program is established.

---

Defect and Quotient Research

AQARION also studies finite deterministic dynamical systems through invariant partitions, quotient maps, and operator defects.

A central operator object is

[
D_\Pi=(I-\Pi)K\Pi,
]

where \Pi is the orthogonal projection onto a partition-constant observable space and K is the Koopman pullback operator under the declared convention.

The defect measures failure of the projected observable space to be invariant:

[
D_\Pi=0
\quad\Longleftrightarrow\quad
K(V_\Pi)\subseteq V_\Pi.
]

This operator work must remain definition-sensitive.

A computation under one convention does not establish equivalence to another convention unless the source definitions have been recovered and compared.

---

D22 Provenance Firewall

The D22 research line is deliberately separated into two claims:

locked operator model
        │
        ├── direct algebra
        ├── exact computation
        └── operator consequences

and

canonical D22 source
        │
        └── source-equivalence question

The first can be mathematically analyzed under its explicit convention.

The second remains a provenance question.

The locked convention is:

[
Ke_j=e_{j-1},
]

[
u_d=e_0-e_d,
]

[
P_d=I-\frac12u_du_d^T,
]

[
Q_d=\frac12u_du_d^T,
]

[
D_d=Q_dKP_d.
]

Under this explicit model,

[
D_d=\frac12u_da_d^T,
]

with

[
a_d^T=u_d^TKP_d.
]

Because

[
P_du_d=0,
]

one obtains

[
D_d^2=0.
]

The resulting Jordan and singular-value consequences are properties of this locked model.

They do not establish equivalence with an unavailable canonical source.

---

General Audit Principle

AQARION treats the following as distinct failure modes.

Specification failure

The program correctly executes a claim that was specified incorrectly.

Implementation failure

The specification is correct but the implementation is wrong.

Execution failure

The implementation is correct but the intended computation did not actually run.

Comparison failure

The computation ran, but the output was compared against an inappropriate oracle.

Independence failure

Two implementations agree because they share the same semantic or implementation error.

Provenance failure

The artifact cannot be established as the claimed source or version.

Formalization failure

A mathematical argument exists, but the formal proof obligation has not been checked.

Promotion failure

The evidence exists but does not satisfy the policy required for a stronger status.

These failures must not be collapsed into one generic notion of “verification.”

---

Negative Controls

Negative controls are first-class research evidence.

A useful verification system should contain deliberately altered claims or implementations for which failure is expected.

Examples include:

wrong sign
wrong indexing convention
wrong cyclic orientation
wrong normalization
wrong quotient relation
wrong orbit depth
wrong phase constraint
wrong matrix projection
wrong boundary condition

A negative control that passes unexpectedly is itself an audit failure.

A negative control that fails as expected does not prove the positive claim.

It only demonstrates that the test is capable of detecting that particular mutation.

---

Independence Standard

AQARION distinguishes:

same function
    ↓
different implementation
    ↓
different algorithmic route
    ↓
independent reconstruction
    ↓
independent source
    ↓
formal proof

These are different evidence strengths.

For example, comparing the FPR closed formula against direct invariant-partition enumeration is stronger than calling the same formula twice.

It is still weaker than an independently developed implementation with separately established semantics.

The repository therefore avoids the phrase “independently reproduced” unless the evidence actually establishes the required independence.

---

Formalization Standard

Lean status is reported separately from mathematical status.

The following are not equivalent:

Lean file exists
Lean parses
Lean elaborates
Lean theorem compiles
Lean theorem corresponds to intended claim

A Lean artifact must not be called a proof merely because a ".lean" file exists.

Formal certification is promoted only after the relevant proposition and proof have actually been checked by the intended formal system.

Current Lean state:

OPEN

---

Computational Evidence Standard

A computation establishes evidence over the domain it actually executed.

For example,

[
\text{all cycle types }n\le7
]

means exactly that.

It does not mean:

[
\text{all finite permutations}.
]

Likewise,

[
\text{1176 cases}
]

would establish evidence over those 1176 cases only.

The phrase “verified” must therefore always be interpreted together with:

- the specification;
- the implementation;
- the domain;
- the execution;
- the oracle;
- the comparison;
- and the independence status.

---

Literature and Novelty

AQARION distinguishes mathematical correctness from research novelty.

A theorem can be correct and classical.

A formula can be correct and already known.

A computational implementation can be useful without being novel mathematics.

Conversely, a potentially novel formulation still requires prior-art investigation.

For the PB/FPR cycle-orbit formula, relevant mathematical territory includes:

- congruences of monounary algebras;
- invariant equivalence relations;
- permutation group actions;
- G-set congruence structures;
- block systems;
- functional-graph congruences;
- cycle decompositions.

The exact prior-art status of the closed weighted-Bell formula remains a research question.

Therefore:

correctness   = separate question
prior art     = separate question
novelty       = OPEN

No novelty claim is promoted without literature support.

---

Publication Gate

Publication is deliberately separated from computational verification.

Current state:

PUBLICATION = BLOCKED

A successful finite computation does not approve publication.

A Lean proof of one proposition does not certify an entire research program.

A policy gate does not establish mathematical truth.

Publication promotion requires its own evidence review.

---

C4 Gate

Current state:

C4 = BLOCKED

This is intentional.

The repository is designed to preserve uncertainty rather than conceal it.

C4 should move only when the required evidence conditions are actually satisfied.

Repeatedly executing the same computation does not automatically strengthen its logical status.

---

Repository Drift

Repository drift is itself an audit finding.

Examples include:

README path ≠ filesystem path
manifest ≠ executable filename
claim record ≠ implementation
source revision ≠ cited revision
receipt ≠ actual execution
workflow description ≠ executed workflow

AQARION treats such discrepancies as evidence-boundary defects.

A documentation correction is therefore not cosmetic.

It can change what a researcher is entitled to claim was actually verified.

---

Historical Records

Historical artifacts remain valuable.

AQARION does not delete a failed claim merely because it was corrected.

A historical record can document:

- the original hypothesis;
- the incorrect computation;
- the counterexample;
- the mutation;
- the correction;
- the revised specification;
- the resulting status change.

The objective is not to present a frictionless history.

The objective is to preserve an auditable one.

---

Current Research Direction

The high-value mathematical direction is the connection between invariant-partition structure and quotient/operator defect geometry.

For an invariant equivalence

[
E
]

one may associate structural data such as

[
E
\longleftrightarrow
\left(
\pi_E,
{d_B,\phi_B}_{B\in\pi_E}
\right).
]

Important questions include:

- How does refinement E\le F act on the cycle-index partition?
- How do phase systems transform under refinement?
- How are meets represented in phase coordinates?
- How are joins represented?
- What algebraic object controls the residual phase constraints?
- Can invariant-partition counts be expressed directly through quotient data?
- How does the cycle-orbit structure interact with the defect operator
  [
  D_\Pi=(I-\Pi)K\Pi?
  ]
- Can rank or defect invariants be characterized combinatorially?
- Which statements admit Lean certification?

These questions are research targets, not promoted theorems unless separately certified.

---

AQARION Research Workflow

The preferred workflow is:

claim
  ↓
freeze specification
  ↓
identify conventions
  ↓
locate primary source
  ↓
implement
  ↓
construct oracle
  ↓
construct negative control
  ↓
execute
  ↓
compare
  ↓
attempt independent reconstruction
  ↓
audit provenance
  ↓
formalize
  ↓
review prior art
  ↓
assign evidence status
  ↓
promotion decision

The workflow is deliberately conservative.

The purpose is not to maximize the number of green checks.

The purpose is to maximize the reliability of the strongest statement that can honestly be made.

---

What a Passing Run Means

A passing run means:

the executed program passed the executed checks
under the executed specification
over the executed domain
at the executed repository revision.

It does not automatically mean:

the theorem is true
the implementation is correct
the specification is correct
the source is canonical
the result is novel
the result is independently reproduced
the result is formally proved
the research program is publication-ready

Those are separate questions.

---

What AQARION Refuses to Do

AQARION does not intentionally:

- convert finite computation into universal proof;
- convert repeated computation into independence;
- convert policy approval into mathematical truth;
- convert repository presence into reproduction;
- convert a source filename into source equivalence;
- convert a Lean file into a Lean proof;
- convert deterministic serialization into RFC compliance without evidence;
- convert a corrected result into a historical deletion;
- convert an open problem into a theorem;
- silently replace canonical terminology;
- fabricate receipts;
- fabricate execution counts;
- fabricate hashes;
- fabricate source provenance;
- promote a claim because it appears repeatedly in documentation.

---

Evidence-First Interpretation Rule

The strongest permissible statement about a research result is the intersection of what its specification, execution, comparison, provenance, and formal evidence actually establish.

A useful hierarchy is:

[
\boxed{
\text{CLAIMED}
\rightarrow
\text{AVAILABLE}
\rightarrow
\text{EXECUTED}
\rightarrow
\text{REPRODUCED}
\rightarrow
\text{INDEPENDENTLY REPRODUCED}
\rightarrow
\text{FORMALIZED}
\rightarrow
\text{PROVED}
}
]

Movement upward requires new evidence.

Repetition is not automatically new evidence.

---

Current Audit Position

AQARION is presently maintained under:

FROZEN AUDIT
NO FABRICATION
NO PROMOTION
C4 BLOCKED
PUBLICATION BLOCKED
LEAN OPEN

The current repository contains substantial mathematical and computational research artifacts.

It also contains intentionally unresolved provenance, formalization, literature-priority, and verification-boundary questions.

Those unresolved questions are part of the research record.

---

Final Principle

A result can run, reproduce, and still test the wrong claim.

A result can be formally checked and still formalize the wrong proposition.

A repository can be internally consistent and still point to the wrong source.

A computation can be exact and still answer the wrong question.

Therefore:

[
\boxed{
\text{specification}
\neq
\text{execution}
\neq
\text{inference}
\neq
\text{formal proof}
\neq
\text{provenance}
}
]

And the governing rule remains:

[
\boxed{
\text{Do not promote a result beyond what its evidence establishes.}
}
]

AQARION — Evidence-First Research Intelligence
