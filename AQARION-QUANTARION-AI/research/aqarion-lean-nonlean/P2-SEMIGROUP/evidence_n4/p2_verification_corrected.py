#!/usr/bin/env python3
# Corrected companion to p2_verification_FINAL.py (that file is kept unchanged as the failed attempt).
# Fixes: (1) Hochster with a standard augmented reduced chain complex; (2) Taylor (x) k differential keeps
# an entry only when lcm(s) == lcm(s minus i) (otherwise the coefficient is a nonunit monomial, zero in k);
# (3) no Koszul "transfer": A, C regular on R_n means Betti(R_n over P) = Betti(S/M_n over S).
import itertools, sys
from collections import defaultdict
def get_generators(n):
    return ([(i,i+n) for i in range(n)]+[(i+n,j+n) for i,j in itertools.combinations(range(n),2)]
            +[tuple(j for j in range(n) if j!=i) for i in range(n)])
def rank_gf(mat,p):
    if not mat or not mat[0]: return 0
    m=[row[:] for row in mat]; rows,cols=len(m),len(m[0]); rank=0
    for c in range(cols):
        piv=-1
        for r in range(rank,rows):
            if m[r][c]%p: piv=r;break
        if piv==-1: continue
        m[rank],m[piv]=m[piv],m[rank]
        inv=pow(m[rank][c],p-2,p)
        for j in range(c,cols): m[rank][j]=(m[rank][j]*inv)%p
        for r in range(rows):
            if r!=rank and m[r][c]%p:
                f=m[r][c]
                for j in range(c,cols): m[r][j]=(m[r][j]-f*m[rank][j])%p
        rank+=1
    return rank
def hochster(n,p):
    gens=[set(g) for g in get_generators(n)]; V=2*n; betti=defaultdict(int)
    for r in range(V+1):
        for W in itertools.combinations(range(V),r):
            by=defaultdict(list)
            for k in range(len(W)+1):
                for face in itertools.combinations(W,k):
                    fs=set(face)
                    if not any(g<=fs for g in gens): by[k-1].append(face)
            maxd=max(by); rk={}
            for d in range(0,maxd+1):
                idx={f:i for i,f in enumerate(by[d-1])}
                mat=[[0]*len(by[d]) for _ in by[d-1]]
                for c,f in enumerate(by[d]):
                    for i in range(len(f)): mat[idx[f[:i]+f[i+1:]]][c]=1 if i%2==0 else p-1
                rk[d]=rank_gf(mat,p)
            for d in range(-1,maxd+1):
                h=len(by[d])-rk.get(d,0)-rk.get(d+1,0)
                if h>0: betti[(len(W)-d-1,len(W))]+=h
    return dict(betti)
def taylor_tensor_k(n,p):
    gens=get_generators(n); N=len(gens)
    lc=lambda s:frozenset().union(*(gens[i] for i in s)) if s else frozenset()
    by={r:list(itertools.combinations(range(N),r)) for r in range(N+1)}; ranks={}
    for r in range(1,N+1):
        idx={s:i for i,s in enumerate(by[r-1])}
        mat=[[0]*len(by[r]) for _ in by[r-1]]
        for c,s in enumerate(by[r]):
            la=lc(s)
            for i in range(len(s)):
                sub=s[:i]+s[i+1:]
                if lc(sub)==la: mat[idx[sub]][c]=1 if i%2==0 else p-1
        ranks[r]=rank_gf(mat,p)
    return {r:len(by[r])-ranks.get(r,0)-ranks.get(r+1,0) for r in range(N+1) if len(by[r])-ranks.get(r,0)-ranks.get(r+1,0)}
P=32003; ok=True
for n in (3,4):
    t=hochster(n,P); b=[sum(v for (i,j),v in t.items() if i==k) for k in range(2*n+1)]
    print("n=%d Hochster Betti of S/M_n: %s total %d"%(n,[x for x in b if x],sum(b)),flush=True)
    ok&=(sum(b)==(36 if n==3 else 100))
tb=taylor_tensor_k(3,P); print("n=3 Taylor(x)k Betti:",tb,"total",sum(tb.values())); ok&=(sum(tb.values())==36)
print("Betti(R_n over P) = Betti(S/M_n over S) when A,C regular on R_n: R_3 total 36, R_4 total 100")
print("ALL PASS" if ok else "CHECK FAILED"); sys.exit(0 if ok else 1)
