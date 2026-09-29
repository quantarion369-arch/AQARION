# JOIN-STABILITY — Independent Audit
## 2026-09-29

### Scope

Independent reconstruction of:

1. finite pullback stability;
2. ordered stable `(E,F)` pairs;
3. join stability;
4. incidence invariance.

### Enumeration

Every total map

    T : [n] -> [n]

and every equivalence relation on `[n]` was reconstructed for
`n = 1,...,6`.

For each map, every ordered pair of pullback-stable equivalence
relations was tested.

### Results

| n | Ordered stable pairs | Join failures | Incidence failures |
|---:|---:|---:|---:|
| 1 | 1 | 0 | 0 |
| 2 | 10 | 0 | 0 |
| 3 | 117 | 0 | 0 |
| 4 | 1,960 | 0 | 0 |
| 5 | 40,385 | 0 | 0 |
| 6 | 1,016,496 | 0 | 0 |

### Receipt reconciliation

The independently computed number of PB-fixed `(T,E)` objects is:

    n=1: 1
    n=2: 6
    n=3: 51
    n=4: 592
    n=5: 8,565
    n=6: 148,896

The ordered pair count is the sum of squares of these per-map
stable-relation counts.

The unordered pair count with repetition is:

    (ordered_pairs + PB_fixed) / 2

giving:

    1
    8
    84
    1,276
    24,475
    582,696

Thus the two previously reported tables are consistent once
their counting conventions are made explicit.

### Mathematical mechanism tested

For every stable pair:

    T*E = E
    T*F = F

was used to construct the induced class maps.

The induced maps were checked to be permutations.

The incidence set `I` was constructed and the product permutation
`σ` was checked against it.

Observed for every ordered stable pair:

    σ(I) = I

### Status

[P] finite pullback rigidity:
    analytic proof candidate, formalization open.

[P] finite join theorem:
    incidence-permutation proof candidate, formalization open.

[V] exhaustive n<=6:
    independently reproduced.

[PV] combined:
    DO NOT promote globally until the proof is formally audited.

Lean:
    OPEN

C4:
    BLOCKED

Publication:
    BLOCKED
