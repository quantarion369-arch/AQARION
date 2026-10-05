"""
AQARION AQ-2026-10-4 - Corrected join logic
H_AQ-001A/C : Congruence join closure (what this package actually proves)
H_AQ-001_PB : PB-Join closure (separate, OPEN)

Distinction:
- congruence (forward-compatible): E ⊆ T*E  :=  x~y => T(x)~T(y)
- PB-stable (backward):           T*E ⊆ E  :=  T(x)~T(y) => x~y
- finite PB-rigid:                T*E = E
"""

from .stability import is_congruence, is_pb_stable, join_partitions

def is_congruence_join_closed(T, partitions):
    """Check that join of two congruences remains a congruence."""
    for i, E in enumerate(partitions):
        if not is_congruence(T, E):
            continue
        for F in partitions[i+1:]:
            if not is_congruence(T, F):
                continue
            J = join_partitions(E, F)
            if not is_congruence(T, J):
                return False, (E, F, J)
    return True, None
