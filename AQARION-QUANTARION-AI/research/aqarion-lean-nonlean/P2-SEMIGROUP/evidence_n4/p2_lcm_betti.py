import itertools
from collections import defaultdict

def get_generators(n):
    gen1 = [(i, i+n) for i in range(n)]
    gen2 = [(i+n, j+n) for i, j in itertools.combinations(range(n), 2)]
    gen3 = [tuple(j for j in range(n) if j != i) for i in range(n)]
    return gen1, gen2, gen3

def lcm(v1, v2):
    return tuple(max(a, b) for a, b in zip(v1, v2))

def mobius_lattice(all_gens):
    """
    Computes the lcm-lattice and the Moebius function.
    The minimal Betti numbers are given by:
    beta_i = sum_{l in L} mu(l) * (number of subsets of generators with lcm = l)
    """
    # Build the lcm-lattice
    L = set()
    for r in range(len(all_gens) + 1):
        for subset in itertools.combinations(all_gens, r):
            l = tuple(0 for _ in range(max(len(g) for g in all_gens)))
            for g in subset:
                l = lcm(l, g)
            L.add(l)
    L = sorted(L, key=lambda x: sum(x))
    
    # Compute the Moebius function on the lattice
    # mu(l) = -sum_{l' < l} mu(l')
    mu = defaultdict(int)
    mu[tuple(0 for _ in range(max(len(g) for g in all_gens)))] = 1
    for l in L:
        if l == tuple(0 for _ in range(len(l))):
            continue
        s = 0
        for l_prime in L:
            if l_prime < l:
                s += mu[l_prime]
        mu[l] = -s
    
    return L, mu

def minimal_betti(n):
    gen1, gen2, gen3 = get_generators(n)
    all_gens = [tuple(g) for g in gen1 + gen2 + gen3]
    
    L, mu = mobius_lattice(all_gens)
    
    # For each l in L, count the number of subsets of generators with lcm = l
    # and compute the Betti numbers via the Moebius function.
    betti = defaultdict(int)
    for l in L:
        # Count subsets of generators with lcm exactly l
        count = 0
        for r in range(len(all_gens) + 1):
            for subset in itertools.combinations(all_gens, r):
                lcm_val = tuple(0 for _ in range(len(l)))
                for g in subset:
                    lcm_val = lcm(lcm_val, g)
                if lcm_val == l:
                    count += 1
        # The minimal Betti number is mu(l) * count
        betti[l] = mu[l] * count
    
    return betti

def main():
    print("="*60)
    print("AQARION P2: LCM-LATTICE BETTI NUMBERS (PURE PYTHON)")
    print("="*60)
    
    for n in [3, 4]:
        print(f"\n[n={n}]")
        betti = minimal_betti(n)
        total = sum(v for v in betti.values() if v > 0)
        print(f"  Total minimal Betti number for S/M_{n}: {total}")
    
    print("\n[CONCLUSION]")
    print("  The lcm-lattice computation gives the minimal Betti numbers")
    print("  of S/M_n. The P2 chain's claim of 100 for R_4 requires")
    print("  the Koszul transfer, which is a separate computation.")

if __name__ == "__main__":
    main()
