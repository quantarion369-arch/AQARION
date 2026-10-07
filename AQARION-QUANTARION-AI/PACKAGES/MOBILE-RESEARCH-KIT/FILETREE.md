# Mobile Research Kit: File Tree

Date: October 7, 2026.

## Selected package structure

    mobile-research-kit/
    ├── README.md
    ├── .gitignore
    ├── CHECKPOINT.md
    ├── FILETREE.md
    ├── manifest.json
    ├── docs/
    │   └── history/
    │       ├── README-25tests.md
    │       └── CHECKPOINT-25tests.md
    ├── examples/
    │   ├── coefficient_sweep.py
    │   ├── contract_collision_lab.py
    │   ├── modular_contract_atlas.py
    │   └── quadratic_contract_atlas.py
    ├── tools/
    │   ├── inspect_environment.py
    │   ├── record_run.py
    │   ├── run_regression.py
    │   ├── run_workflow.py
    │   ├── verify_package.py
    │   ├── verify_quadratic_atlas.py
    │   └── view_report.py
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
        ├── test_run_regression.py
        ├── test_run_workflow.py
        ├── test_verify_package.py
        ├── test_view_report.py
        ├── test_workflow_failures.py
        └── test_workflow_os_errors.py

The tree describes the selected source package, not every file currently
present in the phone directory.

The logical package name is mobile-research-kit.
The current phone working directory is Mobile-Research-Kit-Deliverables.

## Responsibilities

- examples/: experimental programs and atlas generators.
- tools/: inspection, recording, orchestration, verification, and viewing.
- tests/: implementation and failure-path regression tests.
- tests/fixtures/: saved evidence required by fixture-based tests.
- docs/history/: preserved earlier operating documents.
- manifest.json: selected file paths, byte sizes, and SHA-256 hashes.
- CHECKPOINT.md: recorded execution and release boundaries.
- FILETREE.md: selected structure and file responsibilities.

## Verification entry points

Package integrity:

    python tools/verify_package.py

Package integrity followed by the complete test suite:

    python tools/run_regression.py

The integrity verifier checks listed files only.
A successful check does not establish authenticity or verify unlisted files.

## Items requiring presence checks

LICENSE and RECOVERY.md were discussed previously but their current
presence was not established by this document inspection.

Add them to the selected tree after confirming the actual files.
Do not invent filenames for recovery artifacts.

## Generated and excluded items

Runtime reports, caches, temporary directories, and historical archives
are not shown as source components.

Keep the saved quadratic fixture distinct from generated reports.
Recovery excerpts are not replacements for the fixture.

## Maintenance

Update this document when selected files are added, removed, or moved.

Update affected manifest entries deliberately after approved edits.
Verification results apply to the snapshot actually checked.
