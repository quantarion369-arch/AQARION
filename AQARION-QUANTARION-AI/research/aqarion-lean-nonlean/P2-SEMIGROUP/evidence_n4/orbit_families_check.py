#!/usr/bin/env python3
# Brute-force check of the five-family orbit classification of reduced homology of induced subcomplexes of Delta(M_n).
# Needs numpy. n=3..8, fields F_2 and F_32003; one representative per (s,t,r) orbit.
import itertools, sys
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
        M=np.zeros((len(by[d-1]),len(by[d])),dtype=np.int64)
        for f,ci in idx[d].items():
            for k in range(len(f)): M[idx[d-1][f[:k]+f[k+1:]],ci]=(1 if k%2==0 else p-1)
        ranks[d]=rank_mod(M,p)
    H={}
    for d in range(-1,maxd+1):
        h=len(by[d])-ranks[d]-ranks.get(d+1,0)
        if h: H[d]=h
    return H
def predicted(n,s,t,r):
    if s==0 and t==0: return {-1:1}
    if s==0 and t>=2: return {0:t-1}
    if s==1 and r==1: return {0:1}
    if s==n-1 and r==t: return {n-3:1}
    if s==n and t<n: return {n-3:n-t-1} if t<=n-2 else {}
    if s==n and t==n and r==n: return {n-2:1}
    return {}
bad=0; checked=0
for n in range(3,9):
    for p in (2,32003):
        for s in range(n+1):
            for t in range(n+1):
                for r in range(0,min(s,t)+1):
                    if s+t-r>n: continue
                    H=red_hom(induced_complex(n,tuple(range(s)),tuple(range(s-r,s-r+t))),p); checked+=1
                    if H!=predicted(n,s,t,r): bad+=1; print("MISMATCH",n,p,s,t,r,H,predicted(n,s,t,r))
    print("n=%d done"%n,flush=True)
print("%d orbit checks, %d mismatches"%(checked,bad)); print("ALL PASS" if bad==0 else "CHECK FAILED"); sys.exit(0 if bad==0 else 1)
