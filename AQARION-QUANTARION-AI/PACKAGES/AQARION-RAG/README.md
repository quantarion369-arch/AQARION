# AQARION-RAG

Evidence-preserving retrieval-augmented research intelligence for AQARION.

## Status

PROPOSED — scaffold only. No retrieval, answering, or evaluation implemented yet.

## Governing principle

Retrieval establishes what a source says.
Replay establishes what an execution produced.
Mathematical proof establishes what follows from stated assumptions.
Formal verification establishes what a proof assistant checked.

AQARION-RAG must never silently convert one category of evidence into another.

## Scope (v0.1)

- Pin a small corpus of Markdown files to a commit SHA.
- Retrieve passages with citations bound to that snapshot.
- Abstain when evidence is missing or insufficient.
- Never execute commands, modify claims, or grant verification status.

## Placement

This package lives under PACKAGES because it is an application that consumes
and navigates evidence. It is not a verification authority; the authorities
remain in TOOLS (ClaimLock, Replay, ProofGym).
