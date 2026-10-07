# Mobile Research Kit

A Python research toolkit exercised in Termux on Android, combining
experiment scripts, recorded command workflows, report artifacts, and
regression tests.

The kit includes coefficient-sweep and contract-atlas experiments, workflow
recording utilities, and a saved-evidence verifier for quadratic atlas
reports.

Status: experimental. The latest local full-suite run passed 66 tests with
exit 0.

## Project layout

```text
examples/
    coefficient_sweep.py
    contract_collision_lab.py
    modular_contract_atlas.py
    quadratic_contract_atlas.py

tools/
    inspect_environment.py
    record_run.py
    run_workflow.py
    verify_quadratic_atlas.py
    view_report.py

tests/
    Twelve test modules and a quadratic-atlas fixture.
```

The project has been exercised in Termux on Android. Broader platform
compatibility has not yet been established.

## Run the tests

From the project root:

```sh
python3 -m unittest discover -s tests -v
```

Latest recorded local result:

```text
Ran 66 tests in 8.568s
OK
FIXTURE_BACKED_FULL_SUITE_EXIT=0
```

The count describes the current tested source set. Runtime varies.

## Recorded quadratic experiment

Run the quadratic atlas through the workflow runner:

```sh
python3 tools/run_workflow.py --timeout 30 --output-root reports -- python3 examples/quadratic_contract_atlas.py --moduli 2 3 4 5 6 8 --bound 3 --output-dir reports/quadratic-atlas-001
```

The demonstrated workflow reported:

```text
STATUS=completed
RECORDER_EXIT=0
WORKFLOW_RECORDER_EXIT=0
WORKFLOW_STATUS=reports_created
WORKFLOW_EXIT=0
```

Its reported artifacts included an inventory JSON, a run receipt JSON, and
an HTML viewer.

The quadratic atlas produced:

```text
reports/quadratic-atlas-001/atlas.md
reports/quadratic-atlas-001/atlas.json
```

Generated reports are local outputs, not required source files for the
fixture-backed verifier tests.

## Quadratic atlas scope

The reference polynomial is:

    f(x) = x*x + x

Candidates have the form:

    g(x) = c*x*x + a*x + b

The demonstrated experiment used coefficients from -3 through 3 and
moduli 2, 3, 4, 5, 6, and 8.

It compared complete residue enumeration, exact quadratic conditions,
and evaluation at three points. Strict coefficient matching was included
as a deliberately adversarial rule.

Recorded results:

| Modulus | Candidates | Accepted | Primary disagreements | Strict false rejects | Strict false accepts | Failed replays |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 343 | 75 | 0 | 27 | 0 | 0 |
| 3 | 343 | 12 | 0 | 0 | 0 | 0 |
| 4 | 343 | 8 | 0 | 4 | 0 | 0 |
| 5 | 343 | 1 | 0 | 0 | 0 | 0 |
| 6 | 343 | 2 | 0 | 1 | 0 | 0 |
| 8 | 343 | 2 | 0 | 1 | 0 | 0 |
| Total | 2,058 | 100 | 0 | 33 | 0 | 0 |

The strict rule's false rejections are findings, not harness failures.

For example, modulo 4, the candidate -x*x - x and the reference x*x + x
both produced the residue sequence:

    [0, 2, 2, 0]

over inputs 0 through 3, despite failing strict coefficient matching.

These results apply to the demonstrated bounded experiment. They are not
general polynomial classification or formal certification.

## Verify saved quadratic evidence

Verify a generated atlas:

```sh
python3 tools/verify_quadratic_atlas.py reports/quadratic-atlas-001/atlas.json
```

The demonstrated full-report replay produced:

```text
CASES_RECOMPUTED=2058
ACCEPTED_CASES=100
REJECTION_WITNESSES_REPLAYED=1958
EQUIVALENCE_COMPARISONS_REPLAYED=33
SAVED_QUADRATIC_EVIDENCE_REPLAY_OK
```

The verifier uses only the Python standard library and does not import
the atlas generator.

It recomputes residue outputs and checks:

- Report parameters and modulus groups.
- Complete bounded coefficient-grid coverage.
- Complete and three-point acceptance.
- Strict coefficient acceptance and error flags.
- First counterexamples and saved replay status.
- Equivalence comparison lists.
- Summary counts.

The saved exact-route acceptance flag is checked against complete
enumeration. The verifier does not independently implement that route's
algebraic conditions.

The equivalence-comparison counter counts candidate cases containing
complete comparison lists, not individual residue comparisons.

## Fixture-backed regression tests

A validated modulus-2 fixture is included at:

```text
tests/fixtures/quadratic_atlas_q2.json
```

Verify it without generating a new report:

```sh
python3 tools/verify_quadratic_atlas.py tests/fixtures/quadratic_atlas_q2.json
```

Expected totals:

```text
CASES_RECOMPUTED=343
ACCEPTED_CASES=75
REJECTION_WITNESSES_REPLAYED=268
EQUIVALENCE_COMPARISONS_REPLAYED=27
SAVED_QUADRATIC_EVIDENCE_REPLAY_OK
```

Run its six regression tests:

```sh
python3 -m unittest discover -s tests -p 'test_quadratic_atlas_saved_evidence.py' -v
```

The tests check acceptance of the unchanged fixture and rejection of:

- A corrupted recorded output.
- A missing counterexample.
- A corrupted equivalence comparison.
- A corrupted summary count.
- A duplicate candidate replacing another grid entry.

Tests mutate in-memory copies, leaving the fixture unchanged.

## Validation and portability

The latest local full suite passed all 66 tests with explicit exit 0.

A smaller handoff containing the quadratic verifier, its tests, and its
fixture was also extracted into a fresh temporary directory on the same
Termux environment.

That extracted subset passed:

- SHA-256 manifest checks.
- Fixture verification.
- All six bundled regression tests.

This establishes directory independence for that subset on the tested
environment. The entire kit has not yet been validated from a separately
extracted clean package during this session.

The precise Python version should be recorded before release.
Cross-device and cross-version compatibility remain unestablished.

## Limitations

- Experimental implementation, not formal certification.
- The quadratic fixture is derived from the experiment, not an
  independently authored oracle.
- Generator and verifier computations share Python arithmetic.
- The verifier is not hardened for arbitrary untrusted JSON.
- Five corruption scenarios do not cover every possible corruption.
- No public-repository CI result has been established yet.

## License and publication

License selection is pending review of source ownership and provenance.

This draft does not grant reuse or redistribution rights. Add the
appropriate license and update this section before an intended open-source
release.

Any applicable project publication restrictions must be resolved before
making the repository public.
