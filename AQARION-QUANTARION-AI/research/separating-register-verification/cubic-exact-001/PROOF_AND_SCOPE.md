# AQARION: exact cubic certificates and support-bound consequences

## Scope

This package independently reconstructs the three supplied eight-state
examples with binary observation 00001111.

It computes exact ranks over the rationals using Python's standard-library
Fraction type. It verifies a quadratic annihilator and a cubic witness.

It does not import verify10.py, use floating-point rank, repeat the full
census, or certify all 4,608 reported exceptional maps.

## Definitions

For a finite set Y of distinct binary vectors, V_d is the vector space
of functions on Y obtained by evaluating multilinear polynomials of
total degree at most d, including constants.

Repeated temporal columns do not introduce new variables in the support:
the feature matrix still evaluates the specified temporal coordinates.
The code uses squarefree monomials because binary coordinates satisfy x^2=x.

## Small-support theorem

If V_d is not the full function space Q^Y, then |Y| >= 2^(d+1).

Proof:

Failure of full row rank produces a nonzero rational vector w indexed
by Y that annihilates every monomial of degree at most d.

We prove that its nonzero support has size at least 2^(d+1).

For d=0, annihilation of the constant means sum(w)=0. A nonzero vector
with this property needs at least two nonzero entries.

For d>=1, there are at least two distinct support points. Choose a binary
coordinate i on which two such points differ. Both coordinate slices
contain a nonzero weight.

On slice i=1, the restricted weights annihilate every monomial M in the
remaining coordinates of degree at most d-1, because the slice moment
is the global moment of x_i M.

On slice i=0, the same follows from the global moment of (1-x_i)M.

Both expressions have degree at most d. By induction, each nonzero slice
has at least 2^d support points. The slices are disjoint, giving at least
2^(d+1) support points. This proves the theorem.

## Consequences

1. For m=|Y|<=7, V_2 is full.
2. For m<=8, V_3 is full.
3. For m=8, if V_2 is deficient, its rank is exactly seven.

For statement 3, two independent quadratic annihilators could be
combined to cancel at a selected coordinate while remaining nonzero.
The resulting annihilator would have support at most seven, contradicting
the degree-two support bound.

Therefore an n=8 binary itinerary census restricted to m<8 cannot find
a genuine cubic obstruction. Such a run could test implementation behavior,
but the mathematical outcome is already forced.

## Exact witness meaning

The checker orders itinerary words increasingly.

For each example it finds the primitive left-null vector

    (1,-1,-1,1,-1,1,1,-1).

Every constant, linear, and quadratic feature has weighted sum zero.

A cubic feature has a nonzero weighted sum. This certifies that quadratic
features miss a direction detected by a cubic.

The exact rank profile is [1,4,7,8] for all three fixtures.

## Injectivity terminology

The original census filter m=n means that the observation itineraries
separate the states. It does not mean that T is injective.

Each of these three transition maps has image size four.

## Anchor rigidity is a separate completed argument

Let E be an equivalence relation with finite quotient and let P=T^*E.
Assume P is contained in E.

The map X/P -> X/E taking [x]_P to [Tx]_E is well-defined and injective.

The refinement P contained in E also gives a surjection X/P -> X/E
taking [x]_P to [x]_E.

The injection makes X/P finite with at most |X/E| elements. The surjection
gives at least |X/E| elements. Thus the finite cardinalities agree.

The refinement surjection is therefore injective, so P=E.

Only after this equality is established do we define the well-defined
quotient self-map [x]_E -> [Tx]_E. It is injective and therefore bijective.

This proof requires finite X/E, not finite X. No further finite census
is needed to prove the statement.

## Remaining computational obligation

The global count of 4,608 exceptional maps remains a reported
floating-rank census count unless separately certified.

The supplied vectorized runner retains at most 40 non-full examples.
That log is not a complete list of the 4,608 candidates.

Exact checking of the three fixtures does not certify all candidates.
Certifying all exceptional candidates also does not, by itself, certify
the absence of missed exceptions among reported full-rank cases.

## Preservation boundary

The files in this directory are created by the inline Termux block.

They are a new independent checker and its results, not replacements
for the original research scripts or their execution records.

No Git staging, commit, push, registry change, or promotion is performed.
