# AQARION Research Work History and Continuity

Checkpoint date: 2026-10-07

Record type: Consolidated historical inventory and continuity handoff.

## 1. Source-of-truth doctrine

Durable source files, exact repository revisions and execution receipts
are authoritative. Conversation summaries index those artifacts but do
not replace them.

This ledger reconstructs the supplied work history. It does not claim
fresh execution, repository inspection or authentication of historical
outputs.

Mathematical status, computation, implementation independence, Lean
acceptance, artifact provenance and publication status remain separate.

## 2. Governance

- C3: OPEN
- C4: BLOCKED
- Lean: OPEN
- Publication: BLOCKED
- Promotion: DENY
- Promotion code: CL008

Professional terminology: adversarial testing, counterexample analysis,
mutation testing, failure analysis, detection, claim disposition,
verification boundary, computational scaling boundary, independent
implementation, reproducibility evidence and formalization status.

## 3. Historical verification suite

Quick mode reportedly passed 9 of 9 checks:

- 66 cycle types.
- 3984 PB-001 cases.
- 13550 forward-join cases.
- 2088 incidence cases.
- Eight declared mutations detected.

The preserved full-mode receipt reports:

- 138 cycle types.
- Nine anchors.
- 49 two-cycle cases.
- 166484 PB-001 cases.
- 3413 periodic-core maps.
- 625770 forward-join cases.
- 42473 incidence cases.
- Eight declared mutations detected.
- Nine of nine checks passed.

The full-mode receipt is dated 2026-10-05T03:34:30.038167+00:00.
Its recorded source and receipt digests have not been authenticated here.

## 4. Foundation and corrected claims

PB-001 has a historical proof-closed status, but its exact statement must
be bound to source: earlier accounts describe pullback-stability rigidity,
whereas the checklist labels it observable quotient enumeration.

PB-002 records the two-cycle congruence decomposition.

Old PB-003 is refuted. Corrected PB-003Q and PB-003X are historically
reported proof-closed. Preserve the counterexample and correction chain.

PB-CORE-004 records periodic-core restriction and extension.
One later report covers all 50069 maps through n=6 with zero mismatches.
The preserved full receipt separately covers 3413 maps through n=5.

The defective_universal_only comparison was reportedly rejected.
Do not merge distinct runs or their scopes.

D22 records an original proposition, a discovered defect, a corrected
proposition and a provenance chain. Exact statements and artifacts remain
to be recovered.

## 5. Partition–Koopman foundation

For a block-average projection P and Koopman matrix K:

D = (I-P) K P.

The recovered indicator-function argument establishes that D=0 exactly
when each partition block maps into one partition block.

This is forward block invariance, not biconditional pullback stability.

The compressed Gram correction is:

U^T D^T D U = U^T K^T K U - A^T A,

under orthonormal block-basis conventions P=UU^T and A=U^T K U.

The specialization I-A^T A requires K^T K=I.
The historical non-bijective counterexample is T=[0,0,1].

## 6. Periodic-core and aggregate enumeration

Recovered proof route:

1. Reduce pullback-fixed equivalences to congruences of the periodic permutation.
2. Double-count permutation–partition pairs to obtain k! p(k).
3. Count forests rooted at k prescribed core points.
4. Choose the k-element core.

The stabilizer identity is a separate result from core reduction.

Reported aggregate values A_1 through A_12:

1, 6, 51, 592, 8565, 148896, 3018127, 69844608,
1816084233, 52399129600, 1660832066091, 57351480413184.

Formula arithmetic beyond the brute-force scope is not an exhaustive
enumeration of maps at those larger sizes.

## 7. Burnside moment hierarchy

Reported first moments for k=1..10:

1, 2, 3, 5, 7, 11, 15, 22, 30, 42.

Reported second moments:

1, 4, 10, 33, 91, 298, 910, 3017, 9945, 34207.

Reported third moments:

1, 8, 37, 285, 2150, 21205, 233612, 2999988,
43357512, 701807683.

Reported variances:

0, 0, 1, 8, 42, 177, 685, 2533, 9045, 32443.

Method: cycle-type compression, exact Fraction aggregation and a subset
recurrence with 2^r states and O(3^r) transitions before compression.

Reported controls:

- First moment equals p(k) through k=13.
- Cycle-type formula versus brute force through k=6.
- Weighted aggregation through k=10.
- Direct permutation and partition enumeration through k=5.

Moment interpretation: diagonal orbits of ordered tuples of partitions.

The second-moment interpretation uses bipartite multigraphs with k edges,
no isolated vertices and distinguished sides.

## 8. Random-mapping statistics

The proposed variance decomposition uses the periodic-core size K_n and
Burnside second moments.

Historical target:

Var(S(T)) = E[M_2(K_n)] - E[p(K_n)]^2.

A dedicated derivation and source-bound computation are not recovered in
this package. Preserve its historical conjectural status separately from
the established component identities.

## 9. PB asymptotic program

Recovered targets include:

- Leading logarithmic growth proportional to n^(1/3).
- Refined dominant-core shift.
- Gaussian local profile.
- Full asymptotic prefactor.

Numerical support and local saddle calculations do not establish uniform
tail bounds. Global domain decomposition and publication-grade proof
remain unfinished.

## 10. Q54 congruence-count chronology

The initial DFS had a fixed-point class-visibility defect.
The corrected version reportedly matched brute force on 1792 random maps.

Exact small-prefix counts reported:

- 8 states: 260.
- 12 states: 50534.
- 16 states: 38441489.
- 18 states: 121757993.
- 26 states: 10339926119106.
- 34 states: 35954063551732305.

The early full-Q54 Monte Carlo estimates around 10^25 to 10^26 were
explicitly withdrawn after the later root-class computation.

Reported exact layer-respecting count:

1211915286072636318.

Reported exact full forward-invariant count:

1587974166577462510560323119250.

Reported T-closed root-containing sets:

103743466365.

Reported distinct boundary types:

20599.

The root-class decomposition was reportedly checked on 500 random rooted
trees and against earlier exact prefix counts.

Full-Q54 independent confirmation is not established.
The earlier “exact count unfinished” entry is historical, not the latest
reported state.

Exactly one pullback-stable partition is reported for Q54.
That is a different counting problem from forward-invariant congruences.

## 11. Lean continuity

Recovered drafts include iteration, stable iteration, restriction,
extension, inverse properties, finite idempotent-iterate existence and
equivalence-preservation wrappers.

No successful compilation is supplied.

Identified draft corrections include:

- Remove the extra CoreData argument from stable_iterate calls.
- Reverse the associativity rewrite in the periodic_mul arithmetic step.

Compilation, theorem-scope matching and source/toolchain binding remain
open. Draft completeness is not kernel acceptance.

## 12. Equal-block norm result

For m>=2 equal consecutive blocks of size k under a cyclic shift,
with r=d mod k, the recovered formula is:

||D||_F^2 = 2*m*r*(k-r)/k^2.

The historical report describes 462 tested nonidentity shifts.

The original assertion of m*r nonzero rows was incorrect.
For 0<r<k, all m*k rows are nonzero.
A corrected row-wise algebraic derivation was subsequently recovered.

Maximum:

- k even: m/2.
- k odd: m*(k^2-1)/(2*k^2).

The reported delta formula has conflicting cases and remains unresolved
pending its definition and original proof.

## 13. Mobile Research Kit initial package

Historical initial source package:

mobile-research-kit-source-20261007-013443-495059.zip.

Reported inventory: nine files, 12045 bytes.

Initial tools:

- inspect_environment.py: 110 lines.
- record_run.py: 121 lines.
- view_report.py: 101 lines.

Initial tests: 13.

- Five recorder tests.
- Three inventory tests.
- Five viewer tests.

Reported execution: 13 tests in 2.751 seconds, exit zero.
The HTML viewer reportedly opened on the phone.

Reported environment:

- Samsung SM-A156U.
- Android 16.
- AArch64.
- Termux Google Play 2026.06.21.
- Python 3.13.13.

Native Termux availability does not establish a separate Ubuntu or Lean
toolchain.

Receipts are not signatures. A viewer does not authenticate reports.

## 14. Mobile package evolution

Historical package stages:

- 25-test toolkit.
- 17-test experiment package.
- 42-test combined package.
- 52-test modular-atlas package.
- Later 109-test working package.

These are chronological package states, not one fixed test inventory.

## 15. Contract collision and coefficient sweep

Collision experiment:

- Three function variants.
- Equality and parity observables.
- Six combinations.
- 41 inputs from -20 through 20.
- All fixture expectations reportedly met.

Coefficient sweep:

- Candidate x^2+a*x+b.
- Reference x^2+x.
- a and b from -2 through 2.
- 25 candidates.
- One satisfying both observables: (1,0).
- Five parity-only candidates:
  (-1,-2), (-1,0), (-1,2), (1,-2), (1,2).
- Zero equality-only candidates.
- Nineteen satisfying neither.

Historical artifacts: table.md and report.json under a coefficient-sweep
report directory. Exact repository binding remains pending.

## 16. Linear modular atlas

Reported domain:

- a,b from -5 through 5.
- Moduli 2,3,4,5,6.
- 605 candidate-modulus cases.
- 2420 complete-residue evaluations.
- 605 single-point evaluations.

Reported totals:

- 59 complete acceptances.
- 546 rejections.
- Zero classifier disagreements.
- 106 single-point false acceptances.
- Fifteen negative controls detected.

Criterion:

b=0 mod q and a=1 mod q.

Necessity follows from x=0 and x=1.
Sufficiency follows directly from the linear difference.

Historical engineering limitations are recorded in the corresponding
report. Later package improvements must not be backdated into this run.

## 17. Quadratic modular extension

For candidate c*x^2+a*x+b and reference x^2+x:

Functional equality for all integers modulo q holds exactly when:

- q divides b.
- q divides c+a-2.
- q divides 2*(c-1).

Recovered proof uses evaluations at 0,1,2 and the evenness of x*(x-1).

Distinguishing example:

3*x^2-x and x^2+x agree modulo 4 for every integer x although their
coefficients do not agree modulo 4.

The planned three-route atlas compares complete residues, the exact
criterion and an overstrict coefficient classifier.

## 18. Later quadratic verifier repair and published kit replay

Reported repair commit: 43cf1e1.

Changed files:

- tools/verify_quadratic_atlas.py.
- tests/test_quadratic_oracle_separation.py.

Purpose: bind declared reference and candidate formulas to the verifier's
fixed computation.

Reported local regression: 109 tests passed.

The combined relabeling test exercises rejection at the reference check.
Candidate-only rejection remains a separately identified coverage detail.

Manifest reconciliation:

- Corrected README history path.
- Added four omitted test files.
- Updated 35 listed entries.
- Reported zero verification failures.

Reported published replay revision:

8837971b27bc7a3230a9d2532afbb535f017afab.

Reported fresh Termux replay:

- Listed-file manifest verification passed.
- 109 tests passed in 11.339 seconds.
- Published replay success marker printed.
- GitHub workflow reportedly green.

This is user-supplied execution evidence, not assistant execution or full
independent certification.

## 19. Partition–Koopman operator experiment

Descriptive name: Partition–Koopman invariance.
Historical alias: AQ-001.

Reported census:

- n=2: 8 cases.
- n=3: 135 cases.
- n=4: 3840 cases.
- n=5: 162500 cases.
- Total: 166483 cases.
- Reported disagreements: zero.

Implementation accounts conflict:

- Integer-scaled exact matrices.
- Fraction-valued NumPy arrays.
- Earlier floating-point allclose implementation.

Do not merge these accounts without exact source identities.

A later six-alternative experiment reports three distinct alternative
zero-test behaviors and one baseline-equivalent control.

The earlier larger operator suite reports five nondegenerate detection
patterns at n=4 and n=5. These are different suites.

Provenance controls were declared but not executed in the recovered
operator specimen.

## 20. Additional historical measurement

TORE/VAJRA report:

- Left-right mirror error: 0.8502%.
- Contour points: 52936.
- Fourier coefficients retained: 30.
- Reported energy fraction: 72.23%.

The meaning of CLEAN and the acceptance threshold are not recovered.
Preserve this as a measurement report, not a certified theorem.

## 21. Release decisions and reproducibility boundaries

Historical decisions include license selection, destination selection,
transfer-file review and extracted-copy testing.

Later published-kit evidence supersedes the blanket claim that no package
has been published. It does not settle the license question or authenticate
every separate experimental report.

The historical “aqsrion replay PB-006” command is not an established
executable interface in this ledger.

The standalone unittest command is meaningful only in a package whose
source and test directory have been identified.

No five-minute reproduction claim is certified solely by listing commands.

## 22. Remaining priorities

1. Bind historical reports to exact source and execution identities.
2. Preserve the published kit replay as a separate evidence track.
3. Assemble the aggregate enumeration proof without redundant dependencies.
4. Close global bounds for the leading asymptotic law.
5. Recover a source-bound Burnside implementation and controls.
6. Resolve the Partition–Koopman implementation attribution conflict.
7. Complete a descriptive exact distinguishing-example certificate.
8. Execute provenance negative controls before confirming provenance.
9. Compile the existing Lean chain before extending formal claims.
10. Perform literature priority review before novelty claims.

## 23. Promotion boundary

No blanket certification is issued.

Reported computation does not substitute for proof.
Proof does not authenticate an execution.
Package replay does not authenticate unrelated research reports.
Successful compilation does not establish statement fidelity by itself.
Governance promotion remains denied.
