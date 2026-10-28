# Finite persistence certificates and structural consequences

Status: written mathematical arguments for independent review.
No general proof is machine-formalized by this preparation.

## Conventions

X is a nonempty finite set of N states.
T:X->X is deterministic; h is scalar-valued over Q.
Write a_t=h composed with T^t and W_L=span_Q(1,a_0,...,a_(L-1)).
An affine circuit means a minimal dependence among the rows of
the constant-plus-observation evaluation matrix.
Its dependence vector has no zero entries.

## 1. General residual certificate

For any vector v, s_t=v^T*a_t.
Cayley-Hamilton on the N-dimensional pullback operator shows
that s_0,...,s_(N-1) all zero iff every residual is zero.

If v^T*1=0, pass to the quotient by the constant function.
Its dimension is N-1, so s_0,...,s_(N-2) suffice when N>=2.

These statements concern appended scalar observations, not
automatically every newly introduced nonlinear temporal product.

## 2. One-step certificate for a consecutive temporal circuit

Suppose M_L=[1,a_0,...,a_(L-1)] has rank N-1 and its rows form a circuit.
Its column space is ker(v^T).

If v^T*a_L=0, then W_(L+1)=W_L.
Composition sends each generator of W_L back into W_L, so W_L is
invariant and all later observations belong to it.

If v^T*a_L is nonzero, the augmented matrix has rank N.
This is full ROW rank; full column rank is not the general conclusion.

Thus one new residual decides infinite affine persistence in this
consecutive-window setting.

## 3. Fiber-sum certificate

For a persistent temporal affine circuit define

    (T_*v)(y)=sum(v(x): T(x)=y).

The temporal function space is invariant under pullback.
Its one-dimensional annihilator is consequently invariant under T_*,
so T_*v=lambda*v for some scalar lambda.

Conversely, this identity together with v^T*h=0 gives
v^T*a_t=lambda^t*v^T*h=0 for every t.

This equivalence is stated for a temporal affine circuit.
Persistence of added observations alone does not make an arbitrary
old feature space invariant.

## 4. No nonbijective persistent binary circuits with N>4

Assume h is binary, the system is observable, and the complete
temporal affine configuration is a circuit on N>4 states.

If T is not surjective, some state has no preimage.
Since v has full support, T_*v=lambda*v forces lambda=0.

Every nonempty transition fiber then has weight sum zero.
No such fiber is a singleton.

No fiber has three states: two would have the same binary output
and successor, making their entire histories identical.
Therefore every nonempty fiber has size exactly two.

Orient each pair so its first state has output one and its second
has output zero. Their evaluation-row difference is always
(0,1,0,0,...), because all outputs after time zero agree.

Two distinct pairs therefore give a dependence on four states.
For N>4 this is a proper dependent subset, contradicting the circuit.
Hence T is bijective.

The N=4 boundary is genuine:
T=[0,2,0,2], h=[0,0,1,1], v=[1,-1,-1,1].
The two-prefix is bijective, affine rank is three, and T_*v=0.

## 5. One-hot family

For m>=3 the four deterministic overlap-compatible maps have
next residual

    s_m=(m-1)*a+1-b,  a,b in {0,1}.

The values for (a,b)=(0,0),(0,1),(1,0),(1,1) are
1,0,m,m-1. Only (0,1) preserves the circuit.

The one-step theorem already certifies persistence forever.
A second new residual is unnecessary.

At m=2 there are sixteen maps, not four.
Six preserve the affine circuit: four nonbijective maps and
two permutations. The other ten destroy it.

The primitive circuit relation is (m-1,1,-1,...,-1).
Nevertheless the zero-state indicator has the degree-two expression

    1-sum(g_i)+sum(g_0*g_i : i=1,...,m-1),

with coefficients only 0,1,-1.

## 6. Higher nullity

For consecutive scalar observations, if r=dim W_infinity, then

    dim W_L=min(L+1,r).

The surviving left-kernel dimension is N-min(L+1,r).
There is no pause followed by later rank growth.

For an arbitrary initial feature space F, the intersection formula
for surviving kernels is still valid, but pauses can occur before
later growth. For a four-cycle with one-hot observation, starting
from F=span(1,a_1) and appending a_0,a_1,a_2 gives ranks 2,3,3,4.

## Review boundary

These are written proofs, not independent referee approval.
The two archived experiment runs retain their original finite scopes.
No broader classification or novelty is certified.
