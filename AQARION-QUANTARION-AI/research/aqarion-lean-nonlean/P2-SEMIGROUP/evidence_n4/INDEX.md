# evidence_n4 index (status: DRAFT_REQUIRING_REVIEW)

Current scripts (replayable, outputs recorded in SHA256SUMS.txt):
- p2_verification_corrected.py: Betti tables of S/M_n for n=3,4 by corrected Hochster; Taylor (x) k cross-check for n=3.
- hochster_betti.py: Hochster-formula Betti tables of S/M_n for n=3..9 compared with the closed formula.
- std_monomial_check.py: standard-monomial check of the general-n generation argument for n=3..6.

Kept as a record of a failed attempt:
- p2_verification_FINAL.py: its totals (127, 640, 101, 6061, 215, 930) come from script bugs (shifted homology index, inverted lcm test, wrong Koszul transfer). Do not cite them.

All other files here (p2_*.py, validate_p2*.py, p2_resolution.sing) are earlier scratch work, not reviewed, possibly superseded, and may share the bugs above. Their names ("final", "proof", "rigorous") are not claims of correctness.

Not formalized: the argument that A, C are regular on R_n (so Betti of R_n over P equals Betti of S/M_n over S) and the all-n generation argument are unreviewed hand arguments.
