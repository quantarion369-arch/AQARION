# Finite Pullback Rigidity and Join Stability

## 1. Definitions

Let X be a set and let T : X -> X be a function. For a binary
relation E on X, define its pullback by

    T^{-1}(E) = {(x,y) in X x X : T(x) E T(y)}.

The relation E is pullback-stable when

    T^{-1}(E) subseteq E.

Equivalently,

    T(x) E T(y) implies x E y.

For equivalence relations E and F, write E join F for the smallest
equivalence relation containing E union F.

## 2. Finite pullback rigidity

### Theorem

Suppose X is finite, E is an equivalence relation on X, and

    T^{-1}(E) subseteq E.

Then

    T^{-1}(E) = E.

In particular, T induces a permutation on the finite quotient X/E.

### Proof

Let C = X/E be the set of E-equivalence classes, and let m = |C|.

For each E-class A, define

    S_A = { [T(x)]_E : x in A }.

Each S_A is nonempty because A is nonempty.

Suppose A and B are distinct E-classes. If a class belonged to both
S_A and S_B, there would be x in A and y in B with

    T(x) E T(y).

Pullback stability would imply x E y, contradicting A != B.
Therefore the sets S_A, as A ranges over C, are pairwise disjoint.

There are m nonempty, pairwise disjoint subsets S_A of a set with
m elements. Consequently every S_A is a singleton and their union
is all of C.

Thus T sends every E-class into one E-class, and the induced map

    T_bar : X/E -> X/E

is a surjection. Since X/E is finite, T_bar is a permutation.

If x E y, then [x]_E = [y]_E. Applying T_bar gives
[T(x)]_E = [T(y)]_E, so T(x) E T(y). Hence

    E subseteq T^{-1}(E).

Combining this with the assumed inclusion yields

    T^{-1}(E) = E.

QED.

## 3. Finite join stability

### Theorem

Suppose X is finite, T : X -> X, and E,F are equivalence relations
on X. If

    T^{-1}(E) subseteq E
    T^{-1}(F) subseteq F,

then

    T^{-1}(E join F) = E join F.

### Proof

By finite pullback rigidity,

    T^{-1}(E) = E
    T^{-1}(F) = F.

Therefore T induces permutations sigma_E on X/E and sigma_F on X/F.

Construct a bipartite incidence graph. Its left vertices are the
E-classes, its right vertices are the F-classes, and each x in X
contributes an edge joining [x]_E to [x]_F. Multiple elements may
contribute the same endpoint pair; regard the edge set as the set
of realized endpoint pairs.

The pair of quotient permutations sends each realized edge

    ([x]_E, [x]_F)

to

    ([T(x)]_E, [T(x)]_F).

This endpoint-pair action is injective on the full Cartesian product
(X/E) x (X/F), since both quotient maps are permutations. It maps
the finite realized edge set into itself. An injective map from a
finite set to itself is surjective, so the action permutes the
realized edges and is an automorphism of the incidence graph.

Two elements x,y belong to the same E join F class exactly when
their corresponding edges lie in the same connected component.
Graph automorphisms preserve connected components. Therefore

    x (E join F) y
        iff
    T(x) (E join F) T(y).

This proves

    T^{-1}(E join F) = E join F.

QED.

## 4. Why the argument is not circular

The proof does not assume join stability. It derives it from:

1. the finite pullback-rigidity theorem applied separately to E and F;
2. the resulting permutations on the two quotient sets;
3. the induced automorphism of the incidence graph;
4. preservation of graph connected components.

## 5. Infinite-set boundary

The unrestricted infinite-set analogue of the rigidity statement
fails.

Let X = N and T(n) = n+1. Let E identify 0 with 2 and otherwise
have singleton classes. Let F identify 0 with 3 and otherwise have
singleton classes.

For E, if T(x) E T(y), either T(x)=T(y), which implies x=y because
T is injective, or {T(x),T(y)}={0,2}. The latter is impossible
because T never takes the value 0. Thus T^{-1}(E) is equality and
is contained in E. The same reasoning applies to F.

But E join F has a class containing 0, 2, and 3. Since
T(1)=2 and T(2)=3, their images are related by E join F, whereas
1 and 2 are not related by E join F. Thus

    T^{-1}(E join F) subseteq E join F

fails.

This counterexample concerns the unrestricted infinite setting; it
does not refute the finite theorem.

## 6. Evidence boundary

The proofs above are mathematical proof text. They do not establish
that the Lean source compiles or that the repository audit script has
run successfully.

A finite enumeration can detect counterexamples among its enumerated
inputs, but cannot replace the proof for all finite sets.

The Lean status remains OPEN until the relevant theorem statements
and proofs compile in the declared Lean/mathlib environment.
