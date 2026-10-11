✨️ WELCOME TO AQARION ✨️

Evidence-First Mathematical Research for Finite Dynamical Systems, Quotient Structure, and Reproducible Verification

""C3: Open" (https://img.shields.io/badge/C3-OPEN-yellow?style=flat-square)" (#current-governance-snapshot)
""C4: Blocked" (https://img.shields.io/badge/C4-BLOCKED-red?style=flat-square)" (#current-governance-snapshot)
""Lean: Open" (https://img.shields.io/badge/Lean-OPEN-lightgrey?style=flat-square)" (docs/FORMALIZATION.md)
""SDS-002: Quarantined" (https://img.shields.io/badge/SDS--002-QUARANTINED-orange?style=flat-square)" (docs/HISTORICAL-CORRECTIONS.md)
""Publication: Blocked" (https://img.shields.io/badge/Publication-BLOCKED-red?style=flat-square)" (#current-governance-snapshot)
""Promotable: False" (https://img.shields.io/badge/Promotable-false-lightgrey?style=flat-square)" (#current-governance-snapshot)

AQARION is an open mathematical research project maintained by James A. It investigates finite dynamical systems, invariant quotients, Koopman operators, observable subspaces, exact enumeration, and formalizable computational mathematics.

The repository is maintained as an auditable research record. It distinguishes mathematical statements, implementations, finite computations, independent reconstruction, formal proof, provenance, and publication decisions.

«Do not promote a result beyond what its evidence establishes.»

---

Contents

- "Start here" (#start-here)
- "Current governance snapshot" (#current-governance-snapshot)
- "Research scope" (#research-scope)
- "Central mathematical framework" (#central-mathematical-framework)
- "Evidence and claim status" (#evidence-and-claim-status)
- "Research workflow" (#research-workflow)
- "Active research lines" (#active-research-lines)
- "Verification and reproducibility" (#verification-and-reproducibility)
- "Repository architecture" (#repository-architecture)
- "Formal verification" (#formal-verification)
- "Corrections and historical provenance" (#corrections-and-historical-provenance)
- "Publication and collaboration" (#publication-and-collaboration)
- "Development and contribution standards" (#development-and-contribution-standards)

---

Start here

Resource| Purpose
"Research map" (docs/RESEARCH-LINES.md)| Overview of the research lines documented in this repository
"Evidence ledger" (EVIDENCE-LEDGER.md)| Claim-level evidence, scope, receipts, and proof status
"Corrections and refutations" (docs/HISTORICAL-CORRECTIONS.md)| Historical corrections, counterexamples, quarantined material, and retired claims
"Formalization roadmap" (docs/FORMALIZATION.md)| Lean targets, formalization obligations, and environment notes
"Provenance policy" (docs/PROVENANCE.md)| Relationship between claims, source code, execution, and evidence artifacts
"PB-001 research document" (AQARION-QUANTARION-AI/PB_001.md)| Finite-quotient pullback rigidity and binary join closure
"Tools architecture" (AQARION-QUANTARION-AI/TOOLS/README.md)| Documented architecture for reusable research and verification tools
"Master file tree" (FILETREE.md)| Architectural file and directory index
"Issues" (https://github.com/quantarion369-arch/AQARION/issues)| Corrections, reproducibility reports, questions, and research discussion

A listed resource is a navigation target, not independent evidence that its contents are current, executable, or formally verified. File existence, implementation, and test status must be established from the actual artifact and its execution record.

---

Current governance snapshot

The repository README has published the following governance labels. They are reproduced here to keep the project state visible without requiring a separate root status file.

Gate or research item| Recorded state
C3| OPEN
C4| BLOCKED
Lean formalization| OPEN
SDS-002| QUARANTINED
Publication| BLOCKED
Promotion| BLOCKED
Promotable| false

These are governance dispositions, not mathematical conclusions.

- OPEN means the relevant work or obligation remains unresolved.
- BLOCKED means a required gate has not been satisfied.
- QUARANTINED means an artifact or claim is preserved but excluded from promotion pending resolution.
- Promotable: false means the project does not currently authorize promotion under the applicable governance requirements.

A blocked theorem is not thereby false. A quarantined result is not automatically refuted. A documented proof candidate is not automatically a checked proof.

These labels must change only when the corresponding evidence and governance records justify the transition. The existence of a new source file, receipt, test, badge, or report is not by itself sufficient.

---

Research scope

AQARION concentrates on the following mathematical and computational areas.

Finite dynamical systems

Deterministic maps, functional graphs, cycles, transient structure, finite state spaces, and invariant partitions.

Quotient systems

Invariant equivalence relations, quotient maps, semiconjugacy, finite quotient structure, and closure properties.

Koopman operators and observable defects

Pullback operators, block-constant observable spaces, projections, invariance, and the operator measuring failure of an observable subspace to remain invariant.

Exact computational mathematics

Finite exhaustive checks, rational and integer arithmetic, independent algorithms, structured witnesses, counterexample search, and negative controls.

Formal verification

Lean formalization, theorem-to-code correspondence, pinned builds, proof dependency audits, and explicit treatment of unresolved proof obligations.

Research provenance

Claim records, source revisions, execution records, artifact hashes, reproduction instructions, corrections, and historical status transitions.

The project does not treat computational agreement, formal compilation, or publication readiness as interchangeable forms of evidence.

---

Central mathematical framework

Let (X) be a finite set, let (T:X\to X) be a deterministic map, and let (\Pi) be a partition of (X).

Let (V_\Pi) denote the vector space of functions that are constant on each block of (\Pi). Let (P_\Pi) be the orthogonal projection onto (V_\Pi), under the specified inner product, and define the Koopman pullback operator by

[
K_T f=f\circ T.
]

The observable defect is

[
D_\Pi=(I-P_\Pi)K_TP_\Pi.
]

It measures the component of the pulled-back block-constant observables that lies outside the block-constant subspace.

For this finite-dimensional setting,

[
D_\Pi=0
\quad\Longleftrightarrow\quad
K_T(V_\Pi)\subseteq V_\Pi.
]

The equivalence follows from the definition of the projection: (D_\Pi=0) precisely when applying (K_T) to any vector in the range of (P_\Pi) produces a vector in that same range.

For partitions of a finite state space, this invariance condition is connected to congruence and quotient dynamics. Exact hypotheses and conventions matter; conclusions must be stated for the operator, partition, and domain actually defined.

This framework is a research foundation, not a blanket certification of every proposed rank formula, spectral identity, refinement law, or application associated with it.

---

Evidence and claim status

AQARION keeps evidence type separate from claim disposition.

Evidence labels

Label| Meaning
"[D]"| Definition
"[P]"| Mathematical proof
"[V]"| Verification over a declared computational domain
"[PV]"| Mathematical proof and computational verification
"[C]"| Conjecture
"[R]"| Active research or investigation
"[F]"| Refuted claim or claim with a counterexample
"[Q]"| Quarantined artifact or claim

These labels are not interchangeable.

In particular:

definition              != theorem
finite exhaustive check != universal proof
reported execution      != independent reproduction
source file             != executed artifact
Lean source             != checked Lean theorem
successful build        != intended theorem proved
artifact hash           != mathematical correctness
policy PASS             != mathematical truth
public availability     != publication readiness

Claim dispositions

Where used in claim records, the following terms distinguish different situations:

Disposition| Meaning
"OPEN"| Unresolved or active
"FROZEN"| A specified artifact or version is locked for audit
"BLOCKED"| A required gate prevents promotion
"QUARANTINED"| Preserved but excluded from promotion pending resolution
"DEPRECATED"| An obsolete representation or artifact retained for provenance
"SUPERSEDED"| Replaced by a successor
"RETRACTED"| Withdrawn and no longer to be relied on as stated
"REFUTED"| The stated claim is contradicted by a valid counterexample or argument

A claim may have computational evidence while its proof remains open. A proof candidate may be mathematically promising while its formalization remains incomplete. A refuted statement must not be silently rewritten as if the original statement had been correct.

Promotion principle

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

Research workflow

AQARION uses an evidence-first workflow:

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

The order may be adapted to the research problem, but the evidence distinctions must remain intact.

A failed check is retained as evidence. A counterexample is not hidden. A correction does not erase the history of the error. A finite computation does not become a theorem merely by being repeated.

---

Active research lines

1. Invariant-partition enumeration

Research into invariant partitions of finite permutations, including cycle decompositions, phase structure, weighted Bell-type formulas, and direct enumeration oracles.

The repository describes "AQ-FPR-006" as an analytical formula with bounded computational cross-checks. External independent reproduction and literature priority remain separate questions. Consult the "research map" (docs/RESEARCH-LINES.md) and "evidence ledger" (EVIDENCE-LEDGER.md) for the recorded scope and evidence.

2. Finite quotient defects

Research into invariant quotient structure through block-constant observable spaces and operator defects.

The work tracks definitions, projection conventions, transport-energy identities, rank claims, finite computations, and formalization obligations separately. Refuted rank claims and their counterexamples should remain available in the historical record.

No rank formula or refinement law should be generalized beyond the domain actually established by its proof.

3. Finite-quotient pullback rigidity

The PB-001 research line studies a function (T:X\to X), equivalence relations on (X), and the pullback relation

[
T^*E={(x,y)\in X^2:(Tx,Ty)\in E}.
]

Its central finite-quotient statement is that, if (X/E) is finite and (T^*E\subseteq E), then (T^*E=E).

The associated binary join-closure argument uses finite quotient permutations and a bipartite incidence graph.

The research document records an analytic proof candidate and reported finite computational evidence. Independent proof review, execution-artifact reconstruction, Lean formalization, axiom audit, and literature-priority review remain distinct obligations. Consult "PB-001" (AQARION-QUANTARION-AI/PB_001.md) for the detailed statement and current caveats.

4. Formalization and provenance

This research line concerns the connection between mathematical claims, source artifacts, execution, and formal proof.

The requirements include:

- Exact correspondence between a claim and the proposition formalized.
- Pinned toolchain and dependency versions.
- Reproducible clean builds.
- Explicit proof dependencies and axiom auditing.
- Separation of build health from mathematical certification.
- Artifact hashes and execution records.
- Preservation of open and failed obligations.

See the "formalization roadmap" (docs/FORMALIZATION.md) and "provenance policy" (docs/PROVENANCE.md).

---

Verification and reproducibility

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

Repository architecture

The repository contains mathematical research records and documented tooling architecture. The architecture is intended to keep mathematical content separate from reusable infrastructure.

Research records

The research-side directories preserve theorem statements, derivations, experiments, finite computation, formalization targets, and historical corrections.

Reusable tooling

The documented tooling architecture under "AQARION-QUANTARION-AI/TOOLS/" separates the following responsibilities:

Component| Intended responsibility
ClaimLock| Claim records, evidence classifications, dependencies, and promotion history
ProofGym| Executable mathematical verification workflows and adversarial fixtures
JOIN-STABILITY| Research and verification concerning pullback-stable equivalence relations and join closure
Replay| Deterministic computational reproduction and execution records
Verification| Exact checks, independent reconstruction, adversarial tests, and certificates
Provenance| Artifact hashes, environments, execution logs, and research-object metadata
Schemas| Shared machine-readable contracts
Skills| Documented, repeatable research workflows
CLI| Consistent interfaces to established tools
Exact| Reusable exact finite-mathematics utilities
Lean| Formalization targets, build records, and audits
Archive| Preserved historical, superseded, refuted, and quarantined material

This is a description of the intended architecture, not a guarantee that every listed component is implemented, complete, or stable.

Use the relevant source files, tests, workflow definitions, and execution records to determine the actual implementation state. See the "tools README" (AQARION-QUANTARION-AI/TOOLS/README.md) and "master file tree" (FILETREE.md).

---

Formal verification

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

The current recorded Lean status remains OPEN. See "FORMALIZATION.md" (docs/FORMALIZATION.md) for targets and outstanding obligations.

---

Corrections and historical provenance

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

See "HISTORICAL-CORRECTIONS.md" (docs/HISTORICAL-CORRECTIONS.md).

---

Publication and collaboration

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

Use "GitHub Issues" (https://github.com/quantarion369-arch/AQARION/issues) for questions, proposed corrections, reproducibility reports, and literature pointers.

---

Development and contribution standards

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

Quality gate

Before a tool is described as stable, establish that its source exists, its tests execute, its failure cases are meaningful, its reproduction instructions work, its documentation matches the implementation, and its CI actually runs.

Before a mathematical claim is promoted, establish the corresponding mathematical and evidentiary obligations independently.

---

Guiding principles

«Prove first. Verify exhaustively. Predict second. No free parameters.»

«Ideas may come from anywhere. Confidence comes from verification.»

«Do not promote a result beyond what its evidence establishes.»

---

AQARION — Evidence-First Mathematical Research
