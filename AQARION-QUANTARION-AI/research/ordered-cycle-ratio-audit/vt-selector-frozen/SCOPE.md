# Frozen V_t selector: local reproduction evidence

## Provenance

This scope note was prepared after the verified Termux execution.
It was not part of the frozen source or the original receipt.

Seven files from the local evidence directory are copied unchanged.
SHA256SUMS is the original local evidence manifest.
PACKAGE_SHA256SUMS additionally binds that manifest and this scope note.

## Reproduced results

- Frozen source: 10021 bytes; expected source SHA-256 matched.
- Canonical receipt body: expected SHA-256 matched.
- Selector exit: zero; stderr: empty.
- A: six pilot cases.
- B: six linear-search cross-checks; 354 n-values and 4127 (n,t) pairs.
- C: 1130 R <= V_t finite-grid checks, zero violations.
- D: 1110 ratio and positivity finite-grid checks, zero violations.
- E: 5586 t=m finite-window checks, zero violations.

Pilot witnesses (m,N,t):
(4,18,1), (5,26,2), (6,36,2),
(8,62,2), (10,95,3), (15,213,4).

## Interpretation and limits

N is the earliest Case B cutoff certified by the permitted
integer-t envelope family, subject to the stated general envelope
and monotonicity derivations. It is not the true crossing of R.

The linear scan independently cross-checks the search strategy.
It uses the same envelope formula and is not an independent
mathematical oracle.

Groups C, D and E are finite tests, not general proofs.
The source states that the all-n facts rest on paper derivations.
Those derivations are not supplied by this computational package.

Formal certification, novelty clearance and global Case B
classification remain open. No promotion is claimed.

This package is separate from the boundary-tail audit and prior
m=15 work. Do not merge their counts into this receipt.

## File conventions

stdout.txt contains a JSON receipt followed by two hash lines.
It is not a single standalone JSON document.
receipt.extracted.json is the parsed receipt saved separately.

The receipt hash is over canonical JSON of the receipt body.
It is not the raw-file hash of receipt.extracted.json.

Local-verification status and scope documentation are separate
from the frozen mathematical receipt.

This packaging operation did not rerun the selector.
