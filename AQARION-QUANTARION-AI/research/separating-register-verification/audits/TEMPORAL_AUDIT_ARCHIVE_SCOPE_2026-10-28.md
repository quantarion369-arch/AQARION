# Temporal audit archive: publication scope

## Preserved evidence
This archive covers 48 original files in five run directories:
two eight-state-and-case-B runs, one exact claim-correction audit,
one fast sixteen-cycle census, and one earlier interrupted cycle attempt.

Four packages contain historical zero-exit receipts and reported PASS
results. The earlier cycle attempt ends in KeyboardInterrupt and has
no completion receipt, result JSON, or historical manifest. It is retained
as an interrupted attempt, not a successful census.

## Repeat-run comparison
The two eight-state packages have identical file sets and 14 byte-identical
files. Their result JSON differs only in two elapsed times and two
run-specific compile paths. Their verification logs differ only in the
TOTAL_SECONDS value. Their historical manifests differ as preserved.
These are repeat execution records, not independent implementations.

## Boundaries
The eight-state census concerns the fixed observation recorded by its
source and scope document. The case-B written argument is not machine
formalized and is a separate mathematical lane from the dynamics paper.
The correction audit records witness determinants 1 and -1 and rejects
8192 for the tested matrix.
The fast cycle census records 4080 full-rank primitive necklaces and
bridge_test_nonvacuous=false. Zero bridge counterexamples must not be
presented as a nonvacuous bridge test.

This preparation does not rerun, compile, import, or execute archived
programs. It is not a full source audit, independent proof review,
formal certification, novelty assessment, or application-claim promotion.

## Integrity and custody
Historical bytes and local permission modes are preserved and recorded.
Git publication does not reproduce every POSIX permission bit; the
review JSON records the original local modes.
Historical manifests are not rewritten. They contain 41 checked entries.
The new publication manifest binds all 48 originals and two publication
documents; it does not contain its own checksum.
Manuscripts, review packets, registry backups, caches, and unrelated logs
are excluded. Preparation state is distinct from later commit/push state.
