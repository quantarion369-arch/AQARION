#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import combinations, product
from math import factorial
import sys

# Coordinates: q0,q1,q2,q3,z
# Original 16 cell inequalities: a.x + b*m >= 0
ROWS = [
    ((-1,-1,-1,-1,-3), 3),
    (( 1, 1, 1, 0, 2), 0),
    (( 1, 1, 0, 1, 2), 0),
    ((-1,-1, 0, 0,-1), 1),
    (( 1, 0, 1, 1, 2), 0),
    ((-1, 0,-1, 0,-1), 1),
    ((-1, 0, 0,-1,-1), 1),
    (( 1, 0, 0, 0, 0), 0),
    (( 0, 1, 1, 1, 2), 0),
    (( 0,-1,-1, 0,-1), 1),
    (( 0,-1, 0,-1,-1), 1),
    (( 0, 1, 0, 0, 0), 0),
    (( 0, 0,-1,-1,-1), 1),
    (( 0, 0, 1, 0, 0), 0),
    (( 0, 0, 0, 1, 0), 0),
    (( 0, 0, 0, 0, 1), 0),
]

def dot(a, x):
    return sum(F(u)*v for u,v in zip(a,x))

def solve(A, b):
    n = len(b)
    M = [[F(v) for v in A[i]] + [F(b[i])]
         for i in range(n)]
    for c in range(n):
        p = next((r for r in range(c,n) if M[r][c]), None)
        if p is None:
            return None
        M[c],M[p] = M[p],M[c]
        t = M[c][c]
        M[c] = [v/t for v in M[c]]
        for r in range(n):
            if r != c and M[r][c]:
                t = M[r][c]
                M[r] = [M[r][j]-t*M[c][j]
                        for j in range(n+1)]
    return tuple(M[i][-1] for i in range(n))

def rank(A):
    if not A:
        return 0
    M = [[F(v) for v in row] for row in A]
    r = 0
    for c in range(len(M[0])):
        p = next((i for i in range(r,len(M))
                  if M[i][c]),None)
        if p is None:
            continue
        M[r],M[p] = M[p],M[r]
        t = M[r][c]
        M[r] = [v/t for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                t = M[i][c]
                M[i] = [M[i][j]-t*M[r][j]
                        for j in range(len(M[i]))]
        r += 1
        if r == len(M):
            break
    return r

def val(i,x,m):
    a,b = ROWS[i]
    return dot(a,x)+b*m

def vertices(m):
    out=set()
    nonsingular=0
    for I in combinations(range(16),5):
        A=[ROWS[i][0] for i in I]
        b=[-ROWS[i][1]*m for i in I]
        x=solve(A,b)
        if x is None:
            continue
        nonsingular += 1
        if all(val(i,x,m)>=0 for i in range(16)):
            out.add(x)
    return sorted(out),nonsingular

def face_dim(points):
    if not points:
        return -1
    base=points[0]
    D=[tuple(x[j]-base[j] for j in range(5))
       for x in points[1:]]
    return rank(D)

def integer_points(m):
    out=[]
    for q in product(range(m+1),repeat=4):
        pairmax=max(q[i]+q[j]
                    for i in range(4)
                    for j in range(i+1,4))
        if pairmax>m:
            continue
        for z in range(m-pairmax+1):
            out.append(tuple(q)+(z,))
    return out

def fmt(x):
    return str(x.numerator) if x.denominator==1 else str(x)

def ehrhart(m):
    if m%2==0:
        return F(m**5,40)+F(m**4,4)+m**3+2*m**2+F(21*m,10)+1
    return F(m**5,40)+F(m**4,4)+m**3+2*m**2+F(79*m,40)+F(3,4)

def main():
    m=int(sys.argv[1]) if len(sys.argv)>1 else 2
    if m<1:
        raise SystemExit("Scale must be >= 1")

    print("="*58)
    print("AQARION EXACT SPECIAL-FAMILY AUDIT")
    print("m =",m)
    print("Arithmetic: exact fractions; standard library only")
    print("="*58)

    V,ns=vertices(m)
    print("Active systems:",ns,"(4368 possible)")
    print("Distinct vertices:",len(V))

    for k,x in enumerate(V):
        active=[i for i in range(16) if val(i,x,m)==0]
        print("V",k,tuple(map(fmt,x)),
              "integer",all(t.denominator==1 for t in x),
              "active",active)

    facets=[]
    nonfacets=[]
    for i in range(16):
        face=[x for x in V if val(i,x,m)==0]
        d=face_dim(face)
        print("CELL",i,"face_dimension",d,
              "facet",d==4)
        if d==4:
            facets.append(i)
        else:
            nonfacets.append(i)

    print("FACETS:",facets)
    print("NON-FACETS:",nonfacets)

    realmax=max(sum(x) for x in V)
    realopt=[x for x in V if sum(x)==realmax]
    print("REAL MAX L:",fmt(realmax))
    print("REAL OPTIMIZERS:",
          [tuple(map(fmt,x)) for x in realopt])

    IP=integer_points(m)
    intmax=max(sum(x) for x in IP)
    intopt=[x for x in IP if sum(x)==intmax]
    print("INTEGER POINT COUNT:",len(IP))
    print("INTEGER MAX L:",intmax)
    print("INTEGER OPTIMIZERS:",intopt)
    print("EHRHART VALUE:",fmt(ehrhart(m)))
    print("EHRHART MATCH:",F(len(IP))==ehrhart(m))

    # Verify the proposed homothety against the m=1 vertices.
    V1,_=vertices(1)
    scaled={tuple(m*t for t in x) for x in V1}
    print("HOMOTHETY VERTEX CHECK:",scaled==set(V))

    # Verify the exact integer objective formula.
    target=2*m if m%2==0 else 2*m-1
    print("INTEGER OBJECTIVE FORMULA:",intmax==target,
          "predicted",target)

    # IDP obstruction: the m=2 point (1,1,1,1,0)
    # is not a sum of two m=1 integer points.
    if m>=2:
        witness=(1,1,1,1,0)
        feasible=all(val(i,witness,m)>=0 for i in range(16))
        print("IDP WITNESS FEASIBLE AT SCALE 2:",feasible)
        print("IDP WITNESS COORDINATE SUM:",sum(witness))
        print("IDP DECOMPOSITION INTO TWO SCALE-1 POINTS: NO")
        print("Reason: every scale-1 integer point has sum <= 1.")

    print("-"*58)
    checks=[
        len(V)==11,
        facets==[3,5,6,7,9,10,11,12,13,14,15],
        nonfacets==[0,1,2,4,8],
        F(len(IP))==ehrhart(m),
        scaled==set(V),
        intmax==target,
    ]
    print("CHECKS:",sum(checks),"/",len(checks))
    print("FINITE AUDIT:", "PASS" if all(checks) else "FAIL")
    print("Scope: stated special family only.")
    print("No arbitrary-margin, Markov-basis, mixing,")
    print("or novelty claim.")
    print("AUDIT COMPLETE")

if __name__=="__main__":
    main()
