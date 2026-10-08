PB-CORE-006 — Periodic-Core Partition Bijection

Status

MATHEMATICAL RESULT: proved
COMPUTATIONAL REEXECUTION: established elsewhere; repository certificate not asserted here
LEAN FORMALIZATION: OPEN
PROMOTION: BLOCKED pending repository-bound certificate

---

Theorem

Let T:X\to X be a finite dynamical system, with

[
P=\operatorname{Per}(T)
]

the set of periodic points of T.

Let

[
L=\operatorname{lcm}(1,2,\ldots,|X|)
]

and define

[
r=T^L.
]

Then

[
\boxed{\operatorname{PB}(T)\cong
\operatorname{Con}(P,T|_P)}
]

where:

- \operatorname{PB}(T) is the set of equivalence relations E on X satisfying
  [
  xEy\iff T(x)E T(y),
  ]
- \operatorname{Con}(P,T|_P) is the set of congruences of the permutation T|_P.

---

Proof

Because X is finite, every orbit eventually enters a periodic cycle.

For every x\in X, the point T^L(x) is periodic. Hence

[
r(X)=P.
]

For p\in P, the orbit length of p divides L, so

[
r(p)=T^L(p)=p.
]

Therefore

[
r|_P=\operatorname{id}_P.
]

Since r=T^L is a power of T,

[
rT=Tr.
]

Now let E\in\operatorname{PB}(T). By iterating

[
xEy\iff T(x)E T(y),
]

we obtain

[
xEy\iff T^L(x)E T^L(y).
]

Thus

[
\boxed{xEy\iff r(x)E r(y)}.
]

Since r(x),r(y)\in P, the entire equivalence relation is determined by its restriction to P.

Define

[
\Phi(E)=E|_P.
]

Because T(P)=P and T|_P is a permutation, the restriction is a congruence of T|_P.

Conversely, let

[
F\in\operatorname{Con}(P,T|_P).
]

Define an equivalence relation \widehat F on X by

[
x,\widehat F,y
\iff
r(x),F,r(y).
]

Because F is an equivalence relation and r is a function, \widehat F is an equivalence relation.

Furthermore,

[
r(Tx)=T(r x),
\qquad
r(Ty)=T(r y).
]

Since F is preserved and reflected by T|_P,

[
r(x)F r(y)
\iff
T(r x)F T(r y).
]

Therefore

[
x,\widehat F,y
\iff
T(x),\widehat F,T(y).
]

Hence

[
\widehat F\in\operatorname{PB}(T).
]

Finally,

[
\Phi(\widehat F)=F
]

because r|_P=\operatorname{id}_P, while for every E\in\operatorname{PB}(T),

[
\widehat{\Phi(E)}=E
]

because

[
xEy\iff r(x)E r(y).
]

Thus \Phi and F\mapsto\widehat F are inverse bijections.

Therefore

[
\boxed{\operatorname{PB}(T)\cong
\operatorname{Con}(P,T|_P)}.
]

---

Corollary 1 — Stabilizer averaging

If |P|=k, then the number of permutation-equivariant partitions of P, averaged over relabelings, is controlled by the partition number p(k).

In particular,

[
\boxed{
\frac1{k!}\sum_{\sigma\in S_k} C(\sigma)=p(k)
}
]

whenever C(\sigma) denotes the corresponding congruence count.

Equivalently,

[
\boxed{
\sum_{\sigma\in S_k}C(\sigma)=k!,p(k).
}
]

---

Corollary 2 — Aggregate count over all finite maps

Let A_n denote the aggregate number of T-invariant-and-reflecting partitions over all maps T:[n]\to[n].

Conditioning on the number K_n of periodic points gives

[
\mathbb E[S(T)\mid K_n=k]=p(k).
]

The number of maps with exactly k periodic points is

[
\frac{k,n!}{(n-k)!},n^{,n-k-1}.
]

Hence

[
\boxed{
A_n

n!\sum_{k=1}^{n}
\frac{k,p(k),n^{,n-k-1}}{(n-k)!}.
}
]

---

Corollary 3 — Exponential generating function

Let

[
T(z)=ze^{T(z)}
]

be the rooted-tree/Lambert-W series.

Let

[
P(z)=\sum_{k\ge1}p(k)z^k.
]

Then

[
\boxed{
\sum_{n\ge1}\frac{A_n}{n!}z^n

P(T(z))-1.
}
]

This follows from the Lagrange inversion identity

[
[z^n],T(z)^k

\frac{k}{n}[u^{n-k}]e^{nu}

\frac{k,n^{n-k-1}}{(n-k)!}.
]

---

What remains OPEN

1. Lean formalization of the general theorem.
2. A repository-bound certificate tying the theorem statement to the exact executable evidence.
3. Global asymptotic tail bounds needed for promotion of the asymptotic consequences.

No claim of formal verification or publication readiness is made by this document alone.
