"""Join-stability theorem PB_001"""
from.stability import is_congruence, join_partitions

def test_join_stability_for_T(T, congruences):
    """Returns (total, fails) for this T"""
    total=0; fails=0
    for i in range(len(congruences)):
        for j in range(i, len(congruences)):
            total+=1
            p=congruences[i]; q=congruences[j]
            jn=join_partitions(p,q)
            if not is_congruence(T, jn):
                fails+=1
    return total, fails
