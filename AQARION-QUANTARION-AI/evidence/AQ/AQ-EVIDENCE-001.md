AQ-EVIDENCE-001 — Claim-to-Evidence Traceability Contract

Protocol: AQARION Claim-to-Evidence Traceability
Version: 1.1.0
Status: PROPOSED — NOT YET REPOSITORY-VERIFIED
Scope: Mathematical claims, informal proofs, formal proofs, computational verification, independent verification, regression testing, mutation analysis, and CI provenance.

---

1. Purpose

AQ-EVIDENCE-001 defines a consistent, revision-aware contract for connecting each registered AQARION mathematical claim to its precise statement, supporting argument, implementation, executed verification procedures, and documented limitations.

Its central requirement is traceability: every reported status must be supported by evidence appropriate to that status.

The contract distinguishes the following:

- A proof sketch is not a complete mathematical proof.
- A complete informal proof is not necessarily a machine-checked proof.
- A finite computation does not establish a universal theorem outside its stated scope.
- A passing regression suite does not establish that every relevant implementation defect has been excluded.
- A mutation-testing result measures how the executed verification procedure responds to the specific mutants actually tested.
- A passing CI workflow establishes the outcome of the checks performed by that run, not every property of the repository.
- A source hash establishes the identity of the hashed bytes, not their mathematical correctness.
- A verified theorem does not automatically verify every implementation intended to realize it.
- Independent reproduction of a result does not, by itself, establish independent correctness of the underlying specification.
- A frozen artifact does not automatically confer frozen status on related conjectures, extensions, or downstream claims.

This contract defines evidence-recording and review requirements. It does not itself prove an AQARION theorem, verify an implementation, or certify an existing repository artifact.

2. Normative terminology

The terms MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY express requirements within this proposed contract.

2.1 MUST

A mandatory requirement for a claim or artifact represented as conforming to this contract.

2.2 SHOULD

A strong recommendation. A deviation SHOULD be documented with its rationale and any resulting limitation.

2.3 Evidence record

A structured record connecting a claim to the mathematical statement, relevant artifacts, execution observations, revision, and limitations supporting its reported status.

2.4 Tested revision

The exact Git commit whose source tree was used for the reported execution or review.

2.5 Independent verifier

A verifier whose relevant result does not depend on importing, calling, or reusing the implementation under test in a way that compromises the particular independence being claimed.

Independence is relative to a declared threat model. Separate filenames, processes, directories, or repositories do not, by themselves, establish independent correctness.

2.6 Verification scope

The explicitly stated mathematical domain, implementation behavior, test set, execution environment, and assumptions covered by an evidence record.

A result MUST NOT be generalized beyond its verification scope without additional justification.

2.7 Mutation outcome

The recorded result of executing a specified mutant against a declared test or verification procedure.

The outcome MUST describe the observed result, not imply a stronger conclusion about correctness than the evidence supports.

3. Fundamental invariant

Every registered claim MUST be traceable through the following chain:

Claim identifier
  -> Mathematical statement
  -> Definitions and assumptions
  -> Proof obligations
  -> Supporting evidence
  -> Source and test artifacts
  -> Tested revision
  -> Recorded execution results
  -> Explicit limitations
  -> Review and promotion decision

The record MUST distinguish what has been proved, what has been computed, what has been tested, what has been formally checked, what has been independently reproduced, and what remains unresolved.

Evidence MUST be bound to the exact claim and revision it supports.

A change to the mathematical statement, relevant assumptions, proof dependencies, implementation, fixtures, oracle, or verification procedure MUST trigger a review of whether existing evidence remains applicable.

Historical evidence MUST retain its original scope and tested revision.

A successful verification result MUST NOT automatically promote the mathematical proof status of a claim.

4. Required claim record

Every registered claim MUST have a stable identifier and the fields required by the applicable evidence category.

4.1 Identity

Required fields:

- "claim_id": Stable identifier, for example "AQ-001".
- "title": Concise descriptive title.
- "version": Version of the claim statement or governing contract.
- "status": Explicitly defined current status.
- "owner": Responsible project or maintainer role.
- "created": Record creation date.
- "last_reviewed": Most recent substantive review date.

Identifiers MUST NOT be silently reused for mathematically different claims.

A statement change that materially alters the claim MUST be recorded as a revision or a new claim, according to the repository's registry rules.

4.2 Mathematical statement

The record MUST contain:

- The exact claim statement.
- Definitions of all mathematical objects.
- Domain and codomain.
- Assumptions and hypotheses.
- Quantifiers and parameter ranges.
- Boundary cases.
- Required conventions.
- References to supporting lemmas.
- An explicit distinction between theorem, conjecture, definition, and empirical observation.

A computational claim MUST identify its finite domain and the precise property checked.

An ambiguous or incomplete statement MUST NOT receive a verified-theorem status.

Where an implementation is intended to realize a mathematical definition, the record SHOULD identify the correspondence between the formal specification and the implemented operations.

4.3 Proof status

The record MUST use one of the following labels:

- "NO_PROOF"
- "CONJECTURE"
- "PROOF_SKETCH"
- "INFORMAL_PROOF"
- "REVIEWED_PROOF"
- "FORMALIZATION_IN_PROGRESS"
- "FORMALLY_VERIFIED"

Interpretation:

"NO_PROOF"
No proof argument is currently recorded.

"CONJECTURE"
The statement is proposed but not established.

"PROOF_SKETCH"
A proof strategy is recorded, but essential details may remain unresolved.

"INFORMAL_PROOF"
A complete written mathematical argument is available, but independent mathematical review or formal checking may still be outstanding.

"REVIEWED_PROOF"
A complete mathematical argument has undergone documented mathematical review.

"FORMALIZATION_IN_PROGRESS"
A machine-checkable proof is being developed but is not complete.

"FORMALLY_VERIFIED"
The stated theorem has been checked by the declared proof assistant, with the relevant dependencies and assumptions identified and reviewed.

A formal-verification record MUST identify:

- Proof-assistant name and version.
- Relevant source paths.
- Exact theorem declaration.
- Required imported modules and dependency versions.
- Build command and exit status.
- Tested Git revision.
- Whether unresolved placeholders, axioms, or admitted results occur in the theorem's dependency closure.
- Trusted assumptions beyond the declared foundational system.
- Any limitations on the relationship between the formal statement and the intended mathematical claim.

A zero-"sorry" search is useful evidence but is not sufficient by itself to establish that a theorem has been correctly formalized.

The formal statement MUST faithfully represent the intended mathematical claim, and its assumptions MUST be disclosed.

A successful build MUST be attributed only to the declarations and dependencies actually checked by that build.

4.4 Computational evidence

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

The record MUST distinguish exhaustive enumeration of a stated finite domain from random sampling, bounded exploration, and heuristic search.

If numerical tolerances are used, the record MUST identify the tolerance, scaling rule, and relevant numerical failure modes.

If exact arithmetic is claimed, the implementation MUST actually use exact arithmetic for the relevant calculation.

A reported case count MUST come from an executed result or an explicitly reproducible derivation. It MUST NOT be inferred from a planned command or intended test configuration.

A computation that completes without a reported mismatch supports only the property checked over the domain actually examined, subject to the correctness of the implementation, oracle, and execution record.

4.5 Implementation evidence

The record MUST identify:

- Implementation language.
- Source file paths.
- Source revision.
- Relevant source hashes.
- Public interface or entry point.
- Inputs and outputs.
- Error handling and invalid-input behavior.
- Known divergence between the mathematical specification and the code.
- Whether the implementation is the object under test or an independent verifier.

A source hash identifies the hashed bytes. It does not independently establish correctness, reproducibility, authorship, or execution.

If the source changes after a verification run, the earlier result MUST remain associated with the earlier revision unless the evidence is explicitly and validly reproduced against the new revision.

4.6 Regression evidence

The record MUST identify:

- Test names and purposes.
- Commands executed.
- Expected outcomes.
- Actual outcomes.
- Exit codes.
- Tested revision.
- Unexecuted tests.
- Known gaps in coverage.

Tests SHOULD include boundary cases, negative controls, invalid inputs, and regression cases for previously discovered defects.

A test that merely repeats the implementation's own result without an independently specified expected value MUST NOT be represented as an independent correctness oracle.

A test suite's reported status MUST distinguish tests that passed from tests that failed, were skipped, were unavailable, or were not executed.

4.7 Mutation evidence

Mutation testing MUST define each mutant precisely and record the result of the declared verification procedure against that mutant.

For every mutant, record:

- Stable mutant identifier.
- Source modification or executable mutant implementation.
- Intended semantic defect.
- Test or oracle expected to detect the defect.
- Whether the mutant was executed.
- Recorded mutation outcome.
- Relevant observed output or counterexample.
- Reason for a "NOT_DETECTED" result, if known.
- Whether equivalence to the reference behavior has been established over the tested domain.
- The scope of any equivalence argument.
- Any execution error or invalid-mutant determination.

The permitted outcome labels are:

- "DETECTED"
- "NOT_DETECTED"
- "NOT_RUN"
- "INVALID_MUTANT"

These labels have the following meanings.

"DETECTED"

The declared test or verification procedure executed against the mutant and produced the specified evidence that the mutation was detected.

The record SHOULD identify the failing assertion, mismatched result, counterexample, or other detection signal.

A "DETECTED" result does not, by itself, establish that the test suite is complete or that the reference implementation is universally correct.

"NOT_DETECTED"

The mutant was executed, but the declared verification procedure did not detect the intended semantic difference.

The result MUST NOT be interpreted as proof that the mutant is equivalent to the reference implementation.

The record SHOULD state whether the cause is known, such as insufficient test coverage, an ineffective assertion, an unexercised execution path, or a potentially equivalent transformation.

"NOT_RUN"

The mutant was not executed by the declared verification procedure.

A planned execution, generated mutant, or configured test does not qualify as an executed result.

"INVALID_MUTANT"

The proposed mutant could not be evaluated as intended because it was malformed, failed to load, failed to compile, violated the mutation protocol, or otherwise did not represent an evaluable instance of the intended mutation.

The reason MUST be recorded. An invalid mutant MUST NOT be counted as "DETECTED".

Equivalent mutants

Where equivalence has been established, the record MAY add a separate qualification:

"equivalence_status: EQUIVALENT_WITHIN_PROVEN_SCOPE"

This qualification MUST identify the tested domain and the equivalence argument.

It MUST NOT imply universal equivalence unless a valid universal argument establishes that conclusion.

Equivalence is a property supported by its own evidence, not a substitute for recording whether the mutant was executed or whether the declared verification procedure detected a difference.

Mutation accounting

Mutation summaries MUST use an explicit denominator and MUST report unexecuted and invalid mutants separately.

The summary MUST distinguish:

- Mutants executed and "DETECTED".
- Mutants executed and "NOT_DETECTED".
- Mutants not executed.
- Invalid mutants.
- Any excluded mutants and the documented reason for exclusion.

Any reported detection rate MUST state its numerator, denominator, and exclusion policy.

The report MUST NOT silently exclude "NOT_DETECTED", "NOT_RUN", or "INVALID_MUTANT" outcomes to inflate the reported rate.

A complete detection result for the declared mutation set does not prove universal correctness. Mutation analysis measures the sensitivity of the declared verification procedure to the mutations actually defined and evaluated.

4.8 CI provenance

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
- Checks not covered by the workflow.

The record MUST distinguish:

- Workflow configured.
- Workflow triggered.
- Workflow running.
- Workflow passed.
- Workflow failed.
- Workflow cancelled.
- Artifact generated.
- Artifact independently inspected.

A green badge alone MUST NOT be treated as evidence of test counts, mutation outcomes, formal proof completion, or artifact contents.

A workflow pass MUST be described according to the checks actually executed in the corresponding run.

If the workflow configuration changes, the evidence record MUST identify which revision of that configuration was used for the reported result.

4.9 Limitations

Every claim record MUST explicitly state what its evidence does not establish.

Examples include:

- Universal validity beyond the proved theorem's hypotheses.
- Correctness outside the enumerated finite domain.
- Independence of an oracle that shares implementation logic.
- Absence of defects not represented by the mutation set.
- Formal verification when only numerical or Python tests have run.
- Reproducibility on environments not tested.
- Validity of assumptions not independently established.
- Correctness of downstream claims not included in the proof.
- Equivalence of a mutant outside the domain covered by its equivalence argument.
- Correctness of a CI artifact whose contents have not been inspected.

The absence of a known counterexample MUST NOT be represented as proof that no counterexample exists.

4.10 Promotion decision

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

A successful test run alone MUST NOT promote "PROOF_SKETCH" or "INFORMAL_PROOF" to "FORMALLY_VERIFIED".

An artifact's completion status MUST NOT be inferred solely from the completion of a related artifact.

5. Evidence classes

The following labels describe evidence type. They do not, by themselves, define a universal ranking of mathematical strength.

[D] Definition

A declared mathematical definition, convention, or specification.

[P] Mathematical proof

A mathematical argument supporting a stated proposition under explicit hypotheses.

The record SHOULD identify the proof location, assumptions, and essential dependencies.

[V] Computational verification

A reproducible computation over a stated finite domain.

The record MUST disclose the domain, implementation, arithmetic, oracle, and execution evidence.

[PV] Proof plus computational verification

A claim supported by both a mathematical proof and a computational cross-check.

The proof and computation MUST be recorded separately. The computational result MUST NOT be treated as a substitute for missing proof steps.

[L] Formal verification

A proof checked by a declared proof assistant under identified assumptions and dependencies.

The record MUST identify the relevant theorem, build result, source revision, and proof dependencies.

[R] Reproducibility evidence

Evidence that a specified computation or build can be replayed under a declared environment and revision.

Reproducibility does not automatically establish mathematical correctness or implementation independence.

[C] Certification

A project-level decision that explicitly identifies the claim, scope, verification requirements, independent checks, provenance, and approving authority.

Certification MUST NOT be inferred automatically from [P], [V], [L], or [R].

[F] Frozen artifact

An artifact or claim explicitly recorded as frozen in the relevant registry, with an identified revision and scope.

A frozen status does not imply that every related conjecture, extension, implementation, or downstream claim is proved.

Multiple labels MAY apply to a claim, provided each label is independently supported and its scope is recorded.

6. Claim-status promotion rules

The following transitions are permitted only when their stated conditions are met.

6.1 Proposed -> Specified

Required:

- Stable claim identifier.
- Complete mathematical statement.
- Explicit assumptions and definitions.
- Defined evidence requirements.
- Identified owner.

6.2 Specified -> Proof in progress

Required:

- Identified proof obligations.
- Recorded proof strategy or formalization plan.
- Explicit unresolved lemmas.

This transition does not establish correctness.

6.3 Proof in progress -> Informally proved

Required:

- Complete mathematical argument.
- No unresolved essential proof step.
- Assumptions and quantifiers checked against the registered statement.
- Documented review of critical inferences.

Any remaining uncertainty MUST be described rather than hidden by the status label.

6.4 Informally proved -> Formally verified

Required:

- Formal theorem corresponding to the registered statement.
- Successful proof-assistant build.
- Identified dependency closure.
- Review of axioms and unresolved placeholders.
- Confirmation that the formal statement matches the intended theorem.
- Revision-bound proof source and build evidence.

A successful build of an unrelated module is insufficient.

6.5 Computation proposed -> Computationally verified within scope

Required:

- Explicit finite domain.
- Executed verification command.
- Recorded exit status and outputs.
- Correctly specified oracle.
- Reproducible source and fixture identification.
- Reported case count obtained from the execution.
- Explicit numerical-arithmetic policy.
- No unreported mismatches.

This status is bounded by the actual computation and its stated assumptions.

6.6 Computationally verified -> Independently reproduced

Required:

- Independent replay of the stated computation.
- Identified independence boundary.
- Comparison of the relevant outputs.
- Recorded environment and revision information.
- Explicit disclosure of shared dependencies and assumptions.

Two executions of the same code provide reproducibility evidence but do not necessarily establish independent implementation correctness.

6.7 Verified evidence -> Certified

Required:

- Defined certification scope.
- All mandatory proof and verification obligations for that scope met.
- Independent review appropriate to the claim.
- Revision-bound evidence.
- Recorded limitations.
- Explicit certification decision by the designated authority.

Certification MUST NOT exceed the scope of its supporting evidence.

7. Oracle independence requirements

A verifier MUST identify which parts of the computation are independent of the implementation under test.

The record SHOULD distinguish:

1. Independent mathematical specification.
2. Independent construction of inputs and fixtures.
3. Independent implementation of the oracle.
4. Independent comparison procedure.
5. Shared libraries, algorithms, or assumptions.
6. Shared source code or imported modules.
7. Shared preprocessing or serialization logic that could affect the result.

Independence is not binary in every setting. The relevant threat model MUST be stated.

If both the implementation and oracle share a faulty definition, the comparison may reproduce the same error.

Where feasible, use different mathematical formulations, exact arithmetic, hand-constructed boundary cases, and negative controls.

An independent oracle MUST NOT be described as independent merely because it is located in a different file.

The record SHOULD identify the specific failure modes the independence boundary is intended to address.

8. Revision and artifact integrity

Evidence MUST be tied to identifiable source and inputs.

For Git-based projects, record the full tested commit SHA.

Where generated artifacts are used, record their hashes and generation commands.

Where a clean working tree is required, record the result of the working-tree check.

If source changes after a passing CI run, the earlier run remains evidence for the earlier revision. It MUST NOT be silently attributed to the new revision.

If a workflow run is still in progress, its final result MUST NOT be reported as passed.

If an artifact is unavailable for inspection, its contents MUST NOT be inferred from its filename, badge, or expected workflow behavior.

Hashes support integrity checks but do not replace mathematical review, independent verification, or execution evidence.

A hash comparison MUST specify the bytes being hashed and the algorithm used. A displayed prefix MUST NOT be presented as a complete digest.

A generated report MUST be distinguishable from a report whose contents and provenance have been independently inspected.

9. AQARION example: SM003 defect-rank identity

This section illustrates the contract. It is not a substitute for the SM003 proof, source code, workflow, or verification artifacts.

9.1 Claim

For a finite set X, deterministic map T:X\to X, partition
\Pi={B_1,\ldots,B_k}, Koopman operator Kf=f\circ T, and
blockwise averaging orthogonal projector P_\Pi, define

[
D_\Pi=(I-P_\Pi)KP_\Pi.
]

Let H_\Pi have one vertex per partition block. For every source block, connect all target blocks intersecting its image under T. Include isolated vertices.

The claim is

[
\operatorname{rank}(D_\Pi)=k-c(H_\Pi),
]

where c(H_\Pi) is the number of connected components.

The mathematical statement and implementation MUST use the same graph convention, including the treatment of isolated vertices and target blocks reached from each source block.

9.2 Mathematical evidence

For f block-constant, write a_j for its value on B_j.

The function Kf is constant on each source block precisely when the values a_j agree on all target blocks co-occurring in the image of that source block.

Consequently, the kernel of the restriction of D_\Pi to the block-constant space corresponds to assignments constant on the connected components of H_\Pi. Its dimension is c(H_\Pi).

The defect vanishes on the orthogonal complement of the block-constant space because P_\Pi vanishes there. Thus

[
\dim\ker D_\Pi=(|X|-k)+c(H_\Pi),
]

and rank-nullity yields

[
\operatorname{rank}(D_\Pi)=k-c(H_\Pi).
]

This argument supports [P] when its definitions, hypotheses, and operator conventions match the registered theorem.

The proof record MUST preserve the canonical defect definition. An alternative operator MUST NOT be substituted without a separate statement and justification.

9.3 Separate evidence records

SM003 MUST separately record:

- Mathematics: The proof and its assumptions.
- Implementation: The actual operator and graph constructions.
- Computation: The finite cases actually enumerated.
- Mutation analysis: The mutants actually executed and their recorded outcomes.
- CI: The tested commit, workflow run, exit status, and artifacts.
- Formalization: Lean status, if a corresponding proof exists.
- Certification: Any explicit independent certification decision.

A successful CI result alone does not establish all seven items.

9.4 Commit-specific example

A passing SM003 baseline has been reported for commit:

"78f4184d9576e40c7312f6bbea1eda1bcbd0bf4e"

This identifier may be recorded as the reported baseline. The actual workflow run, logs, artifact hashes, case counts, mutation outcomes, and formal proof status MUST be read from their corresponding evidence sources.

They MUST NOT be invented or inferred from the commit identifier or a workflow badge.

Until those records are inspected, the commit-specific CI result MUST remain distinct from any broader claim of certification.

This example records the provenance identifier supplied for the reported baseline; it does not independently establish the current workflow conclusion or the contents of its artifacts.

10. Minimum review checklist

Before accepting a claim record, reviewers MUST check:

- [ ] The mathematical statement is unambiguous.
- [ ] Definitions, assumptions, and quantifiers are explicit.
- [ ] The proof status accurately reflects the available argument.
- [ ] Computational scope and case counts are recorded.
- [ ] Exact versus floating-point arithmetic is disclosed.
- [ ] The oracle is specified and its independence boundary is stated.
- [ ] Source paths and revision are identified.
- [ ] Test commands and actual outcomes are recorded.
- [ ] Mutation outcomes use "DETECTED", "NOT_DETECTED", "NOT_RUN", or "INVALID_MUTANT" as appropriate.
- [ ] Any equivalence qualification identifies its proven scope.
- [ ] Mutation accounting identifies its denominator and exclusions.
- [ ] CI provenance identifies the actual tested revision.
- [ ] Artifacts and hashes are recorded where required.
- [ ] Limitations are explicit.
- [ ] Promotion is justified by the target status requirements.
- [ ] No unsupported certification or frozen-status claim is present.

A failed or uncompleted item MUST be recorded as outstanding rather than silently treated as satisfied.

11. Non-goals

AQ-EVIDENCE-001 does not:

- Prove any mathematical theorem by itself.
- Guarantee the correctness of every registered proof.
- Guarantee that every implementation defect has been anticipated.
- Establish universal correctness from bounded enumeration.
- Establish oracle independence merely from code separation.
- Make mutation coverage equivalent to proof completeness.
- Turn CI success into formal verification.
- Treat a "DETECTED" result as universal proof of correctness.
- Treat a "NOT_DETECTED" result as proof of mutant equivalence.
- Treat "NOT_RUN" or "INVALID_MUTANT" as successful detection.
- Replace AQARION's mathematical claim registry.
- Replace Lean's proof checker.
- Replace independent code review or reproducibility testing.
- Certify unreviewed downstream results.
- Retroactively extend evidence from one revision to a different revision.

12. Acceptance criteria for this document

This document may be considered repository-integrated only after:

1. It is committed at the specified repository path.
2. Its exact commit and file hash are recorded.
3. A reviewer confirms consistency with the existing AQARION claim registry.
4. Existing status labels are mapped explicitly rather than silently reinterpreted.
5. Any overlap with existing governance specifications is documented.
6. The integration does not overwrite or alter the SM003 passing baseline.
7. Any CI checks required by the repository are actually executed and their outcomes recorded.
8. The mutation terminology is consistent throughout the document and related records that claim conformance to this version.
9. The change is reviewed for unintended changes to mathematical statements or evidence scope.

Until these conditions are met, its status remains:

"PROPOSED — NOT YET REPOSITORY-VERIFIED"

This status describes the integration and review state of the document. It does not imply that the mathematical example in Section 9 is itself unproved or that any specific existing repository check has failed.

13. Change control

Changes to this contract MUST preserve the distinction between mathematical proof, computational evidence, implementation behavior, reproducibility, formal verification, mutation analysis, and certification.

A change that weakens an evidence requirement MUST be documented and reviewed explicitly.

Historical evidence MUST retain its original tested revision and scope.

New evidence may supersede an earlier record, but MUST NOT rewrite the historical result of a previous run.

Changes to mutation outcome labels MUST be applied consistently to the governing contract, applicable schemas, verification scripts, generated reports, and documentation that claims conformance. A terminology change MUST NOT silently rewrite the recorded observation from a historical test run.

The contract itself MUST NOT be marked formally verified merely because its requirements are internally consistent or its examples execute.

End of AQ-EVIDENCE-001.
