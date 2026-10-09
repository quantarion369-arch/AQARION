import itertools, numpy as np
def parts(n):
    r=[]
    def rec(rem,cur):
        if not rem: r.append([b[:] for b in cur]); return
        x=rem[0]; rest=rem[1:]
        for i in range(len(cur)):
            nw=[b[:] for b in cur]; nw[i].append(x); rec(rest,nw)
        rec(rest,cur+[[x]])
    rec(list(range(n)),[]); return r
def rank_oracle(f,B):
    idx={x:k for k,b in enumerate(B) for x in b}
    k=len(B); par=list(range(k))
    def find(a):
        while par[a]!=a: par[a]=par[par[a]]; a=par[a]
        return a
    for b in B:
        S=sorted({idx[f[x]] for x in b})
        for s in S[1:]: par[find(s)]=find(S[0])
    return k-len({find(a) for a in range(k)})
tot=bad=0
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
   if rank_oracle(f,B)!=r: bad+=1
print(tot, bad) # expect 166475 0
