import itertools
from aqarion.stability import is_congruence, is_pb_stable, join_partitions
from aqarion.defect import defect_matrix, is_defect_zero

def all_partitions(n):
    # Bell numbers: generate via recursion
    # Simple algorithm for n<=4 is fine
    if n==0:
        yield []
        return
    # Use restricted growth strings
    def gen(a, m):
        if len(a)==n:
            # convert to blocks
            blocks = [[] for _ in range(m)]
            for i, v in enumerate(a):
                blocks[v].append(i)
            yield blocks
            return
        for k in range(m+1):
            # for standard RGS, k <= max+1
            if k < len(set(a))+1 or k <= max(a, default=-1)+1:
                if k==m:
                    yield from gen(a+[k], m+1)
                else:
                    if k <= max(a, default=-1)+1:
                        yield from gen(a+[k], m)
    # Simpler: brute force for n<=4
    elements = list(range(n))
    # generate all set partitions via recursion
    def partitions_of_set(s):
        if not s:
            yield []
            return
        first = s[0]
        rest = s[1:]
        for part in partitions_of_set(rest):
            # put first in its own block
            yield [[first]] + part
            # put first in each existing block
            for i in range(len(part)):
                new_part = [list(b) for b in part]
                new_part[i] = new_part[i] + [first]
                yield new_part
    seen = set()
    for p in partitions_of_set(elements):
        # canonical hash
        canon = tuple(sorted(tuple(sorted(b)) for b in p))
        if canon not in seen:
            seen.add(canon)
            yield [list(b) for b in p]

def all_maps(n):
    for T in itertools.product(range(n), repeat=n):
        yield list(T)

def test_congruence_join_closure_n4():
    """H_AQ-001C: E,F congruences => E∨F congruence. This is what current package actually tests."""
    total = 0
    fails = []
    for n in [2,3,4]:
        parts = list(all_partitions(n))
        for T in all_maps(n):
            congruences = [p for p in parts if is_congruence(T, p)]
            for i in range(len(congruences)):
                for j in range(i+1, len(congruences)):
                    E = congruences[i]
                    F = congruences[j]
                    J = join_partitions(E, F)
                    total += 1
                    if not is_congruence(T, J):
                        fails.append((n, T, E, F, J))
    assert len(fails)==0, f"Congruence join failed {fails[:3]}"
    # 7440 is the n<=4 census count for this specific property in prior receipt
    # Keep count as informational, not as hard assertion for now
    print(f"H_AQ-001C verified: {total} joins, 0 fails for n<=4")

def test_pb_join_separate_hypothesis():
    """H_AQ-001_PB: T*E⊆E, T*F⊆F => T*(E∨F)⊆E∨F — OPEN, not tested by H_AQ-001C"""
    # This test is intentionally marked as expected to fail or be OPEN
    # It demonstrates the exact executable distinction
    counterexample = None
    for n in [2,3,4]:
        parts = list(all_partitions(n))
        for T in all_maps(n):
            pb_stable = [p for p in parts if is_pb_stable(T, p)]
            for i in range(len(pb_stable)):
                for j in range(i+1, len(pb_stable)):
                    E = pb_stable[i]
                    F = pb_stable[j]
                    J = join_partitions(E, F)
                    if not is_pb_stable(T, J):
                        counterexample = (n, T, E, F, J)
                        break
                if counterexample:
                    break
            if counterexample:
                break
        if counterexample:
            break
    # Do NOT assert here — record as OPEN research object
    if counterexample:
        print(f"PB-Join counterexample found (expected OPEN): {counterexample}")
    else:
        print("PB-Join holds for n<=4 in this census (still OPEN for n=5+)")
