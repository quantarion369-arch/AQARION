# JOIN-STABILITY clean reproduction 001

Tested implementation commit: `7d3d9229b7029887a39d81e957361d66a5bcd8b9`.

This directory preserves the actual Termux reproduction and its
acceptance check, together with the preceding 20-test wrapper run.
The wrapper tests used isolated synthetic Git fixtures; the real
reproduction executed the maintained verifier, finite audit, and
validator controls. These are separate evidence layers.

All six declared finite-audit rows matched, with zero join failures.
Source and output hashes were checked against the tested commit.
Copied artifacts retain their original bytes; no log normalization
was performed. Original files remain outside the repository.

The test record's earlier baseline identifies the pre-commit test
checkout. Its source hashes were compared with the tested commit.
Absolute paths in original records identify the original device run.

Scope: structural and finite computational checks only. This is not
a general proof, Lean verification, novelty finding, independent
external reproduction, or authorization to promote claims.
Manifest, registries, proof text, and Lean dispositions are unchanged.
