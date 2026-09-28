
AQARION-TOOLS

Its purpose is not to absorb every research project. It is the reusable infrastructure layer:

AQARION-TOOLS
├── ClaimLock
├── ProofGym
├── JOIN-STABILITY
├── Replay
├── verification utilities
├── evidence schemas
├── research skills
├── CLI/package tooling
└── shared provenance/reproducibility infrastructure

That gives you a clean distinction:

RESEARCH REPOS
    mathematics / experiments / papers

AQARION-TOOLS
    reusable infrastructure

ProofGym
    public mathematical application

Hugging Face / Replit
    executable public surfaces

Facebook
    dissemination

And importantly, don't fork more things into the new personal repo just to populate it. Make it an original repository with its own history.

Here is the transition README I would use as the starting point.

AQARION-TOOLS

AQARION reusable research, verification, provenance, and reproducibility infrastructure

«Prove First · Verify Exhaustively · Predict Second · No Free Parameters»

AQARION-TOOLS is the tooling layer of the AQARION research ecosystem.

It exists to turn mathematical research into repeatable, inspectable, machine-checkable workflows without confusing computation, proof, conjecture, publication, or public visibility.

This repository is an original continuation repository under the "quantarion369-arch" account. It is intentionally separate from the mathematical research repositories and from historical fork lineage.

---

Why This Repository Exists

AQARION has accumulated several independent infrastructure components:

- ClaimLock
- ProofGym
- JOIN-STABILITY verification
- replay and reproducibility tooling
- evidence/claim ledgers
- verification scripts
- research skills
- provenance utilities
- executable research workflows

These tools should no longer be scattered across unrelated research repositories.

"AQARION-TOOLS" provides one maintained home for reusable infrastructure while preserving the original research repositories as their own mathematical records.

---

Architecture

                         AQARION
                            │
          ┌─────────────────┴─────────────────┐
          │                                   │
     RESEARCH LAYER                       TOOLING LAYER
          │                                   │
   Mathematical claims                  AQARION-TOOLS
   FDS research                         │
   Kaprekar research                    ├── ClaimLock
   J30 research                         ├── ProofGym
   other research                       ├── JOIN-STABILITY
          │                             ├── Replay
          │                             ├── Verification
          │                             ├── Evidence
          │                             └── Skills
          │
          └───────────────┬───────────────────┘
                          │
                    Reproducibility
                          │
                  Git + CI + Receipts
                          │
             ┌────────────┴────────────┐
             │                         │
       Public Applications       Research Objects
       Replit / HF               RO-Crate / archives

---

Evidence Discipline

AQARION-TOOLS follows the AQARION evidence taxonomy.

Code| Meaning
"[D]"| Definition
"[P]"| Mathematical proof
"[V]"| Exhaustive computational verification
"[PV]"| Proof + verification
"[C]"| Conjecture
"[R]"| Research / investigation
"KILLED"| Refuted or disproved
"QUARANTINED"| Preserved but not currently promotable

Evidence does not migrate upward automatically.

In particular:

numerical agreement ≠ proof
computation ≠ theorem
candidate ≠ certified
public visibility ≠ certification
AI assistance ≠ mathematical authorship

Certification requires an auditable evidence chain.

---

Core Components

ClaimLock

ClaimLock provides machine-readable claim/evidence locking and provenance controls.

Its purpose is to prevent research status from silently becoming stronger than the underlying evidence.

Target workflow:

claim
  ↓
evidence classification
  ↓
verification/proof artifact
  ↓
reproducibility receipt
  ↓
promotion decision

---

ProofGym

ProofGym is the interactive mathematical verification surface.

Current primary challenge:

JOIN-001

Pullback-Stable Equivalence Relations Are Closed Under Join on Finite Sets

ProofGym is designed to expose the actual mathematical computation rather than simulate a proof environment.

It should distinguish:

[P] mathematical proof
[V] computational verification
[PV] combined evidence

The application must never manufacture a certification result merely because a computation succeeds.

---

JOIN-STABILITY

JOIN-STABILITY is the dedicated research lane for the theorem:

[
T^{-1}(E)\le E,\qquad
T^{-1}(F)\le F
]

on a finite set X, with target:

[
T^{-1}(E\vee F)\le E\vee F.
]

Current proof architecture includes:

JS-00  Definitions
JS-01  Quotient map
JS-02  Kernel refinement
JS-03  Finite kernel equality
JS-04  x E y ↔ Tx E Ty
JS-05  Quotient permutation
JS-06  F quotient permutation
JS-07  Join-chain characterization
JS-08  Chain lifting

The finite-cardinality step is structural and must be proved explicitly.

Computational searches are corroboration, not substitutes for the theorem proof.

The infinite case is treated separately because finiteness is expected to be essential.

---

Replay

Replay provides deterministic reproduction of computational research.

Target chain:

Question
   ↓
Conjecture
   ↓
Counterexample?
   ↓
Correction
   ↓
Computation
   ↓
Proof
   ↓
Verification
   ↓
Hash
   ↓
Receipt

A replayable result should identify:

- source state
- inputs
- algorithm
- parameters
- execution
- output
- verification status
- hashes
- environment where relevant

---

Skills

Reusable AQARION research skills belong here when they are:

- deterministic
- documented
- independently executable
- useful across multiple research repositories

Skills should not become undocumented prompt collections.

Each reusable skill should define:

purpose
inputs
outputs
dependencies
execution
verification
failure conditions
evidence status

---

Repository Boundary

This repository is not the canonical home for every AQARION mathematical result.

Research belongs in research repositories.

Reusable infrastructure belongs here.

Examples:

AQARION mathematical repository
    → theorem / experiment / dataset / paper

AQARION-TOOLS
    → reusable verifier / replay / provenance / tooling

ProofGym
    → interactive application

Hugging Face / Replit
    → deployed public execution surface

This separation prevents infrastructure from obscuring mathematical provenance.

---

Public Continuity

AQARION is transitioning from an earlier GitHub account lineage into the "quantarion369-arch" namespace.

The transition preserves historical provenance.

Forked repositories remain visibly forked where appropriate.

This repository is different:

"AQARION-TOOLS" is an original repository.

It is the clean tooling foundation for the next phase rather than a copied replacement for historical repositories.

Historical repositories remain valuable as provenance and are not rewritten merely to make the transition appear cleaner.

---

Repositories

Research

- AQARION / Quantarion finite dynamical systems
- Kaprekar spectral geometry
- JOIN-STABILITY research
- J30 / Universal Closure research
- other specialized mathematical projects

Tooling

- "AQARION-TOOLS"

Applications

- AQARION ProofGym

Research objects

- RO-Crate / provenance infrastructure

Public execution

- Replit
- Hugging Face Spaces

Dissemination

- public social channels

The source repository and its verification artifacts remain authoritative over screenshots, posts, and deployed interfaces.

---

Development Standard

Every new tool should answer:

1. What problem does it solve?
2. What is its exact input/output contract?
3. Is the computation deterministic?
4. How is it tested?
5. How is it reproduced?
6. What evidence does it produce?
7. What can make its result invalid?
8. Where is its source?
9. Where is its verification?
10. What is explicitly not certified?

No tool should receive a stronger status merely because it has a polished interface.

---

Initial Build Order

The transition is intentionally staged.

PHASE 1
AQARION-TOOLS repository
README
LICENSE
repository policy
basic package structure
CI

PHASE 2
ClaimLock
Replay
shared evidence/provenance schemas

PHASE 3
JOIN-STABILITY
finite verifier
proof dependency graph
adversarial fixtures
verification receipts

PHASE 4
ProofGym
connect application to the reusable tooling layer

PHASE 5
shared CLI/package interfaces
reusable research skills

PHASE 6
RO-Crate/export/reproducibility integration

The goal is not to maximize repository count.

The goal is to make each tool reusable across AQARION research.

---

Quality Gate

Before a tool is treated as stable:

source exists
tests exist
failure cases exist
reproduction exists
documentation exists
evidence status exists
CI executes
no hidden computation
no hard-coded PASS

For mathematical claims:

[D] → [P] → [V] → [PV]

is not an automatic promotion pipeline.

Each evidence transition requires its own justification.

---

Current Transition Status

JASKSG9 historical lineage       PRESERVED
quantarion369-arch namespace     ACTIVE
forked research repositories     PRESERVED
original tooling repository      NEXT
ProofGym                         IMPLEMENTED
JOIN-STABILITY                   ACTIVE RESEARCH
ClaimLock                        CORE TOOL
Replay                           CORE TOOL
Skills                           CORE TOOLING
CI                               REQUIRED
Reproducibility                  REQUIRED

---

Governing Principle

AQARION-TOOLS exists to make research easier to audit, not easier to make claims.

«Ideas may come from anywhere. Confidence comes from verification.»

And:

«Prove First · Verify Exhaustively · Predict Second · No Free Parameters.»

---
