#!/usr/bin/env python3
# Explicit minimal Z^(n+1)-graded free resolution of R_n = k[S] over P, built degree by degree
# (linear algebra mod 32003), then checked: Betti table, d^2=0 over Z, coefficients, exactness mod 2,3,5.
# Usage: python3 n_resolution.py 3   or   python3 n_resolution.py 4     (needs numpy)
import sys, time
from math import comb
from collections import defaultdict
import numpy as np
n=int(sys.argv[1]) if len(sys.argv)>1 else 3
P=32003
def gens_vec(n):
    V=[tuple([0]*n+[-1])]
    for i in range(n): V.append(tuple(1 if j==i else 0 for j in range(n))+(0,))
    for i in range(n): V.append(tuple(0 if j==i else 1 for j in range(n))+(1,))
    V.append(tuple([1]*n+[2])); return V
def wt(b): return sum(b[:-1])-b[-1]
V=gens_vec(n); nv=len(V); vw=[wt(v) for v in V]; dim=n+1
TOP=n*(n-1); WMAX=max(TOP,8); L=n+1
t0=time.time()
def log(*a): print("[%5.0fs]"%(time.time()-t0),*a,flush=True)
out=[]
def rec(i,left,cur):
    if i==nv: out.append(tuple(cur)); return
    for e in range(left//vw[i]+1):
        cur.append(e); rec(i+1,left-e*vw[i],cur); cur.pop()
rec(0,WMAX,[])
def degof(u): return tuple(sum(u[i]*V[i][c] for i in range(nv)) for c in range(dim))
fiber=defaultdict(list)
for u in out: fiber[degof(u)].append(u)
degs=sorted(fiber,key=wt)
log("n=%d: %d monomials, %d multidegrees up to weight %d"%(n,len(out),len(degs),WMAX))
def rref(M,p):
    M=M.copy()%p; r=0; rows,cols=M.shape; piv=[]
    for c in range(cols):
        if r>=rows: break
        nz=np.nonzero(M[r:,c])[0]
        if len(nz)==0: continue
        q=r+nz[0]
        if q!=r: M[[r,q]]=M[[q,r]]
        M[r]=(M[r]*pow(int(M[r,c]),p-2,p))%p
        col=M[:,c].copy(); col[r]=0
        idx=np.nonzero(col)[0]
        if len(idx): M[idx]=(M[idx]-np.outer(col[idx],M[r]))%p
        piv.append(c); r+=1
    return M[:r],piv
def nullspace(M,p):
    rows,cols=M.shape
    if rows==0: return np.eye(cols,dtype=np.int64)
    R,piv=rref(M,p); ps=set(piv); res=[]
    for f in range(cols):
        if f in ps: continue
        v=np.zeros(cols,dtype=np.int64); v[f]=1
        for ri,pc in enumerate(piv): v[pc]=(-R[ri,f])%p
        res.append(v)
    return np.array(res,dtype=np.int64).reshape(len(res),cols)
def sub(b,s): return tuple(x-y for x,y in zip(b,s))
def addm(u,v): return tuple(a+b for a,b in zip(u,v))
zero=(0,)*dim
gens=[[(zero,0)]]+[[] for _ in range(L+1)]
D=[None]+[[] for _ in range(L+1)]
def basis(i,b):
    res=[]
    for j,(s,w) in enumerate(gens[i]):
        d=sub(b,s)
        if d in fiber:
            for u in fiber[d]: res.append((j,u))
    return res
def apply(i,j,u): return {(k,addm(u,v)):c for (k,v),c in D[i][j].items()}
def process(b):
    for i in range(0,L):
        Bi=basis(i,b)
        if not Bi: continue
        idx_i={x:r for r,x in enumerate(Bi)}
        if i==0: M=np.ones((1,len(Bi)),dtype=np.int64)
        else:
            Br=basis(i-1,b); idx_r={x:r for r,x in enumerate(Br)}
            M=np.zeros((len(Br),len(Bi)),dtype=np.int64)
            for c,(j,u) in enumerate(Bi):
                for key,val in apply(i,j,u).items(): M[idx_r[key],c]=(M[idx_r[key],c]+val)%P
        K=nullspace(M,P)
        if K.shape[0]==0: continue
        imgs=[]
        for j2,(t,w) in enumerate(gens[i+1]):
            d=sub(b,t)
            if d in fiber:
                for u2 in fiber[d]:
                    vec=np.zeros(len(Bi),dtype=np.int64)
                    for key,val in apply(i+1,j2,u2).items(): vec[idx_i[key]]=(vec[idx_i[key]]+val)%P
                    imgs.append(vec)
        if imgs: R,piv=rref(np.array(imgs,dtype=np.int64),P)
        else: R,piv=np.zeros((0,len(Bi)),dtype=np.int64),[]
        rank=len(piv)
        for v in K:
            R2,p2=rref(np.vstack([R,v[None,:]]) if rank else v[None,:],P)
            if len(p2)>rank:
                R,rank=R2,len(p2)
                gens[i+1].append((b,wt(b)))
                D[i+1].append({Bi[c]:int(v[c]) for c in np.nonzero(v)[0]})
for pos,b in enumerate(degs):
    process(b)
    if pos%2000==0: log("built through degree index %d / %d (weight %d); generators so far %s"%(pos,len(degs),wt(b),[len(g) for g in gens[:L+1]]))
ok=True
def report(name,cond):
    global ok
    ok&=bool(cond); log(("PASS " if cond else "FAIL ")+name)
def formula(n):
    d=n-2; F=defaultdict(int); F[(0,0)]=1; F[(n+1,n*(n-1))]+=1
    for k in range(1,n+1):
        for dg,cf in (((k-1)*d+2,(n-k+1)*comb(n,k-2) if k>=2 else 0),(k*d+1,2*(n-k+1)*comb(n,k-1)),((k+1)*d,k*comb(n,k+1) if k+1<=n else 0)):
            if cf: F[(k,dg)]+=cf
    return dict(F)
tab=defaultdict(int)
for i in range(L+2):
    for (s,w) in gens[i]: tab[(i,w)]+=1
report("Betti table (homological degree, weight) equals the formula; totals %s"%[len(g) for g in gens[:L+1]], dict(tab)==formula(n) and not gens[L+1])
def sym(x):
    x%=P; return x-P if x>P//2 else x
for i in range(1,L+1): D[i]=[{k:sym(c) for k,c in d.items()} for d in D[i]]
coefs=set(); terms=defaultdict(int)
for i in range(1,L+1):
    for dct in D[i]:
        per=defaultdict(int)
        for (k,u),c in dct.items(): coefs.add(c); per[k]+=1
        for v in per.values(): terms[v]+=1
report("every coefficient is +1 or -1 (entries: %s)"%dict(terms), coefs<={-1,1})
bad=0
for i in range(2,L+1):
    for j in range(len(gens[i])):
        acc=defaultdict(int)
        for (k,u),c in D[i][j].items():
            for key,c2 in apply(i-1,k,u).items(): acc[key]+=c*c2
        if any(acc.values()): bad+=1
report("d^2 = 0 over the integers", bad==0)
aug_bad=sum(1 for dct in D[1] if sum(dct.values())!=0)
report("augmentation eps*d_1 = 0 exactly over the integers (every first-syzygy column has coefficient sum 0)", aug_bad==0)
import json,hashlib
cert={"n":n,"gens":[[[list(s),w] for (s,w) in g] for g in gens[:L+1]],"D":[None]+[[[[k,list(u),c] for (k,u),c in dct.items()] for dct in D[i]] for i in range(1,L+1)]}
blob=json.dumps(cert,sort_keys=True).encode()
open("resolution_n%d.json"%n,"wb").write(blob)
log("wrote resolution_n%d.json (%d bytes) sha256 %s"%(n,len(blob),hashlib.sha256(blob).hexdigest()))
def rank_p(M,p):
    return len(rref(M,p)[1])
def ranks_at(b,p):
    rk={}
    for i in range(1,L+1):
        Bi=basis(i,b)
        if not Bi: rk[i]=0; continue
        Br=basis(i-1,b); idx_r={x:r for r,x in enumerate(Br)}
        M=np.zeros((len(Br),len(Bi)),dtype=np.int64)
        for c,(j,u) in enumerate(Bi):
            for key,val in apply(i,j,u).items(): M[idx_r[key],c]+=val
        rk[i]=rank_p(M,p)
    rk[L+1]=0; return rk
for p in (2,3,5):
    bad=0
    for b in degs:
        rk=ranks_at(b,p); dims=[len(basis(i,b)) for i in range(L+1)]
        good=(dims[0]-1==rk[1])
        for i in range(1,L+1): good&=(dims[i]==rk[i]+rk[i+1])
        bad+=(not good)
    report("exact over F_%d in all %d multidegrees up to weight %d"%(p,len(degs),WMAX), bad==0)
print("ALL PASS" if ok else "SOME CHECK FAILED")
sys.exit(0 if ok else 1)
