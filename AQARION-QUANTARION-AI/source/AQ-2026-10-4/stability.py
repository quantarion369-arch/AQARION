"""Pullback-stable / congruence checks for finite deterministic maps"""
def rel_from_partition(part):
    n=len(part)
    rel=set()
    for i in range(n):
        for j in range(n):
            if part[i]==part[j]:
                rel.add((i,j))
    return rel

def is_congruence(T, part):
    """x~y => T(x)~T(y) (quotient well-defined)"""
    rel=rel_from_partition(part)
    for (x,y) in rel:
        if (T[x], T[y]) not in rel:
            return False
    return True

def join_partitions(p,q):
    """E ∨ F = transitive closure of union"""
    n=len(p)
    parent=list(range(n))
    def find(a):
        while parent[a]!=a:
            parent[a]=parent[parent[a]]
            a=parent[a]
        return a
    def union(a,b):
        ra=find(a); rb=find(b)
        if ra!=rb:
            parent[rb]=ra
    for i in range(n):
        for j in range(n):
            if p[i]==p[j] or q[i]==q[j]:
                union(i,j)
    labels={}; nxt=0; res=[0]*n
    for i in range(n):
        r=find(i)
        if r not in labels:
            labels[r]=nxt; nxt+=1
        res[i]=labels[r]
    return tuple(res)
