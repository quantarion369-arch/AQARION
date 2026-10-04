# AQARION TOOLS — CLAIMLOCK

Claim and evidence management infrastructure for AQARION.

## Purpose

ClaimLock records the relationship between a mathematical claim and the evidence that supports, limits, invalidates, or leaves it unresolved.

ClaimLock is a control layer. It does not prove claims.

## Core Objects

A ClaimLock record should identify:

- claim id
- statement
- evidence class
- proof artifact + hash
- verification artifact + hash
- dependencies
- formalization status
- reproduction instructions
- invalidation history
- successor / witness / correction links

## Evidence Classes

| Code | Meaning |
|---|---|
| `[D]` | Definition |
| `[P]` | Mathematical proof |
| `[V]` | Verification |
| `[PV]` | Proof + verification |
| `[C]` | Conjecture |
| `[R]` | Research |
| `DEPRECATED` | Refuted or invalidated — was KILLED — retained for provenance, excluded from promotion |
| `SUPERSEDED` | Replaced by successor |
| `RETRACTED` | Withdrawn due to error |
| `REFUTED` | Counterexample exists |
| `QUARANTINED` | Retained but not currently promotable |
| `FROZEN` | Locked audit |
| `BLOCKED` | Publication blocked |
| `OPEN` | Open research |

Evidence does not upgrade automatically.

## Invalidation

Deprecated or superseded claims remain identifiable.
Versioned artifacts remain traceable.
Corrections are recorded, not silently rewritten.

Legacy: `KILLED` is deprecated term — use `DEPRECATED` with reason `IMPLEMENTATION_ERROR | REFUTED | RETRACTED`.

## License

Apache License 2.0 — Copyright 2026 James Aaron / quantarion369-arch / AQARION
