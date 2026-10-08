# Support-Rank Theorem for Finite Deterministic Maps

## Theorem Statement

Let $$X$$ be a finite nonempty set, $$T:X\to X$$ a deterministic map, and $$\Pi=\{B_1,\ldots,B_k\}$$ a partition into nonempty blocks. Define:

- $$b_i=|B_i|$$
- $$M_{ij}=|\{x\in B_i:T(x)\in B_j\}|$$ (transport matrix)
- $$S_i=\{j:M_{ij}>0\}$$ (target support of source block $$B_i$$)
- $$H_M$$ = graph on vertices $$\{1,\ldots,k\}$$ where $$j\sim\ell$$ iff $$j,\ell\in S_i$$ for some $$i$$
- $$c(H_M)$$ = number of connected components of $$H_M$$

Then:

$$\boxed{\operatorname{rank}D_\Pi=k-c(H_M)}$$

where $$D_\Pi=(I-P_\Pi)K_TP_\Pi$$, with $$P_\Pi$$ the orthogonal block-averaging projection and $$K_T$$ the pullback Koopman operator.

## Kernel Characterization

Let $$V_\Pi\subseteq\mathbb R^X$$ denote the block-constant subspace. The restricted kernel is:

$$\ker(D_\Pi|_{V_\Pi})=\left\{\sum_jc_j1_{B_j}:c\text{ is constant on each component of }H_M\right\}$$

Therefore:

$$\dim\ker(D_\Pi|_{V_\Pi})=c(H_M)$$

The ambient kernel also contains $$V_\Pi^\perp$$:

$$\ker D_\Pi=V_\Pi^\perp\oplus\ker(D_\Pi|_{V_\Pi})$$

$$\dim\ker D_\Pi=n-k+c(H_M)$$

## Proof

For $$f=\sum_jc_j1_{B_j}$$, the pullback Koopman operator gives:

$$(K_Tf)(x)=f(T(x))=c_j\quad\text{when }T(x)\in B_j$$

The defect $$D_\Pi f$$ vanishes exactly when $$K_Tf$$ is block-constant. This requires:

$$c_j=c_\ell\quad\text{whenever }j,\ell\in S_i$$

Taking the transitive closure over all source blocks, this condition is equivalent to $$c$$ being constant on each connected component of $$H_M$$.

The space of such coefficient vectors has dimension $$c(H_M)$$, establishing the kernel characterization.

Since $$D_\Pi P_\Pi=D_\Pi$$, the operator annihilates $$V_\Pi^\perp$$, giving the ambient kernel decomposition.

## Exact Energy Decomposition

For any block-constant observable $$f=\sum_jc_j1_{B_j}$$:

$$\|D_\Pi f\|^2=\sum_i\frac{1}{b_i}\sum_{j<\ell}M_{ij}M_{i\ell}(c_j-c_\ell)^2$$

Summing over the standard basis:

$$\|D_\Pi\|_F^2=\sum_{i,j}\frac{M_{ij}(b_i-M_{ij})}{b_ib_j}$$

This is an exact identity, not an approximation.

## Rank-One Classification

$$\operatorname{rank}D_\Pi=1\iff H_M\text{ has exactly one 2-vertex component and all other vertices isolated}$$

Equivalently, there exist distinct target blocks $$a,b$$ such that:
1. At least one source block has positive entries in both columns $$a$$ and $$b$$.
2. Every source block with more than one positive entry has support exactly $$\{a,b\}$$.

## Scope and Limitations

- This theorem holds for arbitrary finite deterministic maps, not only permutations.
- The support graph depends only on the zero/nonzero pattern of $$M$$, not its magnitudes.
- The energy formula depends on both support and multiplicities.
- For permutations, the principal-angle specialization applies but is not claimed as novel.
- No enumeration formula for the number of rank-one maps or partitions is supplied here.
