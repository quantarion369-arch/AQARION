# Mobile Research Kit — File Tree

## Package layout

    mobile-research-kit/
    ├── README.md
    ├── .gitignore
    ├── CHECKPOINT.md
    ├── FILETREE.md
    ├── RECOVERY.md
    ├── manifest.json
    ├── examples/
    │   ├── coefficient_sweep.py
    │   ├── contract_collision_lab.py
    │   ├── modular_contract_atlas.py
    │   └── quadratic_contract_atlas.py
    ├── tools/
    │   ├── inspect_environment.py
    │   ├── record_run.py
    │   ├── run_workflow.py
    │   ├── verify_quadratic_atlas.py
    │   └── view_report.py
    ├── tests/
    │   ├── fixtures/
    │   │   └── quadratic_atlas_q2.json
    │   ├── test_coefficient_sweep.py
    │   ├── test_contract_collision_lab.py
    │   ├── test_contract_selection.py
    │   ├── test_inspect_environment.py
    │   ├── test_modular_contract_atlas.py
    │   ├── test_quadratic_atlas_saved_evidence.py
    │   ├── test_quadratic_contract_atlas.py
    │   ├── test_record_run.py
    │   ├── test_run_workflow.py
    │   ├── test_view_report.py
    │   ├── test_workflow_failures.py
    │   └── test_workflow_os_errors.py
    └── docs/
        └── history/
            ├── README-25tests.md
            └── CHECKPOINT-25tests.md

The root name above is the logical package name. The current repository
directory is MOBILE-RESEARCH-KIT; the verified phone directory is
Mobile-Research-Kit-Deliverables.

The historical documents are included in the verified local package.
Their presence in the repository must be checked separately.

## Root documents

| File | Purpose |
|---|---|
| README.md | Installation context, usage commands, results interpretation, and limitations. |
| CHECKPOINT.md | Dated verification evidence, archive identity, and remaining work. |
| FILETREE.md | Package layout and file responsibilities. |
| RECOVERY.md | Recovery history and technical specification. |
| manifest.json | Selected package paths, byte sizes, and SHA-256 hashes. |
| .gitignore | Repository exclusion rules. |

## Implementation

examples/ contains the four experimental programs.

tools/ contains environment inspection, command recording, workflow
coordination, saved-evidence verification, and report viewing.

tests/ contains twelve test modules.

tests/fixtures/quadratic_atlas_q2.json is the original saved fixture used
for quadratic evidence verification. Recovery excerpts are not replacements
for this file.

## Historical records

docs/history/ preserves the earlier README and checkpoint.

Those documents describe an earlier build. Current operating instructions
belong in README.md; current verification evidence belongs in CHECKPOINT.md.

## Additional root items

LICENSE was included as a planned entry in the earlier tree. Add it to the
actual inventory when the completed file is installed.

A separate recovery JSON is visible in the repository, but its full filename
has not been supplied. It is therefore not assigned an invented name here.

## Generated outputs

reports/ is used by the documented workflow commands for generated artifacts.
It is not included in this source tree as a pre-existing packaged directory.

Archives, temporary extraction folders, caches, and backups are not
implementation components.

## Maintenance

Update this tree when files are added, removed, or moved.

Update manifest.json when selected package contents change.

Verification results apply to the files and archive actually tested, not
automatically to subsequent edits.
