# PB-CORE-DIRECT-ENUM-001

## Status and scope

PASS for the stated finite scope only: all labelled maps
[n] -> [n] for n = 1 through 6.

This audit compares actual pullback-fixed equivalence-relation sets
obtained by direct enumeration and periodic-core construction.
It separately compares aggregate direct counts with the candidate formula.

This is bounded computational evidence, not a general proof,
Lean verification, or authorization to promote PB-CORE-006.

## Implementation

- pb_core_audit.py: direct enumeration, periodic-core construction,
  relation-set comparison, and exact aggregate formula evaluation.
- test_pb_core_audit.py: original unit-test suite.
- test_pb_core_audit_extra.py: expanded unit-test suite.

The direct path enumerates partitions of the whole set and checks
E(x,y) iff E(Tx,Ty) by explicit relation-pair membership.

The construction path enumerates pullback-fixed core partitions
and extends them through a power of the map that retracts onto the core.
It also checks the retraction image, identity on the core, and commutation
with the original map.

The paths share the partition generator. Their agreement is complementary
implementation evidence, not complete software independence.

## Fresh worktree replay

Evidence directory: replay-worktree-001/

- Base commit: 91076fe640a259c96417867c5b84cac96b691dc5
- Branch: audit/pb-core-direct-enum-001
- Platform: Android-16-aarch64-64bit-ELF
- Python: 3.13.13
- Unit tests: 21 passed in 0.471 seconds
- Census started UTC: 2026-10-12T06:14:06.147148+00:00
- Census finished UTC: 2026-10-12T06:15:44.144120+00:00
- Census elapsed seconds: 97.996357
- Implementation SHA-256:
  7c3b40c8b98ccda9b6b73f73c149a416bc60ceae428457b69e0365c274ddb42b

| n | Maps checked | Direct total | Constructed total | Formula total | Relation-set mismatches |
|---|-------------:|-------------:|------------------:|--------------:|------------------------:|
| 1 | 1 | 1 | 1 | 1 | 0 |
| 2 | 4 | 6 | 6 | 6 | 0 |
| 3 | 27 | 51 | 51 | 51 | 0 |
| 4 | 256 | 592 | 592 | 592 | 0 |
| 5 | 3125 | 8565 | 8565 | 8565 | 0 |
| 6 | 46656 | 148896 | 148896 | 148896 | 0 |

Total maps checked: 50,069.
All direct-minus-formula differences are zero.

## Evidence layout

Top-level evidence preserves the original standalone runs, unit-test
outputs, exit statuses, and saved hash manifests.

replay-worktree-001/ preserves the fresh replay: environment, commands,
source hashes, outputs, exit statuses, and an artifact hash manifest.

Empty output files are preserved intentionally where the saved run
produced no output on that stream.

## Provenance boundary

The fresh replay used new, uncommitted audit sources in a worktree based
on the recorded base commit. These sources were not in that base commit.

Source hashes identify the audit bytes used in the replay.
The working-tree status and environment are recorded separately.

The replay artifacts.sha256 manifest covers its listed replay artifacts,
not this README or the entire audit directory.

Original saved manifests establish byte consistency with those manifests.
They do not independently authenticate execution history or authorship.

## Replay instructions

Run from this audit directory:

    python -B -m unittest -v test_pb_core_audit test_pb_core_audit_extra
    python -B pb_core_audit.py --max-n 6

These commands display new results without overwriting saved evidence.
The census implementation restricts max-n to 1 through 6.

Verify the saved fresh-replay source hashes from this audit directory:

    sha256sum -c replay-worktree-001/source.sha256

Verify the saved fresh-replay artifact hashes:

    (cd replay-worktree-001 && sha256sum -c artifacts.sha256)

## Governance

Historical PB-CORE receipts and existing verifier scripts are unchanged.
This is an additive audit package, not a replacement for the missing
historical direct-pullback script cited by the existing replay document.

Finite agreement does not establish the general aggregate formula,
resolve formal proof obligations, or change PB-CORE-006 promotion gates.

Existing gates remain:

- Lean: OPEN
- C4: BLOCKED
- Publication: BLOCKED
- Promotion: FALSE
