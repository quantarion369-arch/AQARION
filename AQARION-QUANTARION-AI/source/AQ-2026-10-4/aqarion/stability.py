"""
stability.py - corrected distinction between congruence and PB-stability
"""

def _partition_to_rel(partition, n):
    """partition: list of blocks, each block list of elements 0..n-1"""
    rel = {}
    for block in partition:
        for x in block:
            for y in block:
                rel[(x,y)] = True
    return rel

def _rel_from_partition(partition):
    s = set()
    for block in partition:
        for x in block:
            for y in block:
                s.add((x,y))
    return s

def is_congruence(T, partition):
    """
    Congruence / forward-compatible: E ⊆ T*E
    x~y => T(x)~T(y)
    """
    rel = _rel_from_partition(partition)
    n = len(T)
    for x in range(n):
        for y in range(n):
            if (x,y) in rel:
                if (T[x], T[y]) not in rel:
                    return False
    return True

def is_pb_stable(T, partition):
    """
    PB-stable / backward: T*E ⊆ E
    T(x)~T(y) => x~y
    This is the condition for the disputed PB-Join theorem.
    """
    rel = _rel_from_partition(partition)
    n = len(T)
    for x in range(n):
        for y in range(n):
            if (T[x], T[y]) in rel:
                if (x,y) not in rel:
                    return False
    return True

def join_partitions(E, F):
    """Transitive closure of union of two partitions."""
    # Collect all elements
    elems = set()
    for block in E:
        elems.update(block)
    for block in F:
        elems.update(block)
    elems = sorted(elems)
    parent = {x:x for x in elems}
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]
            x=parent[x]
        return x
    def union(a,b):
        ra, rb = find(a), find(b)
        if ra!=rb:
            parent[rb]=ra
    for block in E:
        for i in range(1,len(block)):
            union(block[0], block[i])
    for block in F:
        for i in range(1,len(block)):
            union(block[0], block[i])
    groups = {}
    for x in elems:
        r=find(x)
        groups.setdefault(r, []).append(x)
    return list(groups.values())
