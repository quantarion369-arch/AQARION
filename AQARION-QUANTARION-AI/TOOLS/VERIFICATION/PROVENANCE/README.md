AQARION TOOLS — PROVENANCE

Execution and artifact provenance infrastructure for AQARION.

Purpose

"PROVENANCE/" records where an artifact came from, how it was produced, and which exact source and environment produced a reported result.

Provenance supports reproducibility and auditability.

It does not establish mathematical truth.

Provenance families

- "manifests/" — artifact and file inventories.
- "hashes/" — cryptographic hashes of defined artifacts.
- "environments/" — toolchain, OS, architecture, and dependency records.
- "runs/" — execution metadata and logs.
- "ro-crate/" — research-object packaging.

Minimum useful provenance

Where applicable, record:

repository
commit
path
artifact
artifact_hash
command
runtime
operating_system
architecture
dependency_versions
input_hashes
output_hashes
verifier
verifier_revision

Hash discipline

A matching hash establishes correspondence to a recorded artifact.

It does not establish:

- mathematical correctness;
- correct implementation of the intended theorem;
- independent verification;
- proof completeness.

Relationship to Replay

PROVENANCE
    ↓
REPLAY
    ↓
VERIFICATION
    ↓
CLAIMLOCK

This is a conceptual dependency, not an automatic certification pipeline.

RO-Crate

RO-Crate packaging belongs here when actually implemented.

The presence of RO-Crate metadata does not itself certify the contained research.

Status

DOCUMENTED — implementation follows shared schema and replay requirements.
