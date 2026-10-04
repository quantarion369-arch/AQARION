# AQARION TOOLS — MASTER FILETREE

Root: "AQARION-QUANTARION-AI/TOOLS/"

Purpose: Master index for reusable AQARION research infrastructure,
verification tooling, research skills, schemas, provenance, replay, and
certification support.

This tree is an architectural map. A directory or filename must not be treated
as implemented merely because it appears here.

Implementation status is tracked separately by the relevant "README.md",
claim ledger, audit, test, or verification artifact.

---

## MASTER TREE

AQARION-QUANTARION-AI/

└── TOOLS/

    │

    ├── README.md

    │

    ├── FILETREE.md

    │

    ├── PROOF-GYM/

    │   ├── README.md

    │   ├── FILETREE.md

    │   ├── fixtures/

    │   ├── verification/

    │   ├── receipts/

    │   ├── tests/

    │   └── cli/

    │

    ├── CLAIMLOCK/

    │   ├── README.md

    │   ├── FILETREE.md

    │   ├── claims/

    │   ├── schemas/

    │   ├── ledgers/

    │   ├── history/

    │   ├── invalidated/

    │   └── cli/

    │

    ├── REPLAY/

    │   ├── README.md

    │   ├── FILETREE.md

    │   ├── manifests/

    │   ├── environments/

    │   ├── runs/

    │   ├── receipts/

    │   └── cli/

    │

    ├── JOIN-STABILITY/

    │   ├── README.md

    │   ├── FILETREE.md

    │   ├── definitions/

    │   ├── proofs/

    │   ├── verification/

    │   ├── fixtures/

    │   ├── counterexamples/

    │   ├── receipts/

    │   └── lean/

    │

    ├── VERIFICATION/

    │   ├── README.md

    │   ├── FILETREE.md

    │   ├── exact/

    │   ├── independent/

    │   ├── adversarial/

    │   ├── negative-controls/

    │   ├── certificates/

    │   └── reports/

    │

    ├── PROVENANCE/

    │   ├── README.md

    │   ├── FILETREE.md

    │   ├── manifests/

    │   ├── hashes/

    │   ├── environments/

    │   ├── runs/

    │   └── ro-crate/

    │

    ├── SCHEMAS/

    │   ├── README.md

    │   ├── FILETREE.md

    │   ├── claims/

    │   ├── evidence/

    │   ├── receipts/

    │   ├── provenance/

    │   ├── fixtures/

    │   └── manifests/

    │

    ├── SKILLS/

    │   ├── README.md

    │   ├── FILETREE.md

    │   ├── CLAIMLOCK-AUDIT.md

    │   ├── FILETREE-AUDIT.md

    │   ├── LEAN-BUILD-AUDIT.md

    │   ├── REPOSITORY-AUDIT.md

    │   ├── VERIFICATION-AUDIT.md

    │   └── RESEARCH-REPLAY.md

    │

    ├── CLI/

    │   ├── README.md

    │   ├── FILETREE.md

    │   ├── aqarion.py

    │   ├── claimlock.py

    │   ├── proofgym.py

    │   ├── replay.py

    │   └── verify.py

    │

    ├── EXACT/

    │   ├── README.md

    │   ├── FILETREE.md

    │   ├── exact_proper.py

    │   ├── arithmetic.py

    │   ├── partitions.py

    │   ├── relations.py

    │   ├── graphs.py

    │   └── operators.py

    │

    ├── LEAN/

    │   ├── README.md

    │   ├── FILETREE.md

    │   ├── builds/

    │   ├── targets/

    │   ├── logs/

    │   ├── manifests/

    │   └── audit/

    │

    └── ARCHIVE/

        ├── README.md

        ├── FILETREE.md

        ├── deprecated/

        ├── retracted/

        ├── refuted/

        ├── superseded/

        ├── quarantined/

        └── historical/

---

## DIRECTORY ROLES

"PROOF-GYM/"

Executable mathematical verification surface.

Responsible for:

- exact finite verification;
- structured witnesses;
- deterministic checks;
- adversarial fixtures;
- negative controls;
- verification receipts;
- research-specific verification workflows.

ProofGym is not a proof system.

---

"CLAIMLOCK/"

Claim and evidence management.

Responsible for:

- claim identifiers;
- claim versions;
- evidence classes;
- dependencies;
- promotion history;
- invalidation history;
- links to proofs and verification artifacts.

ClaimLock is the provenance/control layer for mathematical claims.

---

"REPLAY/"

Deterministic research reproduction.

Responsible for recording and replaying:

- inputs;
- commands;
- environments;
- dependencies;
- source revisions;
- fixture hashes;
- verifier revisions;
- outputs;
- reproduction receipts.

Replay answers:

«Can the computational result be reproduced from the recorded research state?»

---

"JOIN-STABILITY/"

Reusable verification and proof infrastructure extracted from the
JOIN-STABILITY research program.

Responsible for:

- finite equivalence relations;
- joins;
- pullback stability;
- quotient-map arguments;
- chain lifting;
- finite permutation arguments;
- counterexample search;
- exhaustive verification;
- Lean targets.

This directory should contain reusable theorem-specific infrastructure, not
the entire historical research repository.

---

"VERIFICATION/"

Cross-project verification utilities.

Responsible for:

- exact verification;
- independent reconstruction;
- adversarial testing;
- negative controls;
- certificates;
- verification reports.

The directory should contain reusable mechanisms rather than duplicate
project-specific implementations.

---

"PROVENANCE/"

Research execution provenance.

Responsible for:

- SHA-256 manifests;
- environment records;
- runtime records;
- operating-system information;
- architecture;
- dependency versions;
- execution logs;
- RO-Crate metadata.

Hashes identify artifacts.

Hashes do not prove mathematical correctness.

---

"SCHEMAS/"

Shared machine-readable contracts.

Expected schema families include:

claims/

evidence/

receipts/

provenance/

fixtures/

manifests/

Schemas must be established before multiple tools independently invent
incompatible representations of the same research object.

---

"SKILLS/"

Reusable research workflows.

Skills describe how to perform a class of AQARION research task, rather than
implementing the underlying mathematics.

Current skills include:

CLAIMLOCK-AUDIT.md

FILETREE-AUDIT.md

LEAN-BUILD-AUDIT.md

REPOSITORY-AUDIT.md

VERIFICATION-AUDIT.md

RESEARCH-REPLAY.md

The "SKILLS/README.md" defines the skill contract.

---

"CLI/"

Command-line integration.

The CLI should eventually provide a consistent interface to:

claimlock

proofgym

replay

verify

The CLI must call established tool contracts rather than duplicate their
mathematical implementations.

---

"EXACT/"

Reusable exact finite mathematics utilities.

This is where "exact_proper.py" belongs if its actual responsibility is
confirmed to be reusable exact arithmetic / exact finite computation
infrastructure.

The important distinction is:

EXACT/exact_proper.py

must not be assumed to be the correct home merely because the filename sounds
appropriate.

Its actual imports, functions, callers, mathematical contract, and research
dependencies must be audited first.

Potential reusable modules include:

arithmetic.py

partitions.py

relations.py

graphs.py

operators.py

These should only be created when an actual reusable implementation exists.

---

"LEAN/"

Lean build and formalization infrastructure.

Responsible for:

- target declarations;
- reproducible build records;
- pinned rebuilds;
- build logs;
- formalization manifests;
- audit records.

Important distinction:

LEAN BUILD SUCCESS

        ≠

CLAIM CERTIFIED

A successful pinned two-target rebuild is valuable build evidence, but its
exact target names, commit, toolchain, and logs must remain recorded.

---

"ARCHIVE/"

Historical research preservation.

Contains:

- deprecated / retracted / refuted claims;
- quarantined claims;
- superseded implementations;
- historical research artifacts.

AQARION should preserve corrections rather than silently deleting the path by
which they were discovered.

---

## EVIDENCE BOUNDARY

The master tree intentionally separates:

RESEARCH

    ↓

EXACT COMPUTATION

    ↓

VERIFICATION

    ↓

PROVENANCE

    ↓

CLAIM MANAGEMENT

    ↓

FORMALIZATION

No directory location itself grants an evidence class.

A file inside "VERIFICATION/" is not automatically a verified result.

A file inside "LEAN/" is not automatically a proved theorem.

A file inside "CLAIMLOCK/" is not automatically a certified claim.

---

## IMPLEMENTATION STATUS

The following categories are used for this tree:

[EXISTS]

Directory/file currently exists.

[DOCUMENTED]

Architecture or contract documented.

[BUILDING]

Implementation currently being developed.

[PLANNED]

Reserved architectural location.

[AUDIT]

Requires inspection before promotion.

[EXPERIMENTAL]

Research implementation not yet promoted.

[ARCHIVE]

Historical material.

The tree itself should not claim "[EXISTS]" for files that have not actually
been pushed.

---

## CURRENT BUILD ORDER

The intended construction order is:

1. TOOLS/README.md

        │

2. TOOLS/FILETREE.md

        │

3. SKILLS/README.md

        │

4. SKILLS/skill contracts

        │

5. PROOF-GYM/README.md

        │

6. SCHEMAS/README.md

        │

7. CLAIMLOCK/README.md

        │

8. REPLAY/README.md

        │

9. VERIFICATION/README.md

        │

10. PROVENANCE/README.md

        │

11. EXACT/ audit

        │

12. JOIN-STABILITY/ extraction

        │

13. LEAN/ audit

        │

14. CLI integration

Do not implement the entire tree simultaneously.

Build the contracts first.

---

## IMPORTANT FILE-NAMING RULE

AQARION infrastructure is case-sensitive.

The canonical names in this tree are:

PROOF-GYM

CLAIMLOCK

REPLAY

JOIN-STABILITY

VERIFICATION

PROVENANCE

SCHEMAS

SKILLS

CLI

EXACT

LEAN

ARCHIVE

Do not silently substitute:

ProofGym

Proof-Gym

ClaimLock

Replay

Verification

Schemas

Skills

Exact

Lean

unless a separate repository contract explicitly requires those names.

On case-sensitive systems, these are different paths.

---

## IMPORTANT REPOSITORY RULE

The master tree is not permission to create empty speculative infrastructure.

Before adding an implementation:

1. confirm the directory;
2. inspect existing files;
3. identify the research artifact that produced the requirement;
4. define its input/output contract;
5. identify existing code that can be reused;
6. add tests;
7. add provenance;
8. only then promote it into reusable tooling.

The goal is extraction from real AQARION research, not framework-building for
its own sake.

---

## GOVERNING PRINCIPLE

EXTRACT WHAT WE HAVE ACTUALLY LEARNED.

DO NOT INVENT WHAT WE HAVE NOT BUILT.

AQARION infrastructure should make previous research easier to reproduce,
audit, verify, formalize, and reuse.

It should not obscure the distinction between historical experiments and
established results.

## License

Apache License 2.0 — Copyright 2026 James Aaron / quantarion369-arch / AQARION
