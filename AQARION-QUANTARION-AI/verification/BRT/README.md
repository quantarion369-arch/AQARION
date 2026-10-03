BRT

BRT is the exact finite verification package for the block-transition / forward co-occurrence defect-rank identity.

Definition

Let

[
T:X\to X
]

be a finite deterministic transition and let

[
\mathcal P={B_0,\ldots,B_{k-1}}
]

be a partition of X.

Let P be the orthogonal block-average projection and let K be the deterministic Koopman matrix.

Define

[
D=(I-P)KP.
]

For each source block B_i, form the normalized block-transition matrix

[
Q_{ij}

\frac{
|{x\in B_i:T(x)\in B_j}|
}{
|B_i|
}.
]

Construct the forward co-occurrence graph H whose vertices are the partition blocks. Two target blocks are connected when they occur in the same nonzero row of Q.

Let c(H) denote the number of connected components of H.

Exact identity

For the finite deterministic construction,

[
\boxed{\operatorname{rank}(D)=k-c(H)}.
]

Equivalently,

[
\boxed{\dim\ker(D|_{\operatorname{Ran}P})=c(H)}.
]

The reason is that a block-constant observable lies in the kernel of D exactly when its values agree on every pair of target blocks that co-occur from a common source block. Those equality constraints identify exactly the connected components of H.

Verification

The validator uses exact rational arithmetic and independently computes:

- the block-average projection P;
- the deterministic Koopman matrix K;
- the defect D=(I-P)KP;
- the normalized block-transition matrix Q;
- the co-occurrence graph H;
- the exact rank of D;
- the component count c(H).

The repository corpus contains 10 explicit cases.

An independent audit additionally exhaustively checked all deterministic transitions and all set partitions for n\le5:

n=1    1 case
n=2    8 cases
n=3    135 cases
n=4    3840 cases
n=5    162500 cases

total 166484 cases
failures 0

A further 5,000 random exact-rational cases for 2\le n\le10 also produced zero failures.

Mutation control

The mutation suite replaces the partition-block co-occurrence graph with the individual-state transition graph.

The mutation is intentionally evaluated only by component count. The BRT rank formula is not applied to the mutant graph because its vertex set is different.

The mutation must be killed for the suite to pass.

Governance

Executable PASS is computational evidence.

Executable PASS is not, by itself, formal proof.

The package has no publication-promotion authority.

Formalization status must be reported separately from computational verification.

Files

BRT/
├── README.md
├── CHECKPOINT-2026-09-30.md
├── brt_cases.json
├── brt_validation.py
└── brt_mutation.py

The GitHub Actions workflow executes Python compilation, exact validation, mutation testing, and evidence upload.

Current status

COMPUTATIONAL_EVIDENCE: independently reproduced

THEOREM: supported directly by the finite-dimensional kernel argument above

FORMALIZATION: OPEN

C4: BLOCKED

PROMOTION: NO
