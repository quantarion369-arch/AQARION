# Mobile Research Kit

Built on a phone. Executed locally. Reported clearly.

An experimental Python toolkit for inspecting execution environments,
recording bounded command runs, generating local HTML reports, and testing
modular contract equivalence.

Developed and tested in Termux on Android.

## What the kit does

The kit connects practical execution tools with reproducible mathematical
experiments:

- Capture the environment in which a command runs.
- Record an explicit command, its output, and its execution result.
- Coordinate inspection, recording, and report generation.
- Explore bounded coefficient grids for modular contract equivalence.
- Recompute saved experimental evidence without importing the generator.

The package includes five tools, four examples, twelve test modules, and
one saved quadratic fixture.

## Verified build

The whole-kit archive passed extraction testing on October 7, 2026.

| Check | Recorded result |
|---|---|
| Environment | Termux on Android; Python 3.13.13 |
| Extracted test suite | 66 tests passed in 8.525 seconds |
| Full-suite exit code | 0 |
| Extracted fixture verifier | Passed; exit code 0 |
| Fixture cases recomputed | 343 |
| Rejection witnesses replayed | 268 |
| Equivalence comparisons replayed | 27 |
| Whole-kit extraction test | PASS |

Before packaging, all 27 manifest-listed files matched their recorded byte
sizes and SHA-256 hashes.

These results apply to the tested archive and environment. Changes to source
files or package contents require fresh verification.

See CHECKPOINT.md for the archive identity, detailed execution evidence,
and packaging handoff.

## Project layout

    Mobile-Research-Kit-Deliverables/
        .gitignore
        README.md
        CHECKPOINT.md
        manifest.json
        docs/
            history/
                README-25tests.md
                CHECKPOINT-25tests.md
        examples/
            coefficient_sweep.py
            contract_collision_lab.py
            modular_contract_atlas.py
            quadratic_contract_atlas.py
        tests/
            fixtures/
                quadratic_atlas_q2.json
            test_*.py
        tools/
            inspect_environment.py
            record_run.py
            run_workflow.py
            verify_quadratic_atlas.py
            view_report.py

Run the commands below from the project root.

Generated reports are separate from the selected source-package contents.

## Quick start

### 1. Run the tests

    python3 -m unittest discover -s tests -v

The current source set is expected to discover 66 tests.

Check both the test output and the process exit status. A previously passing
build does not establish that an edited copy still passes.

### 2. Verify the included fixture

    python3 tools/verify_quadratic_atlas.py tests/fixtures/quadratic_atlas_q2.json

Expected successful output includes:

    CASES_RECOMPUTED=343
    ACCEPTED_CASES=75
    REJECTION_WITNESSES_REPLAYED=268
    EQUIVALENCE_COMPARISONS_REPLAYED=27
    SAVED_QUADRATIC_EVIDENCE_REPLAY_OK

This check uses the packaged fixture; generating a new experiment report
is not required.

### 3. Exercise the connected workflow

    python3 tools/run_workflow.py --timeout 5 --output-root reports -- python3 -c "print('Connected workflow works')"

Each invocation creates a separate workflow directory with environment
inventory, a receipt, recorded execution output, and viewer artifacts.

Inspect the recorder result and receipt to determine whether the child
command succeeded.

## Tools

| File | Role |
|---|---|
| tools/inspect_environment.py | Capture an environment snapshot. |
| tools/record_run.py | Record an explicit command with a configured timeout. |
| tools/view_report.py | Generate local HTML views of supplied JSON reports. |
| tools/run_workflow.py | Coordinate inventory, command recording, and report generation. |
| tools/verify_quadratic_atlas.py | Recompute and check saved quadratic evidence. |

The original tools are documented as using Python's standard library.

The command recorder requires POSIX process-group handling. The established
test environment is Termux on Android; other environments have not been
verified.

## Workflow result interpretation

The workflow runs the recorded command without an implicit shell.

Use an explicit shell only when shell syntax is required. Commands are not
sandboxed, so choose them with the same care as commands entered directly
in your terminal.

The configured timeout applies to the recorded child process, not to the
entire workflow.

WORKFLOW_STATUS=reports_created indicates that report generation completed.
It does not necessarily indicate that the child command succeeded.

Orchestration failures return 125. A child command may also return 125.
Interpret the status, recorder result, and receipt together rather than
relying on that exit number alone.

Expanded original workflow documentation is retained in
docs/history/README-25tests.md. Its four-tool and 25-test status describes
an earlier version.

## Contract experiments

The examples included in the kit are:

- examples/coefficient_sweep.py
- examples/contract_collision_lab.py
- examples/modular_contract_atlas.py
- examples/quadratic_contract_atlas.py

The quadratic atlas compares the following expressions:

    Reference: x*x + x
    Candidate: c*x*x + a*x + b

The recorded experiment uses integer coefficients from -3 through 3.
Each modulus therefore has 343 candidate coefficient triples.

Run the six-modulus experiment through the connected workflow:

    python3 tools/run_workflow.py --timeout 30 --output-root reports -- python3 examples/quadratic_contract_atlas.py --moduli 2 3 4 5 6 8 --bound 3 --output-dir reports/quadratic-atlas-001

Use a distinct experiment output directory when preserving multiple runs.

### Recorded results

| Modulus | Candidates | Accepted | Strict false rejections |
|---:|---:|---:|---:|
| 2 | 343 | 75 | 27 |
| 3 | 343 | 12 | 0 |
| 4 | 343 | 8 | 4 |
| 5 | 343 | 1 | 0 |
| 6 | 343 | 2 | 1 |
| 8 | 343 | 2 | 1 |
| Total | 2058 | 100 | 33 |

The recorded run reported zero primary disagreements, strict false
acceptances, and failed witness replays.

Strict coefficient matching is deliberately adversarial. Its false
rejections are findings: they identify candidates accepted by the primary
routes but rejected by the stricter coefficient rule.

These results describe the tested bounded grid. They do not establish
general polynomial classification or formal certification.

## Saved-evidence verification

To verify a generated experiment report:

    python3 tools/verify_quadratic_atlas.py reports/quadratic-atlas-001/atlas.json

The report must already exist at the supplied path.

The previously recorded full-report replay covered:

- 2058 candidate cases.
- 100 accepted cases.
- 1958 rejection witnesses.
- 33 equivalence comparison lists.

The extracted-package check separately replayed the included modulus-2
fixture.

### What the verifier checks

The verifier recomputes residue outputs and checks candidate-grid coverage,
acceptance flags, counterexamples, equivalence comparisons, and summaries.

It does not import the atlas generator.

It checks the saved exact-route flag against complete enumeration rather
than independently implementing that route's algebraic conditions.

Six verifier tests cover the unchanged fixture and five deliberate
corruptions:

- Recorded output.
- Missing witness.
- Equivalence comparison.
- Summary count.
- Duplicate candidate.

These tests exercise selected corruption cases, not every possible invalid
report. The verifier is not hardened for arbitrary untrusted JSON.

## Package integrity

manifest.json records expected byte sizes and SHA-256 hashes for 27
selected files. It excludes itself from its own file list.

Hash agreement establishes that a file matches the manifest's recorded
bytes. It does not authenticate authorship, certify experimental findings,
or provide authenticated execution receipts.

The original fixture belongs at:

    tests/fixtures/quadratic_atlas_q2.json

Preserve that file rather than replacing it with an excerpt, reformatted
table, or unverified reconstruction.

After changing a packaged file:

1. Run the relevant tests.
2. Regenerate the package manifest.
3. Check the selected files against the new manifest.
4. Create a new archive.
5. Extract it into a separate directory.
6. Verify the extracted files and rerun the full suite and fixture verifier.

Keep earlier verified archives separate so their identities and recorded
results remain unambiguous.

## Operational boundaries

The toolkit records and displays execution information; it does not make
that information authenticated proof.

Viewer inputs are supplied data. Output sizes are not bounded.

Established coverage does not include:

- Abrupt Android termination.
- Storage exhaustion.
- Power loss.
- Sustained device stability.
- Every descendant-process scenario.
- Workflow-level keyboard interruption.

Treat these as unverified conditions rather than demonstrated guarantees.

## Privacy and documentation

Commands, paths, environment snapshots, and execution output can contain
private information. Review generated artifacts before sharing them.

Generated reports, backups, caches, and older archives are excluded from
the selected source package.

README.md provides operational guidance.

CHECKPOINT.md records build evidence, archive identity, and pending work.

docs/history/ preserves earlier documentation for context. Historical
test counts and status statements do not override the current checkpoint.
```
