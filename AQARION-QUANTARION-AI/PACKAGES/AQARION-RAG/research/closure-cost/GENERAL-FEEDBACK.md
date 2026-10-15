# General nested-alphabet and feedback characterization

Status: paper-level proof; locally checked on every attained case in the
closure-cost equality replay (seeds 0 and 1). Not Lean-formalized.

This theorem proves that upper equality implies the stated structural
conclusions. It does not claim that nested alphabets and common-coordinate
feedback alone, without the full-product and cardinality hypotheses, imply
upper equality.

## Setting

Let T:X->X be a finite map, pi a partition into k nonempty blocks with
indicators e_b, Kf=f composed with T, and

  W_j = span{e_b∘T^i : b<k, i<=j},
  delta_j = dim W_j - dim W_(j-1) for j>=1.

Since W_(j-1) is contained in W_j, every delta_j is nonnegative. Let d be
the least index with delta_d = 0. Then

  delta_j >= 1 for every 1<=j<d,

and delta_j = 0 for every j>=d.

Let P_j be the partition of X according to the first j+1 itinerary letters
(w_0,...,w_j). By the stabilization lemma in THEOREM.md, P_infinity equals
P_(d-1). Let s be the number of blocks of P_infinity; equivalently, s is
the number of distinct length-d itinerary prefixes

  (w_0,...,w_(d-1)).

## Theorem

Assume upper equality:

  s - k = k( prod_(j=1)^(d-1) (1+delta_j) - 1 ).

Then:

1. The length-d itinerary-prefix set is a full product

     A_0 x A_1 x ... x A_(d-1),

   with |A_0|=k and |A_j|=1+delta_j.

2. The alphabets are nested:

     A_0 >= A_1 >= ... >= A_(d-1).

3. There exist a coordinate i < d and a map

     psi:A_i -> A_d

   with A_d contained in A_(d-1), such that

     x_d = psi(x_i)

   for every itinerary, where x_j denotes the j-th itinerary letter.

## Proof

### 1. Maximal splitting

By the stage-wise refinement inequality in THEOREM.md, each block B of
P_(j-1) has at most 1+delta_j children in P_j. By the upper-equality
criterion in THEOREM.md, upper equality forces equality at every stage:

every block B of P_(j-1) has exactly 1+delta_j children in P_j.

Fix such a block B and let m_B = 1+delta_j be its number of children.
Define the children of B to be the nonempty sets

  B ∩ {x : w_j = a},

where w_j is the coordinate-j itinerary letter.

Let

  V_j = span{e_b∘T^j : b<k}

and

  Q_j = (W_(j-1)+V_j)/W_(j-1).

Every function in W_(j-1) is measurable with respect to P_(j-1), hence is
constant on B. Therefore restriction to B, followed by quotienting by the
constants on B, gives a well-defined linear map

  rho_B : Q_j -> {child-constant functions on B}/constants.

The kernel of rho_B consists of classes represented by functions whose
restriction to B is constant. The restrictions to B of the indicators
e_b∘T^j are exactly the child indicators of B. Modulo constants, these
span the full quotient of child-constant functions on B by constants.
Hence rho_B is surjective.

The domain Q_j has dimension delta_j. The target has dimension m_B-1 =
delta_j. Since rho_B is surjective and the two dimensions agree, rho_B is
an isomorphism.

### 2. Uniform alphabets

For a block B of P_(j-1), let A_j(B) be the set of letters occurring at
coordinate j among the children of B.

Suppose b is missing from A_j(B). Then

  rho_B([e_b∘T^j]) = 0.

Since rho_B is injective,

  e_b∘T^j ∈ W_(j-1).

Hence e_b∘T^j is constant on every block B' of P_(j-1).

Fix such a block B'. By maximal splitting, B' has 1+delta_j >= 2 children,
so the coordinate-j letters are not all equal on B'. If e_b∘T^j were
constantly 1 on B', then every point of B' would have coordinate-j letter
b, contradicting the existence of at least two distinct coordinate-j
letters. Therefore e_b∘T^j is constantly 0 on B'.

Since B' was arbitrary, e_b∘T^j is identically zero on X. Thus b does not
occur at coordinate j in any block. Therefore A_j(B) is the same set A_j
for every block B of P_(j-1).

By induction over j, the length-d itinerary-prefix set is

  A_0 x A_1 x ... x A_(d-1),

with |A_0|=k and |A_j|=1+delta_j.

### 3. Nested alphabets

Let 1<=j<=d-1 and let a∈A_j. Choose a realized length-d itinerary word

  w = (w_0,...,w_(d-1))

with w_j = a, and let x be a point realizing w.

The itinerary of Tx is the one-step shift of the itinerary of x.
Therefore the length-(d-1) word

  (w_1,...,w_(d-1))

is realized by Tx. Its coordinate-(j-1) letter is w_j = a. Hence

  a ∈ A_(j-1).

Since a∈A_j was arbitrary,

  A_j ⊆ A_(j-1)

for every 1<=j<=d-1. Thus the alphabets are nested.

### 4. Additive output indicators

Because delta_d=0, W_d=W_(d-1). For each b, the indicator

  [w_d=b] = e_b∘T^d

lies in W_d, hence in W_(d-1).

The space W_(d-1) is spanned by the coordinate indicators

  [w_i=a],  i<d,  a∈A_i.

Therefore, restricted to the full product

  A_0 x ... x A_(d-1),

every [w_d=b] can be written as

  c + sum_(i=0)^(d-1) h_i(w_i),

where c is a constant and each h_i is a real-valued function on A_i.

### 5. Rectangle lemma

Let f be a Boolean-valued additive function on the full product. Suppose
f depends nonconstantly on two distinct coordinates i and i'.

Choose a base word w and changes of the two coordinates giving nonzero
differences

  p = f(w with w_i changed) - f(w),
  q = f(w with w_i' changed) - f(w).

Because the prefix set is a full product, all four words obtained by
changing neither, either, or both of these coordinates are realized.
Hence the four values

  v, v+p, v+q, v+p+q

all lie in {0,1}, where v=f(w).

Thus p, q, and p+q each lie in {-1,0,1}. Since p and q are nonzero,

  p,q ∈ {+1,-1}.

If p=q, then the four values include v and v+2p. No v∈{0,1} allows
v+2p∈{0,1} for nonzero p. Contradiction.

If p=-q, then the four values include v+p and v-p. No v∈{0,1} allows
both v+p and v-p to lie in {0,1} for nonzero p. Contradiction.

Therefore no Boolean-valued additive function depends nonconstantly on two
distinct coordinates. Each nonconstant output indicator depends on at most
one coordinate.

### 6. Common coordinate

Let A_d be the set of letters occurring at coordinate d. By nestedness,

  A_d ⊆ A_(d-1).

Suppose two distinct nonconstant output indicators

  [w_d=b],  [w_d=b']

depend on distinct coordinates i and i'. Let S_b⊆A_i be the support of
[w_d=b] as a function of w_i, and let S_b'⊆A_i' be the corresponding
support for [w_d=b'].

Because both indicators are nonconstant, both supports are nonempty proper
subsets. Because the prefix set is a full product, choose

  a∈S_b,  a'∈S_b'

independently and complete them to a realized word. On that word, both

  [w_d=b]=1  and  [w_d=b']=1,

which is impossible because the final letter w_d has exactly one value.

Therefore all nonconstant output indicators depend on the same coordinate
i.

Define psi:A_i->A_d by

  psi(a)=b  iff  [w_d=b]=1 on the set of words with w_i=a.

This is well-defined because the indicators [w_d=b] sum pointwise to 1:
for every realized word, exactly one final-letter indicator equals 1. If
every indicator is constant, then w_d is constant; take psi to be that
constant map.

In both cases,

  x_d=psi(x_i),

with psi valued in A_d⊆A_(d-1).

## Relation to the binary theorem

The binary all-ones-profile characterization in THEOREM.md is the special
case k=2 and delta_1=...=delta_(d-1)=1. There the feedback map is
necessarily constant, a coordinate, or a complemented coordinate.

The present theorem is the general all-k, all-profile version of the same
structural consequence of upper equality.

## Evidence

The closure-cost equality checker asserted nestedness and common-coordinate
feedback on every attained case in its exhaustive n<=5 sweep, random n in
{8,9} sampling, and constructed systems, across seeds 0 and 1. This is
computational corroboration, not a formal certificate.
