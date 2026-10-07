# Mobile Research Kit — Current Checkpoint

Date: October 7, 2026.  
Status: locally tested prototype. License selection remains pending.

## Current implementation

Five tools:

- `tools/inspect_environment.py`
- `tools/record_run.py`
- `tools/view_report.py`
- `tools/run_workflow.py`
- `tools/verify_quadratic_atlas.py`

Four experiment scripts:

- `examples/coefficient_sweep.py`
- `examples/contract_collision_lab.py`
- `examples/modular_contract_atlas.py`
- `examples/quadratic_contract_atlas.py`

Twelve test modules and one saved-evidence fixture are included.

The workflow coordinator creates an environment snapshot, records an
explicit command, generates an HTML viewer, and prints artifact locations.

The quadratic verifier separately recomputes saved evidence without
importing the atlas generator.

## Latest full-suite evidence

Working-directory suite:

```text
Ran 66 tests in 8.568s
OK
FIXTURE_BACKED_FULL_SUITE_EXIT=0
```

Complete source archive, extracted into a fresh temporary directory:

```text
Ran 66 tests in 8.389s
OK
EXTRACTED_FULL_SUITE_EXIT=0
WHOLE_KIT_EXTRACTION_CHECK_OK
```

The extraction check validated manifest entries before running the suite.

These results establish that the selected whole-kit package runs outside
the original working directory on the same tested environment.

They do not establish cross-device or cross-version compatibility.

## Connected workflow evidence

The quadratic experiment was recorded with:

```sh
python3 tools/run_workflow.py --timeout 30 --output-root reports -- python3 examples/quadratic_contract_atlas.py --moduli 2 3 4 5 6 8 --bound 3 --output-dir reports/quadratic-atlas-001
```

Observed outcome:

```text
STATUS=completed
RECORDER_EXIT=0
WORKFLOW_RECORDER_EXIT=0
WORKFLOW_STATUS=reports_created
WORKFLOW_EXIT=0
QUADRATIC_ATLAS_WORKFLOW_EXIT=0
```

Recorded workflow artifacts:

```text
reports/workflow-bsy9838l/inventory.json
reports/workflow-bsy9838l/runs/run-5xpnje47/receipt.json
reports/workflow-bsy9838l/viewer.html
```

Atlas outputs:

```text
reports/quadratic-atlas-001/atlas.md
reports/quadratic-atlas-001/atlas.json
```

An earlier generated viewer was reported as opened on the user's phone.
Opening these particular workflow viewers has not been established.

## Quadratic atlas results

Reference polynomial:

```text
f(x) = x*x + x
```

Candidate polynomial:

```text
g(x) = c*x*x + a*x + b
```

Coefficient range: -3 through 3 for each coefficient.

| Modulus | Candidates | Accepted | Primary disagreements | Strict false rejects | Strict false accepts | Failed replays |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 343 | 75 | 0 | 27 | 0 | 0 |
| 3 | 343 | 12 | 0 | 0 | 0 | 0 |
| 4 | 343 | 8 | 0 | 4 | 0 | 0 |
| 5 | 343 | 1 | 0 | 0 | 0 | 0 |
| 6 | 343 | 2 | 0 | 1 | 0 | 0 |
| 8 | 343 | 2 | 0 | 1 | 0 | 0 |
| Total | 2,058 | 100 | 0 | 33 | 0 | 0 |

Complete residue enumeration, exact quadratic conditions, and
three-point evaluation agreed across the tested grid.

Strict coefficient matching was deliberately adversarial.
Its false rejections are findings, not harness failures.

This is a bounded quadratic experiment, not a general polynomial
classifier or formal certification.

## Saved-evidence verifier

File:

```text
tools/verify_quadratic_atlas.py
```

The verifier uses Python's standard library and does not import the
atlas generator.

It checks:

- Report kind and basic parameter validity.
- Modulus groups and duplicate moduli.
- Integer coefficients and bounded candidate-grid coverage.
- Missing or duplicate candidates.
- Recomputed outputs over all residue inputs.
- Complete and three-point acceptance.
- Strict coefficient acceptance and error flags.
- First counterexamples and saved replay status.
- Equivalence comparison lists.
- Summary counts.

The saved exact-route acceptance flag is checked against complete
enumeration. The verifier does not independently implement that
route's algebraic conditions.

Full-report replay:

```text
CASES_RECOMPUTED=2058
ACCEPTED_CASES=100
REJECTION_WITNESSES_REPLAYED=1958
EQUIVALENCE_COMPARISONS_REPLAYED=33
SAVED_QUADRATIC_EVIDENCE_REPLAY_OK
```

The equivalence counter counts candidate cases containing complete
comparison lists, not individual residue comparisons.

The verifier was also executed through the workflow runner:

```sh
python3 tools/run_workflow.py --timeout 30 --output-root reports -- python3 tools/verify_quadratic_atlas.py reports/quadratic-atlas-001/atlas.json
```

Observed outcome:

```text
STATUS=completed
RECORDER_EXIT=0
WORKFLOW_RECORDER_EXIT=0
WORKFLOW_STATUS=reports_created
WORKFLOW_EXIT=0
SAVED_EVIDENCE_WORKFLOW_EXIT=0
```

Recorded workflow artifacts:

```text
reports/workflow-peo6vad3/inventory.json
reports/workflow-peo6vad3/runs/run-d38iecjz/receipt.json
reports/workflow-peo6vad3/viewer.html
```

## Fixture-backed regression tests

Test module:

```text
tests/test_quadratic_atlas_saved_evidence.py
```

Fixture:

```text
tests/fixtures/quadratic_atlas_q2.json
```

The fixture retains the modulus-2 group from the validated full report.
Its confirmed size is 223,091 bytes.

Fixture verification:

```text
CASES_RECOMPUTED=343
ACCEPTED_CASES=75
REJECTION_WITNESSES_REPLAYED=268
EQUIVALENCE_COMPARISONS_REPLAYED=27
SAVED_QUADRATIC_EVIDENCE_REPLAY_OK
FIXTURE_VERIFIER_EXIT=0
```

The fixture path was explicitly confirmed during packaging.

Six tests cover:

| Test case | Expected result |
|---|---|
| Unchanged fixture | Accepted with expected totals |
| Corrupted recorded output | Rejected |
| Missing counterexample | Rejected |
| Corrupted equivalence comparison | Rejected |
| Corrupted summary count | Rejected |
| Duplicate candidate replacing another grid entry | Rejected |

Tests mutate in-memory copies, leaving the fixture unchanged.

These tests no longer depend on the generated full report under
`reports/`.

The fixture is experiment-derived, not an independently authored oracle.

## Selected source layout

```text
mobile-research-kit/
├── README.md
├── CHECKPOINT.md
├── .gitignore
├── manifest.json
├── docs/
│   └── history/
│       ├── README-25tests.md
│       └── CHECKPOINT-25tests.md
├── tools/
│   ├── inspect_environment.py
│   ├── record_run.py
│   ├── run_workflow.py
│   ├── verify_quadratic_atlas.py
│   └── view_report.py
├── examples/
│   ├── coefficient_sweep.py
│   ├── contract_collision_lab.py
│   ├── modular_contract_atlas.py
│   └── quadratic_contract_atlas.py
└── tests/
    ├── fixtures/
    │   └── quadratic_atlas_q2.json
    ├── test_coefficient_sweep.py
    ├── test_contract_collision_lab.py
    ├── test_contract_selection.py
    ├── test_inspect_environment.py
    ├── test_modular_contract_atlas.py
    ├── test_quadratic_atlas_saved_evidence.py
    ├── test_quadratic_contract_atlas.py
    ├── test_record_run.py
    ├── test_run_workflow.py
    ├── test_view_report.py
    ├── test_workflow_failures.py
    └── test_workflow_os_errors.py
```

## Packaging evidence

Whole-kit archive:

```text
handoffs/mobile-research-kit-66tests-001.zip
```

Observed packaging result:

```text
SELECTED_SOURCE_FILES=22
ARCHIVE_ENTRIES=28
ARCHIVE_BYTES=45467
PACKAGING_PYTHON=3.13.13
WHOLE_KIT_CONTENT_CHECK_OK
```

The 28 entries comprise:

- Five tools.
- Four examples.
- Twelve test modules.
- One fixture.
- Current README, checkpoint, and ignore rules.
- Two preserved historical documents.
- One SHA-256 manifest.

The original working-directory documentation was not overwritten.

The archive's documentation was written before its successful
whole-kit extraction test. This checkpoint records that subsequent result.

If packaged files are revised, regenerate the manifest and revalidate
the revised package. Existing hashes do not validate edited files.

A smaller verifier-only archive was also created:

```text
handoffs/quadratic-saved-evidence-001.zip
```

It contained five entries, totaled 9,087 bytes, and passed separate
extraction testing with all six bundled tests.

## Development environment

Directly reported during this session:

- Python 3.13.13.
- Termux on Android.

Previously recorded development environment:

- Samsung SM-A156U.
- Android 16.
- AArch64.
- Google Play Termux 2026.06.21.

Other devices, operating systems, and Python versions have not been
established as supported.

Ubuntu / Lean research work remains separate according to the
original project documentation.

## Evidence and limitations

Results come from user-supplied terminal output and an earlier
viewer screenshot, not independent reproduction or signed evidence.

Some workflow failure-path tests simulate subprocess results.

Execution receipts are not mathematical verdicts, signatures,
or certificates.

The workflow is not a command sandbox.
Viewer inputs are not authenticated or proven to share one execution.

Package hashing checks agreement with selected bytes.
It does not authenticate authorship or add source and receipt
hashing to recorded workflows.

Output files are not size-limited.
The recorder's timeout is not guaranteed after the recorder is killed.

The suite does not establish behavior under:

- Abrupt Android termination.
- Storage exhaustion.
- Power loss.
- Every descendant-process scenario.
- Sustained device workloads.
- Workflow-level keyboard interruption.

Previously reported Termux session resets remain unexplained.

The verifier is not hardened for arbitrary untrusted JSON.
Five corruption tests do not cover every possible corruption.

Formal certification and independent-language replication are
not established.

## Privacy and transfer

Commands, paths, device details, stdout, and stderr may contain
private information. Review before sharing.

Generated reports, execution output, HTML viewers, caches,
repair backups, and older archives are excluded from the selected
source package unless deliberately reviewed and included.

Historical documents remain records of earlier checkpoints.
Their 25-test counts do not describe the current 66-test source set.

## GitHub and licensing

Git did not recognize the original Termux working directory as
a repository.

The user reports uploading a README, file-tree description,
and .gitignore to GitHub.

Upload of the complete source files and successful tests against
a fresh GitHub checkout have not yet been confirmed.

No license has been selected.
Review source ownership and provenance before selecting one.

Any applicable publication restrictions require separate resolution.
Passing tests and successful packaging do not clear those restrictions.

---

# Mobile Research Kit: Build and Packaging Checkpoint

Checkpoint date: October 7, 2026.
Latest reported verification: approximately 05:49 EDT.

## Purpose

This document records the build's verified state and packaging handoff.
Usage instructions, experiment commands, and limitations belong in README.md.

Results below distinguish newly reported extraction checks from earlier
recorded experiments. No unperformed operation is marked complete.

## Selected package contents

| Category | Count |
|---|---:|
| Tools | 5 |
| Examples | 4 |
| Test modules | 12 |
| Saved fixtures | 1 |
| Current documentation files | 2 |
| Historical documentation files | 2 |
| .gitignore | 1 |
| Manifest | 1 |
| Total selected files, including manifest | 28 |

The manifest contains 27 file entries and excludes itself.

The earlier Python, Markdown, and JSON inventory counted 27 files and
10660 lines. That filter included manifest.json but excluded .gitignore.

The largest listed file is tests/fixtures/quadratic_atlas_q2.json:
7189 lines and 223091 bytes.

No separate 1800-line file was identified in that inventory.

## Source-package integrity

The local manifest verification reported:

    RESULT: 27 verified; 0 missing or mismatched

Every manifest-listed file matched both its expected byte size and SHA-256
hash at the time of that check.

Original fixture identity:

    Path: tests/fixtures/quadratic_atlas_q2.json
    Bytes: 223091
    SHA-256: 46f873f7c067c01f90cb62e2c21ea5653199b93e9e43bd3b95ab145ae43fe214

The original local fixture is the authoritative packaged file.
Recovery excerpts and reconstructed attachments are not substitutes for it.

Matching the manifest establishes agreement with its recorded bytes.
It does not independently authenticate the manifest or the package's origin.

## Whole-kit extraction test

The previously pending whole-kit archive extraction test completed
successfully.

Tested environment:

    Termux on Android
    Python 3.13.13, as previously reported for the local environment

Archive produced:

    Mobile-Research-Kit-Verified-20261007-054913-408214.zip

Archive location:

    Phone Downloads folder

The packaging sequence selected the manifest-listed files plus manifest.json,
checked ZIP integrity, extracted into a temporary directory, checked extracted
file sizes and hashes, compared the extracted manifest with the source
manifest, and executed the documented test and fixture-verification commands.

Final reported status:

    WHOLE_KIT_EXTRACTION_TEST: PASS

The temporary extraction directory was managed for automatic cleanup.
The verified source folder was not overwritten by this test.

## Extracted execution evidence

Full-suite result:

    Ran 66 tests in 8.525s
    OK
    EXTRACTED_FULL_SUITE_EXIT: 0

Fixture-verifier result:

    CASES_RECOMPUTED=343
    ACCEPTED_CASES=75
    REJECTION_WITNESSES_REPLAYED=268
    EQUIVALENCE_COMPARISONS_REPLAYED=27
    SAVED_QUADRATIC_EVIDENCE_REPLAY_OK
    EXTRACTED_FIXTURE_VERIFIER_EXIT: 0

This closes the outstanding whole-kit extraction-test item for that archive.

It does not establish that later edits or later archives have passed the
same checks.

## Earlier experiment evidence

The earlier local full suite reported 66 passing tests in 8.568 seconds
with explicit exit code 0.

The recorded six-modulus quadratic experiment covered 2058 cases:
100 acceptances and 33 strict false rejections.

It reported zero primary disagreements, strict false acceptances, and failed
witness replays.

An earlier full saved-report replay covered 1958 rejection witnesses and
33 equivalence comparison lists.

A separately extracted six-test verifier subset also passed.

These are retained historical results. The latest extraction test reran
the full suite and the packaged modulus-2 fixture verifier; it did not
establish a new standalone replay of the earlier full six-modulus report.

## Documentation revision handoff

The verified archive above contains the documentation version that described
whole-kit extraction testing as pending.

These replacement README.md and CHECKPOINT.md documents record its completed
status and separate operational guidance from build evidence.

At the time these replacement texts were prepared, writing them into the
phone's source folder was not established.

After installing these documents:

1. Regenerate manifest entries for the changed packaged files.
2. Verify all files against the regenerated manifest.
3. Create a new archive without overwriting the earlier verified archive.
4. Repeat extraction, integrity, full-suite, and fixture-verifier checks.
5. Record the new archive identity and actual results.

Do not reuse the old documentation hashes after changing these files.
Do not describe the revised archive as tested before those checks finish.

## Repository and release boundaries

Historical documentation remains under docs/history/.

Git previously did not recognize the working directory as a repository.
No later repository initialization or commit is established here.

No license selection, upload, publication, or public release is established.

Package verification does not resolve ownership, provenance, privacy review,
or any applicable publication restrictions.

## Current handoff status

Original packaged files: verified against the supplied manifest.
Whole-kit extraction test: passed for the named archive.
Extracted full suite: passed.
Extracted fixture replay: passed.
Replacement documentation: provided as complete text.
Installation of replacement documentation: not yet established.
Updated manifest and revised archive: not yet established.

---

# Mobile Research Kit: Current Packaging Checkpoint

Date: October 7, 2026.

## Current working package

Directory: Mobile-Research-Kit-Deliverables.

Environment previously reported: Python 3.13.13 in Termux on Android.

Current selected implementation:
- Seven tools.
- Four examples.
- Fourteen test modules.
- One saved quadratic fixture.

## Latest supplied execution

Command:

    python tools/run_regression.py

Recorded results:
- Manifest-listed files: 31.
- Files hashed: 31.
- Failed file checks: 0.
- Tests run: 91.
- Full-suite duration: 11.540 seconds.
- unittest result: OK.
- Runner result: REGRESSION_OK.
- Skipped tests: 0.

These results apply to the phone working directory tested.
They do not establish that GitHub or an extracted archive matches it.

## Integrity and regression additions

New tools:
- tools/verify_package.py
- tools/run_regression.py

New test modules:
- tests/test_verify_package.py: 16 tests.
- tests/test_run_regression.py: 9 tests.

The package verifier checks selected files against recorded byte sizes
and SHA-256 hashes. Unlisted files are outside its verification scope.

The regression runner checks package integrity before test discovery.
It rejects an empty suite and reports skipped tests.
Skipped tests do not currently make the runner fail.

The current manifest includes the four new Python files.

## Previously recorded mathematical evidence

Quadratic atlas:
- 2,058 candidate-modulus cases.
- 100 acceptances.
- 33 strict coefficient-rule false rejections.
- Zero primary disagreements.
- Zero strict-rule false accepts.
- Zero failed replays.

Full saved-evidence replay:
- 1,958 rejection witnesses.
- 33 equivalence comparison lists.

Modulus-2 fixture:
- 343 cases.
- 75 acceptances.
- 268 rejection witnesses.
- 27 equivalence comparison lists.

These figures are retained from the preceding checkpoint.
The latest test run is not a newly recorded full atlas generation run.

## Historical evidence

An earlier checkpoint recorded 66 tests passing in 8.568 seconds
with explicit exit code 0.

A separately extracted six-test verifier subset previously passed.
This does not establish whole-package extracted-archive verification.

Original README and checkpoint are retained in docs/history/.

## Release boundaries

Whole-package extracted-archive verification remains pending.

The working directory was previously reported as not recognized by Git
as a repository. Its current Git status has not been rechecked here.

An MIT license personalized for James Aaron
(AQARION & QUANTARION_AI) was prepared in conversation.
Its presence in this working directory has not been verified here.

GitHub file preparation does not establish a verified remote copy,
Git commit, upload, or published release.

After editing this document, deliberately update its manifest entry.
Do not silently regenerate unrelated hashes to hide mismatches.

---

Inspect what is available.
Record what ran.
View what was supplied.
Keep the claims within the evidence.
