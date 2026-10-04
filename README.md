# AQARION

![AQARION D22 Direct Projection Validation]
![AQARION BRT Kernel Validation]

**Auditable Mathematical Research Infrastructure**

> **Repository continuity notice — September 2026**

AQARION development is currently maintained under the `quantarion369-arch` GitHub identity.

Earlier AQARION research exists across the author's previous `JASKSG9` identity and related fork lineage. Those materials are historical provenance and remain relevant to reconstruction and verification.

**Current canonical working repository:** `quantarion369-arch/AQARION`

This repository is the current working home for AQARION / Quantarion-AI research infrastructure, including:

- JOIN-STABILITY
- Theorem and mathematical-kernel infrastructure
- Verification and reproducibility tooling
- Provenance and evidence structures
- Research ledgers
- ClaimLock / ProofGym / Replay infrastructure
- Future reconstruction of earlier AQARION artifacts

### Account and Fork Transition

Active development is consolidated here rather than assuming continued access to `JASKSG9`.

1. Current canonical work — artifacts in `quantarion369-arch/AQARION`
2. Historical provenance — earlier AQARION material associated with `JASKSG9`
3. Fork lineage — repositories preserving part of development history
4. Reconstruction work — explicit recovery and verification of earlier artifacts
5. Verified current state — independently checked artifacts

**Reconstruction rule:**
HISTORICAL SOURCE → RECOVERED ARTIFACT → CONTENT COMPARISON → CURRENT LOCATION → HASH / VERSION / PROVENANCE → VERIFICATION STATUS

Historical material must not be silently rewritten as though it always existed here.

**Access-continuity principle:** This repository remains understandable without requiring future access to `JASKSG9`.

---

### Principle

**Preserve the history. Reconstruct explicitly. Verify independently. Never manufacture continuity.**

---

## What AQARION Is

AQARION is a research program for exact finite mathematics, dynamical systems, operator methods, computational verification, and reproducible software.

**Central objective:**
> Prove First · Verify Exhaustively · Predict Second · No Free Parameters

AQARION treats claims as evidence-bearing objects. Definitions, proofs, exhaustive computation, formal verification, conjectures, refutations, and observations are kept explicitly separated so computational agreement is never silently promoted to proof.

### Research Principles

- **Proof before promotion** — a computational observation is not a theorem
- **Exactness over approximation** — finite objects represented exactly whenever possible
- **Independent verification** — proofs and computational checks are separate lanes
- **Reproducibility by construction** — experiments rerunnable from documented inputs
- **Provenance without mythology** — AI assistance may be part of process, but certification concerns artifact and verification, not authorship inference

### Evidence Classes

| Code | Meaning |
|---|---|
| `[D]` | Definition |
| `[P]` | Mathematical proof |
| `[V]` | Exhaustive or independently reproducible verification |
| `[PV]` | Proof + verification |
| `[C]` | Conjecture |
| `[R]` | Research / exploratory result |
| `DEPRECATED` | Refuted, superseded, or invalidated claim — retained for audit, not promoted |
| `SUPERSEDED` | Replaced by newer claim — see successor |
| `RETRACTED` | Withdrawn due to error — see correction record |
| `REFUTED` | Counterexample exists — see witness |
| `QUARANTINED` | Evidence retained but not currently promoted |

**Governance:** Evidence does not migrate upward automatically.

- Numerical match ≠ proof
- Successful search ≠ certification
- Formalization containing `sorry`/`admit` ≠ completed proof
- Public repository ≠ mathematical certification

---

## What AQARION Studies

Recurring construction:

D_Π = (I - P_Π) K P_Π

where:
- `T: X → X` is a finite dynamical system
- `K` is the Koopman pullback operator
- `Π` is a partition of `X`
- `P_Π` projects onto block-constant observables
- `D_Π` measures failure of partition to be closed under dynamics

Framework: `finite dynamics → quotient structure → operator theory → graph structure → exact computation → formal verification`

### Core Results

- `D_Π = 0` exactly when partition is dynamically closed
- `D_Π = 0` exactly when quotient dynamics is well-defined
- `D_Π² = 0` for every idempotent projection `P_Π`
- `PK = KP` is sufficient for `D_Π = 0`, but not necessary
- Exact rank formulas connect defect operator with complement graph
- Exact Frobenius-energy identity provides quantitative defect measure
- Large finite censuses used as independent verification

Formalization status tracked separately from computational verification.

---

## Research Programs

### JOIN-STABILITY
Finite-set theorem program studying pullback-stable equivalence relations and their joins.

Current work:
- finite kernel-equality arguments
- quotient-map injectivity and permutation structure
- incidence-graph formulations
- chain-lifting proofs
- adversarial counterexample search
- exhaustive finite verification
- formalization planning

### ProofGym
Executable verification surface: exact instances, structured witnesses, deterministic verification, adversarial fixtures, proof dependencies, evidence traces, reproducible receipts.

Goal: make computational evidence auditable, not replace proof with software.

### ClaimLock
Claim/provenance layer associating claims with evidence status, proof artifacts, verification artifacts, hashes, dependencies, reproduction instructions, invalidation history.

### Replay
Records enough to rerun computational research, not merely display result.

Chain: `Question → Conjecture → Counterexample? → Correction → Computation → Proof → Verification → Hash`

---

## Tools

Reusable infrastructure consolidated under: `AQARION-QUANTARION-AI/TOOLS/`

TOOLS/
├── ClaimLock/
├── ProofGym/
├── JOIN-STABILITY/
├── Replay/
├── verification/
├── provenance/
├── schemas/
├── skills/
└── cli/

Boundary: research repos contain investigations; TOOLS contains reusable infrastructure.

---

## Reproducibility

Artifacts designed around:
- deterministic computation
- exact finite enumeration
- independent verification
- machine-readable claim registries
- verification reports
- SHA-256 manifests
- Lean formalization
- Dockerized environments
- CI checks
- RO-Crate metadata
- research ledgers
- explicit evidence status

A target artifact should allow independent researcher to answer:
1. What is claimed?
2. What definitions does it depend on?
3. What constitutes proof?
4. What was computationally verified?
5. What remains conjectural?
6. Can verification be rerun?
7. Which exact files produced result?
8. Which version/hash was evaluated?

---

## AI and Research Provenance

AQARION does not infer whether result was “really produced by AI” from final artifact.

Question is: **Can claim, computation, proof, and verification be independently inspected and reproduced?**

AI systems treated as research-process nodes, not mathematical authorities.

- AI conjecture remains conjecture
- AI proof must still be checked
- AI computation must still be reproducible
- Failed proof remains failed
- Counterexample remains counterexample

---

## Repository Architecture

AQARION
├── Research
│   ├── finite dynamical systems
│   ├── operator theory
│   ├── quotient structures
│   ├── graph methods
│   └── asymptotic investigations
├── Verification
│   ├── exact enumeration
│   ├── adversarial testing
│   ├── proof checking
│   └── reproducibility
├── Formalization
│   └── Lean / machine-checked
├── TOOLS
│   ├── ClaimLock, ProofGym, Replay, schemas, skills
│   └── verification utilities
└── Provenance
    ├── research ledgers, manifests, hashes, RO-Crate

Structure prevents infrastructure, experiments, proofs, and historical artifacts from becoming indistinguishable.

---

## Certification Standard

Observation → Reproducible computation → Independent verification → Mathematical proof → Formal verification → Certified claim

Not every result needs every stage immediately, but no result is promoted beyond its actual evidence.

SEARCH ≠ REPRODUCED
REPRODUCED ≠ MINIMAL
MINIMAL ≠ PROVED
PROVED ≠ FORMALLY VERIFIED
PUBLIC ≠ CERTIFIED

---

## Development Standard

New infrastructure should:
- have defined input/output contract
- include deterministic tests
- preserve existing evidence
- expose failures rather than hide them
- avoid silently changing historical results
- distinguish exploratory code from certification code
- document dependencies
- remain independently runnable

Historical research preserved rather than rewritten. Corrections recorded. **Deprecated claims remain identifiable.** Versioned artifacts remain traceable.

---

## Current Direction

Establish clean reusable spine for:
1. ClaimLock — claim and evidence management
2. Replay — deterministic reproduction
3. JOIN-STABILITY — exact theorem verification
4. ProofGym — executable verification
5. Shared schemas — evidence, provenance, receipts
6. Research skills — reusable workflows
7. CLI tooling — consistent interface
8. RO-Crate integration — machine-readable packaging

Objective: extract reusable infrastructure from already-tested workflows.

---

## Research Philosophy

Result becomes stronger by surviving:
- adversarial testing
- independent reconstruction
- exact enumeration
- counterexample searches
- proof review
- formalization
- reproducibility checks

System designed to preserve negative information as carefully as positive.
Disproved conjecture is useful. Failed proof is useful. Detected bug is useful. Quarantined claim is useful.

> **Guiding Principle:** Ideas may come from anywhere. Confidence comes from verification.
> **Motto:** Prove First · Verify Exhaustively · Predict Second · No Free Parameters

---

## Project Links

- AQARION: https://github.com/quantarion369-arch/AQARION
- TOOLS: https://github.[STRIPPED 68 bytes]
- Org: https://github.com/quantarion369-arch
- Hugging Face: https://huggingface.co/Quantarion9

---

## Status

AQARION is active research and infrastructure. Individual results have different evidence levels. Consult claim registry, ledger, verification report, formalization status, and reproducibility artifacts before treating any result as certified.

Research status is claim-specific, not repository-wide.

**Continuity:** Active development under `quantarion369-arch`. Earlier work under `JASKSG9` retained as historical provenance where accessible. Transition does not imply every historical artifact reconstructed. Policy: `preserve → identify → reconstruct → compare → hash → verify`

---

## Current Verified Snapshots

- **AQ-FPR-006:** `N(m1..ms)=Σ_π Π_B Σ_{d|gcd(B)} d^{|B|-1}` — 138 cycle types n=1..10, 0 mismatches, term-by-term n≤8 PASS, EGF `exp(e^z+½e^{2z}-3/2)` → 2,7,31,164,999,6841 — FROZEN AUDIT
- **AQ-PB-CORE:** `Fix(T*)≅Con(P,T|_P)` — `P=T^n(X)` periodic core — 3412 maps n≤5, 0 failures — [P+CV], Lean OPEN
- **PB-CORE-005:** Corrections `N(3,3)=8`, `N(2,4)=9`, plus 10 lower-table corrections `(1,1,2)=7` etc. — FROZEN

---

## License

**Apache License 2.0 — Apache-2.0**

Copyright 2026 AQARION / quantarion369-arch

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

- SPDX: `Apache-2.0`
- License file: `LICENSE` at repository root
- Current state: Public repository, 156 commits, 1 star, maintained under `quantarion369-arch/AQARION`

Third-party components retain their original licenses as noted in their directories.
