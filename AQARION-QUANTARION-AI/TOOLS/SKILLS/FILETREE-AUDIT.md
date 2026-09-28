Filetree Audit Skill

Purpose

Compare a declared repository filetree against the actual repository tree.

The audit prevents documentation from describing files, directories, workflows, or packages that do not exist.

It also detects naming and capitalization drift.

Inputs

- repository root;
- declared "FILETREE.md";
- actual filesystem tree or Git tree;
- optional exclusion rules.

Checks

1. Existence

Every declared path must be classified as:

EXISTS
MISSING

2. Undeclared paths

Every actual path not represented by the declared tree is classified:

UNDECLARED

This is not automatically an error.

It may indicate:

- newly added material;
- generated files;
- intentionally omitted internals;
- stale documentation.

3. Exact capitalization

Paths are compared case-sensitively.

These are distinct:

verification/
Verification/
VERIFICATION/

Likewise:

Filetree.md
FILETREE.md
filetree.md

The audit must not normalize these names silently.

4. File/directory type

A declared file must exist as a file.

A declared directory must exist as a directory.

A path changing from one type to the other is a structural change and must be reported.

5. Workflow paths

".github/" and ".github/workflows/" are audited explicitly.

Workflow filenames are treated as exact paths.

6. Research/tool boundary

The audit records whether a path belongs to:

RESEARCH
TOOLS
VERIFICATION
FORMALIZATION
CLAIMS
LITERATURE
ARCHIVE

This prevents reusable infrastructure from silently becoming mixed with a research artifact.

Output

Produce a report containing:

DECLARED
ACTUAL
MISSING
UNDECLARED
CASE_MISMATCH
TYPE_MISMATCH
WORKFLOW_MISMATCH
BOUNDARY_WARNINGS
STATUS

Failure conditions

Fail the audit when:

- a required declared path is missing;
- capitalization differs;
- a required file is replaced by a directory or vice versa;
- a required workflow is missing;
- a canonical path is ambiguous.

Do not fail merely because additional files exist.

Repository rule

"FILETREE.md" describes the repository.

It must not describe an imagined future repository as though it already exists.

When a target architecture is useful, label it explicitly as:

TARGET ARCHITECTURE

rather than presenting it as the current tree.

Evidence status

[R] Packaging/reproducibility infrastructure.

The audit establishes documentation/tree consistency only. It does not certify mathematical content.
