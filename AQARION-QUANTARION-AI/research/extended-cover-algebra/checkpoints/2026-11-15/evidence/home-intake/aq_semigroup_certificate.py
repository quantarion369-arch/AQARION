from pathlib import Path
from itertools import combinations
from functools import reduce
from math import gcd, lcm
from datetime import datetime, timezone
import hashlib
import json
import signal
import sympy as s

EXPECTED_HASH = (
    "1a9f22866a38f135859a41616f18a5756e7"
    "fdecc921a2f36b078c20db334a8a0"
)
home = Path.home()
source = home / "AQARION-complete-complex-20261114T163933580791Z.json"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

if not source.is_file():
    raise SystemExit("STOP: the identified complete-complex export is missing.")
if sha(source) != EXPECTED_HASH:
    raise SystemExit("STOP: export SHA256 differs from the recorded receipt.")

data = json.loads(source.read_text())
names = data["variables"]
assert names == "A E0 E1 E2 E3 B0 B1 B2 B3 C".split()

raw = data["variable_semigroup_degrees"]
assert len(raw) == 10 and all(len(v) == 5 for v in raw)
assert all(type(a) is int for v in raw for a in v)

generators = [s.Matrix(v) for v in raw]
G = s.Matrix.hstack(*generators)
assert G.rank() == 5

basis_indices = [0,1,2,3,4]
lattice_det = G[:,basis_indices].det()
assert abs(lattice_det) == 1
print("Export SHA256: PASS")
print("Generator rank: 5")
print("Lattice basis determinant:", lattice_det)
print("Generated lattice: Z^5", flush=True)

class AuditTimeout(Exception):
    pass

def stop(signum, frame):
    raise AuditTimeout()

signal.signal(signal.SIGALRM, stop)

def primitive(vector):
    scale = lcm(*(int(a.q) for a in vector))
    entries = [int(a*scale) for a in vector]
    divisor = reduce(gcd,(abs(a) for a in entries),0)
    return tuple(a//divisor for a in entries)

facets = {}
signal.alarm(20)
try:
    # In dimension five, each facet contains four independent
    # generator rays. Enumerate those possible supporting hyperplanes.
    for chosen in combinations(range(10),4):
        M = s.Matrix.vstack(*(generators[i].T for i in chosen))
        nullspace = M.nullspace()
        if len(nullspace) != 1:
            continue
        normal = primitive(nullspace[0])
        values = [
            sum(a*b for a,b in zip(normal,v))
            for v in raw
        ]
        if all(v >= 0 for v in values):
            pass
        elif all(v <= 0 for v in values):
            normal = tuple(-a for a in normal)
            values = [-v for v in values]
        else:
            continue

        incident = [i for i,value in enumerate(values) if value == 0]
        if G[:,incident].rank() == 4:
            facets[normal] = {
                "incident_generator_indices_zero_based":incident,
                "independent_incident_indices_zero_based":list(chosen),
                "values_on_generators":values
            }
except AuditTimeout:
    raise SystemExit("TIMEOUT: facet certificate not completed or written.")
finally:
    signal.alarm(0)

expected = set()
for i in range(4):
    row = [0]*5
    row[i] = 1
    expected.add(tuple(row))
for i,j in combinations(range(4),2):
    row = [0]*5
    row[i] = row[j] = 1
    row[4] = -1
    expected.add(tuple(row))

assert set(facets) == expected
print("Derived primitive facets:",len(facets))
for normal in sorted(facets):
    print(" ",normal)
print("Expected ten-facet description: PASS")

kappa = (1,1,1,1,1)
sigma = tuple(sum(v[j] for v in raw) for j in range(5))
tau = tuple(a-b for a,b in zip(sigma,kappa))

assert all(
    sum(a*b for a,b in zip(normal,kappa)) == 1
    for normal in facets
)
assert sigma == (5,5,5,5,5)
assert tau == (4,4,4,4,4)
assert tuple(data["module_semigroup_shifts"][5][0]) == tau

def scalar(v):
    return sum(v[:4])-v[4]

assert [scalar(v) for v in raw] == data["weights"]
assert scalar(kappa) == 3
assert scalar(tau) == 12
print("Every primitive facet takes value 1 on kappa: PASS")
print("Ambient degree sum:",sigma)
print("Final semigroup shift:",tau)
print("Canonical generator scalar degree:",scalar(kappa))
print("Final scalar shift:",scalar(tau))

variables = tuple(s.Symbol(name) for name in names)
local = dict(zip(names,variables))
entries = [
    s.Poly(
        s.sympify(row[0],locals=local),
        *variables,domain=s.QQ
    )
    for row in data["matrices"]["D5"]
]
assert len(entries) == 14
assert any(not p.is_zero for p in entries)
common = reduce(s.gcd,entries)
assert common.total_degree() == 0
print("Exported D5 entries have unit gcd: PASS")

generation_proof = [
    "Every generator satisfies ai>=0 and ai+aj-k>=0.",
    "For an integral feasible point with k<=0, use Ei powers and A^(-k).",
    "For k=1, at most one coordinate is zero; subtract a suitable Bi.",
    "For k>=2 with every ai>=1, subtract C; all inequalities remain valid.",
    "For k>=2 with ai=0, every other aj>=k; subtract Bi.",
    "Each positive-k step decreases k, so induction terminates.",
    "Hence S equals the integral points of the stated cone.",
    "Rational feasible points can be scaled to integral points, so the "
    "stated inequality cone equals the generator cone.",
    "Together with the unimodular lattice basis, this proves saturation."
]

canonical_proof = [
    "Primitive facet functionals are integral and equal 1 on kappa.",
    "An interior lattice point has each facet value at least 1.",
    "Subtracting kappa therefore produces a lattice point in the cone.",
    "Conversely kappa plus a cone lattice point is interior.",
    "Thus interior lattice points equal kappa+S.",
    "The normal-semigroup canonical-module theorem gives a principal "
    "canonical module, generated in scalar degree 3."
]

certificate = {
    "format":"AQARION semigroup structural certificate v1",
    "export_filename":source.name,
    "export_sha256":EXPECTED_HASH,
    "replay_script_sha256":sha(Path(__file__)),
    "coordinate_order":["a0","a1","a2","a3","k"],
    "generator_names":names,
    "generators":raw,
    "lattice_basis_indices_zero_based":basis_indices,
    "lattice_basis_determinant":int(lattice_det),
    "primitive_facets":[
        {"normal":list(normal),**facets[normal]}
        for normal in sorted(facets)
    ],
    "kappa":kappa,
    "ambient_degree_sum":sigma,
    "final_shift":tau,
    "canonical_scalar_generator_degree":3,
    "final_scalar_shift":12,
    "D5_unit_gcd":True,
    "semigroup_generation_proof":generation_proof,
    "canonical_translate_proof":canonical_proof,
    "theorem_dependencies":[
        "Normal affine semigroup rings are Cohen-Macaulay.",
        "The canonical module is indexed by interior lattice points."
    ],
    "scope":[
        "Structural certificate for the exported endpoint semigroup.",
        "Does not rerun middle component ranks.",
        "Does not claim recovery of the missing original program.",
        "Does not establish characteristic independence of the complex."
    ]
}

stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
destination = home / f"AQARION-semigroup-certificate-{stamp}.json"
with destination.open("x") as handle:
    json.dump(certificate,handle,indent=2)
    handle.write("\n")

print("\nSTRUCTURAL CERTIFICATE COMPLETE")
print("File:",destination)
print("Bytes:",destination.stat().st_size)
print("SHA256:",sha(destination))
print("Replay script:",Path(__file__))
print("Repository files were not changed.")
