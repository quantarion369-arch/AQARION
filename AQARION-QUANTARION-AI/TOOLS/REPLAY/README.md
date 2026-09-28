AQARION TOOLS — REPLAY

Deterministic research reproduction infrastructure.

Purpose

Replay records enough information to reproduce a computational research result from a defined research state.

Replay answers:

«Can the recorded computation be rerun from its documented inputs, source state, environment, and procedure?»

Replay does not determine whether the underlying mathematical claim is true.

Replay chain

Question
  ↓
Conjecture
  ↓
Counterexample?
  ↓
Correction
  ↓
Computation
  ↓
Verification
  ↓
Receipt

Required provenance

Where applicable, record:

- source repository;
- commit or revision;
- input files;
- fixture hashes;
- algorithm;
- parameters;
- command;
- runtime;
- operating system;
- architecture;
- dependency versions;
- stdout/stderr;
- exit status;
- output artifacts;
- verifier revision;
- artifact hashes.

Reproducibility levels

- "REPLAY-DOCUMENTED" — instructions exist.
- "REPLAY-EXECUTED" — recorded execution succeeded.
- "REPLAY-INDEPENDENT" — execution was performed independently of the producer.
- "REPLAY-MISMATCH" — reproduction disagreed with the recorded result.
- "REPLAY-BLOCKED" — reproduction could not be completed and the reason is recorded.

A successful replay is reproducibility evidence, not mathematical proof.

Relationship to other tools

Replay:

- consumes shared schemas;
- records provenance;
- may invoke verification;
- may produce ProofGym receipts;
- may be referenced by ClaimLock.

Status

DOCUMENTED — implementation follows shared schema and provenance contracts.
