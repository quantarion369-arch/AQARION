#!/usr/bin/env python3
# Track D: meet of equitable partitions is not equitable. Exact arithmetic, no packages.
# Matrices are RECONSTRUCTED to fit the printed receipts (simple 2-regular graph; unique under that constraint);
# the original matrix files were not available, so these are not claimed to be the originals.
from fractions import Fraction
import sys
X=range(6)
def adj(edges):
    A=[[Fraction(0)]*6 for _ in X]
    for a,b in edges: A[a][b]=A[b][a]=Fraction(1)
    return A
def valid(P): flat=[v for B in P for v in B]; return all(P) and sorted(flat)==list(X)
def cnt(A,v,C): return sum(A[v][w] for w in C)
def equitable(A,P):
    for B in P:
        for C in P:
            for v in B:
                for u in B:
                    if cnt(A,v,C)!=cnt(A,u,C): return False,(B,C,v,cnt(A,v,C),u,cnt(A,u,C))
    return True,None
def join(P,Q):
    par=list(X)
    def f(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    for part in (P,Q):
        for B in part:
            for v in B[1:]: par[f(v)]=f(B[0])
    g={}
    for v in X: g.setdefault(f(v),[]).append(v)
    return sorted(g.values())
def meet(P,Q): return sorted(sorted(set(B)&set(C)) for B in P for C in Q if set(B)&set(C))
def quotient(A,P):
    ok,fail=equitable(A,P)
    if not ok: raise ValueError(fail)
    return [[cnt(A,B[0],C) for C in P] for B in P]
W={"W1":([(0,3),(0,4),(3,4),(1,2),(1,5),(2,5)],[[0,1,2,3],[4,5]],[[0,1],[2,4],[3,5]]),
   "W2":([(0,1),(0,5),(1,5),(2,3),(2,4),(3,4)],[[0,3,4,5],[1,2]],[[0,2,3,5],[1,4]])}
ok_all=True
for name,(E,P,Q) in W.items():
    A=adj(E); print("==",name,"edges",E)
    assert valid(P) and valid(Q)
    J,M=join(P,Q),meet(P,Q)
    res=[equitable(A,x) for x in (P,Q,J,M)]
    print("P",res[0][0],"Q",res[1][0],"join",J,res[2][0],"meet",M,res[3][0])
    print("meet failure (B,C,v1,d1,u,d2):",res[3][1])
    ok=res[0][0] and res[1][0] and res[2][0] and (not res[3][0]) and res[3][1][3]!=res[3][1][5]
    print("quotients P,Q,join:",[[list(map(str,r)) for r in quotient(A,x)] for x in (P,Q,J)])
    T=[[x/2 for x in r] for r in A]
    print("A/2 row-stochastic:",all(sum(r)==1 and min(r)>=0 for r in T))
    print("WITNESS PASS" if ok else "NOT A WITNESS"); ok_all&=ok
print("ALL PASS" if ok_all else "CHECK FAILED"); sys.exit(0 if ok_all else 1)
