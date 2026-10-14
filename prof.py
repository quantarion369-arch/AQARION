import itertools, random, sys, time
from fractions import Fraction as F
def rgs(n):
    def rec(i,lab,m):
        if i==n: yield tuple(lab); return
        for l in range(m+1):
            lab.append(l); yield from rec(i+1,lab,max(m,l+1) if l==m else m); lab.pop()
    yield from rec(0,[],0)
class Basis:
    def __init__(s): s.rows={}
    def add(s,v):
        v=[F(x) for x in v]
        for p,r in s.rows.items():
            if v[p]!=0:
                c=v[p]; v=[a-c*b for a,b in zip(v,r)]
        for p,x in enumerate(v):
            if x!=0:
                v=[a/x for a in v]
                for q,r in list(s.rows.items()):
                    if r[p]!=0:
                        c=r[p]; s.rows[q]=[a-c*b for a,b in zip(r,v)]
                s.rows[p]=v; return True
        return False
    def dim(s): return len(s.rows)
def profile(T,lab):
    n=len(T); k=max(lab)+1; B=Basis()
    for b in range(k): B.add([1 if lab[x]==b else 0 for x in range(n)])
    delta=[]; cur=list(range(n))
    while True:
        cur=[T[x] for x in cur]; before=B.dim()
        for b in range(k): B.add([1 if lab[cur[x]]==b else 0 for x in range(n)])
        d=B.dim()-before
        if d==0: break
        delta.append(d)
    return k,tuple(delta)
def stable_size(T,lab):
    cur=list(lab); cnt=len(set(cur))
    while True:
        mp={}; new=[mp.setdefault((cur[x],cur[T[x]]),len(mp)) for x in range(len(T))]
        if len(mp)==cnt: return cnt
        cur,cnt=new,len(mp)
def check(n,maps,stats,viol):
    P=list(rgs(n)); cases=0
    for T in maps:
        for lab in P:
            k,delta=profile(T,lab); s=stable_size(T,lab); C=sum(delta)
            prod=1
            for d in delta: prod*=(1+d)
            ub=k*(prod-1); cases+=1
            if not (C<=s-k<=ub): viol.append((T,lab,k,delta,s))
            key=(k,delta); st=stats.setdefault(key,[10**9,-1,ub,0,0])
            st[0]=min(st[0],s-k); st[1]=max(st[1],s-k); st[3]+=(s-k==C); st[4]+=1
    return cases
if __name__=="__main__":
    stats={}; viol=[]; t0=time.time(); tot=0
    for n in range(1,int(sys.argv[1])+1):
        tot+=check(n,itertools.product(range(n),repeat=n),stats,viol)
        print(f"n<={n}: cases={tot} violations={len(viol)} ({time.time()-t0:.0f}s)",flush=True)
    print("violations:",viol[:3])
