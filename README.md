# ✨️ WELCOME TO AQARION ✨️

**Evidence-First Mathematical Research for Finite Dynamical Systems, Quotient Structure, and Reproducible Verification**

[![SM003 Verify](https://github.com/quantarion369-arch/AQARION/actions/workflows/sm003-verify.yml/badge.svg?style=for-the-badge)](https://github.com/quantarion369-arch/AQARION/actions/workflows/sm003-verify.yml)
[![Mobile Research Kit](https://github.com/quantarion369-arch/AQARION/actions/workflows/mobile-research-kit.yml/badge.svg?style=for-the-badge)](https://github.com/quantarion369-arch/AQARION/actions/workflows/mobile-research-kit.yml)
[![D22 Validation](https://github.com/quantarion369-arch/AQARION/actions/workflows/D22-validation.yml/badge.svg?style=for-the-badge)](https://github.com/quantarion369-arch/AQARION/actions/workflows/D22-validation.yml)
[![Time and Modes](https://github.com/quantarion369-arch/AQARION/actions/workflows/time-and-modes-check.yml/badge.svg?style=for-the-badge)](https://github.com/quantarion369-arch/AQARION/actions/workflows/time-and-modes-check.yml)

[![C3: Open](https://img.shields.io/badge/C3-OPEN-yellow?style=for-the-badge)](#current-governance-snapshot)
[![C4: Blocked](https://img.shields.io/badge/C4-BLOCKED-red?style=for-the-badge)](#current-governance-snapshot)
[![Lean: Open](https://img.shields.io/badge/Lean-OPEN-lightgrey?style=for-the-badge)](#formal-verification)
[![SDS-002: Quarantined](https://img.shields.io/badge/SDS--002-QUARANTINED-orange?style=for-the-badge)](#corrections-and-historical-provenance)
[![Publication: Blocked](https://img.shields.io/badge/Publication-BLOCKED-red?style=for-the-badge)](#publication-and-collaboration)
[![Promotable: False](https://img.shields.io/badge/Promotable-false-lightgrey?style=for-the-badge)](#current-governance-snapshot)


AQARION is an open mathematical research project maintained by James A. It investigates finite dynamical systems, invariant quotients, Koopman operators, observable subspaces, exact enumeration, and formalizable computational mathematics.

The repository is maintained as an auditable research record. It distinguishes mathematical statements, implementations, finite computations, independent reconstruction, formal proof, provenance, and publication decisions.

> Do not promote a result beyond what its evidence establishes.

---

## Contents

- [Start here](#start-here)
- [Current governance snapshot](#current-governance-snapshot)
- [Research scope](#research-scope)
- [Central mathematical framework](#central-mathematical-framework)
- [Evidence and claim status](#evidence-and-claim-status)
- [Research workflow](#research-workflow)
- [Active research lines](#active-research-lines)
- [Verification and reproducibility](#verification-and-reproducibility)
- [Repository architecture](#repository-architecture)
- [AQARION-RAG](#aqarion-rag)
- [Formal verification](#formal-verification)
- [Corrections and historical provenance](#corrections-and-historical-provenance)
- [Publication and collaboration](#publication-and-collaboration)
- [Development and contribution standards](#development-and-contribution-standards)
- [Related resources](#related-resources)

---

## Start here

| Resource | Purpose |
|---|---|
| [AQARION-RAG](AQARION-QUANTARION-AI/PACKAGES/AQARION-RAG/) | Provenance-aware retrieval and evidence navigation over the research corpus |
| [PB-001 research document](AQARION-QUANTARION-AI/PB_001.md) | Finite-quotient pullback rigidity and binary join closure |
| [Tools architecture](AQARION-QUANTARION-AI/TOOLS/README.md) | Documented architecture for reusable research and verification tools |
| [Master file tree](FILETREE.md) | Architectural file and directory index |
| Research map (`docs/RESEARCH-LINES.md`) | Overview of the research lines documented in this repository (pending) |
| Evidence ledger (`EVIDENCE-LEDGER.md`) | Claim-level evidence, scope, receipts, and proof status (pending) |
| Corrections and refutations (`docs/HISTORICAL-CORRECTIONS.md`) | Historical corrections, counterexamples, quarantined material, and retired claims (pending) |
| Formalization roadmap (`docs/FORMALIZATION.md`) | Lean targets, formalization obligations, and environment notes (pending) |
| Provenance policy (`docs/PROVENANCE.md`) | Relationship between claims, source code, execution, and evidence artifacts (pending) |
| [Issues](https://github.com/quantarion369-arch/AQARION/issues) | Corrections, reproducibility reports, questions, and research discussion |

A listed resource is a navigation target, not independent evidence that its contents are current, executable, or formally verified. File existence, implementation, and test status must be established from the actual artifact and its execution record.

---

## Current governance snapshot

The repository README has published the following governance labels. They are reproduced here to keep the project state visible without requiring a separate root status file.

| Gate or research item | Recorded state |
|---|---|
| C3 | OPEN |
| C4 | BLOCKED |
| Lean formalization | OPEN |
| SDS-002 | QUARANTINED |
| Publication | BLOCKED |
| Promotion | BLOCKED |
| Promotable | false |

These are governance dispositions, not mathematical conclusions.

- OPEN means the relevant work or obligation remains unresolved.
- BLOCKED means a required gate has not been satisfied.
- QUARANTINED means an artifact or claim is preserved but excluded from promotion pending resolution.
- Promotable: false means the project does not currently authorize promotion under the applicable governance requirements.

A blocked theorem is not thereby false. A quarantined result is not automatically refuted. A documented proof candidate is not automatically a checked proof.

These labels must change only when the corresponding evidence and governance records justify the transition. The existence of a new source file, receipt, test, badge, or report is not by itself sufficient.

---

## Research scope

AQARION concentrates on the following mathematical and computational areas.

### Finite dynamical systems

Deterministic maps, functional graphs, cycles, transient structure, finite state spaces, and invariant partitions.

### Quotient systems

Invariant equivalence relations, quotient maps, semiconjugacy, finite quotient structure, and closure properties.

### Koopman operators and observable defects

Pullback operators, block-constant observable spaces, projections, invariance, and the operator measuring failure of an observable subspace to remain invariant.

### Exact computational mathematics

Finite exhaustive checks, rational and integer arithmetic, independent algorithms, structured witnesses, counterexample search, and negative controls.

### Formal verification

Lean formalization, theorem-to-code correspondence, pinned builds, proof dependency audits, and explicit treatment of unresolved proof obligations.

### Research provenance

Claim records, source revisions, execution records, artifact hashes, reproduction instructions, corrections, and historical status transitions.

The project does not treat computational agreement, formal compilation, or publication readiness as interchangeable forms of evidence.

---

## Central mathematical framework

Let (X) be a finite set, let (T:X\to X) be a deterministic map, and let (Pi) be a partition of (X).

Let (V_Pi) denote the vector space of functions that are constant on each block of (Pi). Let (P_Pi) be the orthogonal projection onto (V_Pi), under the specified inner product, and define the Koopman pullback operator by

[
K_T f=fcirc T.
]

The observable defect is

[
D_Pi=(I-P_Pi)K_TP_Pi.
]

It measures the component of the pulled-back block-constant observables that lies outside the block-constant subspace.

For this finite-dimensional setting,

[
D_Pi=0
quadLongleftrightarrowquad
K_T(V_Pi)subseteq V_Pi.
]

The equivalence follows from the definition of the projection: (D_Pi=0) precisely when applying (K_T) to any vector in the range of (P_Pi) produces a vector in that same range.

For partitions of a finite state space, this invariance condition is connected to congruence and quotient dynamics. Exact hypotheses and conventions matter; conclusions must be stated for the operator, partition, and domain actually defined.

This framework is a research foundation, not a blanket certification of every proposed rank formula, spectral identity, refinement law, or application associated with it.

---

## Evidence and claim status

AQARION keeps evidence type separate from claim disposition.

### Evidence labels

| Label | Meaning |
|---|---|
| [D] | Definition |
| [P] | Mathematical proof |
| [V] | Verification over a declared computational domain |
| [PV] | Mathematical proof and computational verification |
| [C] | Conjecture |
| [R] | Active research or investigation |
| [F] | Refuted claim or claim with a counterexample |
| [Q] | Quarantined artifact or claim |

These labels are not interchangeable.

In particular:

- definition (
eq) theorem
- finite exhaustive check (
eq) universal proof
- reported execution (
eq) independent reproduction
- source file (
eq) executed artifact
- Lean source (
eq) checked Lean theorem
- successful build (
eq) intended theorem proved
- artifact hash (
eq) mathematical correctness
- policy PASS (
eq) mathematical truth
- public availability (
eq) publication readiness

### Claim dispositions

Where used in claim records, the following terms distinguish different situations:

| Disposition | Meaning |
|---|---|
| OPEN | Unresolved or active |
| FROZEN | A specified artifact or version is locked for audit |
| BLOCKED | A required gate prevents promotion |
| QUARANTINED | Preserved but excluded from promotion pending resolution |
| DEPRECATED | An obsolete representation or artifact retained for provenance |
| SUPERSEDED | Replaced by a successor |
| RETRACTED | Withdrawn and no longer to be relied on as stated |
| REFUTED | The stated claim is contradicted by a valid counterexample or argument |

A claim may have computational evidence while its proof remains open. A proof candidate may be mathematically promising while its formalization remains incomplete. A refuted statement must not be silently rewritten as if the original statement had been correct.

### Promotion principle

No evidence class or disposition upgrades automatically.

Promotion requires an auditable relationship between:

1. The exact statement and its hypotheses.
2. Definitions and frozen conventions.
3. Declared domain and scope.
4. Supporting proof or derivation.
5. Executable verification and its limits.
6. Independent reconstruction, where required.
7. Formalization and axiom audit, where required.
8. Artifact integrity and provenance.
9. Known counterexamples, corrections, and limitations.
10. The actual decision authorizing the transition.

---

## Research workflow

AQARION uses an evidence-first workflow:

```text
Research question
        |
        v
Exact claim and definitions
        |
        v
Freeze hypotheses, conventions, and domain
        |
        v
Derivation and proof obligations
        |
        v
Executable verifier and negative controls
        |
        v
Run and preserve execution evidence
        |
        v
Independent reconstruction
        |
        v
Compare against the intended mathematical claim
        |
        v
Provenance and dependency audit
        |
        v
Formalization and axiom audit, where required
        |
        v
Literature review and scope review
        |
        v
Evidence classification and promotion decision
```

The order may be adapted to the research problem, but the evidence distinctions must remain intact.

A failed check is retained as evidence. A counterexample is not hidden. A correction does not erase the history of the error. A finite computation does not become a theorem merely by being repeated.

---

## Active research lines

### 1. Invariant-partition enumeration

Research into invariant partitions of finite permutations, including cycle decompositions, phase structure, weighted Bell-type formulas, and direct enumeration oracles.

The repository describes AQ-FPR-006 as an analytical formula with bounded computational cross-checks. External independent reproduction and literature priority remain separate questions. The detailed research map and evidence ledger are pending.

### 2. Finite quotient defects

Research into invariant quotient structure through block-constant observable spaces and operator defects.

The work tracks definitions, projection conventions, transport-energy identities, rank claims, finite computations, and formalization obligations separately. Refuted rank claims and their counterexamples should remain available in the historical record.

No rank formula or refinement law should be generalized beyond the domain actually established by its proof.

### 3. Finite-quotient pullback rigidity

The PB-001 research line studies a function (T:X\to X), equivalence relations on (X), and the pullback relation

[
T^*E={(x,y)in X^2:(Tx,Ty)in E}.
]

Its central finite-quotient statement is that, if (X/E) is finite and (T^*Esubseteq E), then (T^*E=E).

The associated binary join-closure argument uses finite quotient permutations and a bipartite incidence graph.

The research document records an analytic proof candidate and reported finite computational evidence. Independent proof review, execution-artifact reconstruction, Lean formalization, axiom audit, and literature-priority review remain distinct obligations. Consult [PB-001](AQARION-QUANTARION-AI/PB_001.md) for the detailed statement and current caveats.

### 4. Formalization and provenance

This research line concerns the connection between mathematical claims, source artifacts, execution, and formal proof.

The requirements include:

- Exact correspondence between a claim and the proposition formalized.
- Pinned toolchain and dependency versions.
- Reproducible clean builds.
- Explicit proof dependencies and axiom auditing.
- Separation of build health from mathematical certification.
- Artifact hashes and execution records.
- Preservation of open and failed obligations.

The formalization roadmap and provenance policy documents are pending.

---

## Verification and reproducibility

A reliable computational result requires more than a displayed output.

Where applicable, a verification record should identify:

- The mathematical statement being checked.
- Input and output formats.
- The exact domain and parameter range.
- Frozen conventions and definitions.
- Algorithm and implementation revision.
- Runtime and dependency environment.
- Exact arithmetic or numerical tolerances.
- Expected invariants and comparison rules.
- Negative controls and known failure cases.
- Execution command and result.
- Artifact hashes and receipt.
- Independent reconstruction status.
- Known limitations.

Different programs are not necessarily independent verifiers. They may share the same mistaken convention, copied algorithm, or faulty specification.

Likewise, a matching hash establishes artifact identity, not mathematical truth. A receipt must be tied to the actual artifact and execution it claims to describe.

The existence of verification directories in the repository architecture does not itself establish that every planned verifier, receipt, or workflow has been implemented or executed.

---

## Repository architecture

The repository contains mathematical research records and documented tooling architecture. The architecture is intended to keep mathematical content separate from reusable infrastructure.

### Research records

The research-side directories preserve theorem statements, derivations, experiments, finite computation, formalization targets, and historical corrections.

### Reusable tooling

The documented tooling architecture under `AQARION-QUANTARION-AI/TOOLS/` separates the following responsibilities:

| Component | Intended responsibility |
|---|---|
| ClaimLock | Claim records, evidence classifications, dependencies, and promotion history |
| ProofGym | Executable mathematical verification workflows and adversarial fixtures |
| JOIN-STABILITY | Research and verification concerning pullback-stable equivalence relations and join closure |
| Replay | Deterministic computational reproduction and execution records |
| Verification | Exact checks, independent reconstruction, adversarial tests, and certificates |
| Provenance | Artifact hashes, environments, execution logs, and research-object metadata |
| Schemas | Shared machine-readable contracts |
| Skills | Documented, repeatable research workflows |
| CLI | Consistent interfaces to established tools |
| Exact | Reusable exact finite-mathematics utilities |
| Lean | Formalization targets, build records, and audits |
| Archive | Preserved historical, superseded, refuted, and quarantined material |

This is a description of the intended architecture, not a guarantee that every listed component is implemented, complete, or stable.

Use the relevant source files, tests, workflow definitions, and execution records to determine the actual implementation state. See the [tools README](AQARION-QUANTARION-AI/TOOLS/README.md) and [master file tree](FILETREE.md).

---

## AQARION-RAG

[AQARION-RAG](AQARION-QUANTARION-AI/PACKAGES/AQARION-RAG/) is a provenance-aware retrieval service for navigating the AQARION research corpus.

```text
Query → BM25-ranked retrieval → Evidence graph → Cited, traceable result
```

Its responsibilities include:

- BM25 relevance ranking over the pinned corpus.
- Content-addressed (SHA-256) source references.
- Claim and supersession relationships via the evidence graph.
- An HTTP service interface for programmatic access.

Retrieval results are navigation aids, not certification of the underlying claims. Claim status remains governed by the evidence and promotion records described above.

See the [AQARION-RAG package](AQARION-QUANTARION-AI/PACKAGES/AQARION-RAG/) for implementation details, evaluation status, and usage.

---

## Formal verification

Lean formalization is an independent research obligation.

For a formalized result to support promotion, the audit must establish that:

1. The theorem source is present and included in the intended build.
2. The toolchain and dependencies are pinned.
3. A clean build succeeds in the declared environment.
4. No forbidden placeholders or unreviewed axioms occur.
5. The theorem's definitions and hypotheses match the intended claim.
6. The proof dependency and axiom audit is recorded.
7. The build receipt identifies the exact source revision and environment.

A successful build is valuable evidence about the formal artifact. It is not, by itself, evidence that every related computational result is reproducible or that the intended research claim has been formalized correctly.

The current recorded Lean status remains OPEN. The formalization roadmap document is pending.

---

## Corrections and historical provenance

AQARION preserves mistakes, counterexamples, retractions, and superseded claims so that later work can identify exactly what changed and why.

A correction should identify:

- The original statement or artifact.
- The precise error or counterexample.
- The corrected statement, if one is justified.
- The affected domain and assumptions.
- The evidence supporting the correction.
- The status transition and its rationale.
- Any dependent claims or artifacts that require re-evaluation.

Historical artifacts must not be silently rewritten to make the research record appear cleaner.

A refuted claim remains distinguishable from a claim that has merely been superseded. A quarantined artifact remains distinguishable from a proven-false statement.

The corrections and historical provenance document is pending.

---

## Publication and collaboration

Publication readiness is assessed separately from computational success, repository completeness, and formalization progress.

Before a result is promoted for publication, its authors should be able to state clearly:

- What is proved.
- What is verified only over a finite or bounded domain.
- What remains conjectural.
- What has been refuted or retracted.
- Which artifacts were actually executed.
- Whether independent reproduction has occurred.
- Which formal proof obligations remain open.
- What prior literature establishes.
- What, if anything, is being claimed as a new contribution.

The current recorded publication gate is BLOCKED. This does not assert that all work in the repository is incorrect; it means that the relevant publication gate has not been cleared.

Collaboration is welcome in finite dynamical systems, Koopman theory, quotient structures, exact combinatorial enumeration, reproducible mathematical computing, Lean formalization, and research provenance.

Use [GitHub Issues](https://github.com/quantarion369-arch/AQARION/issues) for questions, proposed corrections, reproducibility reports, and literature pointers.

---

## Development and contribution standards

Contributions should make the research record more inspectable and reliable.

Before adding a tool or promoting an artifact, establish:

1. Its purpose and exact input/output contract.
2. The mathematical or computational assumptions it uses.
3. Whether the computation is deterministic.
4. The tests and failure cases that exercise it.
5. The reproduction instructions.
6. The evidence it produces and does not produce.
7. Its source revision and dependencies.
8. The relevant provenance record.
9. The relationship to existing tooling.
10. The explicit limits on what it certifies.

Prefer extending established components to creating duplicate tools with overlapping responsibilities. Audit the existing source and interfaces before introducing a new CLI, schema, or claim-management system.

Do not add empty speculative directories merely because they appear in an architectural tree. Do not mark a feature as implemented merely because its planned path is documented.

### Quality gate

Before a tool is described as stable, establish that its source exists, its tests execute, its failure cases are meaningful, its reproduction instructions work, its documentation matches the implementation, and its CI actually runs.

Before a mathematical claim is promoted, establish the corresponding mathematical and evidentiary obligations independently.

---

## Related resources

- [AQARION-RAG](AQARION-QUANTARION-AI/PACKAGES/AQARION-RAG/) — provenance-aware retrieval and evidence navigation
- [AQARION-QUANTARION-AI](https://github.com/JASKSG9/Aqarions-Quantarion-AI) — research corpus layout and CLAIMLOCK promotion policy
- [AQARION-ARITHMETIC-FDS](https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-) — finite dynamical systems, observable quotients, and certified computation
- [AQARION on Hugging Face](https://huggingface.co/Aqarion) — research spaces, models, and datasets
- [AQARION-TB13 on Hugging Face](https://huggingface.co/Aqarion-TB13) — training and evaluation workspaces

---

# AQARION Ecosystem
## Research, Lean Formalization, FASTAPI Development

AQARION is an independent research program developing mathematical ideas,
formalization artifacts, computational implementations, and inspectable
evidence records.

Its work is organized across three complementary repositories: the main
research repository, a dedicated Lean formalization repository, and a
Python/FastAPI development repository.

The project has moved beyond an important infrastructure obstacle:
PBCore006’s Lean build is complete. The successful result, actual console
log, and corrected public records are now published. For this project and
the documented execution, waiting for the initial build is no longer the
bottleneck.

The next stage is to build on that working foundation: make theorem
coverage easier to inspect, strengthen tests and evidence traceability,
and develop clearly specified connections between research, formalization,
and software interfaces.

## The Three-Repository Structure

```text
                              AQARION
                     Research and evidence hub
                                 │
                 ┌───────────────┴───────────────┐
                 │                               │
                 ▼                               ▼
           AQARION-LEAN                   Aqarion-Fastapi
        Formalization projects           API implementation
        Lean source and builds           Python service code
        Receipts and console logs        Tests and tooling
                 │                               │
                 └───────────────┬───────────────┘
                                 ▼
                    Inspectable research artifacts
```

This diagram describes the repositories’ complementary roles. It does
not claim that an automated cross-repository integration is already
implemented.

| Repository | Role | Where to look |
|---|---|---|
| AQARION | Research context, mathematical development, and evidence organization | This repository |
| [AQARION-LEAN](https://github.com/quantarion369-arch/AQARION-LEAN) | Lean formalization projects and recorded build evidence | Source projects, README, status records, and receipts |
| [Aqarion-Fastapi](https://github.com/quantarion369-arch/Aqarion-Fastapi) | Python/FastAPI implementation and service development | README, application source, tests, and workflow configuration |

## A Completed Milestone: PBCore006 Builds Successfully

PBCore006 completed its configured Lean build in an Android/Termux
environment using Ubuntu through proot-distro on ARM64 hardware.

The final recorded output is:

```text
=== RESUME 2026-10-17T22:15:00-04:00 ===

⚠ [784/785] Built PBCore006 (118s)

Build completed successfully (785 jobs).

LAKE_EXIT=0
LOG_EXIT=0
BUILD FINISHED SUCCESSFULLY
```

**The initial PBCore006 build obstacle is resolved.**

This was not merely a proposed setup or an unexecuted command. The
project reported successful completion, the build command returned zero,
and the logging command returned zero.

The displayed warnings were non-fatal. The 118-second figure belongs to
the PBCore006 target, not the entire dependency build. The 785-job count
is a build-work count, not a count of mathematical theorems.

### From Build Execution to Published Evidence

```text
Configured Lean project
          │
          ▼
Dependency compilation across resumed sessions
          │
          ▼
PBCore006 target built successfully
          │
          ▼
Build and logging exit statuses captured
          │
          ▼
Original console log copied into the repository
          │
          ▼
Original and copied log checksums matched
          │
          ▼
README, receipt, and status documents published
          │
          ▼
Fetched remote files checked directly
          │
          ▼
All 11 publication checks passed
```

### Evidence You Can Inspect

- [AQARION-LEAN repository](https://github.com/quantarion369-arch/AQARION-LEAN)
- [Successful build receipt](https://github.com/quantarion369-arch/AQARION-LEAN/blob/main/RECEIPTS/PBCore006-build-result-20261017.md)
- [Actual console log](https://github.com/quantarion369-arch/AQARION-LEAN/blob/main/RECEIPTS/PBCore006-20261017-console.log)
- [Build status](https://github.com/quantarion369-arch/AQARION-LEAN/blob/main/STATUS.md)
- [Consolidated checkpoint](https://github.com/quantarion369-arch/AQARION-LEAN/blob/main/CONSOLIDATED/CHECKPOINT.md)

The preserved device log was 30,496 bytes. Its repository copy matched
the original SHA-256:

```text
0ef92b13e35a1785831ede359280b373f8f2dd9043f8e77afd43aa1616d824a1
```

A subsequent check of fetched remote `main` confirmed that the published
log also matched that checksum.

The integrity check establishes content identity between the preserved
log and the published artifact. It does not independently establish an
unrecorded runtime version or source revision.

## Public Checkpoint Verification

The documentation and console-evidence publication was committed in
`fdf8388`. A subsequent verification checked the repository at:

```text
cfd22c61b2074a0af31d54bdd1b1780c22994878
```

That revision includes the later organizational change grouping Lean
projects under `PROJECTS`.

The supplied verification output recorded:

```text
PASS | STATUS.md records BUILD PASS / 785 jobs / zero exits
PASS | CHECKPOINT.md records BUILD PASS / 785 jobs / zero exits
PASS | STATUS.md has no stale unknown-count or blanket-blocker wording
PASS | CHECKPOINT.md has no stale unknown-count or blanket-blocker wording
PASS | README announces successful build
PASS | README links receipt and console log
PASS | Successful receipt records completion
PASS | Published console log matches preserved SHA-256
PASS | Misleading recovery receipt absent
PASS | Local HEAD matches fetched remote main
PASS | Working tree clean

RESULT: ALL CHECKS PASS
```

These checks establish the state of that published checkpoint. They are
not a new Lean build, a theorem-assumption audit, or a permanent guarantee
about future repository revisions.

The successful execution did not require a build-recovery operation.
The public record now presents it directly as a successful build.

## What Has Changed for the Research Workflow

The completed build changes the immediate task.

Before this milestone, substantial attention was required simply to
bring the configured project and its dependencies through compilation
on the available device.

Now there is a working, recorded foundation on which further work can
proceed.

```text
PREVIOUS INFRASTRUCTURE TASK
───────────────────────────
Establish environment
        ↓
Compile required dependencies
        ↓
Complete the PBCore006 build


CURRENT DEVELOPMENT DIRECTION
─────────────────────────────
Inspect exact formal statements
        ↓
Map claims to declarations and evidence
        ↓
Extend focused tests and formalization
        ↓
Specify software interfaces
        ↓
Publish the next evidence-backed checkpoint
```

This does not mean that all future Lean work will be effortless, that
every project has been rebuilt at the same revision, or that every
research target is proved.

It means the documented PBCore006 build is a completed achievement,
not a standing blocker that must be repeatedly reopened.

## AQARION-LEAN: Building on a Working Formalization Environment

[Explore AQARION-LEAN →](https://github.com/quantarion369-arch/AQARION-LEAN)

AQARION-LEAN provides a dedicated home for Lean projects and their
execution records. The published status documents also contain recorded
AQFPR006 and PB006Audit checkpoints alongside PBCore006.

The repository makes it possible to distinguish:

- Mathematical definitions and theorem statements.
- Lean source implementing particular formalization targets.
- Configured project builds.
- Recorded finite tests and negative controls.
- Receipts and raw console evidence.
- Research questions that remain outside the demonstrated result.

The next formalization work can therefore focus on specific declarations,
assumptions, and proof obligations rather than treating the already
completed PBCore006 build as unfinished.

A successful build is meaningful evidence. The scope of the mathematical
claims attached to it should remain explicit and inspectable.

## Aqarion-Fastapi: Developing the Software Interface

[Explore Aqarion-Fastapi →](https://github.com/quantarion369-arch/Aqarion-Fastapi)

Aqarion-Fastapi is the companion Python/FastAPI development repository.

Its role is distinct from the Lean repository: it provides a place to
develop application behavior, computational routes, service interfaces,
tests, and supporting software tooling.

Consult that repository’s README, source, and workflow records for the
implemented endpoints, recorded checks, and current limitations. This
checkpoint does not assign a new API test result or deployment status.

The intended relationship between the repositories is evidence-aware:

```text
Research claim
      │
      ▼
Precisely identified mathematical statement
      │
      ├────────► Computational implementation and tests
      │
      └────────► Formalization target and Lean declarations
                              │
                              ▼
                   Explicit verification records
                              │
                              ▼
                 Software presents the recorded status
```

This is a development direction, not a claim that the full pipeline is
already automated.

An API response should identify what it computed or retrieved. A build
receipt should identify what execution it records. Neither should
silently become a claim that a different theorem was proved.

## Independent Research on Accessible Hardware

This checkpoint was developed through a phone-centered workflow on a
maintainer-reported Samsung Galaxy A15 5G, model SM-A156U.

The work combined accessible development tools with AI assistance and
direct human execution. It involved learning unfamiliar tooling,
continuing across interrupted sessions, inspecting console output,
and preserving the evidence behind the final result.

```text
Available hardware
       +
Accessible development tools
       +
Mathematical investigation
       +
AI-assisted explanation and drafting
       +
Human review and actual execution
       │
       ▼
A completed, inspectable research milestone
```

The significance is not that hardware limitations disappeared.
It is that a concrete formalization-build milestone was completed
within those limitations and documented publicly.

AI was useful as an assistant, not an authority on what happened.
Commands, source files, logs, checksums, tests, and repository history
remain the basis for the project’s technical claims.

## Next Development Priorities

With this build checkpoint complete, the proposed next priorities are
more focused:

1. Map important research claims to exact source files and declarations.
2. Make theorem scope and assumptions easier to inspect.
3. Extend targeted tests and preserve meaningful negative controls.
4. Keep claim versions, source revisions, and evidence identities distinct.
5. Define cross-repository interfaces before automating status exchange.
6. Preserve future execution records without reopening completed
   milestones merely because an older summary is stale.

These are forward development priorities, not retroactive conditions
on the successful build.

## Checkpoint at a Glance

```text
┌──────────────────────────────────────────────────────────────┐
│                     AQARION PROGRESS                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  PBCore006 build                      SUCCESSFUL              │
│  Reported build jobs                  785                     │
│  Build exit status                    0                       │
│  Logging exit status                  0                       │
│                                                              │
│  Actual console evidence              PRESERVED               │
│  Published log checksum               VERIFIED                │
│  Successful-build receipt             PUBLISHED               │
│  README and status correction         PUBLISHED               │
│  Publication checks                   11 / 11 PASS            │
│                                                              │
│  Immediate PBCore006 build obstacle   RESOLVED                 │
│  Next focus                           TARGETED DEVELOPMENT    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Explore the Work

- [AQARION-LEAN — formalization projects and build evidence](https://github.com/quantarion369-arch/AQARION-LEAN)
- [Aqarion-Fastapi — Python/FastAPI development](https://github.com/quantarion369-arch/Aqarion-Fastapi)

This checkpoint records completed progress, not a promise of universal
correctness or finished integration. Its strength is that the result,
the evidence, and the remaining work are distinguishable.

AQARION is moving forward from a working build foundation toward more
precise formalization, stronger software tests, and clearer connections
between mathematical research and executable artifacts.

---

## Guiding principles

> Prove first. Verify exhaustively. Predict second. No free parameters.

> Ideas may come from anywhere. Confidence comes from verification.

> Do not promote a result beyond what its evidence establishes.

---

**AQARION — Evidence-First Mathematical Research
