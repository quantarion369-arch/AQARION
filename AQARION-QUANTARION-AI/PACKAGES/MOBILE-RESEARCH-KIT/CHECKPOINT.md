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

Inspect what is available.
Record what ran.
View what was supplied.
Keep the claims within the evidence.
