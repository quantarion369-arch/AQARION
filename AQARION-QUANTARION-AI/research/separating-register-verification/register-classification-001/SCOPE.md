# AQARION register-classification verification

## Observation and indexing

The q-ary states are lexicographically ordered coordinate tuples.
Their integer labels use base q.

The fixed balanced observation is:

    h(x) = x // q^(d-1)

Thus the eight-state binary observation is 00001111.

## Checks performed

1. Every binary path/sign/terminal register description through d=5.
2. Separation by the first d observations.
3. Full image-cardinality sequence:

       |T^t(X)| = q^max(d-t,L)

4. Periodic-core size q^L.
5. Core permutation order.
6. Exact rational cube interpolation profiles.
7. Observation-preserving encodings for four small labeled cases.
8. Recovery of each encoding from its own constructed map.
9. No duplicate maps among canonical encoding/terminal pairs.
10. Exact exhaustive comparison with all maps at n=2 and n=4.

## Canonical representation

The canonical map is:

    S(u1,...,ud) = (u2,...,ud,g(u))

where g is either a permuted single coordinate or a constant.

For a fixed balanced observation, the predicted represented count is:

    ((q^(d-1))!)^q * (d*q! + q)

For each positive-dimensional periodic core, the count is:

    ((q^(d-1))!)^q * q!

For a one-state core, the count is:

    ((q^(d-1))!)^q * q

## Expected labeled counts

q=2,d=1: 4
q=2,d=2: 24
q=2,d=3: 4608
q=3,d=2: 3240

The binary eight-state core histogram is:

    1: 1152
    2: 1152
    4: 1152
    8: 1152

The ternary nine-state core histogram is:

    1: 648
    3: 1296
    9: 1296

## Saved map lists

Each labeled_q*_d*.jsonl contains every represented labeled map
for that case, its image-size sequence, periodic-core size,
and core permutation order.

No candidate list is truncated to the first 40 examples.

## Boundaries

The script does not enumerate every map on eight or nine states.

It does not machine-prove the external spectral equality theorem.

It computes exact cube feature ranks. It does not independently
rank every large labeled-map temporal feature matrix.

It does not recover missing original research scripts.

It does not run Lean, change a Git repository, enroll a claim,
or authorize promotion.

All files belong to this separate verification run.
