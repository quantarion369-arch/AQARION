#!/usr/bin/env python3
# Hochster-formula Betti tables of S/M_n for n=3..9 (M_n squarefree), by orbit counting. Needs numpy.
# Compares each table with the closed formula for the Betti table of R_n over F_2 and F_32003.
import itertools, sys, time
from math import comb, factorial
from collections import defaultdict
import numpy as np
def rank_mod(M,p):
    M=M.copy()%p; r=0; rows,cols=M.shape
    for c in range(cols):
        if r>=rows: break
        nz=np.nonzero(M[r:,c])[0]
        if len(nz)==0: continue
        q=r+nz[0]
        if q!=r: M[[r,q]]=M[[q,r]]
        if p>2: M[r]=(M[r]*pow(int(M[r,c]),p-2,p))%p
        col=M[:,c].copy(); col[r]=0
        idx=np.nonzero(col)[0]
        if len(idx): M[idx]=(M[idx]-np.outer(col[idx],M[r]))%p
        r+=1
    return r
def induced_complex(n,SE,SB):
    # faces of the Stanley-Reisner complex of M_n restricted to the vertex set SE (E's) and SB (B's):
    # at most n-2 of the E's, at most one B_i, and B_i never together with E_i
    faces=[]
    for r in range(0,min(len(SE),n-2)+1):
        for FE in itertools.combinations(SE,r):
            faces.append(FE)
            for i in SB:
                if i not in FE: faces.append(FE+(n+i,))
    return faces
def red_hom(faces,p):
    by=defaultdict(list)
    for f in faces: by[len(f)-1].append(tuple(sorted(f)))
    maxd=max(by); idx={d:{f:i for i,f in enumerate(by[d])} for d in by}
    ranks={-1:0,maxd+1:0}
    for d in range(0,maxd+1):
        rows=len(by[d-1]); cols=len(by[d]); M=np.zeros((rows,cols),dtype=np.int64)
        for f,ci in idx[d].items():
            for k in range(len(f)):
                g=f[:k]+f[k+1:]
                M[idx[d-1][g],ci]=(1 if k%2==0 else p-1)
        ranks[d]=rank_mod(M,p)
    H={}
    for d in range(-1,maxd+1):
        h=len(by[d])-ranks[d]-ranks.get(d+1,0)
        if h: H[d]=h
    return H
def formula(n):
    d=n-2; F=defaultdict(int); F[(0,0)]=1; F[(n+1,n*(n-1))]+=1
    for k in range(1,n+1):
        for dg,cf in (((k-1)*d+2,(n-k+1)*comb(n,k-2) if k>=2 else 0),(k*d+1,2*(n-k+1)*comb(n,k-1)),((k+1)*d,k*comb(n,k+1) if k+1<=n else 0)):
            if cf: F[(k,dg)]+=cf
    return dict(F)
def hochster(n,p):
    d=n-2; tab=defaultdict(int)
    for s in range(n+1):
        for t in range(n+1):
            for r in range(0,min(s,t)+1):
                if s+t-r>n: continue
                size=factorial(n)//(factorial(r)*factorial(s-r)*factorial(t-r)*factorial(n-s-t+r))
                SE=tuple(range(s)); SB=tuple(range(s-r,s-r+t))
                for deg,h in red_hom(induced_complex(n,SE,SB),p).items():
                    tab[(s+t-deg-1,s+t*d)]+=h*size
    return dict(tab)
ok=True; t0=time.time()
for n in range(3,10):
    for p in (2,32003):
        tab=hochster(n,p); good=(tab==formula(n)); ok&=good
        tot=[sum(v for (i,w),v in tab.items() if i==k) for k in range(n+2)]
        print(("PASS" if good else "FAIL"),"n=%d char %d: Betti totals %s equal the closed formula"%(n,p,tot),"[%.0fs]"%(time.time()-t0),flush=True)
print("ALL PASS" if ok else "SOME CHECK FAILED"); sys.exit(0 if ok else 1)
