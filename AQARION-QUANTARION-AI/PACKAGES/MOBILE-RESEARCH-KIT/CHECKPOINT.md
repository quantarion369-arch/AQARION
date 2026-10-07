# Mobile Research Kit — Current Checkpoint

Date: October 7, 2026.
Status: locally tested prototype; license not selected.

## Current source set

- Five tools.
- Four examples.
- Twelve test modules.
- One saved-evidence fixture.

## Test evidence

Working-directory full suite:

    Ran 66 tests in 8.568s
    OK
    FIXTURE_BACKED_FULL_SUITE_EXIT=0

Complete package, extracted into a fresh temporary directory:

    Ran 66 tests in 8.389s
    OK
    EXTRACTED_FULL_SUITE_EXIT=0
    WHOLE_KIT_EXTRACTION_CHECK_OK

Results come from user-supplied terminal output.
They are not independent reproduction or authenticated evidence.

## Quadratic experiment

Reference: x*x + x.
Candidate: c*x*x + a*x + b.
Coefficients: -3 through 3.
Moduli: 2, 3, 4, 5, 6, 8.

- 2,058 candidate-modulus cases.
- 100 accepted cases.
- 33 strict coefficient false rejections.
- Zero primary-route disagreements.
- Zero strict false accepts.
- Zero failed replays.

Saved full-report evidence was recomputed:
1,958 rejection witnesses and 33 equivalence comparison lists.

## Fixture and regression tests

Fixture: tests/fixtures/quadratic_atlas_q2.json.

- 343 cases.
- 75 acceptances.
- 268 rejection witnesses.
- 27 equivalence comparison lists.

Six tests cover unchanged evidence and five specific corruptions.
The fixture is experiment-derived rather than an independent oracle.

## Package

Local source archive:

    handoffs/mobile-research-kit-66tests-001.zip

- 22 selected implementation/test/fixture files.
- 28 total entries.
- 45,467 bytes.
- Packaging Python: 3.13.13.
- Archive content checks passed.
- Extracted manifest checks and full suite passed.

The archive's original README and checkpoint state extraction testing
was pending at packaging time. This checkpoint records the subsequent
successful test.

If archive documentation is revised, regenerate its manifest and
revalidate the resulting archive.

## Environment

Reported Python: 3.13.13 in Termux on Android.

Previously recorded:
Samsung SM-A156U, Android 16, AArch64,
Google Play Termux 2026.06.21.

Cross-device and cross-version compatibility remain unestablished.

## Publication state

Git did not recognize the original Termux working directory
as a repository.

The user reports uploading a README, file-tree description,
and .gitignore to GitHub.

Upload of the actual source files and tests against a fresh
GitHub checkout have not yet been confirmed.

No license has been selected.
Applicable publication restrictions require separate resolution.

## Boundaries

Execution receipts are not proof or certificates.
The workflow is not a sandbox.
Viewer inputs are not authenticated.

Whole-package extraction testing occurred on the same environment,
not an independent device.

Formal certification, general polynomial classification,
security auditing, sustained device stability, and all possible
corruption scenarios are not established.
