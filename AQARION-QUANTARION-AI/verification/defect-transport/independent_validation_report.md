Independent Validation Report — AQARION Defect Transport

Scope: Finite deterministic maps, partition-generated observable spaces, support–rank identity, and exact Frobenius energy.

1. Mathematical specification

Let (T:X\to X) be a finite deterministic map and (\Pi={B_1,\ldots,B_k}) a partition into nonempty blocks. Define the pullback Koopman operator (K_Tf=f\circ T), the orthogonal block-averaging projection (P_\Pi), and the defect

[
D_\Pi=(I-P_\Pi)K_TP_\Pi.
]

The transport matrix is

[
M_{ij}=|{x\in B_i:T(x)\in B_j}|,
\qquad b_i=|B_i|.
]

For each source block, define (S_i={j:M_{ij}>0}). The support graph (H_M) connects target vertices that co-occur in some support set (S_i). Let (c(H_M)) be its number of connected components.

2. Independent exhaustive computation

A separately implemented exact-rational checker enumerated every map (T:[n]\to[n]) and every set partition for (n=1,2,3,4).

(n)| Maps| Partitions| Map–partition pairs
1| 1| 1| 1
2| 4| 2| 8
3| 27| 5| 135
4| 256| 15| 3,840
Total| | | 3,984

All 3,984 cases passed:

- Ambient rank equals (k-c(H_M)).
- Restricted rank on the block-constant space equals (k-c(H_M)).
- Component-indicator vectors are annihilated by the restricted defect.
- The component-indicator vectors are linearly independent.
- Direct operator Frobenius energy equals the transport formula exactly.

The calculation used rational arithmetic and exact Gaussian elimination. It used no floating-point rank thresholds.

3. Support-versus-weight control

For block sizes ((4,4)), the matrices

[
M_1=\begin{pmatrix}1&3\3&1\end{pmatrix},
\qquad
M_2=\begin{pmatrix}2&2\2&2\end{pmatrix}
]

have identical support and connected support graphs. Both predict and attain rank one. Their exact energies are (3/4) and (1), respectively.

This supports the proposed distinction between combinatorial support and quantitative defect energy on the tested examples.

4. Repository discrepancy

The committed "self_test_output.json" reports energies (3/8) and (1/2) for the same-support control. Those values disagree with the expected values (3/4) and (1), the current source calculation, and the independent exhaustive check.

The committed "self_test_stdout.json" is byte-identical to "self_test_output.json"; it is not a second independent run.

Disposition: the committed output is inconsistent and must be regenerated from the exact source revision. The self-test must assert the expected energies, not merely that the energies differ.

The validation code also uses "isinstance(value, int)" for state indices. Since Python booleans satisfy this test, a strict input contract should reject Boolean state labels explicitly.

5. Literature and novelty boundary

Recent Koopman literature already uses principal angles and projection/invariance diagnostics. AQARION must not claim novelty for principal-angle invariance itself.

The support–rank theorem is a finite combinatorial specialization involving transport support and connected components. The targeted literature search did not establish an exact prior-art match for this theorem in the stated form. This is not evidence that the result is novel; literature priority remains open.

6. Evidence status

- Mathematical derivation: proved by the argument in the theorem record, subject to ordinary mathematical review.
- Independent finite computation: PASS on the declared (n\le4) domain.
- Current committed self-test output: INCONSISTENT; regenerate and recheck.
- Repository-bound replay with a regenerated receipt: PENDING.
- External independent reproduction: NOT ESTABLISHED.
- Lean formalization: OPEN.
- Formal promotion and publication: BLOCKED.

The exhaustive computation is finite evidence. It is not the proof of the universal theorem and is not a Lean certificate.
