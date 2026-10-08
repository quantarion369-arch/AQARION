AQARION Claim Registry — 2026-10-07
ID	Claim	Status	Evidence	Lean	Replay
AQ-RM-001	Random Mapping Stable-Relation Statistics S(T)=	Fix(T*)		OBSERVED	Burnside first moment, cyclic-point distribution Pr(K_n=k)=(n)_k k / n^{k+1}, forest count k n^{n-k-1}
AQ-RM-002	Burnside Mean E[C(σ)]=p(k)	COMPUTED + PROVED (double-counting)	1..13 exact avg, 1..6 brute vs cycle-type, Σ C(λ)/z_λ =p(k) k≤10	OPEN	BURNSIDE_MOMENTS_k1_10.json
AQ-RM-003	Cycle-Type Compression C(λ)= Σ_π Π_B Σ_{d	gcd} d^{	B	-1}	COMPUTED + VERIFIED
AQ-RM-004	Burnside Moment Hierarchy M_{k,m}=	E_k^m/S_k		COMPUTED	M1-M3 k=1..10 exact integers, Var = M2-p^2, brute control k≤5 PASS
AQ-RM-005	Random-Mapping Variance Var(S(T))=E[M_{K_n,2}]-E[p(K_n)]^2	CONJECTURED	Depends on RM-002/003/004 + forest count	OPEN	Next
PB-001	Observable quotient enumeration	PROVED + VERIFIED	166484 cases full mode, 3984 quick mode, 0 violations	OPEN	PB-001
PB-002	Two-cycle decomposition	PROVED	49 types tested	OPEN	PB-006-TWO-CYCLE
PB-CORE-004 v2	Periodic-core reduction: pullback-fixed equivalences ↔ congruences on periodic permutation	CORRECTED + VERIFIED	50,069 maps n=1..6 0 mismatches, mutation defective_universal_only REJECTED	OPEN	PB-CORE
PB-006	Forward constraint graph theorem	COMPUTED	138 types full mode, 66 types quick mode, 9 anchors, mutation M01-M08 8/8 detected	OPEN	PB-006
MOD-ATLAS-001	Linear modular classifier b≡0,a≡1 mod q exact	COMPUTED + PROVED (necessity via x=0,1)	605 cases 59 accept 546 reject 0 disagreements 106 sample false 15/15 controls	N/A	MODULAR_ATLAS_LINEAR_605.json
MOD-ATLAS-002	Quadratic criterion b≡0,c+a-2≡0,2(c-1)≡0	DERIVED + VERIFIED on examples	Distinguishing example 3x²-x ≡ x²+x mod 4, functional equivalence without coeff match, null polynomial	N/A	QUADRATIC_CRITERION.json
MOBILE-KIT-001	Environment snapshot	COMPUTED	inspect_environment.py 110 lines, INVENTORY_EXIT=0, 3 tests	N/A	reports/capability_manifest.json
MOBILE-KIT-002	Bounded command recording	COMPUTED	record_run.py 121 lines, 5 tests, states started/completed/timed_out/interrupted/launch_failed/recorder_error	N/A	run-*/receipt.json
MOBILE-KIT-003	Static HTML viewer	COMPUTED	view_report.py 101 lines, 5 tests, escaping, overwrite protection	N/A	viewer.html
Disposition vocabulary: CONJECTURED, OBSERVED, COMPUTED, VERIFIED, REPRODUCED, FORMALIZED, PROVED, REFUTED, QUARANTINED
Engineering vocabulary: adversarial testing, counterexample analysis, mutation testing, failure analysis, verification boundary, computational scaling boundary, independent implementation, reproducibility evidence, formalization status, promotion decision

AQARION Work History Checklist — Full — 2026-10-07
Governance: C3 OPEN, C4 BLOCKED, Lean OPEN, Publication BLOCKED, Promotion DENY/CL008 — aqarion_receipt.json quick mode 9/9 PASS (66 types, 3984 PB-001, 13550 FWD-JOIN, 2088 INC, MUT M01-M08 detected). Full mode historically 138 types, 166484 PB-001, 625770 FWD-JOIN, 42473 INC.

Foundation
PB-001 PROOF CLOSED: finite enumeration of observable quotients — 166484 cases full, 3984 quick
PB-002 PROOF CLOSED: two-cycle decomposition
OLD PB-003 REFUTED: counterexample analysis preserved, corrected by PB-003Q/X PROOF CLOSED
PB-CORE-004 v2 CORRECTED: 50,069 maps n=1..6, 0 mismatches, A_n = 1,6,51,592,8565,148896, mutation defective_universal_only REJECTED (false_claim_holds=False)
T5A k!p(k) PROVED: periodic-core reduction lemma
Q54: DFS bugfix — fixed point class visibility, 0 mismatches 1792 random maps, exact Q54 did not finish 500s, Knuth estimator validated on 260,50534,38441489,121757993 → estimates 1.2e13 (26),1.7e17 (34),5e21 (44),1.6e25±1.2e25 (54) — order 1e25 forward-invariant vs 1 stable
Projector Gram correction: U^T D^T D U = U^T K^T K U - A^T A, specialization K^T K=I → I-A^T A, non-bijective counterexample T=[0,0,1]
D22: original proposition preserved, defect discovered, corrected proposition, provenance chain
Burnside Moment Hierarchy — NEW — Verified in Sandbox 2026-10-07
burnside_check_fast.py first moment: k=1..13 exact avg= p(k) = 1,2,3,5,7,11,15,22,30,42,56,77,101 — PASS
Cycle-type compression: C(λ)= Σ_{π∈Part([r])} Π_{B∈π} ( Σ_{d|gcd(λ_i∈B)} d^{|B|-1} ) — verified vs brute C(σ) for every cycle type k≤6
Weighted aggregation: Σ C(λ)/z_λ = p(k), z_λ=Π j^{m_j} m_j! — verified k≤10
Subset recurrence F(S)= Σ_{B⊆S, i∈B} w(B) F(S\B) — Bell-free, 3^r terms, 2^r states, identity control C(1^k)=B_k via recurrence
Moments computed exact (Fraction):
k=1..10 M1=1,2,3,5,7,11,15,22,30,42
M2=1,4,10,33,91,298,910,3017,9945,34207
M3=1,8,37,285,2150,21205,233612,2999988,43357512,701807683
Var=0,0,1,8,42,177,685,2533,9045,32443
Independent control: enumerate permutations + set partitions k=1..5, count fixed partitions directly — first/second/third moment comparisons PASS
Interpretation: M_j(k)=|E_k^j / S_k| — ordered j-tuples, second moment as intersection matrix / bipartite multigraphs with k edges, no isolated vertices, distinguished sides
Evidence capsule: /mnt/data/certification/BURNSIDE_MOMENTS_k1_10.json
Mobile Research Kit — NEW — Independent Toolchain
Checkpoint: mobile-research-kit-source-20261007-013443-495059.zip — 9 files, 12045 bytes, ARCHIVE_CONTENTS_VERIFIED, LOCAL_SOURCE_PACKAGE_OK
Tools: inspect_environment.py 110 lines, record_run.py 121 lines, view_report.py 101 lines
Tests: 13 tests — 5 recorder, 3 inventory, 5 viewer — user-reported 13 tests in 2.751s OK, FULL_TEST_SUITE_EXIT=0, HTML viewer opened on phone
Environment: Samsung SM-A156U, Android 16, AArch64, Termux Google Play 2026.06.21, Python 3.13.13 — native Termux does not establish Ubuntu Lean availability
Evidence boundaries: exit code ≠ mathematical verdict, receipts not signatures, viewer does not authenticate or prove two files share execution
Later packages: 25-test toolkit ZIP (4 tools, 6 test files), 17-test experiment ZIP (contract experiments), 42-test combined (25+11+6) OK, 52-test with modular atlas
Contract Collision Lab + Coefficient Sweep
Collision Lab: 6 combos (reference, subtract_mutation, offset_mutation × equality/parity) over 41 inputs [-20,20] — all fixture expectations met
Coefficient Sweep: f_{a,b}=x²+a x+b vs g=x²+x, |a|≤2,|b|≤2 — 25 candidates, 1 both (1,0), 5 parity_only (-1,-2),(-1,0),(-1,2),(1,-2),(1,2), 0 equality_only, 19 neither — workflow STATUS=completed RECORDER_EXIT=0
Artifacts: reports/coefficient-sweep-001/table.md, report.json
Modular Contract Atlas — NEW — Verified in Sandbox 2026-10-07
Grid: a,b ∈ {-5..5} → 121 pairs × moduli 2,3,4,5,6 = 605 candidate-modulus cases
Complete evaluations: 2420 =121×(2+3+4+5+6), sample evaluations 605 (x=0 only)
Results per modulus:
q=2: 30 accept 91 reject 0 disagreements 25 sample false
q=3: 12/109/0/21
q=4: 9/112/0/24
q=5: 6/115/0/27
q=6: 2/119/0/9
Total: 59 accept 546 reject 0 disagreements 106 false accepts 15/15 controls detected
Linear classifier exact: h(x)=(a-1)x+b, condition b≡0 and a≡1 mod q — necessity via x=0,1, sufficiency trivial — complete-residue route stronger than interval sampling because integer polynomials preserve congruence
False accepts formula: N_b(q)·N_a(q) complete, 11·N_b(q) sample, false=(11-N_a)·N_b
Engineering boundaries: empty sample domains returns acceptance with zero checks, no resource limits, full report in memory, output not transactional, no schema validation, no witness-replay command, no packaged-copy check for atlas — does not invalidate results
Evidence capsule: /mnt/data/certification/MODULAR_ATLAS_LINEAR_605.json
Quadratic Extension — Derived Criterion — Verified in Sandbox
Family: f_{c,a,b}=c x²+a x+b, h=Ax²+Bx+b, A=c-1, B=a-1 = A x(x-1)+(A+B)x+b
Exact criterion: q|b, q|(A+B), q|2A ↔ b≡0, c+a-2≡0, 2(c-1)≡0 mod q — necessity via 0,1,2, sufficiency via x(x-1) even
Distinguishing example: f=3x²- x vs g=x²+x, difference 2x(x-1) divisible by 4 for all x, yet coefficients not matching mod 4 — functional equivalence but coeff mismatch
For odd moduli, q|2A → A≡0 → B≡0, even moduli extra possibility — even vs odd informative
Evidence capsule: /mnt/data/certification/QUADRATIC_CRITERION.json
Next deliverable: quadratic atlas with three routes — exhaustive residue, exact criterion, overstrict coeff-matching (falsely rejects)
Governance and Terminology
Professional terminology: adversarial testing, counterexample analysis, mutation testing, failure analysis, claim disposition (PROVED/VERIFIED/COMPUTED/OBSERVED/CONJECTURED/REFUTED/QUARANTINED), verification boundary, computational scaling boundary, independent implementation, reproducibility evidence, formalization status, promotion decision
Claim states: CONJECTURED, OBSERVED, COMPUTED, VERIFIED, REPRODUCED, FORMALIZED, PROVED, REFUTED, QUARANTINED
Evidence capsule pattern: CLAIM → RUN → EVIDENCE → ATTACK → REPLAY → VERDICT
No sensational terminology: killer attack, autopsy, kill a claim replaced
Remaining Release Decisions
Choose license before open-source release
Choose repository and destination directory (quantarion369-arch/AQARION canonical, JASKSG9 historical)
Review selected transfer files (9 files only, not raw reports)
If new README adopted, create new ZIP with new timestamp and re-verify
Package 52-test working version (atlas) with extracted-copy test
Build quadratic atlas experiment as next substantive extension
Random-mapping variance: E[S(T)^2] = E[M_{K_n,2}] decomposition
Lean dependency graph: smallest useful formalization target
Literature collision map: equitable partitions / lumpability / bisimulation
How to Reproduce (5-minute stranger test)
aqsrion replay PB-006 → CLAIM PB-006 DOMAIN n≤10 RESULT PASS INDEPENDENT PASS MUTATIONS 8/8 DETECTED PROOF OPEN PROMOTION BLOCKED
python3 -m unittest discover -s tests -v — Mobile Research Kit
python3 tools/run_workflow.py --timeout 10 --output-root reports -- python3 examples/modular_contract_atlas.py --moduli 2 3 4 5 6 --bound 5 --sample-radius 0 --output-dir reports/modular-atlas-001
What Survived Adversarial Testing
PB-CORE-004 v2 survived defective_universal_only mutation
Burnside moments survived brute-force control k≤5
Modular atlas survived 15/15 negative controls (omission of constant, omission of slope, OR vs AND)
TORE/VAJRA exact test survived measurement: LR MIRROR ERROR 0.8502% CLEAN, 52,936 contour points →30 Fourier coeffs=72.23% energy
