JOIN-STABILITY

Finite pullback-stable join verification package for AQARION.

«Prove First · Verify Exhaustively · Predict Second · No Free Parameters»

Purpose

JOIN-STABILITY is the AQARION research and verification package for the finite theorem:

[
T^{-1}(E)\le E,\qquad
T^{-1}(F)\le F
]

implies

[
T^{-1}(E\vee F)\le E\vee F
]

for equivalence relations E,F on a finite set X, where T:X\to X is deterministic.

The package separates:

- mathematical definitions,
- proof targets,
- executable verification,
- counterexamples and negative controls,
- reproducibility,
- provenance,
- receipts,
- and publication status.

A successful computation is not treated as a mathematical proof.

---

Scope

The primary theorem target is the finite case:

[
X\text{ finite},\qquad T:X\to X.
]

For equivalence relations E,F on X, define pullback stability by

[
x,E,y \Longrightarrow T(x),E,T(y).
]

Equivalently,

[
T^{-1}(E)\le E.
]

The target is closure under the lattice join:

[
T^{-1}(E\vee F)\le E\vee F.
]

The finiteness assumption is part of the theorem boundary.

The unrestricted infinite extension is not silently included in this package.

---

Proof Architecture

The current proof architecture is:

ID| Component
JS-00| Definitions
JS-01| Quotient map
JS-02| Kernel refinement
JS-03| Finite kernel equality
JS-04| x,E,y\iff T(x),E,T(y)
JS-05| Quotient permutation
JS-06| F-quotient permutation
JS-07| Join-chain characterization
JS-08| Chain lifting
JS-11| Finite pullback-stable join

The finite-cardinality step is explicit.

No executable result substitutes for the mathematical argument at JS-03 through JS-08.

---

Evidence Discipline

Evidence classes used by AQARION include:

- "[D]" Definition
- "[P]" Mathematical proof
- "[V]" Computational verification
- "[PV]" Proof plus verification
- "[C]" Conjecture
- "[R]" Research/investigation
- "KILLED" Refuted
- "QUARANTINED" Preserved but not promotable

The following distinctions are mandatory:

computation != proof
verification != proof
hash != proof
replay != proof
public execution != certification
formal build != automatic certification

A verification program must recompute the claimed result rather than merely reading an expected PASS value.

---

Package Contents

"manifest.json"

Canonical machine-readable package metadata.

This file is authoritative for the package identity, version, claims, dependencies, and source revision.

Do not create a second manifest with overlapping authority.

"zip-clone.md"

Human-readable reproduction contract.

It describes how this package is copied, executed, verified, and interpreted.

"claims.jsonl"

One machine-readable claim record per line.

Claims identify mathematical statements and their current status.

"evidence.jsonl"

Evidence records associated with claims.

Evidence must identify its class and source artifact.

"reproduce.sh"

Deterministic package entrypoint.

It must fail loudly when required inputs or verification components are missing.

"verify.py"

Independent package verifier.

It must reconstruct and check package state rather than trusting a stored PASS.

"fixtures/"

Explicit finite test instances.

Fixtures are inputs, not proofs.

"negative-controls/"

Deliberately invalid inputs used to ensure the verifier can detect failure.

"receipts/"

Generated verification records.

Receipts are outputs of verification and are not themselves mathematical proofs.

"docs/"

Long-form proof architecture, scope boundaries, and research notes.

---

Reproduction

From an extracted package:

./reproduce.sh

Equivalent direct invocation:

python3 verify.py

The verifier must return a non-zero exit status when required package material is missing, malformed, inconsistent, or fails verification.

A successful run means only that the declared verification procedure succeeded for the declared inputs.

---

Negative Controls

The package must test at least:

1. modified fixture
2. incorrect expected result
3. malformed fixture
4. invalid claim identifier
5. missing dependency
6. altered checksum
7. stale source revision
8. forged verification receipt

A verifier that reports PASS when one of these controls is intentionally corrupted is defective.

---

Boundary

This package concerns the finite theorem.

It does not automatically establish:

- the infinite analogue,
- arbitrary families of more than two equivalence relations,
- unrelated lattice operations,
- arbitrary endomorphisms of infinite sets,
- or any stronger theorem not explicitly recorded in "manifest.json".

Known counterexamples and killed claims remain part of the research record rather than being deleted.

---

Status

JOIN-STABILITY is an active AQARION research/verification package.

The repository package distinguishes mathematical status from executable evidence and governance status.

No public interface, ZIP archive, hash, or successful computation may silently promote an open proof target to a theorem.

---

Package Rule

The ZIP archive is a transport format.

The extracted directory is the executable research object.

The Git repository is the versioned source record.

A ZIP hash identifies bytes.

It does not establish mathematical correctness.
