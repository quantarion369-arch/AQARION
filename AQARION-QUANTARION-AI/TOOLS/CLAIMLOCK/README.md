AQARION TOOLS — CLAIMLOCK

Claim and evidence management infrastructure for AQARION.

Purpose

ClaimLock records the relationship between a mathematical claim and the evidence that supports, limits, invalidates, or leaves it unresolved.

ClaimLock is a control layer. It does not prove claims.

Core objects

A ClaimLock record should identify:

- claim ID;
- exact statement;
- definitions and hypotheses;
- evidence class;
- verification domain;
- proof artifact;
- verification artifact;
- formalization status;
- dependencies;
- source revision;
- artifact hashes;
- reproduction instructions;
- limitations;
- invalidation history;
- promotion history.

Evidence classes

- "[D]" Definition
- "[P]" Mathematical proof
- "[V]" Exhaustive or independently reproducible verification
- "[PV]" Proof + verification
- "[C]" Conjecture
- "[R]" Research / exploratory result
- "KILLED" — refuted or invalidated
- "QUARANTINED" — retained but not currently promoted

Evidence does not upgrade automatically.

Invalidation

Killed or superseded claims remain identifiable.

Preserve:

- original statement;
- reason for invalidation;
- supporting counterexample or correction;
- revision;
- replacement claim, where applicable.

Boundary

ClaimLock manages claims.

It does not own:

- mathematical proofs;
- research-specific algorithms;
- Lean projects;
- generic replay execution;
- public application UI.

Those remain in their respective research or tooling layers.

Status

DOCUMENTED — implementation follows schema definition and extraction from existing AQARION claim workflows.

Certification: ClaimLock metadata does not certify the mathematical claim it describes.
