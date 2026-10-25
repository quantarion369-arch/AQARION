# Pinned-source classification and blob-identity checkpoint

## Executed result

The preserved user-executed runs reported:
- Classification checkpoint: 55 focused tests; 174 package tests and 10 subtests.
- Later blob-identity checkpoint: 95 focused tests; 214 package tests and 10 subtests.

These are historical executions, not tests rerun during preservation.

## Preserved scope

This directory contains the complete local session checkpoint:
classification workspace, object-integrity workspace, recovery backup,
tested source copies, commands, outputs, XML reports, receipts, hashes,
starting-state records, and a cumulative RAG patch including new tests.

The original manifest is preserved verbatim as manifest.json.
publication-index.json maps its original paths to archived paths.

Historical Python files use the suffix .py.txt. They are evidence copies,
not additional tests or supported replay commands. Do not blindly run
the historical application drivers on a later checkout.

## Implementation boundary

The current tested patch distinguishes established source absence from
source-loading failures and verifies the selected blob's raw-byte identity
before text decoding. It retains the existing manifest object-ID policy.

Explicit rehashing of the complete commit/tree chain is NOT ESTABLISHED.
The separate reference-verifier experiments are not production test results.

This checkpoint is not a repository-wide integrity audit, independent
execution attestation, research reproduction, or mathematical proof.
The earlier browser-race checkpoint was not rerun.

## Preservation boundary

Original workspaces and the recovery backup remain untouched.
Unrelated research was not copied into this receipt directory.
No source modification, test execution, staging, commit or push was
performed by the publication-preparation script.
