from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction
import hashlib, json, random
import sympy as s

home = Path.home()
src = home / "AQARION-complete-complex-20261114T163933580791Z.json"
expected = "1a9f22866a38f135859a41616f18a5756e7fdecc921a2f36b078c20db334a8a0"

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

assert sha(src) == expected, "Complex export SHA mismatch"
data = json.loads(src.read_text())

names = data["variables"]
x = tuple(s.Symbol(n) for n in names)
local = dict(zip(names, x))

D4 = s.Matrix([
    [s.sympify(e, locals=local) for e in row]
    for row in data["matrices"]["D4"]
])
D5 = s.Matrix([
    [s.sympify(e, locals=local) for e in row]
    for row in data["matrices"]["D5"]
])

assert D4.shape == (35,14)
assert D5.shape == (14,1)

print("Complex SHA256: PASS")
print("D4 shape:", D4.shape)
print("D5 shape:", D5.shape)

# First verify the polynomial identity over QQ[x].
print("Checking D4*D5 over QQ[x]...", flush=True)
product = (D4*D5).applyfunc(s.expand)
assert all(e == 0 for e in product)
print("D4*D5 = 0: PASS")

# A nonzero polynomial entry of D5 proves D5 is nonzero.
assert any(s.expand(e) != 0 for e in D5)
print("D5 nonzero polynomial: PASS")

rng = random.Random(20261114)
witness = None

# Positive integer evaluations avoid accidental zero denominators:
# all entries are polynomials in the ten variables.
for trial in range(1,501):
    point = {
        variable: rng.randint(1,9)
        for variable in x
    }

    M = D4.subs(point)
    v = D5.subs(point)

    # Exact rational rank, not floating-point rank.
    rank = M.rank()
    if rank == 13 and any(value != 0 for value in v):
        witness = {
            "trial": trial,
            "point": {str(k): int(val) for k,val in point.items()},
            "rank": rank,
            "D5_value": [str(value) for value in v],
            "D4_value": [[str(M[i,j]) for j in range(14)]
                         for i in range(35)]
        }
        break

assert witness is not None, (
    "No rank-13 specialization found in 500 deterministic trials. "
    "No rank conclusion from this search."
)

# Independently check the displayed specialized witness.
point = {
    local[name]: value
    for name,value in witness["point"].items()
}
M = D4.subs(point)
v = D5.subs(point)
assert M.rank() == 13
assert M*v == s.zeros(35,1)
assert any(value != 0 for value in v)

witness["complex_sha256"] = expected
witness["specialized_rank"] = 13
witness["specialized_kernel_vector_nonzero"] = True
witness["proof_conclusion"] = (
    "The specialization gives generic rank(D4)>=13. "
    "The polynomial identity D4*D5=0 and D5!=0 give "
    "generic rank(D4)<=13. Hence generic rank(D4)=13."
)

stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
out = home / f"AQARION-D4-rank13-witness-{stamp}.json"

with out.open("x") as f:
    json.dump(witness, f, indent=2)
    f.write("\n")

print("\nEXACT D4 RANK WITNESS: PASS")
print("Trial:", witness["trial"])
print("Specialized rank over QQ:", witness["rank"])
print("Specialized D5 vector nonzero: PASS")
print("Specialized D4*D5=0: PASS")
print("Witness:", out)
print("Bytes:", out.stat().st_size)
print("SHA256:", sha(out))
print("Repository files unchanged.")
