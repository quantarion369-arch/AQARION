# General nested-alphabet and feedback characterization

Status: paper-level proof; locally checked on every attained case in the
closure-cost equality replay (seeds 0 and 1). Not Lean-formalized.

## Setting

Let T:X->X be a finite map, pi a partition into k nonempty blocks with
indicators e_b, Kf=f∘T, and

  W_j = span{e_b∘T^i : b<k, i<=j},
  delta_j = dim W_j - dim W_(j-1).

Let the positive profile be delta_1,...,delta_(d-1), with delta_d=0.
Let s be the number of itinerary classes, and let P_j be the partition by
the first j+1 itinerary letters.

## Theorem

Assume upper equality:

  s - k = k( prod_{j=1}^{d-1}(1+delta_j) - 1 ).

Then:

1. The length-d itinerary-prefix set is a full product

     A_0 x A_1 x ... x A_(d-1),

   with |A_0|=k and |A_j|=1+delta_j.

2. The alphabets are nested:

     A_0 >= A_1 >= ... >= A_(d-1).

3. There exist a coordinate i < d and a map psi:A_i -> A_(d-1) such that

     x_d = psi(x_i)

   for every itinerary, where x_j denotes the j-th itinerary letter.

## Proof

### 1. Maximal splitting

Upper equality forces every stage inequality to be tight. Hence every block
B of P_(j-1) has exactly 1+delta_j children at every stage 1<=j<=d-1.

For each B, let m_B be its number of children. Restriction to B induces a
surjection

  rho_B : (W_(j-1)+span{e_b∘T^j})/W_(j-1) -> r_B(span{e_b∘T^j})/constants.

The source has dimension delta_j and the target has dimension m_B-1. Since
m_B=1+delta_j, both dimensions equal delta_j, so rho_B is an isomorphism.

### 2. Uniform alphabets

Suppose letter b is missing from block B at coordinate j. Then
r_B(e_b∘T^j)=0. By injectivity of rho_B, e_b∘T^j lies in W_(j-1), hence is
constant on every block B' of P_(j-1).

Every B' has 1+delta_j >= 2 letters at coordinate j, so e_b∘T^j cannot be
constantly 1 on B'. Being constant, it is 0 on B'. Thus b appears in no
block. Therefore the set A_j of letters occurring at coordinate j is the same
for every block of P_(j-1).

By induction, the length-d prefix set is

  A_0 x A_1 x ... x A_(d-1),

with |A_0|=k and |A_j|=1+delta_j.

### 3. Nested alphabets

The itinerary of Tx is the shift of the itinerary of x. Hence if
(w_0,...,w_d) is an itinerary prefix, then (w_1,...,w_d) is also a prefix.
Therefore w_j lies in A_(j-1) for 1<=j<=d-1, and w_d lies in A_(d-1).
This gives A_j <= A_(j-1).

### 4. Additive output indicators

Since delta_d=0, each indicator [w_d=b] lies in

  W_(d-1) = span{1, [w_i=a] : i<d, a in A_i}.

Thus on the product set, each [w_d=b] is an additive function

  c + sum_i h_i(w_i).

### 5. Rectangle lemma

Suppose a Boolean-valued additive function depends nonconstantly on two
coordinates i and i'. Choose values where its coordinate differences are p
and q, both nonzero. The four rectangle values

  v, v+p, v+q, v+p+q

must all lie in {0,1}. Hence p,q in {+1,-1}. If p=q, then v+2p is outside
{0,1}. If p=-q, then v+p and v-q are both 1-v, forcing p=0. Contradiction.

Therefore each nonconstant output indicator depends on at most one coordinate.

### 6. Common coordinate

Suppose [w_d=b] depends nonconstantly on coordinate i, and [w_d=b'] depends
nonconstantly on a different coordinate i'. Then b≠b', since one Boolean
function cannot depend nonconstantly on two coordinates.

Let S_b be the set of A_i-values where [w_d=b]=1, and S_b' the corresponding
set for b'. Both are nonempty proper subsets. Because the prefix set is a
full product, choose w_i in S_b and w_i' in S_b' independently. The resulting
word has both indicators equal to 1, but w_d has only one value.
Contradiction.

Hence all nonconstant output indicators share one coordinate i. Define

  psi(a)=b  iff  a lies in the support of [w_d=b].

If every indicator is constant, then w_d is constant; take psi to be that
constant map. In both cases, x_d=psi(x_i), with psi valued in A_(d-1).

## Relation to the binary theorem

The binary all-ones-profile characterization in THEOREM.md is the special case
k=2 and delta_1=...=delta_(d-1)=1. There the feedback map is necessarily
constant, a coordinate, or a complemented coordinate.

The present theorem is the general all-k, all-profile version of the same
structural consequence.

## Evidence

The closure-cost equality checker asserted nestedness and common-coordinate
feedback on every attained case in its exhaustive n<=5 sweep, random n in
{8,9} sampling, and constructed systems, across seeds 0 and 1. This is
computational corroboration, not a formal certificate.
