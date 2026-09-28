# JOIN-STABILITY ZIP-CLONE

## Object

JOIN-STABILITY finite pullback-stable join verification package.

## Package identity

The canonical identity and version are defined by:

    manifest.json

Do not infer package identity from the ZIP filename.

## Clone procedure

Extract the archive without modifying its contents.

Expected root:

    JOIN-STABILITY/

Expected required files:

    README.md
    manifest.json
    zip-clone.md
    claims.jsonl
    evidence.jsonl
    reproduce.sh
    verify.py

Expected package directories:

    fixtures/
    negative-controls/
    receipts/
    docs/

## Verify package structure

Run:

    python3 verify.py

## Reproduce

Run:

    ./reproduce.sh

The reproduction command must invoke the verifier against the extracted package.

## Exit semantics

Exit 0:

    declared verification completed successfully.

Non-zero exit:

    verification failed or package requirements were not satisfied.

A zero exit code does not by itself establish the mathematical theorem.

## Evidence boundary

This package can provide:

    [V] computational verification

It does not automatically provide:

    [P] mathematical proof

A proof artifact must be separately identified.

## Integrity

checksums.sha256 records package-file hashes.

A checksum mismatch means the package has changed relative to the recorded checksum set.

A valid checksum does not establish mathematical correctness.

## Negative controls

The verifier must reject deliberately corrupted or inconsistent package material.

Negative controls are part of the verification contract.

## Portability

The package is intended to be transportable between:

    GitHub
    Hugging Face
    Replit
    Termux
    local machines
    archival storage

The extracted research object must remain self-contained except for explicitly declared dependencies.

## Source authority

Git source revision and manifest metadata identify provenance.

The ZIP archive is not the canonical source of mathematical truth.
