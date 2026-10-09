# AQ-EVIDENCE-001 — Claim-to-Evidence Traceability Contract

**Protocol:** AQARION Claim-to-Evidence Traceability  
**Version:** 1.0.0  
**Status:** PROPOSED — NOT YET REPOSITORY-VERIFIED  
**Scope:** Mathematical claims, formal proofs, computational verification,
independent verification, regression tests, and CI provenance.

---

## 1. Purpose

AQ-EVIDENCE-001 defines a common contract for associating each registered
AQARION mathematical claim with its precise statement, supporting arguments,
implementations, executed verification procedures, and known limitations.

Its purpose is to prevent distinct forms of evidence from being conflated.

In particular:

- A proof sketch is not a formally checked proof.
- A finite computation is not a universal mathematical proof.
- A passing test is not proof that every relevant implementation defect
  has been excluded.
- A mutation-test result measures detection of the mutations actually
  implemented and executed.
- A passing CI workflow establishes only the checks performed by that run.
- A source hash establishes byte-level identity, not mathematical correctness.
- A verified theorem does not automatically verify every implementation
  claiming to implement that theorem.

This contract establishes traceability requirements. It does not itself
prove any AQARION theorem or certify any existing implementation.

## 2. Normative terminology

The words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY express requirements
within this proposed contract.

### MUST

A mandatory requirement for a claim represented as conforming to this
contract.

### SHOULD

A strong recommendation. Any deviation SHOULD be documented with a reason.

### Evidence record

A structured record connecting a claim to the artifacts and observations
supporting its stated status.

### Tested revision

The exact Git commit whose source tree was used for a reported execution.

### Independent verifier

A verifier whose relevant correctness result does not depend on importing,
calling, or reusing the implementation under test in a way that compromises
the independence being claimed.

Independence is relative to a specified threat model. Separate filenames,
processes, or repositories alone do not establish it.

---

## 3. Fundamental invariant

Every registered claim MUST be traceable through the following chain:

    Claim
      -> Mathematical statement
      -> Definitions and assumptions
      -> Proof obligations
      -> Supporting evidence
      -> Source and test artifacts
      -> Tested revision
      -> Recorded execution results
      -> Explicit limitations
      -> Promotion decision

The record MUST distinguish what has been proved, what has been computed,
what has been tested, what has been formally checked, and what remains open.

Evidence MUST be bound to the exact claim and revision it supports.

A change to the mathematical statement, relevant assumptions, proof
dependencies, implementation, fixtures, or verification procedure MUST
trigger a review of whether the existing evidence remains applicable.

A successful verification result MUST NOT automatically promote the
mathematical proof status of a claim.

---

## 4. Required claim record

Every registered claim MUST have a stable identifier and the following
fields.

### 4.1 Identity

Required:

- `claim_id`: Stable identifier, for example `AQ-001`.
- `title`: Concise descriptive title.
- `version`: Version of the claim statement or contract.
- `status`: Current explicitly defined status.
- `owner`: Responsible project or maintainer role.
- `created`: Record creation date.
- `last_reviewed`: Most recent substantive review date.

Identifiers MUST NOT be silently reused for mathematically different claims.

### 4.2 Mathematical statement

Required:

- Exact statement of the claim.
- Definitions of all mathematical objects.
- Domain and codomain.
- Assumptions and hypotheses.
- Quantifiers and parameter ranges.
- Boundary cases.
- Required conventions.
- References to supporting lemmas.
- Explicit distinction between theorem, conjecture, definition, and
  empirical observation.

A computational statement MUST identify its finite domain and the precise
property checked.

An ambiguous or incomplete statement MUST NOT receive a verified-theorem
status.

### 4.3 Proof status

The record MUST use one of the following labels:

- `NO_PROOF`
- `CONJECTURE`
- `PROOF_SKETCH`
- `INFORMAL_PROOF`
- `REVIEWED_PROOF`
- `FORMALIZATION_IN_PROGRESS`
- `FORMALLY_VERIFIED`

Interpretation:

`NO_PROOF`
: No proof argument is currently recorded.

`CONJECTURE`
: The statement is proposed but not established.

`PROOF_SKETCH`
: A proof strategy is recorded, but essential details may remain unresolved.

`INFORMAL_PROOF`
: A complete written mathematical argument is available but has not
  necessarily undergone independent review.

`REVIEWED_PROOF`
: A complete argument has undergone documented mathematical review.

`FORMALIZATION_IN_PROGRESS`
: A machine-checkable proof is being developed but is not complete.

`FORMALLY_VERIFIED`
: The stated theorem has been checked by the declared proof assistant,
  with all required dependencies and assumptions identified.

A formal-verification record MUST identify:

- Proof-assistant name and version.
- Relevant source paths.
- Exact theorem declaration.
- Required imported modules and dependency versions.
- Build command and exit status.
- Tested Git revision.
- Whether unresolved placeholders, axioms, or admitted results occur in
  the theorem's dependency closure.
- Any trusted assumptions beyond the declared foundational system.

A zero-`sorry` search is useful evidence but is not sufficient by itself
to establish that a theorem has been correctly formalized.

The formal statement MUST faithfully represent the intended mathematical
claim, and its assumptions MUST be disclosed.

### 4.4 Computational evidence

Each computational result MUST record:

- Exact property checked.
- Finite domain.
- Number of cases executed.
- Enumeration method.
- Arithmetic model, including exact or floating-point arithmetic.
- Oracle implementation and its mathematical specification.
- Source path and source hash.
- Fixture paths and hashes, where applicable.
- Command executed.
- Exit status.
- Standard output and standard error, or retained references to them.
- Runtime.
- Runtime environment and relevant dependency versions.
- Tested revision.
- Known omissions and limitations.

The record MUST distinguish exhaustive enumeration of a stated finite
domain from random sampling, bounded exploration, and heuristic search.

If numerical tolerances are used, the record MUST identify the tolerance,
scaling rule, and potential numerical failure modes.

If exact arithmetic is claimed, the implementation MUST actually use
exact arithmetic for the relevant calculation.

A reported case count MUST come from an executed result or an explicitly
reproducible derivation. It MUST NOT be inferred from a planned command.

### 4.5 Implementation evidence

The record MUST identify:

- Implementation language.
- Source file paths.
- Source revision.
- Relevant source hashes.
- Public interface or entry point.
- Inputs and outputs.
- Error handling and invalid-input behavior.
- Known divergence between the mathematical specification and the code.
- Whether the implementation is the object under test or an independent
  verifier.

A source hash identifies the hashed bytes. It does not independently
establish correctness, reproducibility, authorship, or execution.

### 4.6 Regression evidence

The record MUST identify:

- Test names and purposes.
- Commands executed.
- Expected outcomes.
- Actual outcomes.
- Exit codes.
- Tested revision.
- Unexecuted tests.
- Known gaps in coverage.

Tests SHOULD include boundary cases, negative controls, invalid inputs,
and regression cases for previously discovered defects.

A test that merely repeats the implementation's own result without an
independent expected value MUST NOT be represented as an independent
correctness oracle.

### 4.7 Mutation evidence

Mutation testing MUST define each mutant precisely.

For every mutant, record:

- Stable mutant identifier.
- Source modification or executable mutant implementation.
- Intended semantic defect.
- Test or oracle expected to detect it.
- Whether the mutant was executed.
- Whether the mutant was killed or survived.
- Counterexample, if killed.
- Reason for survival, if known.
- Whether the mutant is equivalent to the reference implementation
  over the tested domain, if established.

Allowed outcomes:

- `KILLED`
- `SURVIVED`
- `NOT_RUN`
- `INVALID_MUTANT`
- `EQUIVALENT_WITHIN_PROVEN_SCOPE`

`EQUIVALENT_WITHIN_PROVEN_SCOPE` MUST identify the domain and the
equivalence argument. It MUST NOT imply universal equivalence without
a universal proof.

A mutant MUST NOT be counted as killed merely because its source differs
from the reference source.

Mutation coverage MUST use an explicit denominator. Unexecuted, invalid,
and excluded mutants MUST be reported separately.

Killing every declared mutant does not prove universal correctness.
Mutation results measure the sensitivity of the declared test procedure
to the declared mutations.

### 4.8 CI provenance

A CI evidence record MUST include, where available:

- Repository identifier.
- Workflow filename.
- Workflow run identifier or URL.
- Workflow job name.
- Tested commit SHA.
- Checkout state and relevant tree information.
- Workflow conclusion.
- Actual executed commands.
- Test summaries.
- Artifact names and hashes.
- Runtime environment.
- Failed, skipped, or cancelled jobs.
- Any tests or checks not covered by the workflow.

The record MUST distinguish:

- Workflow configured.
- Workflow triggered.
- Workflow running.
- Workflow passed.
- Workflow failed.
- Workflow cancelled.
- Artifact generated.
- Artifact independently inspected.

A green badge alone MUST NOT be treated as evidence of test counts,
mutation outcomes, formal proof completion, or artifact contents.

A workflow pass MUST be described according to the checks actually
executed in the corresponding run.

### 4.9 Limitations

Every claim record MUST explicitly state what its evidence does not
establish.

Examples include:

- Universal validity beyond the proved theorem's hypotheses.
- Correctness outside the enumerated finite domain.
- Independence of an oracle that shares implementation logic.
- Absence of defects not represented by the mutation set.
- Formal verification when only numerical or Python tests have run.
- Reproducibility on environments not tested.
- Validity of assumptions not independently established.
- Correctness of downstream claims not included in the proof.

The absence of a known counterexample MUST NOT be represented as proof
that no counterexample exists.

### 4.10 Promotion decision

Each status change MUST record:

- Previous status.
- Proposed status.
- Decision date.
- Responsible reviewer or authority.
- Evidence supporting promotion.
- Outstanding obligations.
- Explicit acceptance or rejection.
- Tested revision, where relevant.

Promotion MUST be justified by the requirements of the target status.
A successful test run alone MUST NOT promote `PROOF_SKETCH` or
`INFORMAL_PROOF` to `FORMALLY_VERIFIED`.

---

## 5. Evidence classes

The following labels describe evidence type. They do not, by themselves,
define a universal ranking of mathematical strength.

### [D] Definition

A declared mathematical definition, convention, or specification.

### [P] Mathematical proof

A mathematical argument supporting a stated proposition under explicit
hypotheses.

The record SHOULD identify the proof location and essential dependencies.

### [V] Computational verification

A reproducible computation over a stated finite domain.

The record MUST disclose the domain, implementation, arithmetic,
oracle, and execution evidence.

### [PV] Proof plus computational verification

A claim supported by both a mathematical proof and a computational
cross-check.

The proof and computation MUST be recorded separately. The computational
result MUST NOT be treated as a substitute for missing proof steps.

### [L] Formal verification

A proof checked by a declared proof assistant under identified assumptions
and dependencies.

### [R] Reproducibility evidence

Evidence that a specified computation or build can be replayed under
a declared environment and revision.

### [C] Certification

A project-level decision that explicitly identifies the claim, scope,
verification requirements, independent checks, provenance, and approving
authority.

Certification MUST NOT be inferred automatically from [P], [V], [L],
or [R].

### [F] Frozen artifact

An artifact or claim explicitly recorded as frozen in the relevant
registry, with an identified revision and scope.

A frozen status does not imply that every related conjecture, extension,
or downstream claim is proved.

Multiple labels MAY apply to a claim, provided each label is independently
supported and its scope is recorded.

---

## 6. Claim-status promotion rules

The following transitions are permitted only when their stated conditions
are met.

### 6.1 Proposed -> Specified

Required:

- Stable claim identifier.
- Complete mathematical statement.
- Explicit assumptions and definitions.
- Defined evidence requirements.
- Identified owner.

### 6.2 Specified -> Proof in progress

Required:

- Identified proof obligations.
- Recorded proof strategy or formalization plan.
- Explicit unresolved lemmas.

This transition does not establish correctness.

### 6.3 Proof in progress -> Informally proved

Required:

- Complete mathematical argument.
- No unresolved essential proof step.
- Assumptions and quantifiers checked against the registered statement.
- Documented review of critical inferences.

### 6.4 Informally proved -> Formally verified

Required:

- Formal theorem corresponding to the registered statement.
- Successful proof-assistant build.
- Identified dependency closure.
- Review of axioms and unresolved placeholders.
- Confirmation that the formal statement matches the intended theorem.
- Revision-bound proof source and build evidence.

A successful build of an unrelated module is insufficient.

### 6.5 Computation proposed -> Computationally verified within scope

Required:

- Explicit finite domain.
- Executed verification command.
- Recorded exit status and outputs.
- Correctly specified oracle.
- Reproducible source and fixture identification.
- Reported case count obtained from the execution.
- Explicit numerical-arithmetic policy.
- No unreported mismatches.

This status is bounded by the actual computation.

### 6.6 Computationally verified -> Independently reproduced

Required:

- Independent replay of the stated computation.
- Identified independence boundary.
- Comparison of the relevant outputs.
- Recorded environment and revision information.
- Explicit disclosure of shared dependencies and assumptions.

Two executions of the same code are reproducibility evidence, but do not
necessarily establish independent implementation correctness.

### 6.7 Verified evidence -> Certified

Required:

- Defined certification scope.
- All mandatory proof and verification obligations for that scope met.
- Independent review appropriate to the claim.
- Revision-bound evidence.
- Recorded limitations.
- Explicit certification decision by the designated authority.

Certification MUST NOT exceed the scope of its supporting evidence.

---

## 7. Oracle independence requirements

A verifier MUST identify which parts of the computation are independent
of the implementation under test.

The record SHOULD distinguish:

1. Independent mathematical specification.
2. Independent construction of inputs and fixtures.
3. Independent implementation of the oracle.
4. Independent comparison procedure.
5. Shared libraries, algorithms, or assumptions.
6. Shared source code or imported modules.

Independence is not binary in every setting. The relevant threat model
MUST be stated.

If both the implementation and oracle share a faulty definition,
the comparison may reproduce the same error.

Where feasible, use different mathematical formulations, exact arithmetic,
hand-constructed boundary cases, and negative controls.

An independent oracle MUST NOT be described as independent merely because
it is in a different file.

---

## 8. Revision and artifact integrity

Evidence MUST be tied to identifiable source and inputs.

For Git-based projects, record the full tested commit SHA.

Where generated artifacts are used, record their hashes and generation
commands.

Where a clean working tree is required, record the result of the
working-tree check.

If source changes after a passing CI run, the earlier run remains evidence
for the earlier revision. It MUST NOT be silently attributed to the new
revision.

If a workflow run is still in progress, its final result MUST NOT be
reported as passed.

If an artifact is unavailable for inspection, its contents MUST NOT be
inferred from its filename, badge, or expected workflow behavior.

Hashes support integrity checks but do not replace mathematical review,
independent verification, or execution evidence.

---

## 9. AQARION example: SM003 defect-rank identity

This section illustrates the contract. It is not a substitute for the
SM003 proof, source code, workflow, or verification artifacts.

### 9.1 Claim

For a finite set \(X\), deterministic map \(T:X\to X\), partition
\(\Pi=\{B_1,\ldots,B_k\}\), Koopman operator \(Kf=f\circ T\), and
blockwise averaging orthogonal projector \(P_\Pi\), define

\[
D_\Pi=(I-P_\Pi)KP_\Pi.
\]

Let \(H_\Pi\) have one vertex per partition block. For every source block,
connect all target blocks intersecting its image under \(T\). Include
isolated vertices.

The claim is

\[
\operatorname{rank}(D_\Pi)=k-c(H_\Pi),
\]

where \(c(H_\Pi)\) is the number of connected components.

### 9.2 Mathematical evidence

For \(f\) block-constant, write \(a_j\) for its value on \(B_j\).
The function \(Kf\) is constant on each source block precisely when
the values \(a_j\) agree on all target blocks co-occurring in the image
of that source block.

Consequently, the kernel of the restriction of \(D_\Pi\) to the
block-constant space corresponds to assignments constant on the connected
components of \(H_\Pi\). Its dimension is \(c(H_\Pi)\).

The defect vanishes on the orthogonal complement of the block-constant
space because \(P_\Pi\) vanishes there. Thus

\[
\dim\ker D_\Pi=(|X|-k)+c(H_\Pi),
\]

and rank-nullity yields

\[
\operatorname{rank}(D_\Pi)=k-c(H_\Pi).
\]

This argument supports [P] when its definitions and hypotheses match
the registered implementation and theorem.

### 9.3 Separate evidence records

SM003 MUST separately record:

- **Mathematics:** The proof and its assumptions.
- **Implementation:** The actual operator and graph constructions.
- **Computation:** The finite cases actually enumerated.
- **Mutation testing:** The mutants actually executed and their outcomes.
- **CI:** The tested commit, workflow run, exit status, and artifacts.
- **Formalization:** Lean status, if a corresponding proof exists.
- **Certification:** Any explicit independent certification decision.

A successful CI result alone does not establish all seven items.

### 9.4 Commit-specific example

A reported passing SM003 baseline identifies commit

`78f4184d9576e40c7312f6bbea1eda1bcbd0bf4e`.

That identifier may be recorded as the reported baseline. The actual workflow
run, logs, artifact hashes, case counts, mutation outcomes, and formal proof
status MUST be read from their corresponding evidence sources.

They MUST NOT be invented or inferred from the commit identifier.

Until those records are inspected, the commit-specific CI result MUST
remain distinct from any broader claim of certification.

---

## 10. Minimum review checklist

Before accepting a claim record, reviewers MUST check:

- [ ] The mathematical statement is unambiguous.
- [ ] Definitions, assumptions, and quantifiers are explicit.
- [ ] The proof status accurately reflects the available argument.
- [ ] Computational scope and case counts are recorded.
- [ ] Exact versus floating-point arithmetic is disclosed.
- [ ] The oracle is specified and its independence boundary is stated.
- [ ] Source paths and revision are identified.
- [ ] Test commands and actual outcomes are recorded.
- [ ] Mutation outcomes distinguish killed, surviving, and unexecuted
      mutants.
- [ ] CI provenance identifies the actual tested revision.
- [ ] Artifacts and hashes are recorded where required.
- [ ] Limitations are explicit.
- [ ] Promotion is justified by the target status requirements.
- [ ] No unsupported certification or frozen-status claim is present.

A failed item MUST be recorded as outstanding rather than silently treated
as satisfied.

---

## 11. Non-goals

AQ-EVIDENCE-001 does not:

- Prove any mathematical theorem by itself.
- Guarantee the correctness of every registered proof.
- Guarantee that every implementation bug has been anticipated.
- Establish universal correctness from bounded enumeration.
- Establish oracle independence merely from code separation.
- Make mutation coverage equivalent to proof completeness.
- Turn CI success into formal verification.
- Replace AQARION's mathematical claim registry.
- Replace Lean's proof checker.
- Replace independent code review or reproducibility testing.
- Certify unreviewed downstream results.

---

## 12. Acceptance criteria for this document

This document may be considered repository-integrated only after:

1. It is committed at the specified repository path.
2. Its exact commit and file hash are recorded.
3. A reviewer confirms consistency with the existing AQARION claim registry.
4. Existing status labels are mapped explicitly rather than silently
   reinterpreted.
5. Any overlap with existing governance specifications is documented.
6. The integration does not overwrite or alter the SM003 passing baseline.
7. Any CI checks required by the repository are actually executed and
   their outcomes recorded.

Until these conditions are met, its status remains:

`PROPOSED — NOT YET REPOSITORY-VERIFIED`

---

## 13. Change control

Changes to this contract MUST preserve the distinction between mathematical
proof, computational evidence, implementation behavior, reproducibility,
formal verification, and certification.

A change that weakens an evidence requirement MUST be documented and
reviewed explicitly.

Historical evidence MUST retain its original tested revision and scope.
New evidence may supersede an earlier record, but MUST NOT rewrite the
historical result of a previous run.

The contract itself MUST NOT be marked formally verified merely because
its requirements are internally consistent or its examples execute.

**End of AQ-EVIDENCE-001.**
