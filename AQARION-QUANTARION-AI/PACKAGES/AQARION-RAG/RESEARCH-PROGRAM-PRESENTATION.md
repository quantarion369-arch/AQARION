AQARION — Research Program Presentation

Document ID: AQARION-PUBLIC-RESEARCH-PRESENTATION-001
Revision date: 2026-10-09
Repository: "quantarion369-arch/AQARION"
Branch: "main"
Purpose: Public-facing introduction to the research program
Evidence policy: No claim is promoted beyond the evidence recorded for it.

---

1. Overview

AQARION is an evidence-first research program for finite deterministic dynamics and computational mathematics. It connects invariant partitions, quotient dynamics, Koopman operators, periodic cores, cycle-orbit structure, combinatorial enumeration, and machine-auditable verification.

The program has two connected aims:

1. Mathematical: identify precise structural theorems about finite dynamical systems and the equivalence relations they preserve.
2. Methodological: make the path from a research claim to its supporting evidence explicit, reproducible, and open to adversarial checking.

AQARION is not presented as an oracle of mathematical truth. Its repository is an auditable research record containing mathematical arguments, executable artifacts, finite computations, provenance records, corrections, and open obligations.

The governing rule is:

«Do not promote a result beyond what its evidence establishes.»

2. The basic mathematical setting

Let

[
T:\Omega\to\Omega
]

be a map on a finite state space. A partition of (\Omega) groups states into equivalence classes. The central questions include:

- When does the map induce a well-defined map on the quotient classes?
- Which equivalence relations are preserved by pullback under (T)?
- How are stable relations controlled by the periodic part of a finite functional graph?
- How do invariant partitions interact with joins, meets, cycle structure, and operator defects?
- Which finite calculations can be reconstructed independently and connected to a precise theorem?

These questions link elementary finite dynamics to algebra, combinatorics, linear operators, and formal methods.

3. Quotients and operator defects

For a finite deterministic system, the Koopman pullback operator acts on observables by

[
(Kf)(x)=f(Tx).
]

Given a partition (\Pi), let (P_\Pi) denote the declared projection onto observables that are constant on the partition blocks. Under this convention, the canonical defect is

[
D_\Pi=(I-P_\Pi)KP_\Pi
=KP_\Pi-P_\Pi KP_\Pi.
]

Its exactness criterion is

[
D_\Pi=0
\iff K(V_\Pi)\subseteq V_\Pi,
]

where (V_\Pi) is the partition-constant observable space. This expresses quotient compatibility as an invariant-subspace condition.

The definition and projection convention matter. Earlier noncanonical defect formulations and their incorrect numerical consequences are retained in the research history; they must not be conflated with the canonical operator above. Any claim of a specific algebraic identity or numerical defect must be tied to the exact operator definition used.

4. Periodic cores and pullback-fixed equivalences

A finite map eventually enters its periodic core. This suggests a structural classification problem: can equivalence relations satisfying

[
E(x,y)\iff E(Tx,Ty)
]

be described through congruences of the permutation induced by (T) on the periodic core?

The PB-CORE research line develops this restriction/extension viewpoint. If (r=T^L) is a suitable retraction onto the periodic core, the intended correspondence has the form

[
E(x,y)\iff F(r(x),r(y)),
]

where (F) is an equivalence relation on the core compatible with the restricted permutation.

The repository records a paper-level proof candidate, bounded exhaustive audits, arithmetic checks, and a remaining Lean/formalization gate. These are separate evidence objects: a written proof, a bounded census, and a successful formal build are not interchangeable.

The aggregate counting work also studies the expression

[
A_n=
\sum_{k=1}^{n-1}
\frac{n!,k,p(k),n^{n-k-1}}{(n-k)!}
+n!p(n),
]

where (p(k)) is the integer partition function. Its derivation depends on the relevant core classification, the count of permutation congruences, and a rooted-forest count. Formula evaluation over a finite range is arithmetic corroboration, not by itself proof of the combinatorial interpretation.

5. Invariant partitions of permutations

The FPR line studies invariant-partition counts for a finite permutation specified by its cycle lengths. The recorded formula is

[
N(\lambda)=
\sum_{\pi\in\Pi([r])}
\prod_{B\in\pi}
\left(
\sum_{d\mid\gcd(c_i:i\in B)}
d^{|B|-1}
\right),
]

where (c_1,\ldots,c_r) are the cycle lengths and (\Pi([r])) is the set of partitions of the cycle-index set.

The formula is organized by grouping cycles into blocks, choosing compatible common quotient-cycle lengths, and counting relative phase choices. The repository records a formula route and a direct invariant-partition enumeration route over a declared finite domain.

The safe status distinction is explicit:

- Formula and direct enumeration agree on the recorded bounded domain.
- This is computational corroboration.
- External independent reproduction is not established merely by two routes in one artifact.
- Lean status and literature novelty remain separate open questions unless supported by additional evidence.

Corrections to earlier finite values are retained as part of the audit trail.

6. JOIN-STABILITY and the finite/infinite boundary

JOIN-STABILITY asks when the join of two stable equivalence relations remains stable. For finite systems, the research explores quotient permutations and bipartite incidence graphs: connected components of the incidence graph encode the join classes, and finite injective actions can yield bijective actions on the realized finite structure.

The program also records an important boundary: the unrestricted infinite analogue does not hold in general. The finite theorem and the infinite counterexample are distinct results and must not be collapsed into a single universal claim.

Finite searches with no counterexample provide bounded computational evidence only. They do not replace the structural proof or establish an unrestricted theorem.

7. Finite closure depth

The closure-stability line studies iterative joins such as

[
R_{k+1}=R_k\vee T(R_k)
]

and the full orbit-generated join

[
J_T(R)=\bigvee_{k\ge0}T^k(R).
]

A central research question is whether a universal finite number of orbit terms suffices to obtain this closure. The AQ-K2R family is designed to test that question through explicitly constructed partitions, closure depths, and incidence-graph invariants.

The proposed unbounded-depth conclusion must remain tied to the complete family definition and its proof. A finite sample of parameter values, even when independently computed, is not by itself a proof that closure depth is unbounded.

8. Kaprekar dynamics and spectral structure

AQARION's finite-dynamics methods connect to the four-digit base-10 Kaprekar map. The research constructs a paired-gap observable quotient and studies its induced dynamics, partition structure, and Koopman representation.

This application illustrates both the usefulness and the limits of quotient language. A forward-invariant observable quotient need not be a pullback-fixed equivalence relation. The research therefore distinguishes

[
E(x,y)\Rightarrow E(Tx,Ty)
]

from the stronger condition

[
E(x,y)\iff E(Tx,Ty).
]

The Kaprekar spectral-geometry branch investigates additional graph and operator structure. Numerical spectral findings remain separate from exact theorems unless a specific derivation and verification record supports the stronger claim.

9. Reduced Gram matrices and defect rank

The reduced-Gram line seeks smaller exact matrix representations of partition-induced operator defects. A recorded candidate identity is

[
H(M)=N^{-1}\bigl(C-M^TN^{-1}M\bigr),
]

with the corresponding rank relationship between the defect operator and the reduced matrix under the declared matrix setup.

The research motivation is to convert a potentially larger operator calculation into exact rational linear algebra. The theorem's hypotheses, matrix definitions, rank correspondence, and tested cases must remain attached to any public statement. General optimization, arbitrary-block results, and formalization are not implied by a few verified examples.

10. Evidence and certification discipline

AQARION keeps the following questions separate:

Evidence layer| Question answered
Specification| Is the mathematical claim stated precisely, with conventions fixed?
Execution| Did the intended program actually run?
Computation| What did it establish on the declared finite domain?
Independent reconstruction| Was the relevant object reconstructed without relying on the same answer-producing oracle?
Reproducibility| Can the recorded computation be replayed from the declared environment and revision?
Mathematical proof| Does a valid argument establish the general claim?
Formal proof| Has the intended proposition been checked by the declared proof assistant?
Provenance| Are the source, inputs, outputs, environment, and revision bound to the evidence?
Promotion| Does the evidence meet the repository's explicit governance requirements?

A hash identifies bytes; it does not prove a theorem. A passing test establishes that the executed checks passed, not that the specification was correct. A Lean file is not automatically a Lean proof. A formal proof is only relevant to the research claim if it formalizes the intended proposition.

Negative controls are part of the method. They test whether the verification pipeline detects selected mutations, such as a wrong sign, index, quotient relation, phase constraint, or closure depth. Passing a negative control does not prove the positive claim; it establishes only that the test detects that mutation.

11. Current governance boundary

The repository's top-level README records the following governance state as of its latest update:

- C3: OPEN
- C4: BLOCKED
- Lean: OPEN
- SDS-002: QUARANTINED
- Publication: BLOCKED
- Promotion: BLOCKED

These are governance states, not claims that every mathematical line is false or incomplete in the same way. Individual results may have paper-level arguments, finite computational support, or other evidence; each must be assessed against its own source artifacts and obligations.

The repository also preserves a distinction between the live verification namespace under

"AQARION-QUANTARION-AI/verification/"

and historical documentation that describes obsolete paths. A documented path is not proof that a file exists or ran.

12. What remains to be done

The research program's next steps are evidence-driven rather than badge-driven:

1. Replay the designated PB-CORE bounded audit and arithmetic verification in a clean, recorded environment.
2. Audit the source and receipt bindings against the exact repository revision.
3. Formalize the periodic-core restriction/extension argument and check the intended theorem in Lean.
4. Complete the specification and proof audit for the general counting formula.
5. Complete the finite JOIN-STABILITY proof/formalization and preserve the infinite counterexample boundary.
6. Establish the general AQ-K2R closure-depth theorem from its family definition, not only sample values.
7. Audit the reduced-Gram theorem's hypotheses and generality before expanding its claim.
8. Keep novelty review, reproducibility, formalization, and publication approval as distinct gates.

The ordering should be updated only after inspecting the actual live files, receipts, and dependencies; this list is a public-facing summary, not a substitute for the detailed project ledger.

13. Research philosophy

AQARION preserves corrections, failed approaches, counterexamples, and superseded claims. This is deliberate. A failed argument can define the boundary of a theorem; a counterexample can expose a missing hypothesis; a rejected verifier can establish a concrete independence requirement.

The objective is not to maximize the number of green checks. It is to maximize the reliability of the strongest statement that the available evidence supports.

«AQARION connects finite-dynamical mathematics with auditable computation and formal verification, while keeping theoremhood, computation, independence, reproducibility, provenance, and publication status distinct.»

That is the research program's public claim—and the evidence discipline by which the program should be judged.
