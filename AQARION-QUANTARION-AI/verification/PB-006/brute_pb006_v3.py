from itertools import product

# Correct partition numbers via pentagonal number theorem
N = 50
p = [0]*(N+1); p[0] = 1
for n in range(1, N+1):
    total, k = 0, 1
    while True:
        g1 = k*(3*k-1)//2
        g2 = k*(3*k+1)//2
        if g1 > n and g2 > n: break
        sign = 1 if k % 2 else -1
        if g1 <= n: total += sign*p[n-g1]
        if g2 <= n: total += sign*p[n-g2]
        k += 1
    p[n] = total

def cyclic_points(f):
    n = len(f); color = [0]*n; cyc = set()
    for s in range(n):
        if color[s]: continue
        path, cur = [], s
        while color[cur] == 0:
            color[cur] = 1; path.append(cur); cur = f[cur]
        if color[cur] == 1:
            cyc.update(path[path.index(cur):])
        for x in path: color[x] = 2
    return cyc

for n in range(1, 7):
    total = sum(p[len(cyclic_points(f))] for f in product(range(n), repeat=n))
    print(n, total)
print("p(1..6):", p[1:7])
