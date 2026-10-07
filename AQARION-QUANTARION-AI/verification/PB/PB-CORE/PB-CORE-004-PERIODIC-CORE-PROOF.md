AQ-PB-CORE-004 — PERIODIC-CORE CONGRUENCE EQUIVALENCE

Artifact ID: AQ-PB-CORE-004A
Status: "[P]" mathematical proof closed · "[L]" Lean OPEN · "[V]" computational corroboration exists · "C4 BLOCKED"
Scope: finite total maps and pullback-fixed equivalence relations
Dependency: PB-001 / finite pullback rigidity
Purpose: remove transient states from the classification of pullback-fixed equivalence relations.

---

1. Statement

Let X be a finite nonempty set and let

[
T:X\to X
]

be a total map.

Define the periodic core

[
P:=\operatorname{Per}(T)

{x\in X:\exists m\ge 1,\ T^m(x)=x}.
]

Choose h\ge 0 such that

[
T^h(X)=P.
]

Define

[
r:=T^h.
]

Then

[
r(X)=P,
\qquad
r|_P=\operatorname{id}_P,
\qquad
rT=Tr.
]

Let

[
\operatorname{Stab}(T)
:=
{E\in\operatorname{Eq}(X):T^*E=E}.
]

Let

[
\operatorname{Con}(P,T|_P)
:=
{\theta\in\operatorname{Eq}(P):
\forall p,q\in P,\
p\theta q\Longleftrightarrow T(p)\theta T(q)}.
]

Then restriction to the periodic core gives a lattice isomorphism

[
\boxed{
\operatorname{Stab}(T)
\cong
\operatorname{Con}(P,T|_P).
}
]

The inverse map is

[
\boxed{
x,\widehat{\theta},y
\iff
r(x),\theta,r(y).
}
]

---

2. Preliminary facts

Because X is finite, every orbit eventually enters a cycle.

Therefore there exists h such that

[
T^h(X)=P.
]

For p\in P, p is periodic, hence some iterate of T returns to p. Since T^h(X)=P,

[
r(p)=T^h(p)=p.
]

Thus

[
r|_P=\operatorname{id}_P.
]

Since r=T^h,

[
rT=T^hT=T^{h+1}=TT^h=Tr.
]

Therefore

[
\boxed{rT=Tr.}
]

Finally, T|_P is a permutation because every element of P lies on a finite cycle.

---

3. Extension map

For

[
\theta\in\operatorname{Con}(P,T|_P),
]

define a relation \widehat{\theta} on X by

[
x,\widehat{\theta},y
\iff
r(x),\theta,r(y).
]

We prove that this is a member of \operatorname{Stab}(T).

---

4. \widehat{\theta} is an equivalence relation

Reflexivity

For every x\in X,

[
r(x)\theta r(x)
]

because \theta is reflexive.

Therefore

[
x,\widehat{\theta},x.
]

Symmetry

If

[
x,\widehat{\theta},y,
]

then

[
r(x)\theta r(y).
]

By symmetry of \theta,

[
r(y)\theta r(x).
]

Hence

[
y,\widehat{\theta},x.
]

Transitivity

If

[
x,\widehat{\theta},y
\quad\text{and}\quad
y,\widehat{\theta},z,
]

then

[
r(x)\theta r(y)
]

and

[
r(y)\theta r(z).
]

By transitivity of \theta,

[
r(x)\theta r(z).
]

Hence

[
x,\widehat{\theta},z.
]

Therefore

[
\boxed{\widehat{\theta}\in\operatorname{Eq}(X).}
]

---

5. \widehat{\theta} is pullback-fixed

We prove

[
T^*\widehat{\theta}=\widehat{\theta}.
]

For x,y\in X,

[
Tx,\widehat{\theta},Ty
]

if and only if

[
r(Tx)\theta r(Ty).
]

Using rT=Tr,

[
r(Tx)=T(r(x)),
\qquad
r(Ty)=T(r(y)).
]

Thus

[
Tx,\widehat{\theta},Ty
\iff
T(r(x))\theta T(r(y)).
]

Because \theta is T|_P-invariant,

[
T(r(x))\theta T(r(y))
\iff
r(x)\theta r(y).
]

Therefore

[
Tx,\widehat{\theta},Ty
\iff
x,\widehat{\theta},y.
]

Hence

[
\boxed{
T^*\widehat{\theta}=\widehat{\theta}.
}
]

---

6. Restriction followed by extension

Let

[
p,q\in P.
]

Since r|_P=\operatorname{id}_P,

[
r(p)=p,
\qquad
r(q)=q.
]

Therefore

[
p,\widehat{\theta},q
\iff
r(p)\theta r(q)
\iff
p\theta q.
]

Hence

[
\boxed{
(\widehat{\theta})|_P=\theta.
}
]

---

7. Every pullback-fixed equivalence is recovered from its core restriction

Let

[
E\in\operatorname{Stab}(T).
]

Since

[
T^*E=E,
]

iteration gives

[
(T^h)^*E=E.
]

But r=T^h, so

[
r(x)Er(y)
\iff
xEy.
]

Because r(x),r(y)\in P,

[
r(x)E|_P r(y)
\iff
xEy.
]

By definition of the extension,

[
x,\widehat{E|_P},y
\iff
r(x)E|_P r(y).
]

Therefore

[
\boxed{
\widehat{E|_P}=E.
}
]

---

8. The two maps are inverse

Define

[
R:\operatorname{Stab}(T)\to\operatorname{Con}(P,T|_P)
]

by

[
R(E)=E|_P.
]

Define

[
S:\operatorname{Con}(P,T|_P)\to\operatorname{Stab}(T)
]

by

[
S(\theta)=\widehat{\theta}.
]

Sections 6 and 7 establish

[
R(S(\theta))=\theta
]

and

[
S(R(E))=E.
]

Therefore

[
\boxed{
R^{-1}=S.
}
]

Hence

[
\boxed{
\operatorname{Stab}(T)
\cong
\operatorname{Con}(P,T|_P).
}
]

---

9. Order preservation

If

[
E_1\subseteq E_2,
]

then immediately

[
E_1|_P\subseteq E_2|_P.
]

Conversely, if

[
\theta_1\subseteq\theta_2,
]

then

[
r(x)\theta_1r(y)
\Longrightarrow
r(x)\theta_2r(y),
]

so

[
\widehat{\theta_1}
\subseteq
\widehat{\theta_2}.
]

Thus the bijection is an order isomorphism.

Because equivalence relations form a lattice under inclusion, the order isomorphism preserves the lattice operations.

Therefore

[
\boxed{
\operatorname{Stab}(T)
\cong_{\mathrm{lat}}
\operatorname{Con}(P,T|_P).
}
]

---

10. Independence of the chosen h

The construction does not depend on the particular sufficiently large h.

Suppose

[
T^h(X)=P
]

and k\ge h.

Then

[
T^k=T^{k-h}T^h.
]

Restricted to P, T^{k-h} is a permutation of P.

If \theta is invariant under T|_P, then it is invariant under every positive and negative power of that permutation.

Therefore

[
T^h(x)\theta T^h(y)
\iff
T^k(x)\theta T^k(y).
]

Thus the extension relation is independent of which sufficiently large iterate is used.

---

11. Consequence

All transient states are determined by their eventual images in the periodic core.

They contribute no independent degrees of freedom to a pullback-fixed equivalence relation.

The classification problem therefore reduces exactly to

[
\boxed{
\text{finite map}
\longrightarrow
\text{periodic core}
\longrightarrow
\text{permutation}
\longrightarrow
\text{permutation congruence lattice}.
}
]

---

12. Evidence status

Component| Status
Finite eventual-core existence| "[P]"
r| _P=\mathrm{id}
rT=Tr| "[P]"
Extension is equivalence| "[P]"
Extension is pullback-fixed| "[P]"
Restriction ∘ extension| "[P]"
Extension ∘ restriction| "[P]"
Order/lattice preservation| "[P]"
Full theorem| "[P]"
Lean formalization| "[O]" OPEN
Exhaustive finite corroboration| "[V]" repository-recorded
C4| "BLOCKED"
Publication| "BLOCKED"
Promotion| "FALSE"

This artifact does not claim Lean compilation.

---

13. Literature boundary

The reduction of finite unary dynamics to cyclic/core structure and the study of congruence lattices of monounary algebras are classical.

Relevant literature includes:

- Joel Berman, On the congruence lattices of unary algebras, 1972.
- D. Jakubíková-Studenovská and L. Janičková, Congruence lattices of connected monounary algebras, Algebra Universalis 81 (2020), Article 54.
- C. Ratanaprasert and K. Denecke, Unary operations with long pre-periods, Discrete Mathematics 308 (2008), 4998–5005.

The present theorem should therefore be presented as an AQARION formalization/reduction result, not as a claim that the underlying monounary-algebra structure was discovered here.

---

14. Certification boundary

This artifact is mathematically closed at the paper-proof level.

It is not C4-certified.

The remaining certification obligations are:

1. formal Lean proof;
2. reproducible Lean build;
3. receipt/hash reconciliation;
4. consistency between claim registry and formal source;
5. independent replay where required by the AQARION certification policy.

Current final status: "[P] CLOSED · [L] OPEN · C4 BLOCKED".
