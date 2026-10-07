# REPLAY-001

External replay specification.

## Purpose

REPLAY-001 provides an external controller for reproducing a computational
package from a pinned repository revision under an independently supplied
policy.

The replay result is reproducibility evidence.

It is not mathematical proof.

## Trust boundary

The controller, policy, and receipt contract are outside the replayed package.

The replayed package cannot authorize its own execution.

Runtime execution requires both:

1. policy authorization (`policy.execution.allow_exec == true`);
2. explicit `--allow-exec`.

Downloaded source is therefore not automatically executable source.

## Stages

### Acquire

Obtain the source archive for the exact repository and commit specified by
the policy.

A total elapsed-time budget (`policy.archive.max_seconds`) bounds the
download.

Failure is `ACQUIRE_FAIL`.

### Archive

Hash the acquired archive and enforce archive limits:

- `max_bytes`;
- `max_files`;
- `max_file_bytes`;
- `max_seconds`.

The file-count limit is reserved *before* the target file is opened, so
rejection happens before disk is committed.

Failure is `ARCHIVE_REJECT`.

### Inventory

Extract the archive using safe relative-path handling.

Record every file:

- relative path;
- byte size;
- SHA-256.

The inventory is complete for the extracted package tree.

Failure is `INVENTORY_FAIL`.

### Manifest

Compare policy-required files against the complete inventory.

The controller distinguishes:

- expected file absent;
- expected file hash wrong;
- unexpected file present.

A null policy hash means presence-only.

A presence-only match is not cryptographic evidence.

Failure is `MANIFEST_FAIL`.

### Fixtures

Fixtures are the subset of `policy.required_files` whose path begins with
`tests/fixtures/`.

The controller verifies required fixture hashes and parses JSON fixtures.

Failure is `FIXTURE_FAIL`.

### Test coverage

Static AST inspection identifies required test functions, test classes, and
test methods on test classes, without importing the target package.

Static inspection is not runtime execution.

Failure is `TEST_COVERAGE_FAIL`.

### Execution

Runtime test discovery/execution is a separate operation.

It requires:

```text
policy.execution.allow_exec == true
