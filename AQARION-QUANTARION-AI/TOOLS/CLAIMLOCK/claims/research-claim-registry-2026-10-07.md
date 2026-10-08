# AQARION Research Claim Registry

Record date: 2026-10-07

Record type: Consolidated historical claim registry.

## Evidence policy

This registry separates mathematical arguments, reported computations,
independent implementation, formalization and repository provenance.

Historical identifiers are retrieval aliases, not new project names.

A reported PASS is not authentication of an execution. A recorded digest
is not a verified signature. Files referenced below are repository-relative
publication destinations; their presence is not asserted by this document.

## Governance

- C3: OPEN
- C4: BLOCKED
- Lean: OPEN
- Publication: BLOCKED
- Promotion: DENY
- Promotion code: CL008

## Claim inventory

| Descriptive claim | Historical alias | Mathematical status | Computational evidence | Formalization and provenance |
|---|---|---|---|---|
| Random-mapping stable-equivalence statistics | AQ-RM-001 | Research formulation recovered | Uses periodic-core size and permutation congruence counts | Source-bound execution pending |
| Burnside mean of fixed set partitions | AQ-RM-002 | Double-counting argument recovered | First moment reported through k=13; weighted cycle-type aggregation through k=10 | Lean OPEN; original execution unauthenticated |
| Cycle-type formula for permutation congruences | AQ-RM-003 | Formula and proof route recovered | Every cycle type through k=6 reportedly compared with brute force | Complete implementation binding pending |
| Burnside hierarchy of partition moments | AQ-RM-004 | Orbit-count interpretation recovered | First, second and third moments reported for k=1..10; direct control through k=5 | Lean OPEN; control implementation not inspected |
| Random-mapping stable-equivalence variance | AQ-RM-005 | Conditional identity target; historical status CONJECTURED | Proposed combination of cyclic-point distribution and second moments | No dedicated execution recovered |
| Finite pullback-stability rigidity | PB-001 | Historical proof-closed claim | 166484 full-mode cases; 3984 quick-mode cases reported | Exact theorem-to-script mapping pending |
| Two-cycle congruence decomposition | PB-002 | Historical proof-closed claim | 49 two-cycle cases reported | Lean OPEN |
| Corrected finite-partition enumeration | PB-003Q / PB-003X | Historical corrected proof claim | Earlier defective PB-003 retained as refuted | Original and corrected artifacts pending binding |
| Periodic-core restriction and extension | PB-CORE-004 | Paper argument and Lean drafts recovered | 50069-map report through n=6; separate historical receipt covers 3413 maps through n=5 | Lean uncompiled; scopes must remain separate |
| Cycle-phase congruence enumeration | PB-006 | Historical formula and classification program | 138 types full; 66 types quick; nine anchors; eight mutation detections | Historical naming conflicts with “forward constraint graph”; statement binding pending |
| Burnside stabilizer sum | T5A / PB-CORE-006 dependency | Double-counting proof recovered | Sum over permutations equals k! p(k), reported checks through k=8 | Not identical to the periodic-core reduction lemma |
| Aggregate stable-equivalence pair count | PB-CORE-006 | Modular proof route recovered | A_n arithmetic through n=12 reported | Publication-grade proof assembly and Lean OPEN |
| Linear modular functional-equivalence criterion | MOD-ATLAS-001 | Necessity and sufficiency argument included | 605 cases; 59 accepted; 546 rejected; 106 single-point false accepts; 15 controls detected | Historical source binding pending |
| Quadratic modular functional-equivalence criterion | MOD-ATLAS-002 | Necessity and sufficiency argument included | Modulus-four distinguishing example reported | Full quadratic atlas not recovered at this checkpoint |
| Mobile environment inventory | MOBILE-KIT-001 | Engineering functionality, not a mathematical theorem | Three initial inventory tests reported | Snapshot describes one environment only |
| Bounded command recording | MOBILE-KIT-002 | Engineering contract | Five initial recorder tests reported | Exit status does not establish mathematical correctness |
| Static HTML report viewer | MOBILE-KIT-003 | Engineering functionality | Five initial viewer tests reported | Viewer does not authenticate report contents |
| Partition–Koopman block invariance | AQ-001 | General indicator-function proof recovered | 166483 instances reported for n=2..5 | Competing implementation accounts unresolved; provenance controls unexecuted |

## Local evidence destinations

Paths are relative to AQARION-QUANTARION-AI/TOOLS/.

- VERIFICATION/receipts/mathematical-verification-full-mode-2026-10-05.json
- VERIFICATION/reports/burnside-partition-moments-first-through-third-k1-to-k10.json
- VERIFICATION/reports/linear-modular-contract-atlas-605-cases.json
- VERIFICATION/reports/quadratic-modular-functional-equivalence-criterion.json
- CLAIMLOCK/evidence/burnside-partition-moments-evidence-record-2026-10-07.json
- CLAIMLOCK/ledgers/research-work-history-and-continuity-2026-10-07.md

## Receipt authentication boundary

The historical full-mode receipt is preserved without alteration.

Its source_sha256 and receipt_sha256 fields are supplied historical values.
The corresponding source bytes and receipt-hashing procedure have not been
recovered and checked in this registry preparation.

Do not describe the receipt as authenticated or independently reproduced
solely because those fields are present.

## Preserved corrections

- Old PB-003 is retained as refuted, not silently replaced.
- The two-cycle value N(2,4)=9 supersedes the historical documentation value 7.
- The stabilizer identity and periodic-core reduction are distinct results.
- Forward-invariant partitions are not the same as pullback-fixed equivalences.
- Distinct operator detection patterns do not imply statistical independence.
- Equivalent zero-tests and constant-prediction variants are recorded separately.
- Q54 Monte Carlo estimates are superseded by the later reported exact computation.
- A28 finite floating-point testing is not itself a general proof.
- Mathematical acceptance does not authorize publication or governance promotion.

## Publication boundary

This registry records recovered research, not blanket certification.

No result inherits Lean acceptance, repository authentication, independent
verification or publication authorization from another result.
