# AQARION TOOLS — CLAIMLOCK

Claim and evidence management infrastructure for AQARION.

ClaimLock records the relationship between a research claim and the
evidence that supports, limits, contradicts, invalidates, supersedes,
or leaves that claim unresolved.

ClaimLock is a control layer.

It does not prove mathematical claims.

---

## 1. Purpose

A research result may have several independent dimensions of status:

- mathematical statement;
- assumptions and definitions;
- computational evidence;
- independent verification;
- formalization;
- reproducibility;
- provenance;
- contradiction or refutation;
- publication/promotion state.

ClaimLock keeps these dimensions explicit.

The central rule is:

> Evidence status must never become stronger merely because a file,
> program, CI job, agent, or public repository says that it is stronger.

ClaimLock records evidence.

It does not manufacture evidence.

---

## 2. Claim Object

A ClaimLock record should identify, where applicable:

- claim ID;
- claim version;
- exact statement;
- definitions;
- hypotheses;
- scope;
- evidence class;
- proof artifact;
- proof artifact hash;
- verification artifact;
- verification artifact hash;
- computation scope;
- formalization status;
- dependencies;
- source revision;
- reproduction instructions;
- provenance;
- limitations;
- counterexamples;
- correction records;
- successor claims;
- supersession history;
- retraction history;
- promotion history.

A claim record should make it possible to answer:

1. What exactly is being claimed?
2. Under what assumptions?
3. Over what domain?
4. What evidence exists?
5. What evidence does not exist?
6. Can the computation be reproduced?
7. Is the statement formally checked?
8. Has it been contradicted?
9. Has it been superseded?
10. What is the current disposition?

---

## 3. Evidence Classes

Evidence class describes the kind of research object being recorded.

| Code | Meaning |
|---|---|
| `[D]` | Definition |
| `[P]` | Mathematical proof |
| `[V]` | Exhaustive or independently reproducible verification |
| `[PV]` | Proof + verification |
| `[C]` | Conjecture |
| `[R]` | Research / investigation |

Evidence class does not itself determine promotion.

For example:

`[V]` means that a verification artifact exists.

It does not mean:

- the underlying theorem has been proved;
- the implementation is mathematically correct;
- the scope is universal;
- the result is formally verified;
- the claim is publication-ready.

---

## 4. Claim Dispositions

Disposition describes the current state of a claim or research object.

| Disposition | Meaning |
|---|---|
| `OPEN` | Research remains active or unresolved |
| `FROZEN` | The specified artifact/version is locked for audit |
| `BLOCKED` | A declared gate prevents promotion or publication |
| `QUARANTINED` | Evidence is retained but excluded from promotion pending resolution |
| `DEPRECATED` | The artifact or representation is obsolete and retained for provenance |
| `SUPERSEDED` | Replaced by a successor claim or artifact |
| `RETRACTED` | Withdrawn because the result should no longer be relied upon as stated |
| `REFUTED` | A counterexample or contradiction establishes that the stated claim is false |

These dispositions are deliberately distinct.

In particular:

- `REFUTED` is not the same as `RETRACTED`;
- `RETRACTED` is not the same as `SUPERSEDED`;
- `SUPERSEDED` is not necessarily false;
- `DEPRECATED` does not mean mathematically false;
- `FROZEN` does not mean mathematically proved;
- `BLOCKED` does not mean mathematically false;
- `QUARANTINED` does not mean refuted.

---

## 5. Disposition Selection Rules

Use the most specific disposition supported by the evidence.

### OPEN

Use `OPEN` when research remains active or unresolved.

Examples:

- proof incomplete;
- literature comparison incomplete;
- formalization incomplete;
- computational question still under investigation.

### FROZEN

Use `FROZEN` when a particular artifact or version is intentionally
locked for audit.

`FROZEN` means:

> This exact object is the object being audited.

It does not mean:

> This object is mathematically correct.

### BLOCKED

Use `BLOCKED` when a declared gate prevents promotion or publication.

Examples:

- missing independent reproduction;
- missing certificate;
- unresolved provenance;
- failed required audit;
- formalization gate not satisfied.

### QUARANTINED

Use `QUARANTINED` when evidence is worth preserving but is excluded
from promotion pending resolution.

Examples:

- suspicious but not disproved result;
- incomplete reproduction;
- unresolved implementation discrepancy;
- result awaiting independent reconstruction.

### DEPRECATED

Use `DEPRECATED` when an artifact or representation is obsolete and
should no longer be used as the current representation.

The historical artifact may remain valid provenance.

### SUPERSEDED

Use `SUPERSEDED` when a successor claim or artifact replaces the
previous one.

Supersession does not necessarily mean that the earlier claim was false.

### RETRACTED

Use `RETRACTED` when the project withdraws a result because it should
no longer be relied upon as stated.

Typical causes include:

- implementation error;
- incorrect derivation;
- unrecoverable provenance;
- invalid experimental procedure;
- discovered mismatch between stated and executed computation.

### REFUTED

Use `REFUTED` when a mathematical counterexample, contradiction, or
other decisive evidence establishes that the stated claim is false.

A refuted claim should identify the witness or contradiction whenever
possible.

---

## 6. Evidence and Disposition Are Separate

Evidence class and disposition answer different questions.

Evidence class asks:

> What kind of research object is this?

Disposition asks:

> What is its current state?

For example:

```text
evidence_class = [C]
disposition    = OPEN
