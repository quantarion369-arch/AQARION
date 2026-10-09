# Mobile Research Kit: File Tree

Date: October 9, 2026.

## Selected package structure

    mobile-research-kit/
        .gitignore
        README.md
        CHECKPOINT.md
        FILETREE.md
        LICENSE
        OVERVIEW.md
        RECOVERY.md
        manifest.json
        docs/history/CHECKPOINT-25tests.md
        docs/history/README-25-tests.md
        examples/coefficient_sweep.py
        examples/contract_collision_lab.py
        examples/modular_contract_atlas.py
        examples/quadratic_contract_atlas.py
        tools/inspect_environment.py
        tools/record_run.py
        tools/run_regression.py
        tools/run_workflow.py
        tools/verify_package.py
        tools/verify_quadratic_atlas.py
        tools/view_report.py
        tests/test_coefficient_sweep.py
        tests/test_contract_collision_lab.py
        tests/test_contract_evidence.py
        tests/test_contract_selection.py
        tests/test_inspect_environment.py
        tests/test_modular_contract_atlas.py
        tests/test_quadratic_atlas_saved_evidence.py
        tests/test_quadratic_contract_atlas.py
        tests/test_quadratic_empty_evidence.py
        tests/test_quadratic_oracle_mutation.py
        tests/test_quadratic_oracle_separation.py
        tests/test_record_run.py
        tests/test_run_regression.py
        tests/test_run_workflow.py
        tests/test_verify_package.py
        tests/test_view_report.py
        tests/test_workflow_failures.py
        tests/test_workflow_os_errors.py
        tests/fixtures/quadratic_atlas_q2.json

The tree describes the selected source package, not every file currently
present in the phone directory.

The logical package name is mobile-research-kit.
Repository path: AQARION-QUANTARION-AI/PACKAGES/MOBILE-RESEARCH-KIT.

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

## Confirmed inventory

The inspected checkout contains eighteen Python test modules.
LICENSE, OVERVIEW.md, and RECOVERY.md are present.
Presence does not establish license interpretation or recovery completeness.

## Generated and excluded items

Runtime reports, caches, temporary directories, and historical archives
are not shown as source components.

Keep the saved quadratic fixture distinct from generated reports.
Recovery excerpts are not replacements for the fixture.

## Maintenance

Update this document when selected files are added, removed, or moved.

Update affected manifest entries deliberately after approved edits.
Verification results apply to the snapshot actually checked.
