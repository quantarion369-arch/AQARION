# Mobile Research Kit
### Built on a phone. Executed locally. Reported clearly.

A compact Python toolkit developed through an Android / Termux
workflow for inspecting an environment, recording bounded command
executions, and displaying supplied reports in a local HTML page.

The connected workflow brings these steps together:

    Explicit command
          |
          v
    Environment snapshot
          |
          v
    Recorded execution
          |
          v
    HTML report

The tools make local activity easier to inspect.
They do not turn execution records into authenticated proof.

## Status

Locally tested prototype. Not yet a published release.
Checkpoint: 2026-10-07.

- Four tools.
- Six test files.
- 25 saved tests passed in 5.674 seconds.
- FULL_TEST_SUITE_EXIT=0.
- A real connected workflow completed with reports created and exit 0.
- An earlier generated viewer page opened on the user's phone.

These observations come from user-supplied terminal output and
a screenshot, not independent reproduction.

No license has been selected. No repository publication is established.

## Tools

| Tool | Purpose |
|---|---|
| inspect_environment.py | Save an environment snapshot |
| record_run.py | Record a command with a configured timeout |
| view_report.py | Generate HTML from supplied JSON reports |
| run_workflow.py | Coordinate inventory, recording, and viewing |

The first three tools remain independently usable.
The workflow coordinator invokes them as separate Python processes.

## Quick start: connected workflow

Run from the project directory:

    python3 tools/run_workflow.py --timeout 5 --output-root reports -- python3 -c "print('Connected workflow works')"

The output identifies:

- WORKFLOW_DIRECTORY
- INVENTORY_FILE
- RUN_DIRECTORY
- WORKFLOW_RECORDER_EXIT
- RECEIPT_FILE
- VIEWER_FILE
- WORKFLOW_STATUS
- WORKFLOW_EXIT

Open the file identified by VIEWER_FILE in a local HTML viewer.

Each invocation creates a separate workflow directory:

    reports/
    └── workflow-.../
        ├── inventory.json
        ├── viewer.html
        └── runs/
            └── run-.../
                ├── receipt.json
                ├── stdout.txt
                └── stderr.txt

The command is executed directly, without an implicit shell.
Use an explicit shell only when shell syntax is required.

The timeout applies to the recorded child execution.
It is not a deadline for the complete multi-stage workflow.

## Workflow outcomes

WORKFLOW_STATUS=reports_created means report generation finished.
It does not necessarily mean the child command succeeded.

When report generation succeeds, the coordinator returns the
recorder's exit result. Child failure and timeout can therefore
still produce a viewer page.

Orchestration failures return 125 and print:

    WORKFLOW_STATUS=orchestration_failed
    WORKFLOW_EXIT=125

If the recorder already returned, WORKFLOW_RECORDER_EXIT preserves
that result in the terminal output.

A child can itself return 125. Use WORKFLOW_STATUS and the receipt
rather than interpreting the exit number alone.

Artifacts created before an orchestration failure may remain.
Failure does not automatically remove the workflow directory.

## Standalone environment inventory

Prepare the parent directory, then create a new snapshot:

    mkdir -p reports
    python3 tools/inspect_environment.py reports/capability_manifest.json

The inventory saves JSON and also prints it to the terminal.
It refuses to overwrite an existing destination.

It records environment classification, architecture, Python,
available Termux and Android details, selected memory readings,
home-filesystem capacity, and selected command locations.

Interpretation boundaries:

- A command location establishes PATH discovery, not execution.
- Memory readings are snapshots, not workload allowances.
- Storage readings are snapshots, not performance measurements.
- Native-shell inspection does not establish Ubuntu tool availability.
- Environment details do not establish research correctness.

## Standalone command recorder

    python3 tools/record_run.py --timeout 5 --output-root reports -- python3 -c "print('hello')"

Each invocation creates a unique run directory containing
receipt.json, stdout.txt, and stderr.txt.

### Receipt states

| State | Meaning |
|---|---|
| started | Completion has not been recorded |
| completed | Child finished; inspect its return code |
| timed_out | Recorder enforced its timeout |
| interrupted | Keyboard interruption was handled |
| launch_failed | Command could not be launched |
| recorder_error | Operating-system error occurred after launch |

A completed state can include a nonzero child return code.

An abrupt Android termination may leave a started receipt.
That does not establish whether the child is still running.

### Recorder exit behavior

Completed commands normally preserve the child's exit status.
Negative child return codes are mapped to 128 plus the signal number.

Recorder outcomes use:

- 124 for timeout.
- 127 for launch or handled operating-system errors.
- 130 for handled keyboard interruption.

A child can itself return these numbers.
Use the receipt status to distinguish outcomes.

## Standalone HTML viewer

    python3 tools/view_report.py --receipt PATH_TO_RECEIPT_JSON --inventory PATH_TO_INVENTORY_JSON --output PATH_TO_NEW_HTML_FILE

Replace the placeholders with selected local paths.
The output must be a new file.

The viewer displays execution fields, selected environment fields,
and the raw JSON for both inputs.

It displays supplied data. It does not authenticate, reproduce,
or certify the run, or verify that two reports share one execution.

## Tests

    python3 -m unittest discover -s tests -v

| Test group | Count |
|---|---:|
| Environment inventory | 3 |
| Command recorder | 5 |
| HTML viewer | 5 |
| Connected workflow | 4 |
| Workflow failure paths | 6 |
| Workflow operating-system errors | 2 |
| Total | 25 |

Latest user-reported result:

    Ran 25 tests in 5.674s
    OK
    FULL_TEST_SUITE_EXIT=0

Coverage includes artifact creation, child failure, timeout,
overwrite protection, input rejection, report-text escaping,
receipt validation, viewer failures, simulated subprocess launch
errors, and an output root that is an existing file.

Several orchestration tests simulate tool results.
They complement rather than replace the connected execution tests.

Passing tests are not a complete security audit.

## Project layout

    mobile-research-kit/
    ├── .gitignore
    ├── README.md
    ├── CHECKPOINT.md
    ├── tools/
    │   ├── inspect_environment.py
    │   ├── record_run.py
    │   ├── view_report.py
    │   └── run_workflow.py
    └── tests/
        ├── test_inspect_environment.py
        ├── test_record_run.py
        ├── test_view_report.py
        ├── test_run_workflow.py
        ├── test_workflow_failures.py
        └── test_workflow_os_errors.py

This is the selected source/documentation tree.
Generated artifacts and historical checkpoint files are separate.

## Requirements

The tools use Python's standard library.
No third-party Python packages are imported.

The recorder requires a POSIX execution environment for its
process-group handling.

Previously recorded development environment:

- Samsung SM-A156U.
- Android 16.
- AArch64.
- Google Play Termux 2026.06.21.
- Python 3.13.13.

Other environments have not been verified as supported.
Ubuntu / Lean research work remains separate.

## Evidence and limitations

A process exit code is not a mathematical verdict.
Receipts are execution records, not signatures or certificates.
Source hashing and receipt hashing are not implemented.

The workflow does not sandbox the command.
Generating artifacts together does not authenticate them.

Output files are not size-limited.
The recorder's timeout is not guaranteed after the recorder is killed.

Current tests do not establish behavior under abrupt Android
termination, storage exhaustion, power loss, every descendant-process
scenario, or sustained device workloads.

Workflow-level keyboard interruption remains outside established
test coverage.

Termux session resets remain unexplained.
Short passing tests do not establish sustained device stability.

## Privacy and transfer

Commands, paths, device details, stdout, and stderr may contain
private information. Review before sharing.

Nothing is automatically uploaded, committed, or pushed.

Source packages select project files explicitly.
Raw reports, generated HTML, caches, backups, and older archives
are excluded unless deliberately selected and reviewed.

Archive verification checks packaging integrity and agreement with
selected source bytes. It does not establish software correctness.

Older nine-file and 17-test packages are historical snapshots,
not packages of this 25-test version.

## License and publication

No license has been selected.
Choose one before presenting this package as an open-source release.

No repository upload, commit, pull request, or merge is established.

---

Inspect what is available.
Record what ran.
View what was supplied.
Keep the claims within the evidence.
