# AQARION

> **Evidence-first mathematical research for finite dynamical systems, quotient structure, and reproducible verification.**

[![C3: Open](https://img.shields.io/badge/C3-OPEN-yellow?style=flat-square)](STATUS.md)
[![C4: Blocked](https://img.shields.io/badge/C4-BLOCKED-red?style=flat-square)](STATUS.md)
[![Lean: Open](https://img.shields.io/badge/Lean-OPEN-lightgrey?style=flat-square)](docs/FORMALIZATION.md)
[![SDS-002: Quarantined](https://img.shields.io/badge/SDS--002-QUARANTINED-orange?style=flat-square)](docs/HISTORICAL-CORRECTIONS.md)
[![Publication: Blocked](https://img.shields.io/badge/Publication-BLOCKED-red?style=flat-square)](STATUS.md)
[![Promotable: False](https://img.shields.io/badge/Promotable-false-lightgrey?style=flat-square)](STATUS.md)

AQARION is an open research project by **James A**, a Mathematical Research Developer. It studies finite dynamical systems, invariant quotients, Koopman operators, observable subspaces, exact enumeration, and formalizable computational mathematics.

The project is maintained as an auditable research record. It separates mathematical claims, implementations, finite computation, provenance, independent reconstruction, and formal proof.

> **Do not promote a result beyond what its evidence establishes.**

---

## Start Here

| Resource | Purpose |
|---|---|
| [Research map](docs/RESEARCH-LINES.md) | Overview of the active mathematical research lines |
| [Current status](STATUS.md) | Current governance, proof, verification, and promotion state |
| [Evidence ledger](EVIDENCE-LEDGER.md) | Claim-by-claim evidence, domain, receipt, and proof status |
| [Corrections and refutations](docs/HISTORICAL-CORRECTIONS.md) | Preserved counterexamples, retired claims, and corrected records |
| [Formalization roadmap](docs/FORMALIZATION.md) | Lean targets, checked theorems, open obligations, and environment notes |
| [Provenance policy](docs/PROVENANCE.md) | How claims, sources, code, executions, and receipts are connected |
| [Verification artifacts](AQARION-QUANTARION-AI/verification/) | Research-side executable checks and evidence packages |

---

## Research Focus

- **Finite dynamical systems** — deterministic maps, functional graphs, permutation dynamics, and invariant partitions
- **Quotient systems** — invariant equivalence relations, quotient maps, semiconjugacy, and exact closure
- **Operator theory** — Koopman pullbacks, observable subspaces, projections, and operator defects
- **Computational mathematics** — exact arithmetic, finite exhaustive checks, algorithmic cross-checks, and negative controls
- **Formal verification** — proof-oriented specifications, Lean formalization, and reproducible verification workflows

---

## Central Principle

AQARION distinguishes the following layers:

\[
\text{specification}
\neq
\text{implementation}
\neq
\text{execution}
\neq
\text{computation}
\neq
\text{inference}
\neq
\text{formal proof}
\neq
\text{provenance}.
\]

A computation can be exact yet answer the wrong question. A result can reproduce yet rely on the wrong specification. A formal theorem can compile while formalizing a proposition different from the intended research claim.

The project therefore records what is defined, what was run, what was compared, what is proved, what is refuted, and what remains open.

---

## Evidence Labels

| Label | Meaning |
|---|---|
| `[D]` | Defined |
| `[V]` | Verified computation over a declared domain |
| `[P]` | Mathematical proof |
| `[PV]` | Proved and computationally verified |
| `[C]` | Conjecture |
| `[R]` | Active research target |
| `[F]` | Refuted or killed claim |
| `[Q]` | Quarantined artifact or claim |

These labels are deliberately non-interchangeable:

```text
finite exhaustive check != universal theorem
different programs      != independent reproduction
repository artifact     != executed receipt
Lean source file        != checked Lean proof
matching output         != provenance equivalence
policy PASS             != mathematical truth
```

---

## Current Snapshot

| Layer | State |
|---|---|
| C3 | OPEN |
| C4 | BLOCKED |
| Lean formalization | OPEN |
| SDS-002 | QUARANTINED |
| Publication | BLOCKED |
| Promotion | BLOCKED |
| Promotable | false |

These are governance states, not mathematical conclusions. A new receipt, source file, or successful local run does not automatically promote a claim.

See [STATUS.md](STATUS.md) for the live ledger.

---

## Representative Mathematics

For a finite deterministic map \(T:X\to X\) and a partition \(\Pi\), AQARION studies the Koopman defect

\[
D_\Pi=(I-P_\Pi)K_TP_\Pi,
\]

where \(P_\Pi\) is block averaging and \(K_Tf=f\circ T\).

The defect records the failure of partition-constant observables to remain invariant under pullback:

\[
D_\Pi=0
\quad\Longleftrightarrow\quad
K_T(V_\Pi)\subseteq V_\Pi.
\]

This program connects finite quotient structure with exact operator calculations. It does not treat finite computation as a replacement for proof.

See [Defect and quotient research](docs/RESEARCH-LINES.md#defect-and-quotient-research).

---

## Active Research Lines

### Invariant-partition enumeration

AQARION studies invariant partitions of finite permutations using cycle decompositions, phase structure, weighted Bell-type formulas, and direct enumeration oracles.

- Primary artifact: `AQ-FPR-006`
- Status: analytically derived formula with bounded computational cross-checks
- External independent reproduction: not established
- Literature priority: open
- Lean status: open

See [FPR and permutation-block research](docs/RESEARCH-LINES.md#fpr-and-permutation-block-research).

### Finite quotient defects

AQARION studies invariant quotient structure using block-constant observable spaces and operator defects.

- Exact finite checks are retained as finite evidence
- Refuted rank claims are retained with explicit counterexamples
- Transport-energy identities, projection conventions, and rank statements are tracked separately
- Formalization and source-equivalence obligations remain distinct

See [Defect and quotient research](docs/RESEARCH-LINES.md#defect-and-quotient-research).

### Formalization and provenance

AQARION treats formalization and provenance as independent research obligations.

- A Lean file is not a checked theorem merely because it exists
- A theorem is not automatically the intended theorem merely because it compiles
- A script is not automatically an independent reconstruction merely because it is separate
- A repository path does not establish that the artifact was run

See [Formalization](docs/FORMALIZATION.md) and [Provenance](docs/PROVENANCE.md).

---

## Research Workflow

```text
claim
  ↓
freeze specification and conventions
  ↓
identify source and artifact boundary
  ↓
implement
  ↓
construct oracle and negative controls
  ↓
execute and preserve receipt
  ↓
compare against declared target
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
```

The purpose is not to maximize green checks. The purpose is to make the strongest resulting claim reliable, inspectable, and properly scoped.

---

## What AQARION Preserves

AQARION preserves:

- Definitions and frozen conventions
- Mathematical derivations
- Exact finite computations
- Execution receipts and domain declarations
- Negative controls and mutation witnesses
- Counterexamples and refuted claims
- Open proof obligations
- Formalization targets
- Historical corrections
- Provenance and repository-drift findings

A corrected result does not erase the record of the earlier error. A failed computation is not hidden. An unresolved proof obligation is not upgraded into a theorem by repetition.

See [Corrections and refutations](docs/HISTORICAL-CORRECTIONS.md).

---

## Collaboration

Collaboration is welcome in:

- Finite dynamical systems
- Operator and Koopman theory
- Quotient structures and congruences
- Exact combinatorial enumeration
- Reproducible mathematical computing
- Formal verification and Lean
- Research provenance and artifact engineering

Please use [issues](https://github.com/quantarion369-arch/AQARION/issues) and repository discussions for questions, corrections, reproducibility reports, and literature pointers.

---

## Guiding Rule

> **Prove first. Verify exhaustively. Predict second. No free parameters.**

> **Do not promote a result beyond what its evidence establishes.**

---

**AQARION — Evidence-First Research Intelligence**
```
