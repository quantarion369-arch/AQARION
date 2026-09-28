AQARION MATHEMATICAL-KERNEL — FILETREE

Purpose

This directory contains the canonical mathematical decomposition of the AQARION finite-dynamics program.

The tree is intentionally small.

A mathematical object belongs here only if it defines, proves, constrains, refutes, or formally targets a theorem in the kernel.

---

MATHEMATICAL-KERNEL/
│
├── README.md
├── FILETREE.md
│
├── 00-DEFINITIONS/
│   ├── finite-dynamics.md
│   ├── partitions.md
│   ├── quotient.md
│   ├── equivalence-relations.md
│   └── notation.md
│
├── 01-OBSERVABLE-QUOTIENT/
│   ├── projector.md
│   ├── koopman.md
│   ├── defect.md
│   └── quotient-criterion.md
│
├── 02-DEFECT-RANK/
│   ├── defect-graph.md
│   ├── incidence-rank.md
│   ├── rank-bound.md
│   └── global-maximum.md
│
├── 03-PULLBACK-STABILITY/
│   ├── definition.md
│   ├── kernel-refinement.md
│   ├── finite-kernel-equality.md
│   └── quotient-permutation.md
│
├── 04-JOIN-STABILITY/
│   ├── incidence-relation.md
│   ├── join-components.md
│   ├── incidence-automorphism.md
│   ├── finite-join-theorem.md
│   └── chain-lifting.md
│
├── 05-BOUNDARY/
│   ├── infinite-counterexample.md
│   ├── unrestricted-theorem-killed.md
│   └── historical-failed-routes.md
│
├── 06-VERIFICATION-TARGETS/
│   ├── brt-census.md
│   ├── join-census.md
│   ├── negative-controls.md
│   └── reproduction-contract.md
│
├── 07-FORMALIZATION/
│   ├── lean-dependency-map.md
│   ├── theorem-targets.md
│   └── formalization-status.md
│
└── 08-LITERATURE/
    ├── universal-algebra.md
    ├── transformation-semigroups.md
    ├── finite-dynamics.md
    └── novelty-audit.md

---

Boundary Rule

The following belong elsewhere:

execution logs       → VERIFICATION / REPLAY
hashes               → PROVENANCE
claim metadata       → CLAIMLOCK
generic schemas      → SCHEMAS
CI                   → .github / CI infrastructure
application code     → PROOF-GYM or research repository
raw experiments      → research repository

The mathematical kernel records what the mathematics is.

---

Canonical Dependency Direction

DEFINITIONS
    ↓
THEOREMS
    ↓
BOUNDARY RESULTS
    ↓
VERIFICATION TARGETS
    ↓
FORMALIZATION TARGETS
    ↓
CLAIMLOCK / PROMOTION

No reverse dependency should be introduced merely to make a certification artifact convenient.

---

Canonical Theorem IDs

AQ-00   finite deterministic dynamics
AQ-01   partition / block-constant space
AQ-02   block projector
AQ-03   Koopman pullback
AQ-04   defect operator
AQ-05   quotient criterion

BRT-01  defect graph
BRT-02  defect-rank identity
BRT-03  sharp rank bound
BRT-04  global rank maximum

JS-00   pullback stability
JS-01   quotient kernel refinement
JS-02   finite kernel equality
JS-03   quotient permutation
JS-G01  incidence graph
JS-G02  join = component relation
JS-G03  incidence automorphism
JS-11   finite pullback-stable join

NEG-01  infinite counterexample
NEG-02  unrestricted theorem killed

IDs are stable identifiers.

File names may evolve; theorem IDs should not.
