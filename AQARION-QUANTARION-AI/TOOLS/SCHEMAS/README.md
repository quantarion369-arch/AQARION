AQARION TOOLS — SCHEMAS

Shared machine-readable contracts for AQARION claims, evidence, receipts, provenance, fixtures, and manifests.

Purpose

"SCHEMAS/" defines representations shared by multiple tools.

It prevents ClaimLock, Replay, ProofGym, verification utilities, and provenance tooling from inventing incompatible formats for the same research object.

Schema families

- "claims/" — claim identity, statement, dependencies, status, and history.
- "evidence/" — evidence class and evidence metadata.
- "receipts/" — reproducibility and verification receipts.
- "provenance/" — execution environment and source provenance.
- "fixtures/" — deterministic verification inputs and expected structural metadata.
- "manifests/" — artifact and file manifests.

Design rules

1. Machine-readable contracts must be explicit.
2. Required fields must be versioned.
3. Unknown fields must not silently change semantic meaning.
4. Hashes identify artifacts; they do not establish mathematical correctness.
5. A schema version does not certify an artifact.
6. Backward-incompatible changes require a new schema version.
7. Examples must be clearly identified as examples.
8. Historical schemas remain traceable when superseded.

Evidence boundary

Schemas describe evidence. They do not create evidence.

Status

DOCUMENTED — schema layer initialized.

Implementation follows identification and testing of actual shared contracts.
