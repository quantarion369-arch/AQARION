from random import Random

def check(ok, message):
    if not ok:
        raise RuntimeError(message)

def root_check(n, w, q):
    check(n > 0 and n & (n-1) == 0, "Unsupported transform length")
    check((q-1) % n == 0, "Required root unavailable in this field")
    check(pow(w,n,q) == 1 and (n == 1 or pow(w,n//2,q) != 1),
          "Wrong root order")

def ntt(a, w, q, inverse=False):
    n = len(a)
    root_check(n,w,q)
    a = [v % q for v in a]
    j = 0
    for i in range(1,n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i],a[j] = a[j],a[i]
    if inverse:
        w = pow(w,-1,q)
    length = 2
    while length <= n:
        step = pow(w,n//length,q)
        for start in range(0,n,length):
            twiddle = 1
            for i in range(start,start+length//2):
                u = a[i]
                v = a[i+length//2]*twiddle % q
                a[i] = (u+v) % q
                a[i+length//2] = (u-v) % q
                twiddle = twiddle*step % q
        length *= 2
    if inverse:
        a = [v*pow(n,-1,q) % q for v in a]
    return a

def school(a,b,q=None,sign=-1):
    n = len(a)
    out = [0]*n
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            k = i+j
            out[k % n] += x*y*(sign if k >= n else 1)
    return [v % q for v in out] if q else out

def full(a,b,psi,q):
    n = len(a)
    root_check(2*n,psi,q)
    w = psi*psi % q
    A = ntt([x*pow(psi,i,q) % q for i,x in enumerate(a)],w,q)
    B = ntt([x*pow(psi,i,q) % q for i,x in enumerate(b)],w,q)
    C = ntt([x*y % q for x,y in zip(A,B)],w,q,True)
    return [x*pow(psi,-i,q) % q for i,x in enumerate(C)]

def split(a,inverse=False):
    q,zeta,m = 3329,17,128
    if not inverse:
        lanes = [ntt([a[2*j+k]*pow(zeta,j,q) % q for j in range(m)],
                     zeta*zeta % q,q) for k in (0,1)]
        return list(zip(*lanes))
    lanes = [ntt([v[k] for v in a],zeta*zeta % q,q,True) for k in (0,1)]
    return [lanes[k][j]*pow(zeta,-j,q) % q
            for j in range(m) for k in (0,1)]

def quadratic(a,b,mutant=False):
    pairs = []
    for i,((a0,a1),(b0,b1)) in enumerate(zip(split(a),split(b))):
        gamma = pow(17,2*i+1,3329)
        pairs.append((a0*b0 % 3329,a1*b1 % 3329) if mutant else
                     ((a0*b0+gamma*a1*b1) % 3329,
                      (a0*b1+a1*b0) % 3329))
    return split(pairs,True)

def fixtures(n,q,rng):
    zero,one,wrap,shift = ([0]*n for unused in range(4))
    one[0],wrap[-1],shift[1] = 1,1,1
    return [(zero,one),(wrap,shift),([q-1]*n,[q-1]*n),
            ([(-1)**i for i in range(n)],
             [i % 3-1 for i in range(n)])] + [
            ([rng.randrange(q) for unused in range(n)],
             [rng.randrange(q) for unused in range(n)])
            for case in range(8)]

rng = Random(20261020)
full_cases = 0

for n,q,psi in ((8,17,3),(256,8380417,1753)):
    for a,b in fixtures(n,q,rng):
        w = psi*psi % q
        check(ntt(ntt(a,w,q),w,q,True) == [v % q for v in a],
              "Round trip failed")
        check(full(a,b,psi,q) == school(a,b,q),
              "Full product mismatch")
        if n == 8:
            direct = [
                sum(v*pow(w,j*k,q) for j,v in enumerate(a)) % q
                for k in range(n)
            ]
            check(ntt(a,w,q) == direct,
                  "Direct transform mismatch")
        full_cases += 1

quadratic_cases = 0

for a,b in fixtures(256,3329,rng):
    check(split(split(a),True) == [v % 3329 for v in a],
          "Quadratic round trip failed")
    check(quadratic(a,b) == school(a,b,3329),
          "Quadratic product mismatch")
    values = split(a)
    for i,(even,odd) in enumerate(values):
        gamma = pow(17,2*i+1,3329)
        for k,actual in ((0,even),(1,odd)):
            expected = sum(
                a[2*j+k]*pow(gamma,j,3329)
                for j in range(128)
            ) % 3329
            check(actual == expected,
                  "Direct quadratic evaluation mismatch")
    quadratic_cases += 1

rejected = False
try:
    root_check(512,17,3329)
except RuntimeError:
    rejected = True
check(rejected, "Unsupported scalar split accepted")

x = [0]*256
x[1] = 1
check(quadratic(x,x,True) != school(x,x,3329),
      "Scalar mutant survived")

a,b = fixtures(8,17,rng)[1]
check(full(a,b,3,17) != school(a,b,17,1),
      "Cyclic sign mutant survived")

probe = list(range(8))
record = ntt(probe,9,17)

check(ntt(record,9,17) != probe,
      "Wrong inverse sign survived")

check([8*v % 17 for v in ntt(record,9,17,True)] != probe,
      "Missing normalization survived")

wrong_order = [
    record[int(format(i,"03b")[::-1],2)]
    for i in range(8)
]
check(ntt(wrong_order,9,17,True) != probe,
      "Wrong ordering survived")

print("FULL_NEGACYCLIC_CASES:", full_cases)
print("MLKEM_QUADRATIC_CASES:", quadratic_cases)
print("DIRECT_TRANSFORM_EVALUATION=PASS")
print("NTT_ROUND_TRIPS=PASS")
print("SCHOOLBOOK_PRODUCT_ORACLE=PASS")
print("MLKEM_UNSUPPORTED_SCALAR_SPLIT=REJECTED")
print("SCALAR_COMPONENTWISE_MUTANT=REJECTED")
print("CYCLIC_NEGACYCLIC_SIGN_MUTANT=REJECTED")
print("WRONG_INVERSE_SIGN_MUTANT=REJECTED")
print("MISSING_NORMALIZATION_MUTANT=REJECTED")
print("WRONG_ORDERING_MUTANT=REJECTED")
print("ARITHMETIC=EXACT_PYTHON_INTEGERS_MOD_PRIME")
print("SCOPE=RING_MECHANICS_NOT_NIST_CONFORMANCE_OR_TIMING")
print("NTT_INLINE_BOUNDARY_AUDIT=PASS")
