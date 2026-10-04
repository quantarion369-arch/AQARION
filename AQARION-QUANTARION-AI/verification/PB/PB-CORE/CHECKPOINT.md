PB-005 CHECKPOINT — ADVERSARIAL AUDIT

STATUS:
[P] mathematical proof
[V] independent finite reproduction
[R] literature comparison active
LEAN: OPEN
C4: BLOCKED

CORE RESULT:

Finite T:X→X
P = Per(T)

Stab(T)
  ≅
Con(P,T|P)

The transient trees disappear from the classification of
pullback-FIXED equivalences.

IMPORTANT DISTINCTION:

Forward invariant:
    E ⊆ T*E

Pullback stable:
    T*E ⊆ E

Pullback fixed:
    T*E = E

For finite X:

    T*E ⊆ E
        ⇒
    T*E = E

Therefore on the eventual permutation core,
forward invariance and pullback equality coincide.

COMPUTATIONAL STATUS:

873 permutations, n≤6:
    formula mismatches = 0

5,040 permutations, n=7:
    formula mismatches = 0

500 random permutations each:
    n=8: 0 mismatches
    n=9: 0 mismatches
    n=10: 0 mismatches

50,069 finite maps, n≤6:
    restriction failures = 0
    extension failures = 0

582,696 stable pairs, n≤6:
    join failures = 0

The attempted n=12 brute-force extension timed out.
NO RESULT is recorded.

LITERATURE WARNING:

Congruence theory for unary/monounary algebras is classical.
Cycle-divisor congruences are classical.
G-set congruence theory is classical.

Therefore PB-CORE must not claim discovery of those theories.

The research question is narrower:

Can the exact pullback-fixed finite-dynamics classification
be expressed cleanly as an eventual-permutation-core theorem,
with an explicit cycle-index/common-divisor/phase formula,
and an auditable executable verification surface?

That question remains the appropriate AQARION research target.

NEXT ATTACK:

1. Search the monounary literature specifically for the exact
   multi-cycle phase-count formula.

2. Compare PB-005 against existing descriptions of finite
   monounary congruences.

3. Prove the phase-count formula independently by orbit/stabilizer
   arguments rather than relying on enumeration.

4. Test whether the formula extends naturally from a permutation
   to arbitrary finite cyclic group actions.

5. Only after that decide whether PB-005 contains a publishable
   mathematical novelty beyond repackaging and verification.

https://github.com/quantarion369-arch/AQARION/tree/main/AQARION-QUANTARION-AI/verification/PB/PACKAGES/EDUCATIONAL

https://github.com/quantarion369-arch/AQARION/tree/main/AQARION-QUANTARION-AI/verification/PB/PB-CORE
