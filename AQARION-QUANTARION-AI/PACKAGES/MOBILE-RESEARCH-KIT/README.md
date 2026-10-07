# Mobile Research Kit

### Built on a phone. Executed locally. Reported clearly.

An experimental Python toolkit developed and exercised in Termux on Android. It combines environment inspection, bounded command recording, local HTML reports, contract experiments, and saved-evidence verification.

The tools make local activity easier to inspect. They do not turn execution records into authenticated proof.

## Status and requirements

As of October 7, 2026:

- Five tools.
- Four experiment scripts.
- Twelve test modules.
- One quadratic-atlas fixture.
- Working-directory full suite: 66 tests passed in 8.568 seconds, with explicit exit `0`.
- Complete source package: extracted into a fresh temporary directory; all 66 tests passed in 8.389 seconds, with explicit exit `0`.
- Tested environment: Termux on Android, Python 3.13.13.
- License selection remains pending.
- Cross-device and cross-version compatibility remain unestablished.

Validation results come from user-supplied terminal output, not independent reproduction or signed evidence. No GitHub CI result has been established.

The original toolkit is documented as using Python’s standard library. The command recorder requires a POSIX execution environment for process-group handling.

### Source layout

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

Historical documents preserve an earlier four-tool, 25-test checkpoint. Their counts do not describe the current source set.

## Tools and quick start

| Tool | Purpose |
|---|---|
| `inspect_environment.py` | Save an environment snapshot |
| `record_run.py` | Record an explicit command with a configured timeout |
| `view_report.py` | Generate HTML from supplied JSON reports |
| `run_workflow.py` | Coordinate inventory, recording, and viewing |
| `verify_quadratic_atlas.py` | Recompute and check saved quadratic-atlas evidence |

Run all commands below from the project root.

### Run the full suite

```sh
python3 -m unittest discover -s tests -v
```

The current tested source set discovers 66 tests. Runtime varies.

### Run a connected workflow

```sh
python3 tools/run_workflow.py --timeout 5 --output-root reports -- python3 -c "print('Connected workflow works')"
```

The coordinator invokes the inventory, recorder, and viewer as separate Python processes. Each invocation creates its own workflow directory:

```text
reports/
└── workflow-.../
    ├── inventory.json
    ├── viewer.html
    └── runs/
        └── run-.../
            ├── receipt.json
            ├── stdout.txt
            └── stderr.txt
```

The command executes directly, without an implicit shell. Use an explicit shell only when shell syntax is required.

The timeout applies to the recorded child execution—not the entire multi-stage workflow.

`WORKFLOW_STATUS=reports_created` means report generation finished. It does not necessarily mean the child command succeeded. When report generation succeeds, the coordinator returns the recorder’s exit result.

Orchestration failures return `125`. A child can also return `125`, so interpret the workflow status and receipt together rather than relying on the number alone. Artifacts created before failure may remain.

### Use the tools separately

Create a new environment snapshot:

```sh
mkdir -p reports
python3 tools/inspect_environment.py reports/capability_manifest.json
```

The inventory saves JSON and prints it to the terminal. It refuses to overwrite an existing destination.

Record a command:

```sh
python3 tools/record_run.py --timeout 5 --output-root reports -- python3 -c "print('hello')"
```

Generate an HTML viewer from selected reports:

```sh
python3 tools/view_report.py --receipt PATH_TO_RECEIPT_JSON --inventory PATH_TO_INVENTORY_JSON --output PATH_TO_NEW_HTML_FILE
```

Replace the placeholders with local paths. The viewer output must be a new file.

### Interpret recorder outcomes

| Receipt state | Meaning |
|---|---|
| `started` | Completion has not been recorded |
| `completed` | Child finished; inspect its return code |
| `timed_out` | Recorder enforced its timeout |
| `interrupted` | Keyboard interruption was handled |
| `launch_failed` | Command could not be launched |
| `recorder_error` | An operating-system error occurred after launch |

Completed commands normally preserve the child’s exit status. Negative child return codes are mapped to `128` plus the signal number.

Recorder-specific outcomes use:

- `124` for timeout.
- `127` for launch or handled operating-system errors.
- `130` for handled keyboard interruption.

A child can return those same numbers. Use the receipt state to distinguish outcomes.

## Quadratic Contract Atlas

The kit includes coefficient-sweep, contract-collision, modular-atlas, and quadratic-atlas examples.

The demonstrated quadratic experiment uses the reference:

```text
f(x) = x*x + x
```

and candidates:

```text
g(x) = c*x*x + a*x + b
```

Each coefficient ranges from −3 through 3, producing 343 candidates per modulus.

### Run the experiment

```sh
python3 tools/run_workflow.py --timeout 30 --output-root reports -- python3 examples/quadratic_contract_atlas.py --moduli 2 3 4 5 6 8 --bound 3 --output-dir reports/quadratic-atlas-001
```

The atlas produces:

```text
reports/quadratic-atlas-001/atlas.md
reports/quadratic-atlas-001/atlas.json
```

The demonstrated recorded workflow completed with:

```text
STATUS=completed
RECORDER_EXIT=0
WORKFLOW_RECORDER_EXIT=0
WORKFLOW_STATUS=reports_created
WORKFLOW_EXIT=0
```

### Recorded results

The experiment compares complete residue enumeration, exact quadratic conditions, and evaluation at three points. Strict coefficient matching is included as a deliberately adversarial rule.

| Modulus | Candidates | Accepted | Primary disagreements | Strict false rejects | Strict false accepts | Failed replays |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 343 | 75 | 0 | 27 | 0 | 0 |
| 3 | 343 | 12 | 0 | 0 | 0 | 0 |
| 4 | 343 | 8 | 0 | 4 | 0 | 0 |
| 5 | 343 | 1 | 0 | 0 | 0 | 0 |
| 6 | 343 | 2 | 0 | 1 | 0 | 0 |
| 8 | 343 | 2 | 0 | 1 | 0 | 0 |
| Total | 2,058 | 100 | 0 | 33 | 0 | 0 |

Strict false rejections are findings, not harness failures.

For example, modulo 4, `-x*x - x` and `x*x + x` both produced:

```text
[0][2]
```

over inputs 0 through 3, despite failing strict coefficient matching.

These results describe the tested bounded grid. They are not general polynomial classification or formal certification.

## Saved-evidence verification and tests

### Verify a generated atlas

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

The verifier uses only the Python standard library and does not import the atlas generator.

It recomputes residue outputs and checks:

- Report parameters and modulus groups.
- Complete bounded coefficient-grid coverage.
- Complete and three-point acceptance.
- Strict coefficient acceptance and error flags.
- First counterexamples and saved replay status.
- Equivalence comparison lists.
- Summary counts.

The saved exact-route acceptance flag is checked against complete enumeration. The verifier does not independently implement that route’s algebraic conditions.

The equivalence-comparison counter counts candidate cases containing complete comparison lists—not individual residue comparisons.

### Verify the included fixture

The modulus-2 fixture allows verification without first generating a report:

```sh
python3 tools/verify_quadratic_atlas.py tests/fixtures/quadratic_atlas_q2.json
```

Expected output:

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

| Test case | Expected outcome |
|---|---|
| Unchanged fixture | Accepted with the expected totals |
| Corrupted recorded output | Rejected |
| Missing counterexample | Rejected |
| Corrupted equivalence comparison | Rejected |
| Corrupted summary count | Rejected |
| Duplicate candidate replacing another grid entry | Rejected |

Tests mutate in-memory copies, leaving the fixture unchanged. The fixture is derived from the experiment, not an independently authored oracle.

### Complete-package validation

The complete source archive was extracted into a fresh temporary directory on the same Termux/Python 3.13.13 environment.

Manifest checks passed, followed by:

```text
Ran 66 tests in 8.389s
OK
EXTRACTED_FULL_SUITE_EXIT=0
WHOLE_KIT_EXTRACTION_CHECK_OK
```

This establishes operation outside the original project directory on the tested environment. It does not establish compatibility with other devices, operating systems, or Python versions.

## Limitations, privacy, and licensing

### Evidence boundaries

- Process exit codes are not mathematical verdicts.
- Receipts are execution records, not signatures or certificates.
- Environment readings are snapshots, not workload or performance guarantees.
- The viewer displays supplied data; it does not authenticate a run or prove that reports share one execution.
- The workflow does not sandbox commands.
- Output files are not size-limited.
- The recorder’s timeout is not guaranteed after the recorder is killed.
- The verifier is not hardened for arbitrary untrusted JSON.
- Five mutation scenarios do not cover every possible corruption.

Abrupt Android termination, storage exhaustion, power loss, every descendant-process scenario, sustained device workloads, and workflow-level keyboard interruption remain outside established coverage.

Previously reported Termux session resets remain unexplained. Passing short tests does not establish sustained device stability.

### Privacy and package integrity

Commands, paths, device details, stdout, and stderr may contain private information. Review them before sharing.

Generated reports, HTML output, caches, repair backups, and older archives are excluded from the selected source package unless deliberately included and reviewed.

The package manifest records SHA-256 hashes for selected files. Those hashes check agreement with packaged bytes; they do not authenticate authorship, certify results, or add source and receipt hashing to recorded workflows.

If files covered by `manifest.json` are edited—including this README—regenerate the manifest before claiming it validates the revised package.

### License and publication

No license has been selected. Review source ownership and provenance before choosing a license or presenting the project as an open-source release.

Any applicable publication restrictions must be resolved separately. Complete source upload and successful tests against a fresh GitHub checkout have not yet been confirmed.

---

Inspect what is available.  
Record what ran.  
View what was supplied.  
Keep the claims within the evidence.
