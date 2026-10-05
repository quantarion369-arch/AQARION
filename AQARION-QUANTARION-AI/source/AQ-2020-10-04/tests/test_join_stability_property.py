import itertools
from src.aqarion.stability import is_congruence, join_partitions
from src.aqarion.defect import is_nilpotent_D2

def all_maps(n):
    for prod in itertools.product(range(n), repeat=n):
        yield prod

def all_partitions(n):
    seen=set()
    def rec(i, maxv, cur):
        if i==n:
            mapping={}; nxt=0; can=[]
            for x in cur:
                if x not in mapping:
                    mapping[x]=nxt; nxt+=1
                can.append(mapping[x])
            t=tuple(can)
            if t not in seen:
                seen.add(t)
            return
        for v in range(maxv+1):
            cur[i]=v
            rec(i+1, max(maxv, v+1), cur)
        cur[i]=maxv+1
        rec(i+1, maxv+1, cur)
    rec(1,0,[0]*n)
    return list(seen)

def test_D2_nilpotency():
    for n in [2,3,4]:
        for T in all_maps(n):
            for p in all_partitions(n):
                assert is_nilpotent_D2(T,p), f"D^2!=0 for n={n} T={T} p={p}"

def test_join_stable_n4():
    n=4
    for T in all_maps(n):
        parts=all_partitions(n)
        congs=[p for p in parts if is_congruence(T,p)]
        for i in range(len(congs)):
            for j in range(len(congs)):
                jn=join_partitions(congs[i], congs[j])
                assert is_congruence(T,jn), f"join failed for T={T}"
