Theorem: Exact Frobenius Defect Norm for Pair Partitions of a Cyclic Shift

Let X=\mathbb Z_k, k\ge3, and let
[
T(x)=x+1\pmod k.
]
Let K be the Koopman permutation matrix associated with T, and let \Pi_d be the partition
[
\Pi_d=\big{{0,d}\big}\cup
\big{{j}:j\notin{0,d}\big},
\qquad 1\le d<k.
]
Let P_{\Pi_d} be the block-averaging projection and
[
D_d=(I-P_{\Pi_d})KP_{\Pi_d}.
]

Define
[
s=\min(d,k-d).
]

Then

[
\boxed{
|D_d|_F^2=
\begin{cases}
\frac34,&s=1,\[2mm]
1,&s\ge2.
\end{cases}}
]

Proof

For a singleton block {j},
[
P_{\Pi_d}e_j=e_j.
]
For the pair block,
[
P_{\Pi_d}e_0=P_{\Pi_d}e_d
=\frac12(e_0+e_d).
]

The only rows that can be nonzero in
[
D_d=(I-P_{\Pi_d})KP_{\Pi_d}
]
are therefore those belonging to the pair block or whose forward image enters the pair block. Hence

[
\operatorname{supp}_{\mathrm{row}}(D_d)
\subseteq
{0,d,k-1,d-1}.
]

For every distinct index in this set, the corresponding nonzero row has squared Euclidean norm 1/4. Consequently

[
|D_d|_F^2

\frac14
\left|{0,d,k-1,d-1}\right|.
]

If s=1, equivalently d=1 or d=k-1, three distinct indices occur, giving

[
|D_d|_F^2=\frac34.
]

If s\ge2, four distinct indices occur, giving

[
|D_d|_F^2=1.
]

Thus the formula follows.

Computational verification

Direct floating-point matrix evaluation was independently checked for

[
3\le k\le29,\qquad1\le d<k,
]

with no observed discrepancy from the exact formula.

This computational result is classified [CV]. It is not presented as a machine-formal proof.

Relation to defect rank

For every nontrivial pair partition in the tested range,

[
\operatorname{rank}(D_d)=1.
]

Thus the family provides an example in which defect rank remains constant while defect magnitude changes.

Relation to nilpotency depth

For k\ge6,

[
\delta(k,d)=
\begin{cases}
2,&s\le2,\
1,&s\ge3.
\end{cases}
]

Hence |D_d|_F^2 and \delta(k,d) are distinct observables:

[
s=1:
\quad
(|D|_F^2,\delta)=\left(\frac34,2\right),
]

[
s=2:
\quad
(|D|_F^2,\delta)=(1,2),
]

[
s\ge3:
\quad
(|D|_F^2,\delta)=(1,1).
]

In particular, |D|_F^2 does not determine the nilpotency depth.

Status

- Exact algebraic derivation: [P]
- Direct computational verification: [CV]
- Machine-formal proof: OPEN
- Literature priority/novelty claim: OPEN
