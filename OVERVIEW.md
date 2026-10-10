# AQARION: Public Research Artifact Overview and Verification Checkpoint

Checkpoint date: October 9, 2026  
Canonical repository: quantarion369-arch/AQARION  
Document type: public research article, artifact overview, and evidence checkpoint

## Abstract

AQARION maintains research implementations, verification scripts, regression
tests, and workflow artifacts for investigating exact structural relationships
and the reliability of their computational evidence.

This checkpoint brings together three strands:

1. SM003 exact matrix-rank and graph-rank comparison.
2. D22 direct-projection validation.
3. Mobile Research Kit integrity and regression verification.

The evidence described here includes reported hosted workflow results,
artifact inspections described in a supplied audit, and directly supplied
Termux regression output.

These evidence classes are kept distinct. A successful workflow establishes
that its configured checks completed successfully at a particular revision.
It does not, by itself, establish a universal mathematical theorem, formal
verification, novelty, or priority.

## 1. Evidence and Claim Boundaries

This document uses the following distinctions.

### Mathematical proof

A general argument establishing a claim under explicitly stated definitions,
assumptions, and conventions.

A finite computation can support a proof-development process but does not
replace a general argument over an unbounded domain.

### Computational verification

Execution of a specified implementation over a stated finite domain, with
recorded outcomes.

Its scope is limited to the cases, implementation, and conventions actually
tested.

### Regression verification

Execution of tests intended to detect changes in expected software behavior.

Passing regression tests support the tested behavior. They are not a blanket
guarantee that every possible defect has been excluded.

### Artifact and provenance verification

Inspection of files, receipts, hashes, workflow logs, and revision identifiers
to establish what was preserved and what was reported to have run.

Hash agreement establishes consistency with the referenced bytes. It does
not independently establish the correctness of the mathematical content.

### Evidence available for this checkpoint

The Mobile Research Kit local results were supplied as terminal output.

The hosted SM003, D22, and final Mobile Research Kit details were described
in a supplied repository audit. This document records those details with that
attribution; its preparation did not independently reproduce every hosted
artifact inspection.

## 2. SM003: Exact Rank and Mutation Evidence

### Research relationship

The supplied audit identifies the central relationship as

    rank(D_Pi) = k - c(H_Pi),

with

    D_Pi = (I - P) K P.

Here, the audit describes P as the projection onto block-constant functions,
k as the number of partition blocks, and c(H_Pi) as the number of connected
components in a target-block co-occurrence graph, including isolated
vertices.

The precise definitions of K, P, the graph construction, and the underlying
function space must be taken from the canonical research source. Those
definitions are necessary for interpreting or proving the identity.

### Reported hosted evidence

Tested commit:

    78f4184d9576e40c7312f6bbea1eda1bcbd0bf4e

Reported Python version:

    3.12.15

The supplied artifact audit reports:

| Measure | Reported result |
| --- | ---: |
| Enumerated map/partition pairs | 3,984 |
| Expected map/partition pairs | 3,984 |
| Exact matrix-rank versus graph-rank mismatches | 0 |
| Regression tests passed | 14 |
| Skipped tests | 0 |
| Mutation command exit code | 0 |
| Regression command exit code | 0 |

Workflow job:

https://github.com/quantarion369-arch/AQARION/actions/runs/37998843745/job/114051659524

Artifact:

https://github.com/quantarion369-arch/AQARION/actions/runs/37998843745/artifacts/11648112731

### Mutation accounting

The supplied audit reports 12 declared mutation identifiers, comprising:

- 11 valid canonical mutants, each detected at least once.
- One invalid identifier, R:c-only-variant, described as a duplicate of R:c
  and excluded from valid coverage credit.

Selected reported detection counts:

| Mutant | Detection count |
| --- | ---: |
| R:k-c-1 | 3,984 |
| D:KP(I-P) | 2,148 |
| R:ignore-isolated | 1,666 |
| R:preimage | 1,666 |

Equal detection counts do not establish that two mutants are universally
equivalent or that they fail on exactly the same cases.

Mutation detection supports the sensitivity of the particular verification
process to the named alterations. It does not establish immunity to all
possible implementation errors.

### Reported artifact identities

Mutation-report SHA-256:

    1fb8372e03f50cb22278bda84d23c31fe33c40064192c579016b5f80f352a833

Artifact ZIP SHA-256:

    82d1721c57013e97b8d3f0a515dd3f77ad2384e3a4758c83b9882c947084039a

The supplied audit states that the receipt and mutation report agreed on
the report hash and that the downloaded ZIP matched GitHub's artifact
digest.

### Interpretation

This is reported evidence of a bounded exact census, passing regression
tests, and detection of the valid named mutants.

It is not evidence of a Lean-checked proof or a universal theorem established
by finite enumeration alone.

The supplied audit also reports an independent in-session exact-rational
reimplementation. Because that implementation was not yet preserved as a
committed audit artifact, this checkpoint does not count it as a durable,
repository-reproducible deliverable.

### Outstanding provenance issue

The supplied audit identifies SM003 status fields such as
SOURCE_AUDIT_REQUIRED and EXPECTED_MATRIX_PENDING_REPLAY, together with null
reproduction fields, as potentially stale relative to the reported artifact
inspection.

Those fields require source-level review before any update. A provenance
correction must identify the actual tested revision and artifact without
implying formal proof or independent clean-checkout reproduction that has
not occurred.

## 3. D22: Direct-Projection Validation

### Tested revision

    688ea4eb05e207860d0786ae0f0db4ed4a76b498

Workflow:

    .github/workflows/D22-validation.yml

Audit source:

    AQARION-QUANTARION-AI/verification/D22/D22_DIRECT_PROJECTION_AUDIT.py

Report:

    AQARION-QUANTARION-AI/verification/D22/D22-direct-projection-report.txt

### Logging-pipeline correction

The D22 workflow was updated to make failure propagation explicit when
Python output is piped through tee.

The delivered workflow included:

- Explicit Bash execution.
- Explicit pipeline failure handling.
- Capture of standard output and standard error.
- A successful-command control.
- A failing-command control checking preservation of exit code 7.
- Compilation of the audit source.
- Execution of the audit.
- Upload of the generated report.

These controls address a software-evidence problem: a successful logging
command must not conceal a failing validator.

They do not themselves validate a mathematical identity.

### Reported hosted audit results

The supplied audit reports successful logging controls, compilation, and
audit execution.

| Audit scope | Reported result |
| --- | --- |
| Exact-arithmetic parameter checks | 499,499 |
| Dense matrix comparisons | 189 |
| Closed form | PASS |
| Lag identity | PASS |
| Orthogonality | PASS |
| Rank-one factorization | PASS |
| Nilpotency | PASS |
| Frobenius split | PASS |
| Autocorrelation orientation ambiguity | CONFIRMED |

Workflow job:

https://github.com/quantarion369-arch/AQARION/actions/runs/38019186953/job/114116155165

Artifact:

https://github.com/quantarion369-arch/AQARION/actions/runs/38019186953/artifacts/11657638111

Reported artifact ZIP SHA-256:

    956994cb9f90252bcb0ed9471770add25ab06a860503a9f62f47da5477dbc7ef

### Interpretation and limitations

The reported parameter checks are a bounded computational sweep, not a
symbolic verification over every admissible parameter value.

The supplied audit flags the source comment "Full symbolic domain" as
potentially misleading. The exact loop bounds were missing from the pasted
audit text, so this checkpoint does not reconstruct them.

The conservative reported status is retained:

    ANALYTICALLY_SUPPORTED_UNDER_LOCKED_CONVENTION

The supplied audit also reports an autocorrelation orientation ambiguity.
This checkpoint therefore does not claim that the scalar autocorrelation
uniquely recovers orientation.

Any stronger general claim requires a separately documented derivation
under the locked convention and independent review of that derivation.

## 4. Mobile Research Kit: Completed Regression Checkpoint

Package directory:

    AQARION-QUANTARION-AI/PACKAGES/MOBILE-RESEARCH-KIT/

### Earlier successful baseline

The user supplied the following published-snapshot baseline:

    b44e6c6a18ddcaa8f23d69a7c886ce6408bc526b

Reported local result:

- 114 tests passed.
- Zero skipped tests.
- Regression exit code 0.

### Quadratic verifier workload correction

The reviewed verifier constructed the full expected coefficient-triple set
before checking the report's candidate count.

The correction introduced:

    MAX_COEFFICIENT_BOUND = 10

It also computes the expected count and checks each group's candidate-list
type and length before constructing the expected triple set.

The expected number of triples per modulus is:

    (2b + 1)^3

At the operational limit b = 10, this is 9,261 triples per modulus.

The limit is a verifier resource policy, not a mathematical restriction on
the polynomial criterion.

### Added regression tests

Three test methods were added:

1. Excessive bounds fail before accessing report results.
2. Invalid coefficient-bound types and values are rejected.
3. Incorrect candidate counts fail before individual rows are accessed.

Existing saved-evidence replay, tampering, witness, equivalence-comparison,
and duplicate-candidate tests were retained.

### Resource-control boundary

This change bounds coefficient-triple enumeration.

It does not establish comprehensive untrusted-input protection. In
particular, it does not independently bound:

- JSON input size.
- The number of moduli.
- Modulus magnitude.
- Total residue-evaluation work.
- Every possible malformed structure.

Further resource controls, if needed, should be handled as a separate
reviewed change.

### Isolated local validation

A separate worktree was created from:

    688ea4eb05e207860d0786ae0f0db4ed4a76b498

Branch:

    fix/quadratic-workload-limit

The four reviewed files were copied into that worktree, and the existing
regression runner was executed.

Directly supplied terminal output recorded:

| Measure | Result |
| --- | ---: |
| Manifest-listed files | 35 |
| Files hashed | 35 |
| Failed files | 0 |
| Discovered tests | 117 |
| Tests passed | 117 |
| Skipped tests | 0 |
| Regression time | 11.569 seconds |
| Regression exit code | 0 |

The runner reported:

    PACKAGE_VERIFICATION_OK
    REGRESSION_OK

Local commit:

    6e9d89c

Commit message:

    fix: bound quadratic verifier coefficient workload

This local commit was not successfully pushed. Publication proceeded through
manual file replacements instead.

### Reported published checkpoint

The supplied live audit identifies the published main revision as:

    7ea0d79bc39e4fda1251c8d8768e7ab4caad74c8

It reports:

- 35 listed files hashed.
- Zero package-integrity failures.
- 117 tests passed.
- Zero skipped tests.
- Runtime of 3.197 seconds.
- Workflow Python version 3.13.13.

Workflow job:

https://github.com/quantarion369-arch/AQARION/actions/runs/38021376501/job/114122905525

This hosted result is attributed to the supplied audit. It is separate from
the directly supplied Termux result.

### Manifest-listed scope

The package verifier explicitly reports that unlisted files are not
verified.

Accordingly, the 35-file integrity result must not be described as a
verification of every file in the repository or every file in the package
directory.

### Modular-test whitespace

The delivered modular-test file is reported as:

    7,137 bytes

SHA-256:

    ad441397eec57e6af2619c028fda431b3b21e26f2603fa6dd88371eecd995f36

An earlier version was 7,135 bytes, differing by two blank lines.

The supplied audit states that their nonblank lines are identical and that
the currently published 7,137-byte file matches its manifest and passes the
regression.

This checkpoint retains the matching, passing version. It does not require
restoring an older whitespace layout.

### Intermediate workflow failures

The user reported red workflow runs during the individual file updates and
a green run after the final manifest update.

This sequence is consistent with intermediate revisions containing changed
files and stale manifest entries. The individual failure logs were not
examined in this conversation, so the checkpoint does not assign that cause
to every failed run.

The completed revision, rather than an intermediate delivery revision, is
the relevant publication checkpoint.

## 5. Consolidated Status

| Item | Checkpoint status | Boundary |
| --- | --- | --- |
| SM003 exact census | Reported artifact-audited bounded verification | Not a universal proof by enumeration |
| SM003 mutation checks | 11 valid mutants reported detected | Invalid duplicate excluded |
| D22 workflow controls | Reported passed | Logging reliability is distinct from mathematics |
| D22 numerical and exact checks | Reported passed within tested scope | Bounded sweep; locked convention retained |
| Mobile kit local regression | Directly supplied successful output | Local execution, not hosted execution |
| Mobile kit hosted regression | Reported successful at 7ea0d79 | Attributed to supplied live audit |
| Package integrity | 35 listed files verified | Unlisted files outside integrity scope |
| Lean certification | Not established by the evidence here | No promotion to formal verification |
| Novelty or priority | Not established | Requires targeted literature review |
| D22 wording review | Outstanding source-review item | No undocumented edit claimed |
| SM003 provenance reconciliation | Outstanding source-review item | No status update claimed |

## 6. Publication and Maintenance Policy

Future coordinated software changes should be delivered as one complete
review set.

The review set should include:

- Complete replacement files when manual publication is required.
- Exact repository paths.
- Matching manifest updates.
- A clear base revision.
- Local test results with their execution scope.
- A final published revision and its workflow outcome.

Line patches should not be required when the maintainer's publication
method depends on complete-file replacements.

Intermediate workflow failures should be inspected and classified. They
must not automatically be called mathematical counterexamples, nor should
their causes be guessed.

A final successful workflow should be preserved as evidence for that exact
revision, without rewriting the meaning of earlier runs.

## 7. Outstanding Work

The completed Mobile Research Kit delivery does not require another
whitespace restoration or speculative workflow replacement.

The remaining evidence-maintenance priorities are:

1. Review the D22 source wording against its actual parameter bounds.
2. Preserve the D22 orientation limitation and locked convention.
3. Review SM003 status and provenance fields against the tested commit,
   receipt, and artifact.
4. Preserve any independent reimplementation as a durable artifact before
   counting it as repository-reproducible evidence.
5. Locate canonical status-ledger and receipt paths before updating them.
6. Keep general derivations, bounded computations, regression results, and
   formal certification as separate evidence categories.

No completion of these outstanding tasks is claimed by this document.

## Conclusion

AQARION's current checkpoint combines reported hosted artifact evidence with
a directly supplied, successful 117-test Mobile Research Kit regression.

The value of the checkpoint is not merely that workflows are green. It is
that revisions, test scopes, artifact identities, mutation accounting, and
claim limitations are recorded separately.

The Mobile Research Kit delivery is complete at the reported passing
publication checkpoint. D22 and SM003 retain explicit boundaries between
computational support, mathematical derivation, provenance maintenance,
and formal verification.

### Deliverable — Mobile Research Kit: Exact Python/Environment Requirements

Repository: `quantarion369-arch/AQARION` Package: `AQARION-QUANTARION-AI/PACKAGES/MOBILE-RESEARCH-KIT` Branch inspected: `main`

### 1\. Confirmed requirements

| Item                      | Finding                                         |
| ------------------------- | ----------------------------------------------- |
| Declared Python version   | 3.13.13                                         |
| Declaration source        | manifest.json — packaging_python                |
| Regression entry point    | tools/run_regression.py                         |
| Package integrity checker | tools/verify_package.py                         |
| Third-party dependencies  | Not established by the files retrieved so far.  |
| OS requirement            | No package-specific OS restriction established. |

The regression runner uses Python’s standard-library modules, including `pathlib`, `subprocess`, `sys`, and `unittest`. The package verifier uses `argparse`, `hashlib`, `json`, `pathlib`, and `re`. `Path.is_relative_to()` requires Python 3.9 or later, but the manifest’s explicit environment declaration is the more specific target: Python 3.13.13.

### 2\. Existing regression command

Run from the package directory:

```bash
python tools/run_regression.py
```

The runner first checks the package’s listed-file sizes and SHA-256 hashes, then discovers and executes the package’s `unittest` tests. A package-integrity failure stops the regression before the test suite runs.

### 3\. Audit qualification

The exact declared Python version is confirmed from the live manifest. I have not established that Python 3.13.13 is the only supported version, nor that every file in the package is dependency-free. Those require inspection of the remaining source and environment documentation.

No workflow YAML is proposed or replaced. Your existing workflow should invoke the package’s established regression entry point rather than introduce a competing runner.
