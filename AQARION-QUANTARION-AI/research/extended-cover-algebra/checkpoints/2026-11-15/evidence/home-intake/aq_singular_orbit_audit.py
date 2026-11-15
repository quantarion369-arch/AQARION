from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import signal
import sympy as s

home = Path.home()
complex_path = home/"AQARION-complete-complex-20261114T163933580791Z.json"
structure_path = home/"AQARION-semigroup-certificate-20261114T164416695765Z.json"

complex_hash = (
    "1a9f22866a38f135859a41616f18a5756e7"
    "fdecc921a2f36b078c20db334a8a0"
)
structure_hash = (
    "291b40ac0b15a131b733ba96ae98752f505"
    "4ebf0a387c960efca39fb46c07f5b"
)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

assert sha(complex_path) == complex_hash
assert sha(structure_path) == structure_hash

data = json.loads(complex_path.read_text())
structure = json.loads(structure_path.read_text())
assert structure["export_sha256"] == complex_hash

names = data["variables"]
assert names == "A E0 E1 E2 E3 B0 B1 B2 B3 C".split()
x = tuple(s.Symbol(name) for name in names)
local = dict(zip(names,x))
f = [
    s.sympify(entry,locals=local)
    for entry in data["matrices"]["D1"][0]
]
generators = structure["generators"]
normals = [record["normal"] for record in structure["primitive_facets"]]

print("Complex and structural hashes: PASS",flush=True)

# Faces of the exponent cone, represented by their generator supports.
faces = {frozenset(range(10))}
for normal in normals:
    incident = frozenset(
        i for i,generator in enumerate(generators)
        if sum(a*b for a,b in zip(normal,generator)) == 0
    )
    faces |= {face & incident for face in list(faces)}

jacobian = s.Matrix(f).jacobian(x)
G = s.Matrix.hstack(*(s.Matrix(v) for v in generators))
records = []

class AuditTimeout(Exception):
    pass

def stop(signum,frame):
    raise AuditTimeout()

signal.signal(signal.SIGALRM,stop)
signal.alarm(20)

try:
    for face in sorted(faces,key=lambda a:(len(a),sorted(a))):
        indices = sorted(face)
        values = [int(i in face) for i in range(10)]
        point = dict(zip(x,values))

        assert all(polynomial.subs(point) == 0 for polynomial in f)

        dimension = G[:,indices].rank() if indices else 0
        rank = jacobian.subs(point).rank()
        assert rank <= 5

        records.append({
            "support_indices_zero_based":indices,
            "nonzero_coordinates":[names[i] for i in indices],
            "representative":dict(zip(names,values)),
            "orbit_dimension":int(dimension),
            "jacobian_rank":int(rank),
            "tangent_dimension":10-int(rank),
            "singular":rank < 5
        })
finally:
    signal.alarm(0)

singular = [record for record in records if record["singular"]]
maximal = [
    record for record in singular
    if not any(
        set(record["support_indices_zero_based"])
        < set(other["support_indices_zero_based"])
        for other in singular
    )
]

face_counts = Counter(record["orbit_dimension"] for record in records)
singular_counts = Counter(record["orbit_dimension"] for record in singular)

assert dict(face_counts) == {0:1,1:10,2:30,3:30,4:10,5:1}
assert len(singular) == 6
assert {
    tuple(record["nonzero_coordinates"]) for record in maximal
} == {("E0",),("E1",),("E2",),("E3",),("C",)}

print("Orbit count:",len(records))
print("Face counts:",dict(sorted(face_counts.items())))
print("Singular orbit counts:",dict(sorted(singular_counts.items())))
print("Maximal singular orbit closures:",flush=True)
for record in maximal:
    print(
        " ",record["nonzero_coordinates"],
        "dimension",record["orbit_dimension"],
        "Jacobian rank",record["jacobian_rank"],
        "tangent dimension",record["tangent_dimension"],
        flush=True
    )

certificate = {
    "format":"AQARION singular-orbit certificate v1",
    "complex_sha256":complex_hash,
    "structural_certificate_sha256":structure_hash,
    "replay_script_sha256":sha(Path(__file__)),
    "field":"QQ; geometric interpretation after algebraic closure",
    "ambient_dimension":10,
    "variety_dimension":5,
    "jacobian_smoothness_rank":5,
    "orbit_records":records,
    "maximal_singular_orbits":maximal,
    "reduced_singular_locus":{
        "components":["E0-axis","E1-axis","E2-axis","E3-axis","C-axis"],
        "dimension":1,
        "codimension_in_X":4,
        "ideal_description":
            "(A,B0,B1,B2,B3) plus all pairwise products "
            "of distinct members of {E0,E1,E2,E3,C}"
    },
    "proof_dependencies":[
        "The established normal toric endpoint identification.",
        "Faces are all intersections of the certified facets.",
        "Distinguished face points represent all geometric torus orbits.",
        "Smoothness is invariant under the torus action.",
        "Characteristic-zero Jacobian criterion."
    ],
    "scope":[
        "Determines the reduced geometric singular locus.",
        "Does not compute the nonreduced Jacobian singular subscheme.",
        "Does not establish behavior in positive characteristic.",
        "Does not alter the existing resolution bundle."
    ]
}

stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
destination = home/f"AQARION-singular-orbits-{stamp}.json"
with destination.open("x") as handle:
    json.dump(certificate,handle,indent=2)
    handle.write("\n")

print("\nSINGULAR-LOCUS CERTIFICATE COMPLETE")
print("File:",destination)
print("Bytes:",destination.stat().st_size)
print("SHA256:",sha(destination))
print("No resolution ranks were rerun.")
print("Repository files unchanged.")
