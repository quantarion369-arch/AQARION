from pathlib import Path
from fractions import Fraction
from functools import reduce
from datetime import datetime, timezone
import hashlib
import json
import signal
import sympy as s

home = Path.home()
source = home/"AQARION-complete-complex-20261114T163933580791Z.json"
structure = home/"AQARION-semigroup-certificate-20261114T164416695765Z.json"

expected_source = (
    "1a9f22866a38f135859a41616f18a5756e7"
    "fdecc921a2f36b078c20db334a8a0"
)
expected_structure = (
    "291b40ac0b15a131b733ba96ae98752f505"
    "4ebf0a387c960efca39fb46c07f5b"
)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

assert sha(source) == expected_source, "Complex export hash mismatch"
assert sha(structure) == expected_structure, "Structural certificate hash mismatch"

data = json.loads(source.read_text())
structural = json.loads(structure.read_text())
assert structural["export_sha256"] == expected_source

x = tuple(s.Symbol(name) for name in data["variables"])
local = dict(zip(data["variables"],x))
weights = data["weights"]
shifts = data["module_scalar_shifts"]
assert weights == [1]*5+[2]*5

D = {}
for level in range(1,6):
    D[level] = s.Matrix([
        [s.sympify(entry,locals=local) for entry in row]
        for row in data["matrices"][f"D{level}"]
    ])
    assert D[level].shape == (
        len(shifts[level-1]),len(shifts[level])
    )
    for entry in D[level]:
        s.Poly(entry,*x,domain=s.QQ)

class StageTimeout(Exception):
    pass

def stop(signum,frame):
    raise StageTimeout()

signal.signal(signal.SIGALRM,stop)

def stage(label,function):
    print("\n"+label,flush=True)
    signal.alarm(20)
    try:
        result = function()
    finally:
        signal.alarm(0)
    print("PASS",flush=True)
    return result

receipt = {
    "complex_sha256":expected_source,
    "structural_certificate_sha256":expected_structure,
    "replay_script_sha256":sha(Path(__file__)),
    "field":"QQ",
    "results":{}
}

def compositions():
    for level in range(1,5):
        for j in range(D[level+1].cols):
            product = (D[level]*D[level+1][:,j]).applyfunc(s.expand)
            assert all(entry == 0 for entry in product)
        print(f"D{level}*D{level+1}=0",flush=True)
    return True

try:
    stage("Checking four compositions from exported matrices...",compositions)
    receipt["results"]["compositions"] = True

    f = list(D[1])
    assert f == list(D[5])[6:14]+list(D[5])[0:6]

    G = stage(
        "Recomputing endpoint Groebner basis...",
        lambda:s.groebner(f,*x,order="grevlex")
    )
    print("Basis elements:",len(G.polys))
    receipt["endpoint_groebner_basis"] = [
        str(p.as_expr()) for p in G.polys
    ]

    z = s.Symbol("endpointSaturationVariable")
    H = stage(
        "Recomputing endpoint saturation at A...",
        lambda:s.groebner(f+[z*x[0]-1],z,*x,order="lex")
    )
    elimination = [
        p.as_expr() for p in H.polys
        if not p.as_expr().has(z)
    ]
    assert all(G.reduce(p)[1] == 0 for p in elimination)
    receipt["results"]["J_colon_A_infinity_equals_J"] = True
    receipt["saturation_elimination_generators"] = [
        str(p) for p in elimination
    ]
    print("J:A^infinity=J: PASS")

    A,E0,E1,E2,E3,B0,B1,B2,B3,C = x
    images = {
        B0:E1*E2*E3/A,
        B1:E0*E2*E3/A,
        B2:E0*E1*E3/A,
        B3:E0*E1*E2/A,
        C:E0*E1*E2*E3/A**2
    }
    assert all(
        s.cancel(p.subs(images,simultaneous=True)) == 0 for p in f
    )
    solving_equations = [
        A*B0-E1*E2*E3,
        A*B1-E0*E2*E3,
        A*B2-E0*E1*E3,
        A*B3-E0*E1*E2,
        A**2*C-E0*E1*E2*E3
    ]
    assert all(G.reduce(p)[1] == 0 for p in solving_equations)
    receipt["results"]["localized_endpoint_identification"] = True
    print("Localized endpoint identification: PASS")

    common = reduce(s.gcd,[
        s.Poly(p,*x,domain=s.QQ) for p in D[5]
    ])
    assert common.total_degree() == 0
    receipt["results"]["D5_unit_gcd"] = True

    # Weighted Hilbert numerator from the initial ideal.
    terms = {(0,)*10:1}
    for polynomial in G.polys:
        generator = polynomial.LM(order=G.order).exponents
        updated = terms.copy()
        for exponent,coefficient in terms.items():
            lcm = tuple(max(a,b) for a,b in zip(exponent,generator))
            updated[lcm] = updated.get(lcm,0)-coefficient
        terms = {e:c for e,c in updated.items() if c}

    t = s.Symbol("t")
    N = s.expand(sum(
        c*t**sum(a*b for a,b in zip(exponent,weights))
        for exponent,c in terms.items()
    ))
    expected_N = (
        1-8*t**3-3*t**4+24*t**5
        -24*t**7+3*t**8+8*t**9-t**12
    )
    assert s.expand(N-expected_N) == 0
    receipt["hilbert_numerator"] = str(N)
    print("Independent endpoint Hilbert numerator: PASS")

    def monomials(degree,position=0):
        if position == len(weights):
            if degree == 0:
                yield ()
            return
        for exponent in range(degree//weights[position]+1):
            for rest in monomials(
                    degree-exponent*weights[position],position+1):
                yield (exponent,)+rest

    monomial_cache = {
        degree:list(monomials(degree)) for degree in range(4)
    }

    def polynomial_columns(M):
        columns = []
        for j in range(M.cols):
            vector = {}
            for i in range(M.rows):
                for exponent,c in s.Poly(
                        M[i,j],*x,domain=s.QQ).terms():
                    if c:
                        vector[(i,exponent)] = Fraction(int(c.p),int(c.q))
            columns.append(vector)
        return columns

    columns = {i:polynomial_columns(D[i]) for i in (2,3,4)}

    def insert(vector,basis):
        vector = dict(vector)
        while vector:
            pivot = min(vector)
            scale = vector[pivot]
            if pivot not in basis:
                basis[pivot] = {
                    key:value/scale for key,value in vector.items()
                }
                return
            for key,value in basis[pivot].items():
                result = vector.get(key,Fraction(0))-scale*value
                if result:
                    vector[key] = result
                else:
                    vector.pop(key,None)

    def rank_component(level,degree,lower_only=False):
        basis = {}
        for column,shift in zip(columns[level],shifts[level]):
            if shift > degree or (lower_only and shift == degree):
                continue
            for multiplier in monomial_cache[degree-shift]:
                vector = {
                    (row,tuple(a+b for a,b in zip(exponent,multiplier))):c
                    for (row,exponent),c in column.items()
                }
                insert(vector,basis)
        return len(basis)

    # Compute ring dimensions from the independently recomputed numerator.
    P = [0]*10
    P[0] = 1
    for weight in weights:
        for degree in range(weight,10):
            P[degree] += P[degree-weight]

    def pd(degree):
        return P[degree] if 0 <= degree < len(P) else 0

    def rd(degree):
        return sum(
            int(N.coeff(t,j))*pd(degree-j)
            for j in range(13)
        )

    def fd(level,degree):
        return sum(pd(degree-shift) for shift in shifts[level])

    component_results = []
    ranks = {}

    for degree in (4,5,6):
        required = fd(1,degree)-(pd(degree)-rd(degree))
        rank = stage(
            f"D2 image dimension in degree {degree}...",
            lambda degree=degree:rank_component(2,degree)
        )
        assert rank == required
        ranks[(2,degree)] = rank
        print("Computed =",rank,"required =",required)
        component_results.append([2,degree,rank,required])

    lower_degree5 = stage(
        "Degree-five span of lower-degree D2 columns...",
        lambda:rank_component(2,5,True)
    )
    assert lower_degree5 == 15
    receipt["results"]["degree4_generators_have_no_degree5_relation"] = True

    for degree in (6,7,8,9):
        image_D2 = fd(1,degree)-(pd(degree)-rd(degree))
        required = fd(2,degree)-image_D2
        rank = stage(
            f"D3 image dimension in degree {degree}...",
            lambda degree=degree:rank_component(3,degree)
        )
        assert rank == required
        ranks[(3,degree)] = rank
        print("Computed =",rank,"required =",required)
        component_results.append([3,degree,rank,required])

    for degree in (8,9):
        required = fd(3,degree)-ranks[(3,degree)]
        rank = stage(
            f"D4 image dimension in degree {degree}...",
            lambda degree=degree:rank_component(4,degree)
        )
        assert rank == required
        print("Computed =",rank,"required =",required)
        component_results.append([4,degree,rank,required])

    receipt["component_results"] = component_results
    receipt["generator_degree_argument"] = [
        "The linked structural proof identifies a codimension-five "
        "Gorenstein endpoint with final scalar shift 12.",
        "D2 spans the endpoint kernel in degrees 4,5,6.",
        "Its degree-four generators have no degree-five relation.",
        "Thus the minimal third module has no generators below degree 6.",
        "Gorenstein duality excludes second-module generators above 6.",
        "Therefore D2 generates the whole endpoint kernel.",
        "Duality gives third-module shifts 6^8,7^24,8^3.",
        "The D3 component spans therefore give full kernel generation.",
        "Duality gives fourth-module shifts 8^6,9^8.",
        "The D4 component spans therefore give full kernel generation.",
        "Final exactness uses nonzero D5, its unit gcd, and rank D4=13."
    ]
    receipt["scope"] = (
        "JSON-only replay of endpoint and component computations. "
        "Global conclusions also use the linked structural theorem "
        "and stated generator-degree argument. No novelty or "
        "characteristic-independence claim."
    )

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    destination = home/f"AQARION-algebra-replay-{stamp}.json"
    with destination.open("x") as handle:
        json.dump(receipt,handle,indent=2)
        handle.write("\n")

    print("\nJSON-ONLY ALGEBRAIC REPLAY COMPLETE")
    print("Receipt:",destination)
    print("Bytes:",destination.stat().st_size)
    print("SHA256:",sha(destination))
    print("Replay script:",Path(__file__))
    print("No old column files or endpoint-construction script were loaded.")
    print("Repository files were not changed.")

except StageTimeout:
    print("\nINCOMPLETE: current stage exceeded 20 seconds.")
    print("No completed replay receipt was written.")
except AssertionError as exc:
    print("\nCHECK FAILED:",exc)
    raise
