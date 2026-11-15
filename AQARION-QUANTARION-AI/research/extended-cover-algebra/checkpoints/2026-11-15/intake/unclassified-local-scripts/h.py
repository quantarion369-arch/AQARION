import itertools as it
from collections import Counter
def subs(n,k):
    for piv in it.combinations(range(n),k):
        free=[(i,c) for i in range(k) for c in range(piv[i]+1,n) if c not in piv]
        for bits in range(1<<len(free)):
            G=[[0]*n for _ in range(k)]
            for i,p in enumerate(piv): G[i][p]=1
            for j,(i,c) in enumerate(free):
                if (bits>>j)&1: G[i][c]=1
            yield [sum(G[i][c]<<i for i in range(k)) for c in range(n)]
def rk(cols,d):
    cur={0}
    for _ in range(d): cur={s^c for s in cur for c in cols}|cur
    return len(cur)
for n in range(3,8):
    for k in range(1,n):
        cnt=Counter(); t=0
        for cols in subs(n,k):
            cnt[(1<<k)-rk(cols,k-1)]+=1; t+=1
        print(n,k,k-1,t,dict(sorted(cnt.items())))
        assert set(cnt)<={0,1}
print("deficit always 0 or 1")
