
**AQARION — Evidence-First Mathematical Research


THIS IS WHAT I HAVE SO FAR LETS CREATE ON WHOLE NICE README ITS MY MAIN 9NE PLEASE DOUBLE CHECK EVERYTHING

I found the main inconsistencies: your opening badges announce progress, but the old governance table and later sections still say “Lean OPEN” and “Publication BLOCKED.” The fetched main repository page also contains those older statements and labels `EVIDENCE-LEDGER.md` as pending even though that file appears in the repository listing.[1]

The replacement below removes those contradictions, repairs the mathematical notation, consolidates the repeated ecosystem material, and separates completed build progress from ongoing theorem work. I could retrieve the main repository page, but the Lean and FastAPI fetches failed; their checkpoint descriptions below rely on the terminal evidence and material you supplied—not a fresh audit of their source.

Replace your main README with the following. This is inline content only; nothing has been edited or pushed.

````markdown
# ✨ WELCOME TO AQARION ✨
### Evidence-First Mathematical Research

Finite dynamical systems · Quotient structure · Observable defects  
Exact computation · Lean formalization · Reproducible verification

[![Lean Build: PBCore006 PASS](https://img.shields.io/badge/Lean_Build-PBCore006_PASS-2ea44f?style=for-the-badge)](https://github.com/quantarion369-arch/AQARION-LEAN)
[![Build Evidence: Published](https://img.shields.io/badge/Build_Evidence-PUBLISHED-0969da?style=for-the-badge)](https://github.com/quantarion369-arch/AQARION-LEAN/blob/main/RECEIPTS/PBCore006-build-result-20261017.md)
[![AQARION Core: Active Development](https://img.shields.io/badge/AQARION_Core-ACTIVE_DEVELOPMENT-8250df?style=for-the-badge)](#current-checkpoint)
[![Publication: Open](https://img.shields.io/badge/Publication-OPEN-00897b?style=for-the-badge)](#publication-and-collaboration)
[![Verification: Claim-Specific](https://img.shields.io/badge/Verification-CLAIM--SPECIFIC-57606a?style=for-the-badge)](#evidence-and-claim-status)

AQARION is an independent mathematical research project maintained by
James A. It investigates finite dynamical systems, invariant partitions,
quotient structure, Koopman operators, observable subspaces, and exact
computational mathematics.

The project connects mathematical investigation with executable artifacts,
Lean formalization, software development, and inspectable evidence.

**PBCore006 has completed its Lean build successfully. Its actual console
log and successful-build receipt are published. AQARION Core remains
under active research and development.**

Publication is open for sharing research artifacts, receiving technical
feedback, independent reproduction, and collaboration. Verification
status remains specific to each claim and its supporting evidence.

> Do not promote a result beyond what its evidence establishes.

```text
                         AQARION
                Independent mathematical research
                             │
             ┌───────────────┼───────────────┐
             ▼               ▼               ▼
       Mathematical     Computational      Formal
       investigation    verification       development
             │               │               │
             └───────────────┼───────────────┘
                             ▼
                  Inspectable public evidence
```

---

## Contents

- [Start here](#start-here)
- [Current checkpoint](#current-checkpoint)
- [The AQARION ecosystem](#the-aqarion-ecosystem)
- [Research scope](#research-scope)
- [Central mathematical framework](#central-mathematical-framework)
- [Active research lines](#active-research-lines)
- [Lean build milestone](#lean-build-milestone)
- [Mobile-first research workflow](#mobile-first-research-workflow)
- [Evidence and claim status](#evidence-and-claim-status)
- [Verification and reproducibility](#verification-and-reproducibility)
- [Repository architecture](#repository-architecture)
- [AQARION-RAG](#aqarion-rag)
- [Formal verification](#formal-verification)
- [Corrections and historical provenance](#corrections-and-historical-provenance)
- [Publication and collaboration](#publication-and-collaboration)
- [Development and contribution standards](#development-and-contribution-standards)
- [Related resources](#related-resources)
- [Guiding principles](#guiding-principles)

---

## Start here

| Resource | Purpose |
|---|---|
| [Research overview](OVERVIEW.md) | Orientation to the research program |
| [Research presentation](RESEARCH-PROGRAM-PRESENTATION.md) | A broader presentation of AQARION |
| [Root checkpoint](CHECKPOINT.md) | Repository checkpoint record |
| [Evidence ledger](EVIDENCE-LEDGER.md) | Evidence records and stated limitations |
| [Master file tree](FILETREE.md) | File and directory navigation |
| [PB-001 research document](AQARION-QUANTARION-AI/PB_001.md) | Finite-quotient pullback rigidity and related research |
| [Tools architecture](AQARION-QUANTARION-AI/TOOLS/README.md) | Documented research-tooling architecture |
| [AQARION-RAG](AQARION-QUANTARION-AI/PACKAGES/AQARION-RAG/) | Retrieval and evidence-navigation package |
| [AQARION-LEAN](https://github.com/quantarion369-arch/AQARION-LEAN) | Lean projects, build records, and console evidence |
| [Aqarion-Fastapi](https://github.com/quantarion369-arch/Aqarion-Fastapi) | Python/FastAPI development |
| [Issues](https://github.com/quantarion369-arch/AQARION/issues) | Questions, corrections, reproducibility reports, and discussion |

A navigation link identifies an artifact or workspace. Its presence does
not imply that every statement in it has been proved, every planned
feature implemented, or every workflow recently executed.

Implementation details and result status should be read from the relevant
source, tests, receipts, and dated records.

---

## Current checkpoint

Checkpoint reference: October 18, 2026.

| Area | Current presentation |
|---|---|
| AQARION Core | Active research and development |
| PBCore006 Lean build | PASS — 785 reported jobs, build exit 0 |
| PBCore006 console evidence | Preserved and published |
| Successful-build receipt | Published |
| Lean publication check | All 11 specified artifact and synchronization checks passed at the recorded revision |
| API development | Maintained in the companion FastAPI repository |
| Public sharing and collaboration | Open |
| Mathematical verification | Claim-specific |
| Cross-repository automation | Development direction; not presented as complete |

### Completed infrastructure progress

The initial PBCore006 build obstacle is resolved. The project has a
recorded successful build and published execution evidence.

This is a completed milestone—not a standing build blocker.

It does not mean that every mathematical target is finished, every
stored Lean file is included in the same build, or every future revision
has already been checked.

### Current development direction

```text
COMPLETED FOUNDATION
────────────────────
Working mobile development environment
                 ↓
Required dependency compilation
                 ↓
Successful PBCore006 build
                 ↓
Preserved and published evidence


FORWARD DEVELOPMENT
───────────────────
Continue AQARION Core research
                 ↓
Map claims to exact artifacts and declarations
                 ↓
Extend focused tests and formalization
                 ↓
Specify cross-repository interfaces
                 ↓
Publish additional scoped checkpoints
```

The README does not impose a blanket C4, publication-blocked, or
promotable-false disposition on the entire program. Any claim-specific
gate must identify its actual requirements, evidence, and decision record.

---

## The AQARION ecosystem

AQARION’s work is organized across three complementary repositories.

```text
                              AQARION
                    Core research and evidence
                                 │
                  ┌──────────────┴──────────────┐
                  ▼                             ▼
            AQARION-LEAN                  Aqarion-Fastapi
          Formalization projects         Python API development
          Source and build records       Service implementation
          Receipts and console logs      Tests and tooling
                  │                             │
                  └──────────────┬──────────────┘
                                 ▼
                     Inspectable research artifacts
```

This diagram describes responsibilities, not a completed automated
integration.

| Repository | Role |
|---|---|
| AQARION | Mathematical research, computational artifacts, evidence organization, and historical records |
| [AQARION-LEAN](https://github.com/quantarion369-arch/AQARION-LEAN) | Lean formalization projects and recorded build evidence |
| [Aqarion-Fastapi](https://github.com/quantarion369-arch/Aqarion-Fastapi) | Python/FastAPI implementation, service interfaces, and supporting tests |

### AQARION Core

This repository remains the central research workspace.

Development includes mathematical definitions, derivations, exact finite
experiments, witnesses, counterexamples, verification tools, and the
documentation connecting them.

### AQARION-LEAN

The Lean repository provides a dedicated home for formalization projects,
project configurations, build receipts, and execution logs.

Its recorded checkpoints include AQFPR006, PB006Audit, and PBCore006.
Their individual scope should be read from their corresponding source
and evidence records.

### Aqarion-Fastapi

The FastAPI repository provides a separate workspace for application
behavior, computational routes, service interfaces, tests, and tooling.

Consult that repository’s README and execution records for implemented
endpoints and current limitations. This README does not assign a new API
test result, production-readiness status, or deployment claim.

---

## Research scope

### Finite dynamical systems

Deterministic maps, functional graphs, cycles, transient structure, finite
state spaces, and invariant partitions.

### Quotient structure

Equivalence relations, congruences, quotient maps, semiconjugacy,
pullback relations, and closure questions.

### Koopman operators and observable defects

Pullback operators, block-constant observable spaces, projections,
invariance, and the component measuring failure of exact observable
descent.

### Exact computational mathematics

Integer and rational arithmetic, finite enumeration, independent
algorithms, structured witnesses, counterexample search, and negative
controls.

### Formal verification

Lean definitions and theorem targets, project builds, declaration-level
inspection, proof dependencies, and explicit formalization obligations.

### Research provenance

Claim identities, source revisions, execution records, hashes,
reproduction instructions, corrections, and supersession history.

These areas are connected, but their evidence is not interchangeable.

---

## Central mathematical framework

Let \(X\) be a finite nonempty set, let \(T:X\to X\) be a deterministic
map, and let \(\Pi\) be a partition of \(X\).

Work in the real vector space \(\mathbb{R}^{X}\), equipped with the
counting inner product. Let \(V_{\Pi}\) be the subspace of functions
constant on each block of \(\Pi\), and let \(P_{\Pi}\) be the orthogonal
projection onto \(V_{\Pi}\).

Define the Koopman pullback operator by

\[
K_Tf=f\circ T.
\]

Define the observable defect by

\[
D_{\Pi}=(I-P_{\Pi})K_TP_{\Pi}.
\]

The defect extracts the component of the pulled-back block-constant
observables that lies outside the original block-constant subspace.

```text
Observable f
     │
     ▼
PΠ: project onto block-constant observables
     │
     ▼
KT: pull back along the dynamics
     │
     ├────────► PΠ component: remains inside VΠ
     │
     └────────► (I − PΠ) component: observable defect
```

### Exact observable descent

For these definitions,

\[
D_{\Pi}=0
\quad\Longleftrightarrow\quad
K_T(V_{\Pi})\subseteq V_{\Pi}.
\]

Indeed, \((I-P_{\Pi})\) annihilates exactly the vectors in
\(V_{\Pi}\), and \(P_{\Pi}\) acts as the identity on that subspace.

In this finite setting, the condition is also equivalent to forward
compatibility of the partition:

\[
x\sim_{\Pi}y
\quad\Longrightarrow\quad
T(x)\sim_{\Pi}T(y).
\]

If the partition is forward-compatible, pulling back a block-constant
function leaves it block-constant. Conversely, if \(T(x)\) and \(T(y)\)
lie in different blocks, the indicator of one of those blocks
distinguishes their pullback values.

This gives a precise foundation for quotient dynamics. It does not
automatically establish additional rank formulas, spectral identities,
refinement laws, or applications.

---

## Active research lines

### 1. Invariant-partition enumeration

Research into partitions preserved by finite permutations, including
cycle structure, phase relationships, weighted Bell-type formulas, and
direct enumeration.

AQ-FPR-006 is documented as a research line involving an analytical
formula and bounded computational cross-checks. Its mathematical scope,
independent reproduction, and literature relationship should be assessed
from the relevant artifacts rather than inferred from a project label.

### 2. Observable defects and quotient structure

Research into the relationship between invariant partitions,
block-constant subspaces, operator defects, and exact quotient descent.

Definitions, projection conventions, proposed identities, rank claims,
and computational checks are tracked separately. Counterexamples and
corrected statements remain part of the research record.

### 3. Finite-quotient pullback rigidity

The PB-001 research line considers a map \(T:X\to X\), an equivalence
relation \(E\), and the pullback relation

\[
T^{*}E
=
\{(x,y)\in X^{2}:T(x)\,E\,T(y)\}.
\]

A central research statement concerns the implication

\[
X/E\text{ finite},\qquad T^{*}E\subseteq E
\quad\Longrightarrow\quad
T^{*}E=E.
\]

Related work investigates binary join closure through finite quotient
permutations and incidence constructions.

Consult [PB-001](AQARION-QUANTARION-AI/PB_001.md) for the detailed
argument, hypotheses, evidence, and limitations. This overview does not
assign a new proof-review or formalization result to that document.

### 4. Formalization and evidence identity

Research infrastructure connects statements to their implementations,
execution records, and formal declarations.

The development direction includes:

- Exact statement and hypothesis identification.
- Source and claim versioning.
- Explicit build coverage.
- Focused tests and negative controls.
- Declaration-specific proof inspection.
- Evidence integrity and supersession records.
- Clear separation of completed results from proposed work.

---

## Lean build milestone

### PBCore006 — BUILD PASS

PBCore006 completed its configured Lean build in an Android/Termux
environment using Ubuntu through proot-distro on ARM64 hardware.

```text
=== RESUME 2026-10-17T22:15:00-04:00 ===

⚠ [784/785] Built PBCore006 (118s)

Build completed successfully (785 jobs).

LAKE_EXIT=0
LOG_EXIT=0
BUILD FINISHED SUCCESSFULLY
```

The warnings shown in the console were non-fatal.

The 118-second duration applies to the PBCore006 target, not the complete
dependency build. The 785-job total is not a theorem count.

### Preserved evidence

| Artifact | Location |
|---|---|
| Successful-build receipt | [PBCore006 build result](https://github.com/quantarion369-arch/AQARION-LEAN/blob/main/RECEIPTS/PBCore006-build-result-20261017.md) |
| Actual console log | [Published console evidence](https://github.com/quantarion369-arch/AQARION-LEAN/blob/main/RECEIPTS/PBCore006-20261017-console.log) |
| Build ledger | [STATUS.md](https://github.com/quantarion369-arch/AQARION-LEAN/blob/main/STATUS.md) |
| Consolidated record | [CHECKPOINT.md](https://github.com/quantarion369-arch/AQARION-LEAN/blob/main/CONSOLIDATED/CHECKPOINT.md) |

The device log was 30,496 bytes. The original and repository copy produced
matching SHA-256 checksums:

```text
0ef92b13e35a1785831ede359280b373f8f2dd9043f8e77afd43aa1616d824a1
```

The evidence publication was committed in `fdf8388`.

A subsequent check of fetched remote revision

```text
cfd22c61b2074a0af31d54bdd1b1780c22994878
```

confirmed all 11 specified publication checks:

```text
[PASS] STATUS.md records successful completion
[PASS] CHECKPOINT.md records successful completion
[PASS] Checked stale status wording absent from STATUS.md
[PASS] Checked stale status wording absent from CHECKPOINT.md
[PASS] README announces the successful build
[PASS] README links the receipt and console log
[PASS] Successful-build receipt records completion
[PASS] Published log matches the preserved SHA-256
[PASS] Misleading recovery receipt absent
[PASS] Local HEAD matches fetched remote main
[PASS] Working tree clean

RESULT: ALL CHECKS PASS
```

This is a dated artifact and synchronization check—not a new build or
a theorem audit. It does not guarantee the status of future revisions.

The build succeeded; no build recovery was required. Earlier inaccurate
documentation was corrected without rebuilding Lean.

---

## Mobile-first research workflow

This milestone was developed through a phone-centered workflow on a
maintainer-reported Samsung Galaxy A15 5G, model SM-A156U.

```text
Physical Android phone
          │
          ▼
Termux
          │
          ▼
Ubuntu through proot-distro
          │
          ▼
Lean / Lake / Mathlib
          │
          ▼
Project builds and computational work
          │
          ▼
Logs, receipts, checksums, and Git publication
```

The process involved extended dependency compilation and multiple resumed
sessions. The recorded outcome demonstrates completed work on the
available hardware, not workstation-equivalent speed or unrestricted
resources.

AI assistance supported explanations, commands, troubleshooting, and
documentation. Human execution and inspectable artifacts remained the
basis for deciding what actually happened.

```text
AI proposes
     │
     ▼
Researcher reviews and executes
     │
     ▼
Files and terminal output provide evidence
     │
     ▼
Claims are accepted, limited, or corrected
```

The value of the workflow is practical accessibility combined with
evidence discipline.

---

## Evidence and claim status

AQARION separates evidence type from claim disposition.

### Evidence labels

| Label | Meaning |
|---|---|
| `[D]` | Definition |
| `[P]` | Mathematical proof recorded for the stated claim |
| `[V]` | Computational verification over a declared domain |
| `[PV]` | Mathematical proof and computational verification |
| `[C]` | Conjecture |
| `[R]` | Active investigation |
| `[F]` | Refuted statement |
| `[Q]` | Quarantined artifact or claim |

A label is a summary. The supporting record must explain its scope and
basis.

### Claim dispositions

| Disposition | Meaning |
|---|---|
| OPEN | Active or unresolved |
| FROZEN | A specified artifact or version is fixed for inspection |
| BLOCKED | An identified requirement prevents a specified transition |
| QUARANTINED | Preserved but excluded from reliance or promotion pending review |
| DEPRECATED | An obsolete representation retained for provenance |
| SUPERSEDED | Replaced by an identified successor |
| RETRACTED | Withdrawn as stated |
| REFUTED | Contradicted by a valid counterexample or argument |

These terms apply to specified records, not automatically to every
artifact in the repository.

### Essential distinctions

```text
Definition                  is not automatically a theorem
Finite exhaustive check     is not automatically a universal proof
Reported execution          is not independent reproduction
Source file                 is not proof of execution
Lean source                 is not proof of build inclusion
Build success               is not a complete theorem-scope audit
Matching checksum           is not mathematical correctness
Public availability         is not peer review
```

A valid counterexample must satisfy the claim’s domain and hypotheses
while violating its conclusion. An alleged witness that fails the
hypotheses does not refute the conditional claim.

Rejected or invalid evidence can remain in the audit trail without
changing the mathematical assessment.

---

## Verification and reproducibility

A useful verification record should identify, where applicable:

1. The exact claim and hypotheses.
2. The tested domain and parameter range.
3. Definitions and frozen conventions.
4. Source revision and implementation.
5. Runtime environment and dependencies.
6. Exact arithmetic or numerical tolerances.
7. Command and captured exit statuses.
8. Expected invariants and comparison rules.
9. Negative controls and failure cases.
10. Output artifacts, hashes, and receipts.
11. Independent reconstruction status.
12. Known limitations.

```text
Claim
  │
  ▼
Specified implementation
  │
  ▼
Actual execution
  │
  ▼
Output and exit status
  │
  ▼
Integrity and scope checks
  │
  ▼
Recorded conclusion
```

Different programs are not necessarily independent verifiers: they can
share a mistaken definition, copied method, or faulty specification.

Likewise, a checksum identifies file contents. It does not establish
mathematical truth or demonstrate that an unrecorded command ran.

### Reproduction guidance

Use the instructions associated with the particular package or Lean
project. Do not assume that one command at the repository root verifies
every research line.

A build or test result should name its actual scope rather than inherit
the apparent breadth of the repository.

---

## Repository architecture

The main repository separates mathematical research records from
reusable tooling and evidence infrastructure.

```text
AQARION/
│
├── README.md
├── OVERVIEW.md
├── CHECKPOINT.md
├── EVIDENCE-LEDGER.md
├── FILETREE.md
├── RESEARCH-PROGRAM-PRESENTATION.md
│
└── AQARION-QUANTARION-AI/
    ├── Research records and mathematical artifacts
    ├── PACKAGES/
    │   └── AQARION-RAG/
    └── TOOLS/
        └── Research-tooling architecture and implementations
```

This is an orientation diagram, not a complete file inventory.
Consult [FILETREE.md](FILETREE.md) and the actual checkout for detail.

### Documented tooling responsibilities

| Component | Intended responsibility |
|---|---|
| ClaimLock | Claim records, dependencies, evidence classification, and transition history |
| ProofGym | Verification workflows and adversarial fixtures |
| JOIN-STABILITY | Pullback-stability and join-closure research |
| Replay | Computational reproduction and execution records |
| Verification | Exact checks, independent reconstruction, and certificates |
| Provenance | Hashes, environments, logs, and artifact relationships |
| Schemas | Machine-readable contracts |
| Skills | Repeatable research procedures |
| CLI | Interfaces to established tooling |
| Exact | Reusable exact finite-mathematics utilities |
| Lean | Formalization targets, build records, and audits |
| Archive | Historical, superseded, refuted, or quarantined material |

These are architectural responsibilities, not a blanket assertion that
every component is complete, stable, or integrated.

---

## AQARION-RAG

[AQARION-RAG](AQARION-QUANTARION-AI/PACKAGES/AQARION-RAG/) is the
repository’s provenance-aware retrieval and evidence-navigation package.

Its documented design includes BM25-ranked retrieval, SHA-256 source
references, claim relationships, supersession information, and an HTTP
service interface.

```text
Query
  │
  ▼
Ranked retrieval
  │
  ▼
Source references and evidence relationships
  │
  ▼
Traceable navigation result
```

Consult the package source, README, tests, and execution records for its
implemented capabilities and current evaluation status.

Retrieval makes records easier to find. It does not certify the truth
of a retrieved claim or authorize a status transition by itself.

---

## Formal verification

Lean build progress and theorem-level review are distinct.

The PBCore006 build is complete and supported by published evidence.
Further formalization work concerns the exact declarations, assumptions,
and research targets being established.

A theorem-specific audit should identify:

- The declaration and its source location.
- Whether it is included in the relevant build.
- Its definitions and hypotheses.
- Proof dependencies and axioms.
- Any placeholders or assumptions requiring review.
- The relationship to the intended mathematical statement.
- The source revision and execution evidence available.

```text
Research statement
        │
        ▼
Formal proposition
        │
        ▼
Lean declaration and proof
        │
        ▼
Build inclusion and acceptance
        │
        ▼
Statement / assumption review
        │
        ▼
Scoped formalization claim
```

Not every verification activity requires every possible audit step.
The applicable requirements should be stated for the result being
presented—not imposed retroactively through unexplained global labels.

---

## Corrections and historical provenance

AQARION preserves corrections so readers can identify what changed,
why it changed, and which conclusions are affected.

A correction should identify:

- The original statement or artifact.
- The error, counterexample, or reporting problem.
- The affected hypotheses and domain.
- The justified replacement, if any.
- Supporting evidence.
- Dependent records requiring review.
- A successor or supersession relationship.

A refuted mathematical claim is not the same as a stale README.
A documentation correction is not necessarily a failed computation.
A quarantined artifact is not automatically a proven-false statement.

Historical records may remain available without continuing to govern the
current status after they have been explicitly superseded.

---

## Publication and collaboration

AQARION is open for public sharing, technical feedback, independent
reproduction, and collaboration.

“Publication open” means that research artifacts may be shared and
reviewed. It does not declare every claim proved, peer-reviewed,
certified, or ready for unrestricted promotion.

Individual releases should explain:

- What is established.
- What was tested only over a bounded domain.
- What remains conjectural.
- Which artifacts actually ran.
- Whether independent reproduction occurred.
- Which formalization questions remain.
- How the work relates to existing literature.

Contributions are welcome in finite dynamical systems, quotient
structure, Koopman methods, exact enumeration, Lean formalization,
software testing, and reproducible research tooling.

Use [GitHub Issues](https://github.com/quantarion369-arch/AQARION/issues)
for questions, counterexamples, reproducibility reports, corrections,
and literature pointers.

---

## Development and contribution standards

Prefer small, inspectable changes with explicit scope.

### Before adding or changing a tool

- State its purpose and input/output contract.
- Identify mathematical assumptions.
- Inspect related existing components.
- Include meaningful tests and failure cases.
- Document dependencies and reproduction instructions.
- Explain what its output establishes.
- Preserve actual execution evidence where a result is claimed.

### Before changing a claim’s status

- Identify the exact statement and version.
- Check the evidence against its hypotheses and domain.
- Preserve contrary evidence and known limitations.
- Record the reason for the transition.
- Avoid treating a badge or summary as independent evidence.

### Before describing a component as stable

Establish that its implementation exists, its relevant tests execute,
its failure cases are meaningful, its instructions work, and its
documentation matches its actual behavior.

Do not create speculative directories or duplicate governance systems
merely to make an architecture diagram look complete.

---

## Related resources

### Companion development repositories

- [AQARION-LEAN](https://github.com/quantarion369-arch/AQARION-LEAN)
- [Aqarion-Fastapi](https://github.com/quantarion369-arch/Aqarion-Fastapi)

### Research resources and historical links

- [AQARION-RAG](AQARION-QUANTARION-AI/PACKAGES/AQARION-RAG/)
- [AQARION-QUANTARION-AI](https://github.com/JASKSG9/Aqarions-Quantarion-AI)
- [AQARION-ARITHMETIC-FDS](https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-)
- [AQARION on Hugging Face](https://huggingface.co/Aqarion)
- [AQARION-TB13 on Hugging Face](https://huggingface.co/Aqarion-TB13)

External and historical resources retain their own revision histories.
A link is not a claim that the destination has been audited at the same
checkpoint as this README.

---

## Guiding principles

> Prove first. Verify exhaustively. Predict second. No free parameters.

> Ideas may come from anywhere. Confidence comes from verification.

> Do not promote a result beyond what its evidence establishes.

Exhaustive verification applies to the explicitly declared finite
domain. Exact and approximate methods should both state their assumptions,
parameters, and limitations.

```text
┌──────────────────────────────────────────────────────────────┐
│                         AQARION                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Core research                    ACTIVE DEVELOPMENT          │
│  PBCore006 Lean build             SUCCESSFUL                  │
│  Build evidence                   PRESERVED AND PUBLISHED     │
│  Public sharing                   OPEN                       │
│  Collaboration                    WELCOME                    │
│  Verification                     CLAIM-SPECIFIC              │
│                                                              │
│  Research → Implementation → Checks → Inspectable evidence    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

AQARION is moving forward from a working build foundation toward deeper
mathematical understanding, more precise formalization, stronger tests,
and clearer connections between research and executable artifacts.
````

Citations:
[1] AQARION / Quantarion-AI: reusable infrastructure for ... - GitHub https://github.com/quantarion369-arch/AQARION
