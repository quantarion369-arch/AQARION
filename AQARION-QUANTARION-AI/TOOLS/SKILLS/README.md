AQARION TOOLS — SKILLS

Reusable procedural skills for building, auditing, verifying, formalizing, and packaging AQARION research artifacts.

This directory contains skills, not the implementations they operate on.

The distinction is intentional:

- "SKILLS/" describes repeatable procedures and audit workflows.
- "schemas/" will define machine-readable contracts.
- "verification/" will contain reusable verification implementations.
- "Replay/" will contain replay infrastructure.
- "ClaimLock/" will contain claim/provenance infrastructure.
- "PROOF-GYM/" will provide executable verification surfaces.
- "cli/" will provide command-line orchestration after the underlying contracts stabilize.

Current Skills

The current skill set is deliberately small. These are extracted from workflows already used in AQARION research rather than invented as a large framework in advance.

"CLAIMLOCK-AUDIT.md"

Procedure for auditing mathematical claims against their recorded evidence, dependencies, verification artifacts, formalization status, and promotion state.

Primary concerns:

- claim identity;
- evidence class;
- proof versus computation;
- verification domain;
- dependency integrity;
- formalization status;
- invalidation and quarantine history;
- unsupported or inflated wording.

"FILETREE-AUDIT.md"

Procedure for auditing repository structure against the actual artifact set.

Primary concerns:

- exact paths;
- exact capitalization;
- missing files;
- stale references;
- duplicated infrastructure;
- research/tool boundary;
- documentation-to-tree consistency;
- planned versus implemented structure.

This skill is especially important for AQARION because repository structure is part of reproducibility and because GitHub paths are case-sensitive in relevant environments.

"LEAN-BUILD-AUDIT.md"

Procedure for auditing Lean projects and build claims without confusing a successful build with completion of the underlying mathematics.

Primary concerns:

- pinned toolchain;
- dependency state;
- clean rebuilds;
- target selection;
- exact build commands;
- repeated build evidence;
- "sorry" / "admit" detection;
- imported theorem dependencies;
- generated artifacts;
- distinction between build success and theorem completion.

A successful pinned rebuild is recorded as successful build evidence. It is not silently reclassified as a completed proof if proof obligations remain elsewhere.

Planned Skill Families

The following names are the intended logical skill families. They do not imply that corresponding directories or files already exist.

SKILLS/
├── CLAIMLOCK-AUDIT.md
├── FILETREE-AUDIT.md
├── LEAN-BUILD-AUDIT.md
│
├── claimlock/             [planned]
├── verification/          [planned]
├── formalization/         [planned]
├── research/              [planned]
├── reproducibility/       [planned]
└── packaging/             [planned]

The current top-level skill files remain authoritative until a later refactor explicitly replaces them.

Relationship to "TOOLS/FILETREE.md"

The parent tool-tree currently establishes this development order:

TOOLS/
│
├── SKILLS/                ← START HERE
│
├── schemas/               ← define receipts/claims
├── verification/          ← extract exact verification utilities
├── Replay/                ← make replay reproducible
├── ClaimLock/             ← implement the claim ledger
├── PROOF-GYM/             ← connect executable verification material
└── cli/                   ← orchestrate stable contracts last

See:

"AQARION-QUANTARION-AI/TOOLS/FILETREE.md"

The conceptual lowercase names in that planning tree are not instructions to rename the existing "SKILLS" directory. The repository's actual path is:

"AQARION-QUANTARION-AI/TOOLS/SKILLS/"

Skill Design Standard

Every AQARION skill should be:

1. Specific — one recognizable research or engineering procedure.
2. Executable — gives concrete steps and commands where applicable.
3. Evidence-aware — distinguishes observation, computation, verification, proof, and formalization.
4. Path-exact — uses repository paths and filenames exactly as they exist.
5. Adversarial — includes failure modes and negative controls where appropriate.
6. Reproducible — records inputs, environment, commands, outputs, and relevant hashes.
7. Non-promotional — never upgrades a result merely because a workflow succeeded.
8. Composable — can later be connected to schemas, verification tools, Replay, ClaimLock, ProofGym, and CLI infrastructure.

Evidence Discipline

AQARION uses the following evidence vocabulary:

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

In particular:

SEARCH              != REPRODUCED
REPRODUCED          != PROVED
PROVED              != FORMALLY VERIFIED
FORMALLY VERIFIED   != REPOSITORY-WIDE CERTIFICATION
PUBLIC              != CERTIFIED

Historical Principle

Skills are extracted from actual AQARION work.

They should preserve useful negative information, including:

- killed conjectures;
- failed proof attempts;
- counterexamples;
- implementation bugs;
- incorrect shortcuts;
- provenance gaps;
- incomplete formalization;
- successful builds that establish only build status.

The purpose is not to rewrite research history into a cleaner narrative. The purpose is to make the research process reusable and auditable.

Next Extraction Targets

After the three current skills are stable, the next extraction targets should come from existing AQARION workflows rather than from speculative framework design.

Priority areas include:

1. verification procedures already exercised in exact finite research;
2. provenance and replay procedures already used for independent reconstruction;
3. formalization/build procedures already used with pinned Lean environments;
4. packaging procedures for claims, fixtures, receipts, manifests, and reports;
5. research procedures for adversarial testing and promotion decisions.

Implementation should follow the contracts established by the skills. The skills should not be retrofitted to whatever implementation happens to exist later.

Status

Status: ACTIVE — initial skill layer established.

Current files:

- "CLAIMLOCK-AUDIT.md"
- "FILETREE-AUDIT.md"
- "LEAN-BUILD-AUDIT.md"
- "FILETREE.md"
- "README.md"

Scope: procedural infrastructure only.

Certification: this directory is infrastructure documentation; the existence of a skill does not certify any mathematical claim processed by that skill.
