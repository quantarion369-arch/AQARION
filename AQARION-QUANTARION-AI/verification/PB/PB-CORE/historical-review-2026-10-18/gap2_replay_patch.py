#!/usr/bin/env python3
"""affine rank = rank_Q([M | 1]); gap = m - affine rank"""
from fractions import Fraction
EXPECTED=(6,4,2); T=(1,2,3,4,5,0); BLOCKS=(frozenset({0,1,2}),frozenset({3,4,5}))
def assert_gap2_witness(itinerary_fn,rank_fn):
    if not callable(itinerary_fn): raise TypeError("itinerary_fn must be callable")
    if not callable(rank_fn): raise TypeError("rank_fn must be callable")
    distinct={tuple(it) for it in itinerary_fn(T,BLOCKS)}; m=len(distinct)
    if m==0: raise AssertionError("no itineraries returned")
    matrix=sorted(distinct); augmented=[list(r)+[1] for r in matrix]
    try: rank=rank_fn(augmented)
    except Exception as e: raise RuntimeError(f"rank_fn failed: {e}") from e
    if not isinstance(rank,int) or isinstance(rank,bool): raise TypeError(f"rank must be int, got {rank!r}")
    actual=(m,rank,m-rank)
    if actual!=EXPECTED: raise AssertionError(f"GAP-2 mismatch: observed {actual}, expected {EXPECTED}; matrix={matrix!r}")
    return actual
def reference_itinerary_fn(T,blocks):
    n=len(T); beta={}
    for i,b in enumerate(blocks):
        for s in b:
            if s in beta: raise ValueError(f"overlap at {s}")
            beta[s]=i
    if set(beta)!=set(range(n)): raise ValueError("blocks must partition states")
    out=[]
    for start in range(n):
        s=start; it=[]
        for _ in range(n): it.append(beta[s]); s=T[s]
        out.append(tuple(it))
    return out
def exact_rational_rank(matrix):
    if not matrix: return 0
    w=len(matrix[0]); a=[[Fraction(v) for v in r] for r in matrix]
    rows=len(a); piv=0
    for c in range(w):
        p=next((r for r in range(piv,rows) if a[r][c]!=0),None)
        if p is None: continue
        a[piv],a[p]=a[p],a[piv]; pv=a[piv][c]
        a[piv]=[v/pv for v in a[piv]]
        for r in range(rows):
            if r!=piv and a[r][c]:
                f=a[r][c]; a[r]=[a[r][k]-f*a[piv][k] for k in range(w)]
        piv+=1
        if piv==rows: break
    return piv
def wrong_rank(m): return exact_rational_rank(m)+1
def main():
    print("MATCH:",assert_gap2_witness(reference_itinerary_fn,exact_rational_rank))
    try: assert_gap2_witness(reference_itinerary_fn,wrong_rank)
    except AssertionError as e: print("MISMATCH caught:",str(e)[:80],"...")
    else: raise AssertionError("negative test failed")
if __name__=="__main__": main()
