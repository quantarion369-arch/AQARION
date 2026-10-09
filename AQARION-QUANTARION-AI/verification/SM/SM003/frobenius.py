import itertools, numpy as np
from fractions import Fraction as Fr
def parts(n):
    r=[]
    def rec(rem,cur):
        if not rem: r.append([b[:] for b in cur]); return
        x=rem[0]; rest=rem[1:]
        for i in range(len(cur)):
            nw=[b[:] for b in cur]; nw[i].append(x); rec(rest,nw)
        rec(rest,cur+[[x]])
    rec(list(range(n)),[]); return r
tot=be=bi=0
for n in (3,4,5):
 for f in itertools.product(range(n), repeat=n):
  for B in parts(n):
   tot+=1
   idx={x:k for k,b in enumerate(B) for x in b}
   s=Fr(0); si=Fr(0)
   for i,b in enumerate(B):
    for j,c in enumerate(B):
     m=sum(1 for x in b if idx[f[x]]==j)
     s+=Fr(m*(len(b)-m), len(b)*len(c))
     si+=Fr(m*(len(b)-m)//(len(b)*len(c)))
   K=np.zeros((n,n))
   for x in range(n): K[x,f[x]]=1
   P=np.zeros((n,n))
   for b in B:
    for i in b:
     for j in b: P[i,j]=1/len(b)
   fro=float((((np.eye(n)-P)@K@P)**2).sum())
   if abs(fro-float(s))>1e-9: be+=1
   if abs(fro-float(si))>1e-9: bi+=1
print(tot, be, bi) # expect 166475 0 125348
