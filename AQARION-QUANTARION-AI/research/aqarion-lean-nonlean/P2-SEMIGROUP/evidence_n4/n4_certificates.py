#!/usr/bin/env python3
# n=4 certificates for the AQARION P2 research note (unreviewed). Pure Python, no packages.
import itertools, sys
from math import comb
from collections import defaultdict
VARS=['A','C','E0','E1','E2','E3','B0','B1','B2','B3']
IDX={v:i for i,v in enumerate(VARS)}
WT=(4,1,2,2,2,2,4,4,4,4)  # positive weights; ties broken by larger exponent tuple
def mono(*names):
    u=[0]*10
    for x in names: u[IDX[x]]+=1
    return tuple(u)
def key(u): return (sum(a*b for a,b in zip(WT,u)),u)
def lead(p): return max(p,key=key)
def padd(p,q,c=1):
    r=dict(p)
    for u,v in q.items():
        r[u]=r.get(u,0)+c*v
        if r[u]==0: del r[u]
    return r
def pmul(m,p): return {tuple(a+b for a,b in zip(m,u)):v for u,v in p.items()}
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
G=[]
for i in range(4):
    Es=['E%d'%j for j in range(4) if j!=i]
    G.append({mono('A','B%d'%i):1, mono(*Es):-1})
    G.append({mono('E%d'%i,'B%d'%i):1, mono('A','C'):-1})
for i in range(4):
    for j in range(i+1,4):
        l=[x for x in range(4) if x not in (i,j)]
        G.append({mono('B%d'%i,'B%d'%j):1, mono('C','E%d'%l[0],'E%d'%l[1]):-1})
G.append({mono('A','A','C'):1, mono('E0','E1','E2','E3'):-1})
LEADS=[lead(g) for g in G]
ok_all=True
def report(name,ok):
    global ok_all
    ok_all&=bool(ok); print(("PASS " if ok else "FAIL ")+name, flush=True)
# (1) Groebner: derive a standard representation for every non-coprime S-pair, then re-verify it
expected={mono('A','B%d'%i) for i in range(4)}|{mono('E%d'%i,'B%d'%i) for i in range(4)}|\
  {mono('B%d'%i,'B%d'%j) for i in range(4) for j in range(i+1,4)}|{mono('A','A','C')}
report("15 leading monomials equal the claimed initial ideal L", set(LEADS)==expected and len(set(LEADS))==15)
pairs=[(i,j) for i,j in itertools.combinations(range(15),2) if not all(min(x,y)==0 for x,y in zip(LEADS[i],LEADS[j]))]
cert={}
for (i,j) in pairs:
    L=tuple(max(x,y) for x,y in zip(LEADS[i],LEADS[j]))
    p=padd(pmul(sub(L,LEADS[i]),G[i]),pmul(sub(L,LEADS[j]),G[j]),-1); steps=[]
    while p:
        lt=lead(p)
        for k,lg in enumerate(LEADS):
            if all(x<=y for x,y in zip(lg,lt)):
                m=sub(lt,lg); c=p[lt]//G[k][lg]; steps.append((k,m,c)); p=padd(p,pmul(m,G[k]),-c); break
        else:
            steps=None; break
    cert[(i,j)]=steps
report("%d non-coprime S-pairs, each reduces to zero"%len(pairs), all(v is not None for v in cert.values()))
good=True
for (i,j) in pairs:
    L=tuple(max(x,y) for x,y in zip(LEADS[i],LEADS[j]))
    S=padd(pmul(sub(L,LEADS[i]),G[i]),pmul(sub(L,LEADS[j]),G[j]),-1); acc={}
    for (k,m,c) in cert[(i,j)]:
        t=pmul(m,G[k])
        if not key(lead(t))<key(L): good=False
        acc=padd(acc,t,c)
    if acc!=S: good=False
report("each S-pair equals sum c*mono*g_k exactly, every term below the lcm (standard representation)", good)
# (2) Hilbert numerator, grading, canonical module degree
def vecs(n=4):
    V=[tuple([0]*n+[-1])]
    for i in range(n): V.append(tuple(1 if j==i else 0 for j in range(n))+(0,))
    for i in range(n): V.append(tuple(0 if j==i else 1 for j in range(n))+(1,))
    V.append(tuple([1]*n+[2])); return V
V=vecs(); phi=lambda b: sum(b[:-1])-b[-1]
report("grading phi=a0+a1+a2+a3-k: weights 1,1,1,1,1,2,2,2,2,2 on A,E0-3,B0-3,C", [phi(v) for v in V]==[1,1,1,1,1,2,2,2,2,2])
WMAX=20
S={(0,)*5}; fr=set(S)
while fr:
    new=set()
    for b in fr:
        for v in V:
            c=tuple(x+y for x,y in zip(b,v))
            if phi(c)<=WMAX and c not in S: new.add(c)
    S|=new; fr=new
cone=set()
for a in itertools.product(range(0,2*WMAX+1),repeat=4):
    km=min(a[i]+a[j] for i in range(4) for j in range(i+1,4))
    for k in range(sum(a)-WMAX,km+1): cone.add(a+(k,))
report("generated semigroup = cone integer points up to weight %d (%d points)"%(WMAX,len(S)), S==cone)
hs=[0]*(WMAX+1)
for b in cone: hs[phi(b)]+=1
def pm(p,q):
    r=[0]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q): r[i+j]+=x*y
    return r
D=[1]
for _ in range(5): D=pm(D,[1,-1])
for _ in range(5): D=pm(D,[1,0,-1])
Q=pm(hs,D)[:WMAX+1]
def formula(n):
    d=n-2; F=defaultdict(int); F[(0,0)]=1; F[(n+1,n*(n-1))]+=1
    for k in range(1,n+1):
        for dg,cf in (((k-1)*d+2,(n-k+1)*comb(n,k-2) if k>=2 else 0),(k*d+1,2*(n-k+1)*comb(n,k-1)),((k+1)*d,k*comb(n,k+1) if k+1<=n else 0)):
            if cf: F[(k,dg)]+=cf
    return dict(F)
NF=[0]*(WMAX+1)
for (i,w),v in formula(4).items(): NF[w]+=(-1)**i*v
report("HS(R)*(1-t)^5(1-t^2)^5 = Betti numerator, degree 12, zeros through weight %d"%WMAX, Q==NF and all(x==0 for x in Q[13:]))
interior={a+(k,) for a in itertools.product(range(1,WMAX+2),repeat=4) for k in range(-WMAX,WMAX+2)
          if all(a[i]+a[j]>k for i in range(4) for j in range(i+1,4)) and phi(a+(k,))<=WMAX}
shifted={tuple(x+1 for x in s) for s in S if phi(s)+3<=WMAX}
report("interior integer points = kappa+S, kappa=(1,1,1,1,1), up to weight %d"%WMAX, interior==shifted)
report("least interior weight is 3, so a(R)=-3 and deg numerator = 15-3 = 12", min(phi(b) for b in interior)==3)
# (3) Taylor + unit-pair cancellation for S/M_4
n=4; d=n-2
def E(i): return 1<<i
def B(i): return 1<<(n+i)
gens=[sum(E(j) for j in range(n) if j!=i) for i in range(n)]+[E(i)|B(i) for i in range(n)]+[B(i)|B(j) for i in range(n) for j in range(i+1,n)]
m_=len(gens); N=1<<m_
Lc=[0]*N
for s in range(1,N):
    low=(s&-s).bit_length()-1
    Lc[s]=Lc[s&(s-1)]|gens[low]
Dm={0:{}}; R=defaultdict(set)
for s in range(1,N):
    row={}; pos=0
    for g in range(m_):
        if s>>g&1:
            t=s^(1<<g); row[t]=(-1)**pos; pos+=1
    Dm[s]=row
    for t in row: R[t].add(s)
pc=lambda x: bin(x).count('1')
alive=set(range(N)); elim=0
for s in sorted(range(N),key=lambda s:(pc(s),s)):
    if s not in alive: continue
    piv=None
    for t,c in Dm[s].items():
        if Lc[t]==Lc[s] and abs(c)==1: piv=(t,c); break
    if piv is None: continue
    a,c=piv; b=s
    rowb=dict(Dm[b]); del rowb[a]
    for x in list(R[a]):
        if x==b: continue
        cx=Dm[x][a]
        for y,cy in rowb.items():
            new=Dm[x].get(y,0)-cx*c*cy
            if new: Dm[x][y]=new; R[y].add(x)
            elif y in Dm[x]: del Dm[x][y]; R[y].discard(x)
        del Dm[x][a]
    for t in list(Dm[b]): R[t].discard(b)
    for t in list(Dm[a]): R[t].discard(a)
    for x in list(R[a]): Dm[x].pop(a,None)
    for x in list(R[b]): Dm[x].pop(b,None)
    del Dm[a]; del Dm[b]; alive.discard(a); alive.discard(b); R.pop(a,None); R.pop(b,None); elim+=1
crit=sorted(alive)
wts=[1]*n+[d]*n
wd=lambda mask: sum(wts[i] for i in range(2*n) if mask>>i&1)
tab=defaultdict(int)
for s in crit: tab[(pc(s),wd(Lc[s]))]+=1
report("Taylor complex: %d cells, %d unit pairs cancelled, %d cells remain (100 expected)"%(N,elim,len(crit)), len(crit)==100)
report("minimal: no remaining entry joins cells of equal multidegree", sum(1 for s in crit for t in Dm[s] if Lc[t]==Lc[s])==0)
report("all remaining coefficients are +-1", set(c for s in crit for c in Dm[s].values())<={-1,1})
bad=0
for s in crit:
    acc=defaultdict(int)
    for t,c in Dm[s].items():
        for u,c2 in Dm[t].items(): acc[u]+=c*c2
    if any(acc.values()): bad+=1
report("d^2 = 0 over the integers", bad==0)
report("weighted Betti table of S/M_4 equals the formula table of R", dict(tab)==formula(4))
print("ALL PASS" if ok_all else "SOME CHECK FAILED")
sys.exit(0 if ok_all else 1)
