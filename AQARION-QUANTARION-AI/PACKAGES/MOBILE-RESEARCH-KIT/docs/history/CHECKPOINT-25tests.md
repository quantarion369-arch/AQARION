# Mobile Research Kit — Connected Workflow Checkpoint

Date: 2026-10-07
Status: locally tested prototype; not published.

## Current implementation

Four tools:

- tools/inspect_environment.py
- tools/record_run.py
- tools/view_report.py
- tools/run_workflow.py

The coordinator creates an environment snapshot, records an explicit
command, generates a viewer, and prints the artifact locations.

## Latest user-reported test evidence

- Ran 25 tests in 5.674 seconds.
- Result: OK.
- FULL_TEST_SUITE_EXIT=0.

Test groups:

- Inventory: 3.
- Recorder: 5.
- Viewer: 5.
- Connected workflow: 4.
- Workflow failure paths: 6.
- Workflow operating-system errors: 2.

Total: 25.

## Manual connected-workflow evidence

Command:

    python3 tools/run_workflow.py --timeout 5 --output-root reports -- python3 -c "print('Connected workflow works')"

User-reported outcome:

- Inventory file created.
- Execution receipt created.
- Recorder status: completed.
- RECORDER_EXIT=0.
- WORKFLOW_RECORDER_EXIT=0.
- HTML viewer created.
- WORKFLOW_STATUS=reports_created.
- WORKFLOW_EXIT=0.
- WORKFLOW_COMMAND_EXIT=0.

Opening this particular workflow-generated viewer has not been
reported. An earlier generated viewer opened on the user's phone.

## Evidence source

Results come from user-supplied terminal output and an earlier
viewer screenshot, not independent reproduction or signed evidence.

Some failure-path tests use simulated subprocess results.

## Selected source deliverables

- .gitignore
- README.md
- CHECKPOINT.md
- tools/inspect_environment.py
- tools/record_run.py
- tools/view_report.py
- tools/run_workflow.py
- tests/test_inspect_environment.py
- tests/test_record_run.py
- tests/test_view_report.py
- tests/test_run_workflow.py
- tests/test_workflow_failures.py
- tests/test_workflow_os_errors.py

Total: 13 selected files.

## Observed development environment

Previously recorded:
Samsung SM-A156U; Android 16; AArch64.
Google Play Termux 2026.06.21; Python 3.13.13.

Other environments have not been verified.

## Limitations

Workflow-level keyboard interruption, abrupt Android termination,
storage exhaustion, power loss, sustained device stability, and all
descendant-process scenarios are not established by the suite.

Termux session resets remain unexplained.
Output files are not size-limited.
The timeout is not guaranteed after the recorder is killed.

The workflow is not a command sandbox.
Reports are not signatures, certificates, or mathematical verdicts.
No source or receipt hashing is implemented.
Viewer inputs are not authenticated or proven to share one execution.

## Transfer and publication

Exclude raw reports, execution output, generated viewer pages,
caches, backups, and old archives unless deliberately reviewed.

Older packages remain historical snapshots.
The packaging command separately reports the current archive name,
size, member count, and verification outcome.

No license selection or repository publication is established.
Ubuntu / Lean research work remains separate.
