#AQARION-QUANTARION-AI

Research spine for AQARION — finite dynamical systems, pullback-stable joins, defect operators, quotient geometry, and reproducible verification infrastructure.

«Prove First · Verify Exhaustively · Predict Second · No Free Parameters»

This directory is the current canonical research root under quantarion369-arch/AQARION.

It contains the mathematical research, documentation, verification material, and reusable tooling that together form the auditable AQARION record.

Historical lineage: JASKSG9 → Current: quantarion369-arch

---

Folder Map — What You Are Looking At

This screenshot shows:

AQARION-QUANTARION-AI/
├── DOCS/
├── TOOLS/
├── scripts/
├── verification/
└── PB_001.md

This README lives at AQARION-QUANTARION-AI/README.md and is the entry point for this folder.

---

Purpose

AQARION-QUANTARION-AI/ exists to keep five concerns distinct:

Mathematical definitions and theorems
Computational verification
Reusable infrastructure
Provenance and reproducibility
Publication and certification status

A file's location does not promote its evidence class. A file in verification/ is not automatically verified. A file in TOOLS/ is not automatically stable. Promotion requires an explicit evidence gate.

---

Subdirectories

DOCS/

Long-form documentation, checkpoints, design notes, proof architecture, evidence logs, and research ledgers.

Contains:

CHECKPOINTS/ — time-stamped research checkpoints (e.g., AQ-S5, AQ-S29)
Proof plans JS-00 through JS-11
Evidence boundaries
Scope notes (finite vs infinite)
Counterexample records

DOCS is narrative and archival. It does not execute. It explains why a result is what it claims to be.

Last commit in your screenshot: 2 days ago — active.

TOOLS/

Reusable research infrastructure. This is the extraction layer — not the research itself.

TOOLS/
├── README.md               # Tooling overview (406 lines, canonical)
├── FILETREE.md             # Master filetree (924 lines)
├── CLAIMLOCK/
│   ├── README.md           # Claim / evidence / provenance control
│   └── schemas/
├── PROOF-GYM/
│   ├── README.md           # Executable verification surface
│   ├── fixtures/
│   └── verification/
├── JOIN-STABILITY/
│   ├── README.md           # Finite theorem package
│   ├── definitions/
│   ├── proofs/
│   ├── verification/
│   └── counterexamples/
├── REPLAY/
├── VERIFICATION/
├── PROVENANCE/
├── SCHEMAS/
├── SKILLS/
│   ├── README.md
│   ├── CLAIMLOCK-AUDIT.md
│   ├── FILETREE-AUDIT.md
│   └── LEAN-BUILD-AUDIT.md
├── CLI/
├── EXACT/
├── LEAN/
└── ARCHIVE/
    ├── README.md
    ├── deprecated/
    ├── retracted/
    ├── refuted/
    ├── superseded/
    ├── quarantined/
    └── historical/

Last commit in your screenshot: 2 minutes ago — this is your current working layer.

Tools must be:

deterministic
path-exact (case-sensitive)
tested with negative controls
reproducible with hashes
documented with input/output contracts

No tool receives a stronger status merely because it has a polished interface.

scripts/

Operational scripts for building, verifying, hashing, and reproducing research artifacts.

Contains helpers for:

manifest generation
hash verification
replay entrypoints
RO-Crate packaging
checkpoint archiving

Scripts must fail loudly when required inputs are missing. Scripts must not hard-code PASS.

Last commit: 3 days ago.

verification/

Independent verification material for results claimed in AQARION-QUANTARION-AI/.

exact finite enumeration
adversarial fixtures
independent reconstruction
Lean build logs
verification receipts with source_hash, implementation_hash, output_hash

A successful verification run means only that the declared verification procedure succeeded for the declared inputs. It does not establish certification by itself.

Last commit: 1 hour ago — actively worked.

PB_001.md

Problem Book entry 001 — the first canonical problem statement for the finite pullback-stable join theorem.

Type: [P] / [V] target

Status: OPEN → FROZEN when audit-locked

It defines:

finite set X
deterministic map T : X → X
equivalence relations E, F with T^{-1}(E) ≤ E, T^{-1}(F) ≤ F
target T^{-1}(E ∨ F) ≤ E ∨ F

PB_001 is the mathematical anchor that TOOLS/JOIN-STABILITY/ verifies and DOCS/ documents.

Last commit: 2 days ago.

---

Evidence Discipline — Canonical Vocabulary

AQARION distinguishes evidence class from claim disposition. They must never be conflated.

Evidence Classes

| Code | Meaning |
|---|---|
| [D] | Definition |
| [P] | Mathematical proof |
| [V] | Exhaustive or independently reproducible verification |
| [PV] | Proof + verification |
| [C] | Conjecture |
| [R] | Research / investigation |

Claim Dispositions

| Disposition | Meaning |
|---|---|
| OPEN | Research remains active or unresolved |
| FROZEN | Artifact/version locked for audit |
| BLOCKED | Declared gate prevents promotion or publication |
| QUARANTINED | Evidence retained but excluded from promotion pending resolution |
| DEPRECATED | Obsolete representation retained for provenance |
| SUPERSEDED | Replaced by successor claim or artifact |
| RETRACTED | Withdrawn because result should no longer be relied upon as stated |
| REFUTED | Counterexample or contradiction exists |

These are deliberately distinct:

REFUTED ≠ RETRACTED
RETRACTED ≠ SUPERSEDED
SUPERSEDED is not necessarily false
DEPRECATED does not mean mathematically false
FROZEN does not mean proved
BLOCKED does not mean false
QUARANTINED does not mean refuted

Legacy Mapping

KILLED is not a current disposition. Historical records may contain it. Migration must be explicit:

legacy: KILLED + reason=COUNTEREXAMPLE  →  REFUTED
legacy: KILLED + reason=IMPLEMENTATION_ERROR → RETRACTED
legacy: KILLED + reason=REPLACED → SUPERSEDED
legacy: KILLED + reason=OBSOLETE_REPRESENTATION → DEPRECATED

No silent rewrite of historical wording during provenance reconstruction.

Evidence Boundaries

SEARCH              != REPRODUCED
REPRODUCED          != INDEPENDENTLY VERIFIED
COMPUTED            != PROVED
PROVED              != FORMALLY VERIFIED
FORMALLY VERIFIED   != AUTOMATICALLY CERTIFIED
PUBLIC              != CERTIFIED

---

Promotion Rule

Promotion is evidence-driven, never interface-driven.

A claim is not promoted because:

a README says PASS
a CI job passed
a finite experiment found no counterexample
an AI system asserted it
a public post received attention

Promotion requires the declared gate for that claim: exact proof, independent verification, hash, receipt, and audit.

---

Reproducibility

Every computational claim in this folder should be answerable:

What exactly is being claimed?
Under what assumptions?
Over what domain (e.g., n ≤ 5, |X| ≤ 8)?
What was computed?
What was proved?
What was formally checked?
Can it be rerun via reproduce.sh / verify.py?
What hashes identify source and output?
What does it NOT establish?

If those answers are missing, the result remains [R] or [C], not [P] or [PV].

---

Current Build Order for This Root

AQARION-QUANTARION-AI/README.md          ← YOU ARE HERE
        │
DOCS/CHECKPOINTS/
        │
TOOLS/README.md + FILETREE.md
        │
TOOLS/SKILLS/ + CLAIMLOCK/
        │
TOOLS/PROOF-GYM/ + JOIN-STABILITY/
        │
verification/ + scripts/
        │
PB_001.md frozen + receipts/

Do not build the entire tree at once. Extract what has actually been learned.

---

Numerical Census Note

Exact finite census for n ≤ 5:

1 + 4 + 27 + 256 + 3125 = 3413 maps — corrected from 3412

This is verification evidence [V], not proof [P] of a universal theorem.

---

Continuity Notice

Earlier AQARION work was developed under JASKSG9. Current development is under quantarion369-arch/AQARION.

This folder is the current working home. Historical material is preserved as provenance where accessible, not silently rewritten to appear as current.

Policy: preserve → identify → reconstruct → compare → hash → verify

Missing history is not filled by inference.

---

Governing Principle
Ideas may come from anywhere. Confidence comes from verification.
​
Preserve the history. Correct the claim. Do not manufacture continuity.
AQARION exists to make verification explicit, reproducible, and auditable.

---

Status

Folder: AQARION-QUANTARION-AI/
Status: ACTIVE — research spine
Last verified: your screenshot shows 2 min ago (TOOLS), 1 hour ago (verification)
Certification: no file location certifies a claim by itself

---

License

Apache License 2.0 — Copyright 2026 James Aaron / quantarion369-arch / AQARION Project

Canonical Links

Main repo: https://github.com/quantarion369-arch/AQARION
TOOLS: https://github.com/quantarion369-arch/AQARION/tree/main/AQARION-QUANTARION-AI/TOOLS
Filetree: https://github.com/quantarion369-arch/AQARION/blob/main/FILETREE.md
Push this as:
AQARION-QUANTARION-AI/README.md
It now gives GitHub a front-page README when someone clicks into that folder — exactly what was missing in your screenshot.
