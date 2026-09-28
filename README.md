AQARION

Auditable Mathematical Research Infrastructure

AQARION is a research program for exact finite mathematics, dynamical systems, operator methods, computational verification, and reproducible mathematical software.

Its central objective is simple:

«Prove First · Verify Exhaustively · Predict Second · No Free Parameters»

AQARION treats mathematical claims as evidence-bearing objects. Definitions, proofs, exhaustive computation, formal verification, conjectures, refutations, and research observations are kept explicitly separated so that computational agreement is never silently promoted to proof.

---

Research Principles

AQARION is built around five principles:

- Proof before promotion — a computational observation is not a theorem.
- Exactness over approximation — finite objects are represented and tested exactly whenever possible.
- Independent verification — proofs and computational checks are separate evidence lanes.
- Reproducibility by construction — experiments should be rerunnable from documented inputs and procedures.
- Provenance without mythology — AI assistance may be part of the research process, but certification concerns the mathematical artifact and its verification, not claims about authorship by inference.

Evidence classes

Code| Meaning
"[D]"| Definition
"[P]"| Mathematical proof
"[V]"| Exhaustive or independently reproducible verification
"[PV]"| Proof + verification
"[C]"| Conjecture
"[R]"| Research / exploratory result
"KILLED"| Refuted or invalidated claim
"QUARANTINED"| Evidence retained but not currently promoted

Evidence does not migrate upward automatically.

A numerical match does not become a proof.
A successful search does not become certification.
A formalization containing "sorry"/"admit" does not become a completed formal proof.
A public repository does not, by itself, constitute mathematical certification.

---

What AQARION Studies

AQARION develops reusable methods around finite dynamical systems and their induced operators.

A recurring construction is

[
D_\Pi=(I-P_\Pi)KP_\Pi,
]

where:

- T:X\to X is a finite dynamical system,
- K is the Koopman pullback operator,
- \Pi is a partition of X,
- P_\Pi projects onto block-constant observables,
- D_\Pi measures the failure of the partition to be closed under the dynamics.

This framework connects:

finite dynamics → quotient structure → operator theory → graph structure → exact computation → formal verification.

---

Core Results

The current AQARION core includes exact results concerning the defect operator and partition closure.

Among the established results are:

- D_\Pi=0 exactly when the partition is dynamically closed.
- D_\Pi=0 exactly when the corresponding quotient dynamics is well-defined.
- D_\Pi^2=0 for every idempotent projection P_\Pi.
- PK=KP is sufficient for D_\Pi=0, but is not necessary.
- Exact rank formulas connect the defect operator with a complement graph.
- An exact Frobenius-energy identity provides a quantitative defect measure.
- Large finite censuses have been used as independent verification of these identities.

Formalization status is tracked separately from computational verification; incomplete formal files are never presented as completed certification.

---

Research Programs

JOIN-STABILITY

A finite-set theorem program studying pullback-stable equivalence relations and their joins.

Current work includes:

- finite kernel-equality arguments;
- quotient-map injectivity and permutation structure;
- incidence-graph formulations;
- chain-lifting proofs;
- adversarial counterexample search;
- exhaustive finite verification;
- formalization planning.

The finite theorem and its verification are maintained as separate evidence lanes until the formalization and independent review requirements are satisfied.

ProofGym

ProofGym is the executable verification surface for mathematical claims.

It is designed to make a mathematical statement inspectable through:

- exact finite instances;
- structured witnesses;
- deterministic verification;
- adversarial fixtures;
- proof dependencies;
- evidence traces;
- reproducible verification receipts.

The goal is not to replace mathematical proof with software. The goal is to make computational evidence auditable.

ClaimLock

ClaimLock is intended as the claim/provenance layer for AQARION.

It provides a structured way to associate claims with:

- evidence status;
- proof artifacts;
- verification artifacts;
- hashes;
- dependencies;
- reproduction instructions;
- invalidation history.

Replay

Replay infrastructure records enough information to rerun computational research rather than merely displaying its final result.

The intended chain is:

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

---

Tools

Reusable infrastructure is being consolidated under:

AQARION-QUANTARION-AI/
└── TOOLS/

The tools layer is intended to contain reusable components rather than duplicate individual research repositories.

Planned infrastructure includes:

TOOLS/
├── ClaimLock/
├── ProofGym/
├── JOIN-STABILITY/
├── Replay/
├── verification/
├── provenance/
├── schemas/
├── skills/
└── cli/

The boundary is deliberate:

research repositories contain mathematical investigations;
TOOLS contains reusable infrastructure.

---

Reproducibility

AQARION treats reproducibility as an engineering requirement rather than a publication slogan.

Where applicable, research artifacts are designed around:

- deterministic computation;
- exact finite enumeration;
- independent verification;
- machine-readable claim registries;
- verification reports;
- SHA-256 manifests;
- Lean formalization;
- Dockerized environments;
- CI checks;
- RO-Crate metadata;
- research ledgers;
- explicit evidence status.

A target artifact should allow an independent researcher to answer:

1. What exactly is being claimed?
2. What definitions does the claim depend on?
3. What constitutes proof?
4. What was computationally verified?
5. What remains conjectural?
6. Can the verification be rerun?
7. Which exact files produced the result?
8. Which version/hash was evaluated?

---

AI and Research Provenance

AQARION does not attempt to infer whether a mathematical result was “really produced by AI” from the final artifact.

That is not a reliable certification problem.

Instead, AQARION records AI assistance as part of the research process when such provenance is available.

The relevant question is:

«Can the mathematical claim, computation, proof, and verification be independently inspected and reproduced?»

AI systems are therefore treated as research-process nodes rather than as mathematical authorities.

An AI-generated conjecture remains a conjecture.

An AI-generated proof must still be checked.

An AI-generated computation must still be reproducible.

A failed proof remains failed.

A counterexample remains a counterexample.

---

Repository Architecture

AQARION is intentionally separated into layers.

AQARION
│
├── Research
│   ├── finite dynamical systems
│   ├── operator theory
│   ├── quotient structures
│   ├── graph methods
│   └── asymptotic investigations
│
├── Verification
│   ├── exact enumeration
│   ├── adversarial testing
│   ├── proof checking
│   └── reproducibility
│
├── Formalization
│   └── Lean / machine-checked mathematics
│
├── AQARION-QUANTARION-AI
│   └── TOOLS
│       ├── ClaimLock
│       ├── ProofGym
│       ├── Replay
│       ├── schemas
│       ├── skills
│       └── verification utilities
│
└── Provenance
    ├── research ledgers
    ├── manifests
    ├── hashes
    └── RO-Crate metadata

The structure is designed to prevent infrastructure, experiments, proofs, and historical research artifacts from becoming indistinguishable.

---

Certification Standard

AQARION uses a conservative promotion rule:

Observation
    ↓
Reproducible computation
    ↓
Independent verification
    ↓
Mathematical proof
    ↓
Formal verification where applicable
    ↓
Certified claim

Not every research result needs every stage immediately.

But no result is promoted beyond its actual evidence.

In particular:

SEARCH ≠ REPRODUCED
REPRODUCED ≠ MINIMAL
MINIMAL ≠ PROVED
PROVED ≠ FORMALLY VERIFIED
PUBLIC ≠ CERTIFIED

This distinction is part of the research infrastructure itself.

---

Development Standard

AQARION development follows a strict preference for small, inspectable artifacts.

New infrastructure should:

- have a defined input/output contract;
- include deterministic tests;
- preserve existing evidence;
- expose failures rather than hide them;
- avoid silently changing historical results;
- distinguish exploratory code from certification code;
- document dependencies;
- remain independently runnable where practical.

Historical research is preserved rather than rewritten to make the current state appear cleaner.

Corrections are recorded.

Killed claims remain identifiable.

Versioned artifacts remain traceable.

---

Current Direction

The immediate infrastructure direction is to establish a clean reusable spine for:

1. ClaimLock — claim and evidence management.
2. Replay — deterministic research reproduction.
3. JOIN-STABILITY — exact theorem verification and proof infrastructure.
4. ProofGym — executable mathematical verification.
5. Shared schemas — evidence, provenance, receipts, and claim registries.
6. Research skills — reusable workflows for rigorous computational mathematics.
7. CLI tooling — one consistent interface for verification and replay.
8. RO-Crate integration — machine-readable research packaging.

The objective is not to build an oversized framework before the mathematics requires it.

The objective is to extract reusable infrastructure from already-tested research workflows.

---

Research Philosophy

AQARION is intentionally skeptical of its own results.

A result becomes stronger by surviving:

- adversarial testing;
- independent reconstruction;
- exact enumeration;
- counterexample searches;
- proof review;
- formalization;
- reproducibility checks.

The system is therefore designed to preserve negative information as carefully as positive information.

A disproved conjecture is useful.

A failed proof is useful.

A detected implementation bug is useful.

A quarantined claim is useful.

They show where the boundary of current knowledge actually lies.

---

Guiding Principle

«Ideas may come from anywhere. Confidence comes from verification.»

AQARION exists to make that verification process explicit, reproducible, and auditable.

Prove First · Verify Exhaustively · Predict Second · No Free Parameters

---

Project Links

- AQARION: https://github.com/quantarion369-arch/AQARION
- TOOLS: https://github.com/quantarion369-arch/AQARION/tree/main/AQARION-QUANTARION-AI/TOOLS
- Quantarion-AI: https://github.com/quantarion369-arch
- Hugging Face: https://huggingface.co/Quantarion9

---

Status

AQARION is an active research and infrastructure project.

Individual results have different evidence levels. Consult the corresponding claim registry, research ledger, verification report, formalization status, and reproducibility artifacts before treating any individual result as certified.

Research status is claim-specific, not repository-wide.

https://github.com/quantarion369-arch/AQARION/https://github.com/quantarion369-arch/AQARION/tree/main/AQARION-QUANTARION-AI/TOOLS
