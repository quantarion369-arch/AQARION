# Addendum 2026-11-24: trace wording erratum and formal-verification cross-link

This file is additive. No existing file, receipt, verifier script or per-bundle SHA256SUMS in this
package was modified, so every preserved hash still verifies.

## 1. Trace wording erratum (confirmed against code)

The integral verifier's elimination routine `reduce_units` (evidence/integral/verify.py, lines
197-242) performs integer row operations only. It chooses an entry of absolute value 1 in a remaining
row, removes that row as the pivot row, and subtracts `row[j] * unit` times the pivot row from every
remaining row that has an entry in column `j`. The trace is complete when no rows remain. It performs
no column operations and does not output Smith transformation matrices.

Two statements in the preserved text over-describe this:

- evidence/integral/PROOF_BOUNDARY.txt line 8: "unimodular row/column operations".
- evidence/integral/PROOF_BOUNDARY.txt line 10, and the verifier's printed text near verify.py line
  317: "integral Smith form I_r plus zero".

The conclusions are still correct, by an argument that is a mathematical remark and is not formalized
in Lean. The retained pivot rows, restricted to the pivot columns in trace order, form a triangular
matrix with diagonal entries plus or minus 1, so an r-by-r minor is a unit. The zero residual rows
bound the rank above by r. Together they give rank r over every field. Row operations are
unimodular, so the ideal of r-by-r minors is the unit ideal; hence the product of the nonzero Smith
invariant factors is 1 and each one is 1. The second implementation's column-only replay is a
separate corroborating route to the same determinantal-ideal conclusion. It is a second
implementation, not an independent external reproduction.

## 2. Same phrase, not yet checked

evidence/divisor/PROOF_DEPENDENCIES.txt line 49 uses the phrase "unimodular row/column". Only the
integral verifier's `reduce_units` has been read for this erratum. The divisor verifier's routine has
not been audited for the same issue, so this line is flagged, not corrected. THEOREM_DRAFT.md line 148
and PROOF_DEPENDENCIES.txt line 41 concern integer Smith forms and torsion factors of the divisor
audit and are likewise not examined here.

## 3. Formal verification cross-link

Formal repository: https://github.com/quantarion369-arch/AQARION-LEAN

- Bridge (semigroup, cone and lattice translation theorems): commit
  e8d7efafada29801deefb8e0aa9377f5fdca8d1f, p2-bridge run 45528017684, success.
- Generic unit-pivot trace theorem `P2Mathlib.rank_of_unitTrace`, promoted into the gated library at
  commit dff1f26153194e249048760030f5e89b6872b35d (p2-lean run 45539161347, success; mathlib gate:
  exactly 3 axiom reports, allowed axioms propext, Classical.choice, Quot.sound, no sorryAx).
- Current receipt, trace note and report addendum: commit
  3e89463d2093def30e1c0884b34b7dff3e7b560d (files P2-SEMIGROUP/CI_RECEIPT_CURRENT.json,
  TRACE_NOTE.md, REPORT.md).

The generic theorem certifies rank r over every field for a valid unit-pivot trace of an integer
matrix. It has not yet been bound to the nine frozen component matrices or their saved traces.
Computational receipts here remain computational evidence.

## 4. Status

Lemma 2, kernel generation and the overall resolution theorem remain DRAFT_REQUIRING_REVIEW. The
formal results are CI-reported and have not had external or independent review.
