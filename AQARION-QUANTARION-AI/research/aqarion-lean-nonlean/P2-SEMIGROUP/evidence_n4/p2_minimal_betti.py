import itertools
from collections import defaultdict

def get_generators(n):
    gen1 = [(i, i+n) for i in range(n)] 
    gen2 = [(i+n, j+n) for i, j in itertools.combinations(range(n), 2)] 
    gen3 = [tuple(j for j in range(n) if j != i) for i in range(n)]
    return gen1, gen2, gen3

def build_taylor_basis(all_gens):
    basis = []
    for r in range(len(all_gens) + 1):
        for subset in itertools.combinations(range(len(all_gens)), r):
            basis.append(subset)
    return basis

def lcm_of_subset(subset, all_gens):
    lcm = set()
    for idx in subset:
        lcm.update(all_gens[idx])
    return frozenset(lcm)

def build_taylor_differential(basis, all_gens, p):
    by_rank = defaultdict(list)
    for subset in basis:
        by_rank[len(subset)].append(subset)
    
    differentials = {}
    for r in range(1, len(all_gens) + 1):
        C_r = by_rank[r]
        C_rm1 = by_rank[r-1]
        index_rm1 = {subset: i for i, subset in enumerate(C_rm1)}
        mat = [[0] * len(C_r) for _ in range(len(C_rm1))]
        for col_idx, subset in enumerate(C_r):
            lcm = lcm_of_subset(subset, all_gens)
            for i in range(len(subset)):
                sub_subset = subset[:i] + subset[i+1:]
                lcm_i = lcm_of_subset(sub_subset, all_gens)
                if lcm != lcm_i:
                    coefficient = 1 if i % 2 == 0 else p - 1
                    row_idx = index_rm1[sub_subset]
                    mat[row_idx][col_idx] = coefficient
        differentials[r] = mat
    return differentials

def rank_over_finite_field(mat, p):
    """Computes the rank of a matrix over GF(p)."""
    if not mat or not mat[0]:
        return 0
    mat = [row[:] for row in mat]
    rows, cols = len(mat), len(mat[0])
    rank = 0
    for c in range(cols):
        pivot = -1
        for r in range(rank, rows):
            if mat[r][c] % p != 0:
                pivot = r; break
        if pivot != -1:
            mat[rank], mat[pivot] = mat[pivot], mat[rank]
            inv = pow(mat[rank][c], p-2, p)
            for j in range(c, cols):
                mat[rank][j] = (mat[rank][j] * inv) % p
            for r in range(rows):
                if r != rank and mat[r][c] % p != 0:
                    factor = mat[r][c]
                    for j in range(c, cols):
                        mat[r][j] = (mat[r][j] - factor * mat[rank][j]) % p
            rank += 1
    return rank

def main():
    print("="*60)
    print("AQARION P2: MINIMAL BETTI NUMBERS VIA RANK COMPUTATION")
    print("="*60)
    
    n = 4
    gen1, gen2, gen3 = get_generators(n)
    all_gens = gen1 + gen2 + gen3
    print(f"  Number of generators: {len(all_gens)}")
    
    basis = build_taylor_basis(all_gens)
    print(f"  Taylor basis size: {len(basis)}")
    
    p = 32003
    differentials = build_taylor_differential(basis, all_gens, p)
    
    # Compute ranks of all differentials
    ranks = {}
    for r in sorted(differentials.keys()):
        mat = differentials[r]
        ranks[r] = rank_over_finite_field(mat, p)
        print(f"  rank(d_{r}) = {ranks[r]}")
    
    # Compute minimal Betti numbers
    # beta_r = dim ker(d_r) - rank(d_{r+1})
    # dim ker(d_r) = |C_r| - rank(d_r)
    print("\n  Minimal Betti numbers:")
    total = 0
    for r in range(len(all_gens) + 1):
        C_r_size = len([s for s in basis if len(s) == r])
        ker_dim = C_r_size - (ranks.get(r, 0) if r > 0 else 0)
        next_rank = ranks.get(r+1, 0) if r < len(all_gens) else 0
        beta_r = ker_dim - next_rank
        if beta_r > 0:
            print(f"    beta_{r} = {beta_r}")
            total += beta_r
    
    print(f"\n  TOTAL: {total}")
    if total == 100:
        print("  [PASS] Total matches the P2 claim of 100 cells!")
    else:
        print(f"  [FAIL] Total {total} does not match 100.")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
