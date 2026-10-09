AQ-PB-CORE-004 — Periodic-Core Congruence Equivalence

Artifact ID: AQ-PB-CORE-004A
Scope: Finite nonempty sets, total maps, and pullback-fixed equivalence relations
Mathematical status: Paper proof, corrected retraction lemma
Lean: OPEN — compilation not claimed
Independent computational evidence: Bounded reports require separate authentication and replay
C4: BLOCKED
Publication: BLOCKED
Promotion: FALSE

---

1. Definitions and theorem

Let (X) be a finite nonempty set and (T:X\to X) a total map. Define the periodic core

[
P=\operatorname{Per}(T)
={x\in X:\exists m\ge1,\ T^m(x)=x}.
]

An equivalence relation (E) on (X) is pullback-fixed if

[
\forall x,y\in X,\qquad
E(x,y)\iff E(Tx,Ty).
]

Write (\operatorname{Stab}(T)) for the set of pullback-fixed equivalence relations on (X). Write (\operatorname{Con}(P,T|_P)) for the equivalence relations (\theta) on (P) satisfying

[
\forall p,q\in P,\qquad
\theta(p,q)\iff\theta(Tp,Tq).
]

Theorem (PB-CORE-004). Restriction to the periodic core is an order isomorphism

[
\operatorname{res}:\operatorname{Stab}(T)
\longrightarrow \operatorname{Con}(P,T|_P),
\qquad E\longmapsto E|_P.
]

Its inverse maps (\theta) to the relation (\widehat{\theta}) defined by

[
\widehat{\theta}(x,y)
\iff \theta(r(x),r(y)),
]

where (r) is the periodic retraction constructed below. Consequently, restriction and extension are inverse order isomorphisms and preserve the induced lattice operations.

2. Correct construction of the periodic retraction

Because (X) is finite, every orbit eventually reaches a cycle. Hence there exists (h_0\ge0) such that

[
T^{h_0}(X)=P.
]

Choose a positive integer (L) such that:

1. (L\ge h_0);
2. every cycle length of (T) divides (L).

Such an (L) exists because there are finitely many cycles: take a common multiple of their lengths and, if necessary, multiply it by a sufficiently large positive integer to ensure (L\ge h_0).

Define (r=T^L). Then

[
\boxed{r(X)=P,\qquad r|_P=\operatorname{id}_P,\qquad rT=Tr.}
]

Proof. Since (L\ge h_0), every point in (T^L(X)) lies on a cycle. Thus (T^L(X)\subseteq P). Since (T|_P) is a permutation, (T^L(P)=P), so (P\subseteq T^L(X)). Hence (r(X)=P).

For each (p\in P), its cycle length divides (L). Therefore (T^L(p)=p), proving (r|_P=\operatorname{id}_P).

Finally, iterates of the same map commute:

[
rT=T^LT=T^{L+1}=TT^L=Tr.
]

This proves the three retraction identities. (\square)

Correction note. The weaker condition (T^h(X)=P) does not imply (T^h|_P=\operatorname{id}_P). For a two-cycle (T(a)=b,\ T(b)=a), one has (P=X) and (T(X)=P), but (T|_P\ne\operatorname{id}_P). The common-multiple condition on (L) is essential for the pointwise identity.

3. Restriction maps pullback-fixed relations to core congruences

Let (E\in\operatorname{Stab}(T)). Restricting its defining biconditional to (p,q\in P) gives

[
E(p,q)\iff E(Tp,Tq).
]

Thus (E|_P\in\operatorname{Con}(P,T|_P)), so restriction is well-defined.

Moreover, iteration of pullback-fixedness gives, for every (j\ge0),

[
E(x,y)\iff E(T^jx,T^jy).
]

Taking (j=L) yields

[
\boxed{E(x,y)\iff E(r(x),r(y).}
]

Equivalently, with the closing delimiter written explicitly,

[
\boxed{E(x,y)\iff E(r(x),r(y)).}
]

This identity is the key to the inverse construction.

4. Extension maps core congruences to pullback-fixed relations

Let (\theta\in\operatorname{Con}(P,T|_P)). Define

[
\widehat{\theta}(x,y)
\iff\theta(r(x),r(y)).
]

Because (r(x),r(y)\in P) and (\theta) is an equivalence relation, reflexivity, symmetry, and transitivity of (\widehat{\theta}) follow from those of (\theta). Thus (\widehat{\theta}) is an equivalence relation on (X).

For all (x,y\in X), using (rT=Tr),

[
\begin{aligned}
\widehat{\theta}(Tx,Ty)
&\iff\theta(r(Tx),r(Ty))\
&\iff\theta(T(r(x)),T(r(y)))\
&\iff\theta(r(x),r(y))\
&\iff\widehat{\theta}(x,y).
\end{aligned}
]

The third equivalence is the defining biconditional invariance of (\theta) on the core. Therefore (\widehat{\theta}\in\operatorname{Stab}(T)).

5. Restriction and extension are inverse

5.1 Restriction after extension

For (p,q\in P), the retraction law gives (r(p)=p) and (r(q)=q). Hence

[
\widehat{\theta}(p,q)
\iff\theta(r(p),r(q))
\iff\theta(p,q).
]

Therefore

[
\boxed{\operatorname{res}(\widehat{\theta})=\theta.}
]

5.2 Extension after restriction

Let (E\in\operatorname{Stab}(T)). Section 3 gives

[
E(x,y)\iff E(r(x),r(y)).
]

Since (r(x),r(y)\in P), this is equivalent to

[
(E|_P)(r(x),r(y)),
]

which by definition is (\widehat{E|_P}(x,y)). Consequently,

[
\boxed{\widehat{E|_P}=E.}
]

Thus restriction and extension are mutually inverse bijections.

6. Order and lattice structure

If (E_1\subseteq E_2), then (E_1|_P\subseteq E_2|_P).

If (\theta_1\subseteq\theta_2), then

[
\theta_1(r(x),r(y))
\Longrightarrow
\theta_2(r(x),r(y)),
]

so (\widehat{\theta}_1\subseteq\widehat{\theta}_2).

The bijection and its inverse are therefore order-preserving:

[
\boxed{
\operatorname{Stab}(T)
\cong_{\mathrm{ord}}
\operatorname{Con}(P,T|_P).
}
]

Both families are lattices under inclusion: meets are intersections, and joins are the equivalence-relation closures of unions. An order isomorphism preserves these operations. Hence the bijection is also a lattice isomorphism.

7. Independence of the retraction exponent

Suppose (L_1,L_2) both satisfy the conditions of Section 2, with (r_i=T^{L_i}). For any pullback-fixed (E), iteration gives

[
E(x,y)\iff E(r_i(x),r_i(y)),
\qquad i\in{1,2}.
]

Thus extension recovers the same (E) from its core restriction under either valid retraction.

For a core congruence (\theta), its biconditional invariance under the core permutation ensures that pulling (\theta) back along either valid retraction gives the same relation. The classification therefore does not depend on the chosen valid exponent.

8. Scope and certification boundary

This theorem concerns pullback-fixed relations:

[
E(x,y)\iff E(Tx,Ty).
]

It must not be conflated with forward-stable relations:

[
E(x,y)\Longrightarrow E(Tx,Ty),
]

which are relevant to the one-directional quotient/defect criterion. These two classes are not interchangeable.

Obligation| Status
Corrected restriction/extension proof| PROVED ON PAPER
Lean formalization and build| OPEN — not claimed compiled
Bounded v2 source/receipt authentication against repository commit| NOT ESTABLISHED
Independent replay of bounded census| NOT ESTABLISHED
C4| BLOCKED
Publication| BLOCKED
Promotion| FALSE

This document does not claim that a Lean build has passed, that a receipt has been authenticated, or that finite computation establishes the universal theorem.

9. Literature boundary

The reduction of finite unary dynamics to periodic-core structure and the study of congruence lattices of monounary algebras are classical. Present this result as an AQARION proof and verification formulation of the stated reduction, not as a claim that the surrounding monounary-algebra structure is newly discovered.
