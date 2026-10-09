import itertools, numpy as np
from rank import parts, rank_oracle
def comps(k, groups, only=None):
    par=list(range(k))
    def find(a):
        while par[a]!=a: par[a]=par[par[a]]; a=par[a]
        return a
    for S in groups:
        S=sorted(S)
        for s in S[1:]: par[find(s)]=find(S[0])
    nodes=range(k) if only is None else only
    return len({find(a) for a in nodes})
def variants(f,B):
    idx={x:k for k,b in enumerate(B) for x in b}
    k=len(B); img=[{idx[f[x]] for x in b} for b in B]
    touched=set().union(*img) if img else set()
    pre={}
    for i in range(k):
        for j in img[i]: pre.setdefault(j,set()).add(i)
    return {
        "TRUE": k-comps(k,img),
        "ignore isolated": k-comps(k,img, sorted(touched)),
        "preimage": k-comps(k, list(pre.values())),
        "c": comps(k,img),
        "k-c-1": k-comps(k,img)-1,
        "first": k-comps(k, [[idx[f[b[0]]]] for b in B])
    }
tot=0; kills={}
for n in (3,4,5):
 for f in itertools.product(range(n), repeat=n):
  for B in parts(n):
   tot+=1
   K=np.zeros((n,n))
   for x in range(n): K[x,f[x]]=1
   P=np.zeros((n,n))
   for b in B:
    for i in b:
     for j in b: P[i,j]=1/len(b)
   r=int(np.linalg.matrix_rank((np.eye(n)-P)@K@P, tol=1e-9))
   for name,v in variants(f,B).items():
    if v!=r: kills[name]=kills.get(name,0)+1
print(tot, kills) # TRUE 0, ignore 77819, preimage 77819, c 129387, k-c-1 166475, first 125348
