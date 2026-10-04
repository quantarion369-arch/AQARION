PB-CORE-005 — Adversarial Research Addendum

Status: [P][V] with independent computational reproduction
Formalization: OPEN
Certification: BLOCKED
Publication: BLOCKED pending novelty review and certification

1. Independent reproduction

A structurally separate implementation was used to test the cycle-orbit formula and finite-core reduction.

Permutation formula

All permutations through n=6:

[
1+2+6+24+120+720=873.
]

Result:

n=1  mismatches=0
n=2  mismatches=0
n=3  mismatches=0
n=4  mismatches=0
n=5  mismatches=0
n=6  mismatches=0

A further exhaustive check of all 5,040 permutations at n=7 also produced

mismatches=0

Random independent checks of 500 permutations each at n=8,9,10 produced zero mismatches.

The n=12 brute-force attempt was computationally interrupted and is deliberately recorded as no result, not as PASS or FAIL.

2. Finite-map core reduction

All maps

[
T:[n]\to[n]
]

through n=6 were independently enumerated:

[
1+4+27+256+3125+46656=50069.
]

The independent test compared:

1. direct enumeration of pullback-fixed equivalences on X;
2. invariant equivalences on the eventual periodic core.

Results:

restriction failures = 0
extension failures   = 0

Aggregate direct stable-equivalence counts:

n=1   1
n=2   6
n=3   51
n=4   592
n=5   8565
n=6   148896

These reproduce the canonical PB-CORE-005 run.

3. Join cross-check

The previously recorded exhaustive finite join computation through n=6 contains

[
582696
]

stable ordered/unordered-pair cases according to the repository's stated convention, with

join failures = 0

No join result is promoted merely because PB-CORE-005 succeeds.

4. Mathematical audit

The core reduction remains:

[
E\in\operatorname{Stab}(T)
\iff
E=\operatorname{Ext}_h(E|_P),
\qquad P=\operatorname{Per}(T),
]

for any sufficiently large h with T^h(X)=P.

The inverse maps are restriction and extension.

The key finite fact is pullback rigidity:

[
T^*E\subseteq E
\implies
T^*E=E.
]

Therefore, on the finite permutation core, forward congruence invariance and exact pullback invariance coincide.

5. Literature adversarial finding

The mathematical neighborhood is not novel.

Classical and modern literature explicitly studies:

- congruences of unary algebras;
- congruence lattices of monounary algebras;
- finite monounary algebras as functional digraphs;
- congruences of G-sets.

Berman's 1972 work treats congruences of unary algebras directly. Later work studies connected monounary congruence lattices and the structure of finite monounary algebras. The cycle-divisor description is already present in this literature.

Therefore the following claims are not publication-safe novelty claims:

"discovered congruence theory for unary algebras"
"discovered cycle congruences"
"first classification of congruences of permutation cycles"
"first connection between finite functional maps and unary-algebra congruences"

6. Defensible AQARION contribution

The current defensible contribution is instead:

1. isolate the pullback-fixed condition
   T^*E=E as the exact object of study;

2. prove the finite restriction/extension reduction to the eventual permutation core;

3. give an explicit cycle-index/common-divisor/phase formula in the chosen representation;

4. connect the theorem to executable exhaustive verification;

5. provide independently reproduced finite evidence;

6. preserve an auditable proof/computation/provenance separation;

7. turn the reduction into an educational laboratory in which transient dynamics and congruence structure can be explored separately.

The exact novelty of item 3 remains OPEN until the relevant unary-algebra literature has been compared directly against the formula.

7. Evidence status

PB-CORE-004
[P] mathematical proof
[V] independent finite verification through n=6
[R] literature novelty review continuing
[L] OPEN
[C4] BLOCKED

PB-CORE-005
[P] mathematical classification
[V] exhaustive permutations through n=6 + independent n=7
[V/R] independent random extension n=8..10
[R] exact novelty status OPEN
[L] OPEN
[C4] BLOCKED

No evidence promotion is made from computational agreement alone.
