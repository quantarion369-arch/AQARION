# Project 2: formal Lean status (pointer)

The Lean formalization of parts of the Project 2 proof draft lives in a separate repository so that its build and axiom gates stay independent of this research record.

- Repository: https://github.com/quantarion369-arch/AQARION-LEAN
- Checked commit: 1f5f98be8ac0b058aa0419e5d66044a686933452
- Folder: P2-SEMIGROUP (REPORT.md = current status, REPLAY.md = how to rebuild and compare)

## Formally checked (see REPORT.md for exact axioms and CI gates)

- The integer lattice points of the cone defined by the ten facet inequalities are exactly the sums of the ten generators.
- The ten facet forms are irredundant; the interior point (1,1,1,1,1) satisfies all ten strictly; the generators A and E0-E3 span Z^5.
- The semigroup of generated degrees equals the cone intersected with Z^5, and the interior integer points are (1,1,1,1,1) plus the semigroup.
- The real cone equals the nonnegative real span of the ten generators, and its topological interior is the set where all ten forms are strictly positive.
- Unit-pivot elimination to a partial identity gives the same rank over every field.

## Not formalized

The endpoint presentation (Lemma 2), the kernel-generation claims, the binding of the nine saved component certificates to the rank lemma, Hochster's theorem, Danilov-Stanley, canonical-module duality and the final resolution.

## Scope

This note records build and proof-check status of the listed Lean statements only. The draft's theorem status remains DRAFT_REQUIRING_REVIEW, no governance gate in this repository changes, and no independent external review has taken place.
