# Multi-group closure-gap audit

## Scope

Finite exhaustive partition census for the fixed transition map:

    T = (5, 6, 6, 5, 0, 2, 0, 2)

All 4,140 set partitions were compared against a saved production census.
Independent behavioral checks use pair trajectories.
Independent ranks use exact SymPy rank of stacked group-indicator
observation matrices H*A**t, for t=0 through 7.

## Recorded results

| Gap | Partitions |
|---:|---:|
| 0 | 2228 |
| 1 | 1517 |
| 2 | 349 |
| 3 | 44 |
| 4 | 2 |

Maximum over two-group partitions: 4.
Maximum over partitions with three or more groups: 3.

All per-partition stable-class counts, ranks, and gaps matched.
A separate three-witness audit records rank growth through horizon 16.

## Replay

Use an environment containing the dependency in requirements.txt.
From this package directory, run:

    python3 -B verify_multigroup.py --output-dir /tmp/multigroup-audit-new-run

The output directory must not already exist.
The replay reads the bundled production receipt, not a local repository
checkout or a hard-coded sandbox directory. It writes only to the
specified output directory.

A successful replay writes status.json and report.json with result PASS.
The direct replay script does not create its own checksum manifest;
the archived receipts include their original execution wrappers' manifests.

## Evidence

- receipts/production: original eight-state production census.
- receipts/independent-full: original exhaustive independent audit.
- receipts/independent-witness: original three-witness audit.
- verify_multigroup.py: portability adaptation of the full audit driver.

Archived receipt files are preserved byte-for-byte. Historical absolute
paths inside them are provenance, not portable execution instructions.
The portable driver changes the original input/output path declarations.
The portable driver was successfully replayed from outside the checkout; all 4,140 per-partition results matched. The execution receipt is preserved in receipts/portable-replay.

The earlier interactive production census driver was not saved.
Its receipt preserves the executed production snapshot and result data.
This package does not reconstruct or misrepresent that missing driver.

## Non-claims

Not a census of all eight-state transition maps.
Not a general maximum theorem, formal proof, or novelty claim.
No production checker, claim registry, or Lean changes.
Literature supplies background, not verification of these recorded results.
