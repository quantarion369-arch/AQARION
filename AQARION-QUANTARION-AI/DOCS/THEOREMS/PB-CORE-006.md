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

---


# PB-CORE-006 — Aggregate Enumeration of Pullback-Fixed Equivalences

**Canonical claim ID:** `PB-CORE-006`  
**Subject:** Aggregate enumeration over finite self-maps  
**Status:** Candidate pending independent proof review and repository-bound verification  
**Lean:** OPEN  
**C4:** BLOCKED  
**Publication:** BLOCKED  
**Promotion:** NOT AUTHORIZED

---

## 1. Definitions

For an integer \(n\geq1\), let

\[
[n]=\{1,\ldots,n\}.
\]

For each map \(T:[n]\to[n]\), define

\[
\operatorname{Stab}(T)
=
\left\{
E\in\operatorname{Eq}([n]):
T^*E=E
\right\},
\]

where \(\operatorname{Eq}([n])\) is the set of equivalence relations on
\([n]\), and

\[
x\mathrel{T^*E}y
\iff
T(x)\mathrel E T(y).
\]

Define the aggregate count

\[
A_n
=
\sum_{T:[n]\to[n]}
|\operatorname{Stab}(T)|.
\]

Let \(p(k)\) denote the integer partition function: the number of integer
partitions of \(k\).

The claim counts pairs \((T,E)\), where \(T\) is a labelled self-map and
\(E\) is an equivalence relation satisfying the exact pullback condition
\(T^*E=E\).

---

## 2. Candidate aggregate formula

The proposed identity is

\[
\boxed{
A_n
=
\sum_{k=1}^{n-1}
\frac{n!}{(n-k)!}\,
k\,n^{\,n-k-1}\,p(k)
+
n!\,p(n).
}
\]

The endpoint \(k=n\) is separated deliberately. There are no transient
vertices in that case, so the forest factor is \(1\). The expression
\(n^{n-k-1}\) must not be applied at \(k=n\), where it would have exponent
\(-1\).

Equivalently, with the endpoint explicitly included in the summation
convention,

\[
A_n
=
\sum_{k=1}^{n}
\binom nk F(n,k)\,k!\,p(k),
\]

where

\[
F(n,k)=
\begin{cases}
k\,n^{\,n-k-1},&1\leq k<n,\\
1,&k=n.
\end{cases}
\]

The two displayed forms are equivalent because

\[
\binom nk k!=\frac{n!}{(n-k)!}.
\]

**Evidence status:** The formula and derivation are maintained as a
candidate pending independent review and a repository-bound verification
record. This overview does not claim Lean certification or publication
approval.

---

## 3. Periodic-core reduction

Let \(T:X\to X\) be a self-map on a finite set, and let

\[
P=\operatorname{Per}(T)
\]

be its set of periodic points.

The restriction

\[
\sigma=T|_P:P\to P
\]

is a permutation. A sufficiently large iterate \(r=T^h\) maps \(X\) onto
\(P\) and restricts to the identity on \(P\).

For a pullback-fixed equivalence \(E\),

\[
x\mathrel E y
\iff
T(x)\mathrel E T(y).
\]

Iterating this equivalence gives

\[
x\mathrel E y
\iff
r(x)\mathrel E r(y).
\]

Therefore \(E\) is determined by its restriction to \(P\). Conversely,
an equivalence on \(P\) invariant under the core permutation pulls back
along \(r\) to a pullback-fixed equivalence on \(X\).

This gives the periodic-core correspondence

\[
\operatorname{Stab}(T)
\cong
\operatorname{Con}(P,\sigma),
\]

where \(\operatorname{Con}(P,\sigma)\) denotes the equivalence relations
preserved by \(\sigma\). Since \(\sigma\) is a permutation on a finite
set, forward preservation implies exact invariance.

This reduction is a dependency of the aggregate enumeration. It is not
the identity of the asymptotic claim in the API repository.

---

## 4. Aggregate count on a permutation core

For a \(k\)-element labelled set, define

\[
S_k
=
\sum_{\sigma\in S_k}
|\operatorname{Con}([k],\sigma)|.
\]

The proposed aggregate identity is

\[
\boxed{S_k=k!\,p(k).}
\]

A direct counting argument proceeds by counting pairs \((\sigma,E)\)
where \(E\) is an equivalence relation and \(\sigma\) preserves \(E\).

Fix an equivalence relation whose block-size profile has \(m_s\) blocks
of size \(s\). Thus

\[
\sum_{s\geq1}s\,m_s=k.
\]

The number of equivalence relations with this profile is

\[
\frac{k!}{\prod_{s\geq1}(s!)^{m_s}m_s!}.
\]

A permutation preserves a fixed equivalence relation precisely when it
permutes blocks of equal size and independently permutes the elements
inside each block. The number of such permutations is

\[
\prod_{s\geq1}(s!)^{m_s}m_s!.
\]

Multiplying these two counts gives \(k!\) for each block-size profile.
The profiles correspond to integer partitions of \(k\), of which there
are \(p(k)\). Therefore the pair count is

\[
S_k=k!\,p(k).
\]

This derivation is recorded as the intended combinatorial argument.
Independent review and the required verification record remain part of
the promotion gate.

---

## 5. Counting maps with a prescribed periodic core

Suppose the periodic core has \(k\) labelled vertices.

There are

\[
\binom nk
\]

choices for its vertex set.

For \(1\leq k<n\), the remaining vertices form a labelled rooted forest
whose \(k\) roots are the prescribed periodic vertices. The fixed-root
forest count is

\[
F(n,k)=k\,n^{\,n-k-1}.
\]

For \(k=n\), there are no transient vertices, and

\[
F(n,n)=1.
\]

The self-map on the periodic core is a permutation. Summing the number
of compatible equivalences over all core permutations contributes
\(S_k=k!p(k)\).

Thus the contribution from maps whose periodic core has size \(k\) is

\[
\binom nk F(n,k)\,k!\,p(k).
\]

Summing over the possible core sizes yields the candidate aggregate
formula in Section 2.

This decomposition also explains the endpoint: the full-core term is

\[
\binom nn\cdot1\cdot n!\,p(n)=n!\,p(n).
\]

---

## 6. Reported reference values

The repository receipt records the following values for the proposed
formula:

| \(n\) | Reported \(A_n\) |
|---:|---:|
| 1 | 1 |
| 2 | 6 |
| 3 | 51 |
| 4 | 592 |
| 5 | 8,565 |
| 6 | 148,896 |
| 7 | 3,018,127 |
| 8 | 69,844,608 |
| 9 | 1,816,084,233 |
| 10 | 52,399,129,600 |
| 11 | 1,660,832,066,091 |
| 12 | 57,351,480,413,184 |

These are recorded reference values, not a claim that the verifier was
rerun for this document revision. The receipt currently states that the
arithmetic replay reports PASS (12/12 match) but source and manifest hashes
are absent. The values must not be represented as newly reproduced or
cryptographically bound to the current source.

---

## 7. Dependency on the asymptotic research

The separate API research claim is:

**PB-ASYM-001 — Random-mapping stable-count asymptotics**

Its legacy research location is:

`Aqarion-Fastapi/research/pb-core-006/`

The shared historical directory name is not a shared claim identity.

The dependency is directional:

\[
\boxed{
\text{PB-CORE-006 aggregate enumeration}
\longrightarrow
\text{PB-ASYM-001 asymptotic analysis}.
}
\]

PB-ASYM-001 studies asymptotic consequences of the aggregate counting
problem. It requires additional analytic estimates, including justified
local expansions, uniform remainder bounds, tail control, and the
validity of the discrete approximation.

Even if PB-CORE-006 is proved, that does not automatically prove any
asymptotic expansion, second-order coefficient, global error bound, or
publication claim in PB-ASYM-001.

Conversely, numerical agreement with an asymptotic prediction does not
prove the exact aggregate counting identity.

The separate structural cycle-classification work in PB-CORE-005 is
also not required for the block-profile argument for \(S_k=k!p(k)\).
Its status must be tracked independently.

---

## 8. Verification and governance obligations

The following obligations remain distinct:

1. Independently review the periodic-core correspondence.
2. Independently review the permutation/equivalence pair count.
3. Verify the fixed-root forest factor and endpoint handling.
4. Recompute the arithmetic reference values.
5. Tie the verifier run to the exact source revision and manifest.
6. Formalize the required claims in Lean and verify the project build.
7. Keep asymptotic obligations in PB-ASYM-001 rather than merging them
   into this claim's evidence record.

A receipt must identify the tested source revision, source hashes,
manifest hash, executed command, environment, case counts, and result.
A historical report or an unbound receipt does not establish a fresh
reproduction.

---

## 9. Final status

PB-CORE-006 is the aggregate-enumeration claim.

PB-ASYM-001 is the dependent asymptotic research claim.

Their identities and evidence records must remain separate.

**Current status:**

- Aggregate formula: candidate pending independent review.
- Arithmetic replay: receipt reports PASS (12/12 match); not yet cryptographically bound to a specific source revision.
- Source-bound provenance: incomplete.
- Lean: open.
- C4: blocked.
- Publication: blocked.
- Promotion: not authorized.

