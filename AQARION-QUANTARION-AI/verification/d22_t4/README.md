D22 Direct Projection Theorem Package

Convention

Let k\ge3, with indices in \mathbb Z/k\mathbb Z. Let

[
Ke_j=e_{j-1},
]

and define

[
u_d=e_0-e_d,
\qquad
1\le d\le k-1.
]

Let

[
P_d=I-\frac12u_du_d^\top,
\qquad
Q_d=I-P_d=\frac12u_du_d^\top.
]

The observable defect is

[
D_d=Q_dKP_d.
]

All statements below are conditional on this convention. Equivalence with any external or historical D22 definition is a separate provenance question.

D22-OP-001 — Direct rank-one factorization

Since

[
Q_d=\frac12u_du_d^\top,
]

we have

[
D_d

\frac12u_du_d^\top KP_d

\frac12u_da_d^\top,
]

where

[
a_d^\top=u_d^\top KP_d.
]

Thus

[
\boxed{D_d=\frac12u_da_d^\top}.
]

In particular,

[
\operatorname{rank}(D_d)\le1.
]

The factor is obtained directly from the projection definition and does not depend on a fitted lag formula.

D22-CF-002 — Explicit closed factor

Because

[
u_d^\top K=e_1^\top-e_{d+1}^\top,
]

and

[
u_d^\top Ku_d

-\mathbf1_{d=1}
-\mathbf1_{d=k-1},
]

we obtain

[
a_d^\top

e_1^\top-e_{d+1}^\top
+
\frac12
\left(
\mathbf1_{d=1}
+
\mathbf1_{d=k-1}
\right)
(e_0^\top-e_d^\top).
]

Equivalently,

[
\boxed{
a_d

e_1-e_{d+1}
+
\frac12
\left(
\mathbf1_{d=1}
+
\mathbf1_{d=k-1}
\right)
(e_0-e_d).
}
]

Hence the defect is completely determined by the projection construction.

D22-NIL-003 — Square-zero defect

Since

[
P_du_d=0,
]

we have

[
a_d^\top u_d

u_d^\top KP_du_d

0. 

]

Therefore

[
D_d^2

\frac14u_d(a_d^\top u_d)a_d^\top

0. 

]

Thus

[
\boxed{D_d^2=0}.
]

D22-FROB-004 — Exact norm split

For a rank-one matrix,

[
|u_da_d^\top|_F^2

|u_d|^2|a_d|^2.
]

Since |u_d|^2=2,

[
|D_d|_F^2

\frac12|a_d|^2.
]

For interior 2\le d\le k-2,

[
a_d=e_1-e_{d+1},
]

so

[
\boxed{|D_d|_F^2=1}.
]

For d=1 or d=k-1,

[
|a_d|^2=\frac32,
]

so

[
\boxed{|D_d|_F^2=\frac34}.
]

Because D_d has rank one,

[
\boxed{|D_d|_2=|D_d|_F}.
]

D22-LAG-005 — Full transmitted lag identity

For m\in\mathbb Z/k\mathbb Z, define

[
L_m(d)=u_d^\top K^m u_d.
]

Then

[
\boxed{
L_m(d)

2\delta_{m,0}
-\delta_{m,d}
-\delta_{m,-d}.
}
]

Furthermore define

[
a_d^{(m)\top}=u_d^\top K^mP_d.
]

Then

[
\boxed{
a_d^{(m)\top}

e_m^\top-e_{m+d}^\top
-\frac12L_m(d)u_d^\top.
}
]

The D22 closed factor is the m=1 case:

[
a_d=a_d^{(1)}.
]

Therefore the lag structure is a consequence of the direct projection construction rather than an input used to fit a_d.

D22-UNIQ-006 — Corrected identifiability statement

The directed support of

[
u_d^\top K=e_1^\top-e_{d+1}^\top
]

identifies d and therefore determines a_d.

However, the scalar cyclic autocorrelation

[
L_m(d)

2\delta_{m,0}
-\delta_{m,d}
-\delta_{m,-d}
]

is invariant under

[
d\longleftrightarrow k-d.
]

Therefore scalar autocorrelation alone does not uniquely determine the orientation of d.

The previous stronger claim that "lag plus norm uniquely recovers a_d" is not retained without an explicit directed-lag convention.

Provenance boundary

These theorems establish the mathematics of the explicitly specified operator model.

They do not establish that this model is identical to an external canonical D22 construction.

Canonical-source equivalence remains a separate open claim:

[
\boxed{
\text{SOURCE-EQUIVALENCE = OPEN}.
}
]
