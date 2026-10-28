# Temporal circuits: research evidence 001

## Status

Research evidence and written proof notes.
Not a formal proof certificate, novelty clearance, or submission.

This directory preserves two completed local experiment runs.
Preparation copied and verified their bytes; it did not rerun them.

## Contents

- family/: original two-fixed-points/one-hot-cycle experiment.
- five-point-classification/: original exact overlap/circuit classifier.
- PERSISTENCE_NOTES.md: subsequent written mathematical refinements.
- PUBLICATION_MANIFEST.json: source identities, hashes, and scope.
- SHA256SUMS: checksums for this prepared research subtree.

## Archived experiment scopes

The family run reports 19 cases for cycle lengths 2 through 20,
741 horizon-degree checks, 247 deletion checks, 15 Fraction
cross-checks, 38 negative controls, and zero reported failures.

The classifier examines all 4,368 five-point supports in the ordered
four-bit cube over Q. It finds 160 affine circuits and exactly two
deterministically realizable circuit supports:

    [0,2,4,9,15]
    [0,6,11,13,15]

Each has one deterministic realization, which is a permutation.

The classifier also checks overlap-count formulas on 273 small
supports and resimulates 982 deterministic realizations.

## Evidence boundaries

The copied scripts and results establish their implemented finite
scopes. They do not classify all temporal circuits.

The persistence notes contain written arguments developed after
these runs. The archived runs must not be described as having
tested every theorem in those notes.

In particular:
- Four compatible deterministic maps and one persistent map applies
  to the one-hot family only for m>=3.
- At m=2 there are sixteen compatible deterministic maps and six
  persistent ones.
- Circuit persistence concerns the affine dependence.
  Quadratic reconstruction is already complete in this family.
- Growing primitive obstruction coefficients do not establish
  unavoidable growth of decoder coefficients.
- Static coordinate symmetries need not preserve temporal overlap.

The existing temporal-interpolation manuscript is unchanged.

## Attribution and review

Weighted null designs and their trace/support arguments are
established literature, including Frankl-Pach, European Journal of
Combinatorics 4(1), 21-23 (1983).

Word-overlap constructions and cycle covers are established
combinatorial machinery. No originality claim is certified here.

Independent mathematical review and precise literature comparison
remain separate from successful execution and checksum verification.

## Publication boundary

Only this research subtree is prepared.
No application source, manuscript, production claim registry,
Git index, commit, remote, or submission is changed.
