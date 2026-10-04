# AQARION PROOF-GYM

Executable mathematical verification surface for AQARION research.

ProofGym is a tooling/application layer for exposing finite mathematical
claims through exact computation, structured witnesses, verification
procedures, and reproducible evidence.

It is not a replacement for mathematical proof.

Its purpose is to make computational evidence inspectable.

## Purpose

ProofGym connects a mathematical claim to an executable verification
workflow.

The intended chain is:

MATHEMATICAL CLAIM

        │

        ▼

DEFINITIONS / INPUTS

        │

        ▼

EXACT COMPUTATION

        │

        ▼

STRUCTURED RESULT

        │

        ▼

VERIFICATION

        │

        ▼

EVIDENCE RECEIPT

Where a mathematical proof exists, the proof remains a separate
evidence artifact.

A successful computation does not automatically establish the theorem.

## Evidence Separation

ProofGym follows the AQARION evidence taxonomy:

Code| Meaning
"[D]"| Definition
"[P]"| Mathematical proof
"[V]"| Exhaustive or independently reproducible verification
"[PV]"| Proof + verification
"[C]"| Conjecture
"[R]"| Research / exploratory result
"DEPRECATED"| Obsolete representation — retained for provenance, excluded from promotion — was KILLED
"SUPERSEDED"| Replaced by successor
"RETRACTED"| Withdrawn due to error
"REFUTED"| Counterexample exists
"QUARANTINED"| Preserved but not currently promotable
"FROZEN"| Locked for audit
"BLOCKED"| Gate prevents promotion
"OPEN"| Active research

Evidence does not migrate upward automatically.

COMPUTATION!= PROOF

VERIFICATION!= FORMAL PROOF

FORMAL PROOF!= AUTOMATIC CERTIFICATION

PUBLIC RESULT!= CERTIFIED RESULT

## Current Mathematical Target

The primary ProofGym target is the JOIN-STABILITY research program.

The current theorem direction is:

T⁻¹(E) ≤ E

T⁻¹(F) ≤ F

with target:

T⁻¹(E ∨ F) ≤ E ∨ F.

Here:

- "X" is a finite set;
- "T : X → X" is a deterministic map;
- "E" and "F" are equivalence relations;
- "≤" denotes refinement/inclusion of equivalence relations;
- "E ∨ F" is their join.

The finite theorem is maintained as a mathematical proof problem and as an
independently testable computational problem.

These are separate evidence lanes.

## JOIN-STABILITY Proof Architecture

The current proof dependency plan is:

JS-00 Definitions

  │

  ▼

JS-01 Quotient map

  │

  ▼

JS-02 Kernel refinement

  │

  ▼

JS-03 Finite kernel equality

  │

  ▼

JS-04 x E y ↔ Tx E Ty

  │

  ▼

JS-05 Quotient permutation

  │

  ▼

JS-06 F quotient permutation

  │

  ▼

JS-07 Join-chain characterization

  │

  ▼

JS-08 Chain lifting

  │

  ▼

JOIN-STABILITY THEOREM

The finite-cardinality step is explicit.

It must not be hidden inside a computational experiment.

## Verification Surface

ProofGym should expose computational verification through:

- exact finite instances;
- deterministic algorithms;
- structured witnesses;
- counterexample search;
- adversarial fixtures;
- invariant checks;
- verification receipts;
- reproducible inputs;
- explicit failure states.

A ProofGym verifier should be able to answer:

1. What mathematical object was evaluated?
2. What exact input was used?
3. What algorithm was executed?
4. What result was recomputed?
5. What invariant was checked?
6. Did the verification pass?
7. What evidence class does the result support?
8. What does the result not establish?

## No Hard-Coded PASS

A verifier must never manufacture a positive result.

Forbidden design:

if expected_result:

    PASS

Required design:

reconstruct input

       ↓

recompute independently

       ↓

evaluate invariant

       ↓

compare actual result

       ↓

PASS / FAIL

Expected values may be stored as fixtures, but they must never substitute
for recomputation.

## Adversarial Verification

ProofGym should preserve negative controls.

Examples include:

- modified fixtures;
- incorrect expected values;
- malformed inputs;
- altered maps;
- altered partitions;
- incorrect theorem parameters;
- deliberately truncated computations;
- invalid hashes;
- wrong recurrence depth;
- corrupted witnesses.

A verifier that only demonstrates successful positive examples is incomplete
as an audit surface.

## Independence

Where an independent verifier exists, ProofGym should not silently import the
producer's implementation as its verification mechanism.

The preferred architecture is:

PRODUCER

   │

   │ fixture / claim

   ▼

PROOF-GYM INPUT

   │

   ▼

INDEPENDENT RECONSTRUCTION

   │

   ▼

RECOMPUTATION

   │

   ▼

VERIFICATION RECEIPT

This distinction is particularly important for AQ-K2R and JOIN-STABILITY
research.

## Relationship to Mathematical Proof

ProofGym may verify consequences of a theorem without proving the theorem.

For example:

[P]

symbolic mathematical proof

and:

[V]

exhaustive finite verification

are complementary but distinct.

A large finite census can provide strong verification evidence while
remaining logically insufficient for a universal theorem.

Conversely, a mathematical proof may establish a theorem without requiring
exhaustive enumeration.

ProofGym records the distinction.

## Relationship to Lean

Lean formalization is a separate evidence lane.

A successful Lean build demonstrates that the specified Lean project and
selected targets build successfully under the recorded environment.

It does not by itself establish that:

- every informal claim has been formalized;
- every intended theorem is present;
- no theorem is imported from an unintended source;
- the project contains no admitted assumptions;
- the mathematical statement matches the intended research claim.

ProofGym may consume Lean verification artifacts, but it should not conflate
build status with mathematical certification.

## Receipts

A future ProofGym receipt should identify, where applicable:

claim_id

claim_version

input_hash

fixture_hash

algorithm

parameters

result

expected_result

verification_status

evidence_class

source_revision

verifier_revision

environment

timestamp

The exact machine-readable schema belongs in the shared "schemas/" layer once
that layer is established.

ProofGym should consume the schema rather than inventing a competing receipt
format.

## Repository Boundary

ProofGym belongs to the reusable tooling layer.

It should not become the canonical storage location for every AQARION research
result.

RESEARCH REPOSITORIES

    mathematical claims

    experiments

    papers

    datasets

    research-specific code

AQARION TOOLS

    reusable verification infrastructure

    receipts

    schemas

    replay

    claim management

    skills

PROOF-GYM

    executable mathematical verification surface

Research-specific mathematics should remain traceable to its source repository.

## Development Standard

Every ProofGym component should define:

- purpose;
- exact input contract;
- exact output contract;
- dependencies;
- deterministic behavior;
- verification procedure;
- failure conditions;
- evidence status;
- reproduction instructions.

No component should receive a stronger research status merely because it has a
successful interface.

## Initial Build Order

ProofGym should be built only after the underlying contracts are stable.

Recommended order:

1. README / scope

       ↓

2. input contract

       ↓

3. verification contract

       ↓

4. fixtures

       ↓

5. independent computation

       ↓

6. negative controls

       ↓

7. receipt schema

       ↓

8. CLI integration

       ↓

9. public application surface

The application should come after the verifier.

Not the other way around.

## Current Status

Directory: "AQARION-QUANTARION-AI/TOOLS/PROOF-GYM/"

Status: INITIAL INFRASTRUCTURE — README / contract stage.

Current role: executable mathematical verification surface.

Primary research connection: JOIN-STABILITY.

Certification: the existence of ProofGym does not certify any mathematical claim.

## Governing Principle

ProofGym exists to make computational evidence inspectable.

It does not exist to make computation look like proof.

«Ideas may come from anywhere. Confidence comes from verification.»

«Prove First · Verify Exhaustively · Predict Second · No Free Parameters.»

## License

Apache License 2.0 — Copyright 2026 James Aaron / quantarion369-arch / AQARION
