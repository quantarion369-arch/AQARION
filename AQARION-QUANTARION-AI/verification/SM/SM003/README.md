# AQ-SM-003-MATRIX - Block-transition defect geometry

Claim:
- ||D||² = Σ m(|B|-m)/(|B||B'|)
- rank(D) = k - c

Ground truth: matrix_rank((I-P)KP, tol=1e-9)
Domain: n=3,4,5 = 166475 cases, n=6 f0=0 = 1578528 => total 1745003
Exact rational required. Integer division // fails 125348/166475.
Default matrix_rank fails 15400/166475 without absolute tol.

Files:
- rank.py - k-c oracle, 0 mismatches
- frobenius.py - energy identity, 0 exact / 125348 intdiv fail
- mutation.py - 5 mutants killed: ignore 77819, preimage 77819, c 129387, k-c-1 166475, first 125348
- manifest.json - local registry
- README.md - this file

Evidence: [V] finite exhaustive, oracle-level mutation tested
Witness requirement: non_injective_f + unreached_block + non_singleton_block
Injective f blinds ignore_isolated and preimage mutants (0 kills on injective).

Run:
python3 rank.py
python3 frobenius.py
python3 mutation.py
