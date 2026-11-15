from pathlib import Path
from datetime import datetime, timezone
import hashlib
import itertools
import json
import platform
import sys
import time
import traceback

import sympy as sp
from sympy import QQ

HERE = Path(__file__).resolve().parent
SOURCE = Path(__file__).resolve()
CASES = (3, 4, 5, 6)

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def write_json(name, data):
    (HERE / name).write_text(
        json.dumps(data, indent=2) + "\n",
        encoding="utf-8"
    )

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

environment = {
    "created_utc": utc_now(),
    "provenance": (
        "Fresh reconstruction of the inline SymPy audit "
        "from the research conversation; not recovered historical bytes."
    ),
    "python_executable": sys.executable,
    "python_version": sys.version,
    "platform": platform.platform(),
    "sympy_version": sp.__version__,
    "sympy_location": sp.__file__,
    "engine": "SymPy AGCA",
    "coefficient_field": "QQ",
    "polynomial_order": "grevlex",
    "cases": list(CASES),
    "source_sha256": hashlib.sha256(
        SOURCE.read_bytes()
    ).hexdigest()
}
write_json("environment.json", environment)

receipt = {
    "started_utc": utc_now(),
    "status": "RUNNING",
    "source_sha256": environment["source_sha256"],
    "completed_cases": [],
    "scope": "Finite rational polynomial-module audit",
    "limitations": [
        "Not an integral exactness certificate",
        "Not an all-n proof verification",
        "Not a second computer-algebra implementation",
        "Does not independently establish the toric presentation"
    ]
}
write_json("results.json", receipt)

def build(n):
    A, C = sp.symbols("A C")
    E = sp.symbols(f"E0:{n}")
    B = sp.symbols(f"B0:{n}")
    variables = (A,) + E + B + (C,)

    pairs = list(itertools.combinations(range(n), 2))
    m = 2*n + len(pairs)
    hi = {pair: 2*n+j for j, pair in enumerate(pairs)}

    def U(omitted):
        return sp.prod(
            E[j] for j in range(n) if j not in omitted
        )

    generators = (
        [A*B[i] - U({i}) for i in range(n)]
        + [E[i]*B[i] - A*C for i in range(n)]
        + [
            B[i]*B[j] - C*U({i,j})
            for i,j in pairs
        ]
    )

    columns = []
    degrees = []

    def add(entries, degree):
        v = [sp.Integer(0)] * m
        for row, coefficient in entries.items():
            v[row] = coefficient
        columns.append(tuple(v))
        degrees.append(degree)

    r = n-1
    for i in range(n-1):
        add({
            i: E[i], r: -E[r],
            n+i: -A, n+r: A
        }, n)

    for i,j in pairs:
        q = hi[i,j]
        u = U({i,j})

        add({q: A, i: -B[j], n+j: -u}, 2*n-3)
        add({q: A, j: -B[i], n+i: -u}, 2*n-3)

        add({
            q: E[i], n+i: -B[j], j: -C
        }, 2*n-3)

        add({
            q: E[j], n+j: -B[i], i: -C
        }, 2*n-3)

    for i,j,k in itertools.combinations(range(n), 3):
        u = U({i,j,k})

        add({
            hi[i,j]: B[k],
            hi[i,k]: -B[j],
            n+j: -C*u,
            n+k: C*u
        }, 3*n-6)

        add({
            hi[i,j]: B[k],
            hi[j,k]: -B[i],
            n+i: -C*u,
            n+k: C*u
        }, 3*n-6)

    return variables, generators, columns, degrees

def minimality(F, columns, degrees):
    lower = []
    records = []

    for degree in sorted(set(degrees)):
        group = [
            v for v,d in zip(columns, degrees)
            if d == degree
        ]

        L = F.submodule(*lower) if lower else None
        keys = {}
        entries = {}

        for j,v in enumerate(group):
            vector = F.convert(v)
            remainder = (
                L.reduce_element(vector)
                if L is not None else vector
            )

            for row,polynomial in enumerate(remainder):
                for monomial,c in polynomial.to_dict().items():
                    key = (row, monomial)
                    if key not in keys:
                        keys[key] = len(keys)
                    entries[keys[key], j] = sp.Rational(c)

        matrix = sp.SparseMatrix(
            len(keys), len(group), entries
        )
        rank = matrix.rank()

        require(
            rank == len(group),
            f"Minimality failed at degree {degree}"
        )

        records.append({
            "degree": degree,
            "candidate_columns": len(group),
            "independent_classes": rank
        })
        lower.extend(group)

    return records

def audit(n):
    started = time.time()
    variables, generators, columns, degrees = build(n)

    R = QQ.old_poly_ring(*variables, order="grevlex")
    F = R.free_module(len(generators))
    M = F.submodule(*columns)

    print(f"\n=== n={n} ===", flush=True)
    print("Candidate columns:", len(columns), flush=True)
    print("Computing complete polynomial kernel...", flush=True)

    Z = R.free_module(1).submodule(
        *[(g,) for g in generators]
    ).syzygy_module()

    print(
        "Computed kernel generators:",
        len(Z.gens),
        flush=True
    )

    print("Testing kernel <= candidates...", flush=True)
    for j,z in enumerate(Z.gens):
        require(
            M.contains(z),
            f"Kernel generator {j} is outside candidate module"
        )

    print("Testing candidates <= kernel...", flush=True)
    for j,v in enumerate(M.gens):
        require(
            Z.contains(v),
            f"Candidate {j} is outside kernel"
        )

    print("Testing degree-layer minimality...", flush=True)
    layers = minimality(F, columns, degrees)

    expected = (
        (n-1)
        + 4*len(list(itertools.combinations(range(n), 2)))
        + 2*len(list(itertools.combinations(range(n), 3)))
    )
    require(
        len(columns) == expected,
        "Unexpected candidate-column count"
    )

    result = {
        "n": n,
        "candidate_columns": len(columns),
        "computed_kernel_generators": len(Z.gens),
        "kernel_equals_candidate_module": True,
        "minimal_homogeneous_generators": True,
        "degree_layers": layers,
        "elapsed_seconds": round(time.time()-started, 3)
    }

    print(json.dumps(result, indent=2), flush=True)
    return result

print("SOURCE SHA256:", environment["source_sha256"], flush=True)
print("PYTHON:", platform.python_version(), flush=True)
print("SYMPY:", sp.__version__, flush=True)
print("ENGINE: SymPy AGCA; FIELD: QQ", flush=True)

try:
    for n in CASES:
        result = audit(n)
        receipt["completed_cases"].append(result)
        write_json("results.json", receipt)

    final_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    require(
        final_hash == environment["source_sha256"],
        "Source changed during execution"
    )

    receipt["source_sha256_after"] = final_hash
    receipt["status"] = "PASSED"
    receipt["finished_utc"] = utc_now()
    write_json("results.json", receipt)

    print("\nHASH-BOUND MODULE AUDIT: PASSED", flush=True)
    print("Integral and all-n claims are not asserted.", flush=True)

except BaseException as error:
    receipt["status"] = "FAILED_OR_INTERRUPTED"
    receipt["finished_utc"] = utc_now()
    receipt["error"] = repr(error)
    receipt["traceback"] = traceback.format_exc()
    write_json("results.json", receipt)
    raise
