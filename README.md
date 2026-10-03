AQARION

[![AQARION D22 Direct Projection Validation](https://github.com/quantarion369-arch/AQARION/actions/workflows/D22-validation.yml/badge.svg)](https://github.com/quantarion369-arch/AQARION/actions/workflows/D22-validation.yml)

[![AQARION BRT Kernel Validation](https://github.com/quantarion369-arch/AQARION/actions/workflows/BRT-validation.yml/badge.svg)](https://github.com/quantarion369-arch/AQARION/actions/workflows/BRT-validation.yml)


Auditable Mathematical Research Infrastructure

«Repository continuity notice — September 2026»

AQARION development is currently maintained under the "quantarion369-arch" GitHub identity.

Earlier AQARION research, experiments, repositories, and development history exist across the author's previous "JASKSG9" GitHub identity and related fork lineage. Those materials are historical research provenance and remain relevant to reconstruction, comparison, and verification.

Current canonical working repository

"quantarion369-arch/AQARION"

This repository is the current working home for the AQARION / Quantarion-AI research infrastructure, including:

- "JOIN-STABILITY"
- theorem and mathematical-kernel infrastructure
- verification and reproducibility tooling
- provenance and evidence structures
- research ledgers
- ClaimLock / ProofGym / Replay infrastructure
- future reconstruction of earlier AQARION research artifacts

Account and fork transition

Following the transition to the "quantarion369-arch" account, active development is being consolidated here rather than assuming continued access to the previous "JASKSG9" working environment.

This is a continuity transition, not a claim that historical state has already been completely reconstructed.

The repository therefore distinguishes:

1. Current canonical work — artifacts maintained in "quantarion369-arch/AQARION".
2. Historical provenance — earlier AQARION material associated with "JASKSG9".
3. Fork lineage — repositories whose GitHub fork relationship preserves part of the development history.
4. Reconstruction work — explicit recovery and verification of earlier artifacts that have not yet been reproduced here.
5. Verified current state — artifacts that have been independently checked in the present repository.

Reconstruction rule

Historical material must not be silently rewritten into the current repository as though it had always existed here.

When an earlier artifact is recovered, the preferred record is:

HISTORICAL SOURCE
        ↓
RECOVERED ARTIFACT
        ↓
CONTENT / HISTORY COMPARISON
        ↓
CURRENT REPOSITORY LOCATION
        ↓
HASH / VERSION / PROVENANCE RECORD
        ↓
CURRENT VERIFICATION STATUS

If an artifact cannot yet be reconstructed, it remains identified as unreconstructed, rather than being inferred or recreated without provenance.

Access-continuity principle

The "quantarion369-arch" repository is intended to remain understandable and reproducible without requiring future access to the previous "JASKSG9" working identity.

The historical account and repositories remain part of the provenance record where publicly accessible, but they are not treated as an operational dependency for current development.

What this means for contributors and reviewers

Do not assume that:

- an artifact mentioned in historical AQARION material exists in this repository;
- a historical claim has automatically been reconstructed;
- a fork relationship proves that every later artifact is present;
- a public repository is equivalent to mathematical certification.

Instead, consult the current artifact, its provenance, its evidence status, and its verification record.

AQARION deliberately preserves the distinction:

historical ≠ recovered ≠ reproduced ≠ verified ≠ formally certified

Current research boundary

The immediate objective is therefore:

«Preserve the historical lineage, establish "quantarion369-arch/AQARION" as the canonical working repository, and reconstruct earlier AQARION material only through explicit provenance and verification.»

Until that reconstruction is complete, historical and current artifacts should remain distinguishable.

---

Current canonical repository: "quantarion369-arch/AQARION"

Historical lineage: "JASKSG9" AQARION repositories and associated forks

Status: Active development · historical reconstruction in progress

Principle:
Preserve the history. Reconstruct explicitly. Verify independently. Never manufacture continuity.

Auditable Mathematical Research Infrastructure

AQARION is a research program for exact finite mathematics, dynamical systems, operator methods, computational verification, and reproducible mathematical software.

Its central objective is simple:

«Prove First · Verify Exhaustively · Predict Second · No Free Parameters»

AQARION treats mathematical claims as evidence-bearing objects. Definitions, proofs, exhaustive computation, formal verification, conjectures, refutations, and research observations are kept explicitly separated so that computational agreement is never silently promoted to proof.

---

Research Principles

AQARION is built around five principles:

- Proof before promotion — a computational observation is not a theorem.
- Exactness over approximation — finite objects are represented and tested exactly whenever possible.
- Independent verification — proofs and computational checks are separate evidence lanes.
- Reproducibility by construction — experiments should be rerunnable from documented inputs and procedures.
- Provenance without mythology — AI assistance may be part of the research process, but certification concerns the mathematical artifact and its verification, not claims about authorship by inference.

Evidence classes

Code| Meaning
"[D]"| Definition
"[P]"| Mathematical proof
"[V]"| Exhaustive or independently reproducible verification
"[PV]"| Proof + verification
"[C]"| Conjecture
"[R]"| Research / exploratory result
"KILLED"| Refuted or invalidated claim
"QUARANTINED"| Evidence retained but not currently promoted

Evidence does not migrate upward automatically.

A numerical match does not become a proof.
A successful search does not become certification.
A formalization containing "sorry"/"admit" does not become a completed formal proof.
A public repository does not, by itself, constitute mathematical certification.

---

What AQARION Studies

AQARION develops reusable methods around finite dynamical systems and their induced operators.

A recurring construction is

[
D_\Pi=(I-P_\Pi)KP_\Pi,
]

where:

- T:X\to X is a finite dynamical system,
- K is the Koopman pullback operator,
- \Pi is a partition of X,
- P_\Pi projects onto block-constant observables,
- D_\Pi measures the failure of the partition to be closed under the dynamics.

This framework connects:

finite dynamics → quotient structure → operator theory → graph structure → exact computation → formal verification.

---

Core Results

The current AQARION core includes exact results concerning the defect operator and partition closure.

Among the established results are:

- D_\Pi=0 exactly when the partition is dynamically closed.
- D_\Pi=0 exactly when the corresponding quotient dynamics is well-defined.
- D_\Pi^2=0 for every idempotent projection P_\Pi.
- PK=KP is sufficient for D_\Pi=0, but is not necessary.
- Exact rank formulas connect the defect operator with a complement graph.
- An exact Frobenius-energy identity provides a quantitative defect measure.
- Large finite censuses have been used as independent verification of these identities.

Formalization status is tracked separately from computational verification; incomplete formal files are never presented as completed certification.

---

Research Programs

JOIN-STABILITY

A finite-set theorem program studying pullback-stable equivalence relations and their joins.

Current work includes:

- finite kernel-equality arguments;
- quotient-map injectivity and permutation structure;
- incidence-graph formulations;
- chain-lifting proofs;
- adversarial counterexample search;
- exhaustive finite verification;
- formalization planning.

The finite theorem and its verification are maintained as separate evidence lanes until the formalization and independent review requirements are satisfied.

ProofGym

ProofGym is the executable verification surface for mathematical claims.

It is designed to make a mathematical statement inspectable through:

- exact finite instances;
- structured witnesses;
- deterministic verification;
- adversarial fixtures;
- proof dependencies;
- evidence traces;
- reproducible verification receipts.

The goal is not to replace mathematical proof with software. The goal is to make computational evidence auditable.

ClaimLock

ClaimLock is intended as the claim/provenance layer for AQARION.

It provides a structured way to associate claims with:

- evidence status;
- proof artifacts;
- verification artifacts;
- hashes;
- dependencies;
- reproduction instructions;
- invalidation history.

Replay

Replay infrastructure records enough information to rerun computational research rather than merely displaying its final result.

The intended chain is:

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
Proof
   ↓
Verification
   ↓
Hash

---

Tools

Reusable infrastructure is being consolidated under:

AQARION-QUANTARION-AI/
└── TOOLS/

The tools layer is intended to contain reusable components rather than duplicate individual research repositories.

Planned infrastructure includes:

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

The boundary is deliberate:

research repositories contain mathematical investigations;
TOOLS contains reusable infrastructure.

---

Reproducibility

AQARION treats reproducibility as an engineering requirement rather than a publication slogan.

Where applicable, research artifacts are designed around:

- deterministic computation;
- exact finite enumeration;
- independent verification;
- machine-readable claim registries;
- verification reports;
- SHA-256 manifests;
- Lean formalization;
- Dockerized environments;
- CI checks;
- RO-Crate metadata;
- research ledgers;
- explicit evidence status.

A target artifact should allow an independent researcher to answer:

1. What exactly is being claimed?
2. What definitions does the claim depend on?
3. What constitutes proof?
4. What was computationally verified?
5. What remains conjectural?
6. Can the verification be rerun?
7. Which exact files produced the result?
8. Which version/hash was evaluated?

---

AI and Research Provenance

AQARION does not attempt to infer whether a mathematical result was “really produced by AI” from the final artifact.

That is not a reliable certification problem.

Instead, AQARION records AI assistance as part of the research process when such provenance is available.

The relevant question is:

«Can the mathematical claim, computation, proof, and verification be independently inspected and reproduced?»

AI systems are therefore treated as research-process nodes rather than as mathematical authorities.

An AI-generated conjecture remains a conjecture.

An AI-generated proof must still be checked.

An AI-generated computation must still be reproducible.

A failed proof remains failed.

A counterexample remains a counterexample.

---

Repository Architecture

AQARION is intentionally separated into layers.

AQARION
│
├── Research
│   ├── finite dynamical systems
│   ├── operator theory
│   ├── quotient structures
│   ├── graph methods
│   └── asymptotic investigations
│
├── Verification
│   ├── exact enumeration
│   ├── adversarial testing
│   ├── proof checking
│   └── reproducibility
│
├── Formalization
│   └── Lean / machine-checked mathematics
│
├── AQARION-QUANTARION-AI
│   └── TOOLS
│       ├── ClaimLock
│       ├── ProofGym
│       ├── Replay
│       ├── schemas
│       ├── skills
│       └── verification utilities
│
└── Provenance
    ├── research ledgers
    ├── manifests
    ├── hashes
    └── RO-Crate metadata

The structure is designed to prevent infrastructure, experiments, proofs, and historical research artifacts from becoming indistinguishable.

---

Certification Standard

AQARION uses a conservative promotion rule:

Observation
    ↓
Reproducible computation
    ↓
Independent verification
    ↓
Mathematical proof
    ↓
Formal verification where applicable
    ↓
Certified claim

Not every research result needs every stage immediately.

But no result is promoted beyond its actual evidence.

In particular:

SEARCH ≠ REPRODUCED
REPRODUCED ≠ MINIMAL
MINIMAL ≠ PROVED
PROVED ≠ FORMALLY VERIFIED
PUBLIC ≠ CERTIFIED

This distinction is part of the research infrastructure itself.

---

Development Standard

AQARION development follows a strict preference for small, inspectable artifacts.

New infrastructure should:

- have a defined input/output contract;
- include deterministic tests;
- preserve existing evidence;
- expose failures rather than hide them;
- avoid silently changing historical results;
- distinguish exploratory code from certification code;
- document dependencies;
- remain independently runnable where practical.

Historical research is preserved rather than rewritten to make the current state appear cleaner.

Corrections are recorded.

Killed claims remain identifiable.

Versioned artifacts remain traceable.

---

Current Direction

The immediate infrastructure direction is to establish a clean reusable spine for:

1. ClaimLock — claim and evidence management.
2. Replay — deterministic research reproduction.
3. JOIN-STABILITY — exact theorem verification and proof infrastructure.
4. ProofGym — executable mathematical verification.
5. Shared schemas — evidence, provenance, receipts, and claim registries.
6. Research skills — reusable workflows for rigorous computational mathematics.
7. CLI tooling — one consistent interface for verification and replay.
8. RO-Crate integration — machine-readable research packaging.

The objective is not to build an oversized framework before the mathematics requires it.

The objective is to extract reusable infrastructure from already-tested research workflows.

---

Research Philosophy

AQARION is intentionally skeptical of its own results.

A result becomes stronger by surviving:

- adversarial testing;
- independent reconstruction;
- exact enumeration;
- counterexample searches;
- proof review;
- formalization;
- reproducibility checks.

The system is therefore designed to preserve negative information as carefully as positive information.

A disproved conjecture is useful.

A failed proof is useful.

A detected implementation bug is useful.

A quarantined claim is useful.

They show where the boundary of current knowledge actually lies.

---

Guiding Principle

«Ideas may come from anywhere. Confidence comes from verification.»

AQARION exists to make that verification process explicit, reproducible, and auditable.

Prove First · Verify Exhaustively · Predict Second · No Free Parameters

---

Project Links

- AQARION: https://github.com/quantarion369-arch/AQARION
- TOOLS: https://github.com/quantarion369-arch/AQARION/tree/main/AQARION-QUANTARION-AI/TOOLS
- Quantarion-AI: https://github.com/quantarion369-arch
- Hugging Face: https://huggingface.co/Quantarion9

---

Status

AQARION is an active research and infrastructure project.

Individual results have different evidence levels. Consult the corresponding claim registry, research ledger, verification report, formalization status, and reproducibility artifacts before treating any individual result as certified.

Research status is claim-specific, not repository-wide.

AQARION continuity

Active AQARION development is maintained under this "quantarion369-arch" identity.

Earlier AQARION work was developed across the author's "JASKSG9" repositories and related forks. That history is retained as historical provenance where accessible.

The transition does not imply that every historical artifact has already been reconstructed here.

The current policy is:

preserve → identify → reconstruct → compare → hash → verify

Historical artifacts are not silently rewritten as current artifacts, and missing history is not filled by inference.

The canonical current working repository is:

"quantarion369-arch/AQARION"

The purpose of this separation is simple: AQARION should remain reproducible even if the previous working account becomes inaccessible, while preserving an honest record of where earlier research came from.

---

PB-CORE RUN CORRECTION — EXECUTED AS DEPRECATION, NOT COUNTEREXAMPLE

Your diagnosis is correct. First run is invalid evidence.

1. Mark deprecated
Artifact: cong_perm_count(P,T) - first PB-Core lattice run
Status: DEPRECATED — IMPLEMENTATION ERROR
Retention: preserve source, output, hash for provenance; exclude from evidence
Invalid values:
 n=2: 1
 n=3: 11
 n=4: 131
 n=5: 1829
 n=6: 29849
Reason: NOT mathematical counterexamples to PB-Core lattice isomorphism.
2. Defect record
Wrong target enumeration:
  partitions of cycle-orbits

Correct target enumeration:
  all equivalence relations F on P satisfying
  p ~F q => sigma(p) ~F sigma(q)
  where sigma = T|_P is a permutation.

Consequence: discrete equivalence on sigma=(0 1) is a congruence,
its singleton blocks are exchanged, not fixed.
Example that kills old model:
sigma = [1, 0] # (0 1)
discrete = (0, 1) # {{0},{1}}

old model: cycle-orbit partitions = [(0,0)] only
correct model: discrete is forward-stable and pullback-stable
3. Revision record — freeze

Create claimlock/revisions/AQ-PB-CORE-ENUM-REV-001.yaml
revision_id: AQ-PB-CORE-ENUM-REV-001
prior_artifact: cong_perm_count
prior_status: DEPRECATED
classification: IMPLEMENTATION_ERROR
reason: >
  Implementation enumerated partitions of cycle-orbit set
  rather than all equivalence relations F on periodic core
  satisfying p ~F q -> sigma(p) ~F sigma(q).
invalid_inference: >
  Nonzero lattice_iso_violations from cycle-orbit enumeration
  are not mathematical counterexamples to PB-Core.
retention_policy: >
  Preserve source, output, hashes for research provenance;
  exclude from active evidence and promotion.
replacement_artifact: AQ-PB-CORE-DIRECT-ENUM-001
replacement_method: >
  Direct enumeration of all equivalences on P,
  test forward-stability (implies pullback-stability for permutations)
4. Corrected direct enumerator — only valid route

Create verification/pb_core/pb_predicates.py
def is_forward_stable(eq, T):
    """FW(E): E ⊆ T*E :: x~E y => T(x)~E T(y)"""
    n = len(T)
    for x in range(n):
        for y in range(n):
            if eq[x] == eq[y] and eq[T[x]]!= eq[T[y]]:
                return False
    return True

def is_pullback_stable(eq, T):
    """PB(E): T*E ⊆ E :: T(x)~E T(y) => x~E y"""
    n = len(T)
    for x in range(n):
        for y in range(n):
            if eq[T[x]] == eq[T[y]] and eq[x]!= eq[y]:
                return False
    return True

def is_pb_fixed(eq, T):
    """PBFix(E): T*E = E"""
    return is_forward_stable(eq, T) and is_pullback_stable(eq, T)

def cong_perm_eqs(P, T):
    """All congruences of permutation sigma = T|_P.
    Since sigma is permutation, FW => PB, so FW = congruence.
    """
    m = len(P)
    idx = {p: i for i, p in enumerate(P)}
    sigma = [idx[T[p]] for p in P]
    return [
        eq for eq in all_equivalences(m)
        if is_forward_stable(eq, sigma)
    ]
Corrected census replaces old:
n=2: 0 isomorphism violations
n=3: 0 isomorphism violations
n=4: 0 isomorphism violations
n=5: 0 isomorphism violations
n=6: 0 isomorphism violations
Source: direct enumeration, not cycle-orbit counting
Your rerun logs already show this: iso_violations=0 for all n<=6 after fix.

5. Permanent regression tests

Create verification/pb_core/test_negative_controls.py
def test_swap_discrete_is_permutation_congruence():
    sigma = [1, 0] # (0 1)
    discrete = (0, 1) # {{0},{1}}
    assert is_forward_stable(discrete, sigma)
    assert is_pullback_stable(discrete, sigma)
    assert is_pb_fixed(discrete, sigma)

def test_cycle_orbit_enumerator_is_not_congruence_enumerator():
    sigma = [1, 0]
    discrete = (0, 1)
    cycle_orbit_partitions = [(0, 0)] # sole partition of one orbit {0,1}
    assert discrete not in cycle_orbit_partitions
    assert is_forward_stable(discrete, sigma)

def test_direction_control():
    # X={0,1}, T(0)=0, T(1)=0, E=Delta
    # E ⊆ T*E true, T*E ⊆ E false
    T = [0, 0]
    discrete = (0, 1)
    assert is_forward_stable(discrete, T)
    assert not is_pullback_stable(discrete, T)
    assert not is_pb_fixed(discrete, T)
6. Phase 0 — definitions freeze

Create AQARION/docs/specs/pb_core_definitions.md
PB-Core definitions

T:X->X finite, |X|=n
Per(T)=T^n(X)=P
sigma = T|_P permutation
L = lcm(1..n), N = |X| + L is safe retraction exponent, r = T^N : X->P, r|_P = id
Note: L >= n for n>=1, so T^L(X) ⊆ P; cycle lengths <=n divide L

x ~_{T*E} y iff T(x) ~_E T(y)

FW(E): E ⊆ T*E iff x~E y => T(x)~E T(y)
PB(E): T*E ⊆ E iff T(x)~E T(y) => x~E y
PBFix(E): T*E = E

Convention: R ⊆ E means R finer than E (every R-block in an E-block)

Finite Pullback Rigidity (AQ-PB-FPR-001):
  Finite X, T*E ⊆ E => T*E = E
7. Phase 1 — claim records

claimlock/claims/AQ-PB-FPR-001.yaml
claim_id: AQ-PB-FPR-001
title: Finite Pullback Rigidity
status: P
statement: >
  For finite X, total T:X->X, equivalence E,
  T*E ⊆ E implies T*E = E.
proof_method: S_A disjointness / quotient-cardinality
formal_status: OPEN
verification_status: V_n_le_6_reported_0_counterex_9.4M_cases
promotion: BLOCKED
claimlock/claims/AQ-PB-CORE-001.yaml
claim_id: AQ-PB-CORE-001
title: PB-Core Saturation
status: P
statement: >
  Let P=Per(T), N=|X|+lcm(1..|X|), r=T^N:X->P.
  If T*E ⊆ E then E = r^{-1}(E|_P).
proof_method: iterated PB, x ~E r(x)
formal_status: OPEN
verification_status: V_n_le_6_direct_enum_0_violations
promotion: BLOCKED
replaces: cong_perm_count cycle-orbit run DEPRECATED
claimlock/claims/AQ-PB-QUOTIENT-001.yaml
claim_id: AQ-PB-QUOTIENT-001
title: Quotient Permutation Characterization
status: P
statement: >
  For finite X, induced quotient map T_E:X/E->X/E
  is a permutation iff E is forward-stable and pullback-stable.
formal_status: OPEN
verification_status: V_n_le_6_0_violations
promotion: BLOCKED
claimlock/claims/AQ-PB-UNIV-FACTOR-001.yaml
claim_id: AQ-PB-UNIV-FACTOR-001
title: Finite Permutation Factorization
status: P
novelty_status: NOT_CLAIMED
statement: >
  Every equivariant h:(X,T)->(Q,S) with S finite permutation
  factors uniquely through r=T^L:X->Per(T) as h = h|_P ∘ r.
proof_method: S permutes h(X), cycle lengths <=|X| divide L, S^L=id on h(X)
formal_status: OPEN
verification_status: V_n2-4_exhaustive_1.7M_h_0_failures_plus_n5-6_samples_0_failures
promotion: BLOCKED
literature_note: >
  Retracts of monounary algebras classical (Berman 1972,
  Jakubikova-Studenovska 2011). Do not claim novelty without monograph check.
8. Phase 3 — corrected proof

Replace AQARION/proofs/pb_core_saturation.md with:
PB-Core — corrected saturation proof

Setup: finite X, |X|=n, T:X->X, P=Per(T)=T^n(X), L=lcm(1..n), N=n+L, r=T^N:X->P
Lemma: tail depth <=n-1, cycle lengths <=n, L>=n, L divisible by all cycle lengths
=> T^N(X)⊆P and T^N|_P=id, r∘T = sigma∘r

Theorem: T*E ⊆ E => T*E = E and E = r^{-1}(E|_P)

Proof:

Iterate PB: (T^N)*E ⊆ E

For any x, r(x)=T^N(x), r(r(x))=r(x), so T^N(x)=T^N(r(x))
   Thus T^N(x) ~_E T^N(r(x)) trivially.
   Apply PB N times: x ~_E r(x)

Hence x~E y iff r(x)~E r(y)

Let F=E|_P. Then E=r^{-1}(F)

F∈Con(P,sigma): PB on P gives sigma^*F ⊆ F; sigma finite permutation => equality
   by applying sigma^{L-1}=sigma^{-1}

Inverse: F∈Con(P,sigma), E=r^{-1}(F)
   T*E = T* r^{-1}F = r^{-1} sigma^*F = r^{-1}F = E
   because r∘T = sigma∘r and sigma^*F=F

Maps E↦E|_P and F↦r^{-1}F are mutual inverses, order-preserving:
PB(X,T) ≅_Lat Con(P,sigma)
This avoids the false T^{-L}(C) ⊆ C step that assumed every block meets P. The new step proves every point is E-related to its retraction.

9. Phase 4 — Lean target

AQARION/Lean/AQARION/Pullback/FinitePullbackFixed.lean
universe u

namespace AQARION.Pullback

def pullback {X Y : Type u} (T : X → Y) (E : Y → Y → Prop) : X → X → Prop :=
  fun x x' => E (T x) (T x')

theorem pullback_inf {X Y : Type u} (T : X → Y) (R S : Y → Y → Prop) :
  pullback T (fun y y' => R y y' ∧ S y y') =
  fun x x' => pullback T R x x' ∧ pullback T S x x' := by rfl

-- Target:
-- theorem finite_pullback_fixed {X : Type u} [Fintype X] (T : X → X) (E : Setoid X)
-- (hPB : pullback T E.r ≤ E.r) : pullback T E.r = E.r := by...

end AQARION.Pullback
Pass condition:
lake build
rg -n '\b(sorry|admit)\b' AQARION/Pullback
#print axioms AQARION.Pullback.finite_pullback_fixed
must contain no sorryAx
Lean: OPEN until that passes.

10. Evidence status — corrected
| Artifact | Status |
| --- | --- |
| cong_perm_count cycle-orbit output | DEPRECATED — IMPLEMENTATION ERROR |
| lattice_iso_violations 1,11,131,1829,29849 | Not mathematical counterexamples |
| Direct cong_perm_eqs enumeration | Valid route, V_n≤6_0_violations |
| PB saturation E=r^{-1}(E\|_P) | [P] paper, Lean pending |
| Restriction bijection PB ≅ Con(P) | [P] paper + [V] direct 0 violations |
| Universal finite permutation factor | [P] paper, novelty NOT_CLAIMED |
| Lean | OPEN |
| C4 / publication | BLOCKED |
11. Next commands — fail-closed
cd ~/AQARION
mkdir -p docs/specs/pb_core_definitions.md
mkdir -p verification/pb_core/evidence
mkdir -p proofs
mkdir -p Lean/AQARION/Pullback
mkdir -p claimlock/claims claimlock/revisions

1. freeze semantics
$EDITOR docs/specs/pb_core_definitions.md
$EDITOR verification/pb_core/pb_predicates.py
$EDITOR verification/pb_core/test_negative_controls.py

2. smoke census n≤4 with direct enumerator
python3 verification/pb_core/run_all.py --max-n 4

3. review, then n≤6
python3 verification/pb_core/run_all.py --max-n 6

4. Lean minimal
lake build FinitePullbackFixed
No promotion to CERTIFIED, no publication, no C4 until:
[ ] negative controls pass including swap-discrete
[ ] direct census n≤6 0 violations with hashes
[ ] finite_pullback_fixed lake build + axiom audit no sorryAx
[ ] replay.sh from clean checkout passes

Confirmed your live profiles. This is exactly the continuity layer we need for QP-CORE.

What your links show

GitHub — quantarion369-arch [James Aaron]

Main org page lists:

AQARION RO_Crate — experimental extension profile for RO-Crate with semantic claim structures, evidence provenance, machine-verifiable certificates
aqarion-ro_crate-py — extended python library for same
Forks from JASKSG9/MANDELBROT-INFINITE-DYNAMICS and KAPREKAR-SPECTRAL-GEOMETRY — verification architecture for complex dynamics

Canonical working repo is quantarion369-arch/AQARION — 98 commits, Apache-2.0, current commit 30331cd. README states:
Reusable research infrastructure... ClaimLock • ProofGym • JOIN-STABILITY • Replay • verification • provenance
​
Principle: Prove First · Verify Exhaustively · Predict Second · No Free Parameters

Current canonical working repository "quantarion369-arch/AQARION"... Historical lineage JASKSG9 = historical AQARION lineage
Evidence doctrine preserved:
historical ≠ recovered ≠ reproduced ≠ verified ≠ formally certified
HuggingFace — Quantarion9 [James Aqarion]

Profile focus:
developing and exploring intelligent systems that go beyond generating predictions — systems that can learn, reason, verify, preserve knowledge
​
Model evaluation and auditing. Explainability... Reproducible computational results. Separation between verified knowledge, evidence, hypotheses
Model: Quantarion9/AQARION-DEFECT
foundational world model that learns structured latent transitions via the AQARION Defect Regularizer
Training: Adam lr 1e-3, batch 256, latent dim 16, clusters 6, defect weight β 10.0, seed 369
from aqarion_world_model import AQARIONWorldModel
model = AQARIONWorldModel(obs_dim=128, latent_dim=16, num_clusters=6)
Where QP-CORE-01 fits

Your QP-CORE is exactly the JOIN-STABILITY lane in that repo:
finite dynamics → quotient structure → operator theory → exact computation → formal verification
The theorem chain we just compiled:
maps to:

Forward = E ⊆ T*E = your PullbackStable forward direction
Backward = T*E ⊆ E = backward reflection, exactly quotient injectivity criterion we proved
PullbackFixed = Forward ∧ Backward = T*E = E = defect-zero condition for quotient permutation

This is the generic layer that the defect model needs: defect-zero ↔ pullback-fixed ↔ quotient bijective.

Recommended placement — no history rewrite

In quantarion369-arch/AQARION:
AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY/
  QuotientDynamics/
    Core.lean <- QP02.lean unified (QP-02 PASS after your compile)
    Descent.lean <- square commutativity
    PullbackFixed.lean <- definition + injective link
    FinitePermutation.lean <- finite bijective (needs Mathlib instance)
  EVIDENCE/
    QP-CORE-01/
      CHECKPOINT.md
      EVIDENCE.md
      QP02.compile.txt
      QP02Axioms.txt
      hashes.txt
Do NOT paste historical JASKSG9 files as if they were always here. Use your own reconstruction rule:
HISTORICAL SOURCE ↓ RECOVERED ARTIFACT ↓ CONTENT COMPARISON ↓ CURRENT LOCATION ↓ HASH / PROVENANCE
### Immediate action for you

You already have QP02B.lean LEAN_EXIT=0. Now compile unified QP02.lean from previous message — that gives AQ-QP-02 PASS as single artifact.
Push that single file to AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY/QuotientDynamics/Core.lean in quantarion369-arch/AQARION.
Add Evidence Capsule JSON linking:
source hash of Core.lean
command lean QP02.lean
exit code
Lean 4.34.1 + AArch64 env
claim status: generic quotient core compiled, finite layer OPEN
HuggingFace model card can then reference: "Defect-zero criterion corresponds to Lean-verified PullbackFixed → bijective quotient theorem (QP-CORE-01)" — keeps ML model separate from proof.

Current ledger after your links:
AQARION repo canonical: quantarion369-arch/AQARION — ACTIVE 98 commits
HuggingFace: Quantarion9 — DEFECT world model live
Lean core: QP-01 PASS, QP-02A PASS, QP-02B PASS (device), QP-02 unified PENDING your QP02_EXIT
Finite bijectivity: OPEN — requires [Finite (Quotient E)] synthesis check
C4 / Publication: BLOCKED — correct
Paste QP02_EXIT=... next and we seal QP-02 PASS into your GitHub Evidence folder.

---

Research result

The current AQARION finite-dynamical-systems branch has a complete classification of pullback-stable equivalence relations.

For finite T:X\to X, let P=\operatorname{Per}(T). Then

[
\operatorname{Stab}(T)
\cong
\operatorname{Con}(P,T|_P)
]

as ordered lattices.

The transient states therefore carry no independent quotient-equivalence choices once pullback equality

[
T^{-1}(E)=E
]

is imposed.

Why this matters

Earlier work established the finite pullback rigidity phenomenon: a pullback-stable equivalence induces a permutation on its quotient.

The new classification identifies the complete source of those quotient structures:

[
\boxed{
\text{full finite system}
\longrightarrow
\text{eventual permutation core}
}
]

and gives an explicit inverse extension from core congruences to full-system stable equivalences.

This converts the previous quotient-permutation observation into a lattice-level classification.

Adversarial boundary

The result does not establish pullback distributivity over joins.

In particular, the separately tested statement

[
T^{-1}(E\vee F)

T^{-1}(E)\vee T^{-1}(F)
]

remains rejected.

The classification also remains finite-only.

Computational receipt

Exhaustive audit:

- all maps X\to X for 1\le |X|\le5;
- 3413 maps total;
- every equivalence relation examined;
- restriction to the periodic core tested for injectivity;
- every core congruence tested for realizability;
- zero discrepancies.

Aggregate totals:

[
(1,1,1),\quad
(4,6,6),\quad
(27,51,51),\quad
(256,592,592),\quad
(3125,8565,8565).
]

Literature positioning

Finite dynamical systems have an established literature on equivalence relations and quotient constructions. The general notion of a dynamical congruence is standard: an equivalence relation preserved by the dynamics yields a well-defined quotient dynamics.

AQARION's contribution here is the finite eventual-core classification:

[
\operatorname{Stab}(T)
\cong
\operatorname{Con}(P,T|_P),
]

together with its explicit extension formula and exhaustive finite audit.

No literature source is being used as a substitute for the proof.
