# ✨️ WELCOME TO AQARION ✨️

**Evidence-First Mathematical Research for Finite Dynamical Systems, Quotient Structure, and Reproducible Verification**

AQARION is open for public sharing, technical feedback, independent
reproduction, and collaboration.

Released artifacts should be read according to their recorded scope:
research proposals, computational results, Lean build records, and
formally established statements are identified separately.

Open publication does not imply that every claim is proved, peer-reviewed,
or ready for unrestricted promotion.

[![Lean Build: PASS](https://img.shields.io/badge/Lean_Build-PASS-2ea44f?style=for-the-badge&logo=lean&logoColor=white)](https://github.com/quantarion369-arch/AQARION-LEAN)
[![Build Evidence: Published](https://img.shields.io/badge/Build_Evidence-PUBLISHED-0969da?style=for-the-badge)](https://github.com/quantarion369-arch/AQARION-LEAN/blob/main/RECEIPTS/PBCore006-build-result-20261017.md)
[![Publication: Open](https://img.shields.io/badge/Publication-OPEN-00897b?style=for-the-badge)](#publication-and-collaboration)
[![Collaboration: Welcome](https://img.shields.io/badge/Collaboration-WELCOME-8250df?style=for-the-badge)](#publication-and-collaboration)
[![Verification: Claim-Specific](https://img.shields.io/badge/Verification-CLAIM--SPECIFIC-57606a?style=for-the-badge)](#formal-verification)
[![SDS-002: Quarantined](https://img.shields.io/badge/SDS--002-QUARANTINED-orange?style=for-the-badge)](#corrections-and-historical-provenance)

PBCore006 has a recorded successful Lean build with published console
evidence. Publication is open for sharing research artifacts, receiving
feedback, and collaboration. Mathematical verification and promotion
remain specific to each claim and its supporting evidence.

---

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
