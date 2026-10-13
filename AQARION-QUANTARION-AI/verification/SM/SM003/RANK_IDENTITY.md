SM003 — Universal Rank Identity and Degenerate-Mutant Equivalence

Repository: "quantarion369-arch/AQARION"
File: "AQARION-QUANTARION-AI/verification/SM/SM003/RANK_IDENTITY.md"
Claim: (\operatorname{rank}(D_\Pi)=k-c(H_\Pi))
Evidence status: Informal mathematical proof; Lean formalization and independent clean-checkout certification are not asserted.

1. Definitions

Let (X) be a finite nonempty set, let (T:X\to X) be a total map, and let
[
\Pi={B_1,\ldots,B_k}
]
be a partition of (X) into nonempty blocks.

Use the row-indexed Koopman matrix convention
[
K[x,y]=
\begin{cases}
1,&T(x)=y,\
0,&\text{otherwise}.
\end{cases}
]

Let (P=P_\Pi) be the orthogonal projector onto functions constant on each block. Thus, for (x,y\in X),
[
P[x,y]=
\begin{cases}
1/|B|,&x,y\in B\text{ for some }B\in\Pi,\
0,&\text{otherwise}.
\end{cases}
]

Define the canonical defect
[
D_\Pi=(I-P)KP.
]

Construct the undirected graph (H_\Pi) as follows:

1. There is one vertex for each block (B_i).
2. For each source block (B\in\Pi), let
   [
   S_B={B_i\in\Pi:T(B)\cap B_i\ne\varnothing}.
   ]
3. Connect every pair of distinct vertices in (S_B). Equivalently, (S_B) induces a clique.
4. Retain all (k) vertices, including isolated vertices.

Write (c(H_\Pi)) for the number of connected components, counting isolated vertices.

2. Theorem

For every such finite system and partition,
[
\boxed{\operatorname{rank}(D_\Pi)=k-c(H_\Pi).}
]

Proof

For each target block (B_i), define (q_i\in\mathbb R^X) by
[
q_i(y)=
\begin{cases}
1/|B_i|,&y\in B_i,\
0,&y\notin B_i.
\end{cases}
]

The vectors (q_1,\ldots,q_k) are linearly independent: their supports are nonempty and pairwise disjoint.

For any (x\in X), let (B(x)) denote its source block and let (b(T(x))) denote the index of the block containing (T(x)). The row of (KP) indexed by (x) is (q_{b(T(x))}). Left multiplication by (I-P) subtracts the average of these rows over the source block. Therefore, if (x\in B),
[
D_\Pi[x,\cdot]
=q_{b(T(x))}
-\frac1{|B|}\sum_{u\in B}q_{b(T(u))}.
]

Fix a source block (B), and write (S_B) for its set of hit target-block indices. The rows indexed by (x\in B) consequently lie in
[
V_B=\operatorname{span}{q_i-q_j:i,j\in S_B}.
]

Conversely, the span of those rows equals (V_B). Indeed, for any (i,j\in S_B), choose (x_i,x_j\in B) whose images lie in target blocks (B_i,B_j), respectively. Subtracting the corresponding defect rows gives
[
D_\Pi[x_i,\cdot]-D_\Pi[x_j,\cdot]=q_i-q_j.
]
Thus all generators of (V_B) lie in the span of the defect rows from (B).

Taking all source blocks,
[
\operatorname{rowspan}(D_\Pi)
=\operatorname{span}{q_i-q_j:
i,j\in S_B\text{ for some }B\in\Pi}.
]

The graph (H_\Pi) contains an edge between every pair of target-block vertices that occur together in some (S_B). Its edge-difference vectors (q_i-q_j) therefore generate exactly the same space as the displayed row span.

For a graph on (k) vertices with (c) connected components, the span of its edge differences has dimension (k-c): within each component, differences span the subspace whose coefficients sum to zero, of dimension one less than the number of vertices in that component. The independence of the (q_i) preserves these dimensions when the abstract coordinate vectors are represented by the (q_i).

Summing over components gives
[
\operatorname{rank}(D_\Pi)=k-c(H_\Pi).
]
(\square)

3. Consequence for "R:first"

In the current SM003 implementation, "R:first" keeps only the first target hit by each source block and supplies each retained target as a singleton group to "component_count".

Singleton groups introduce no edges. Because the component counter retains all (k) vertices, including isolated vertices, this calculation always returns (k). Its prediction is therefore
[
R_{\mathrm{first}}=k-k=0
]
on every valid input.

The canonical graph prediction is (k-c(H_\Pi)), which equals the exact defect rank by the theorem. Hence
[
R_{\mathrm{first}}\ne\operatorname{rank}(D_\Pi)
\quad\Longleftrightarrow\quad
\operatorname{rank}(D_\Pi)>0.
]

The existing "D:KP(I-P)" mutant evaluates (KP(I-P)). Since (P) is an orthogonal projector, (P(I-P)=0), so
[
KP(I-P)=0
]
for every valid input. Its zero-test consequently always returns "True". Under SM003's stated D-level kill rule, it is detected exactly when the independent closure oracle returns "False".

The defect has rank zero exactly when every source block maps into a single target block: this is precisely the partition-invariance condition. Thus the D-level mutant is detected exactly when the defect rank is positive. The same is true of "R:first".

Conclusion: "R:first" and "D:KP(I-P)" have identical detection sets over the entire stated finite domain, not merely over a bounded census. This conclusion follows from the implementation definitions and the rank identity above.

4. Scope and limitations

- This is an informal proof, not a Lean-checked theorem.
- It does not establish that a repository test suite passed, that CI ran, or that a clean-checkout replay occurred.
- The result assumes the stated row-indexed convention for (K), the block-average projector (P), the canonical defect ((I-P)KP), and the graph construction retaining isolated vertices.
- A formalization must preserve these conventions, particularly the inclusion of isolated graph vertices and the definition of the target blocks hit by each source block.
