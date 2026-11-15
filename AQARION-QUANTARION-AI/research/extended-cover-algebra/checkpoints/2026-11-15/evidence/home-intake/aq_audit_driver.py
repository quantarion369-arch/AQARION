#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

p = argparse.ArgumentParser()
p.add_argument("input", nargs="?")
p.add_argument("--root", default=str(Path.home()/"AQARION-tablet"))
p.add_argument("--ranks", action="store_true")
p.add_argument("--cas", default="M2",
               help='Example: "proot-distro login debian -- M2"')
p.add_argument("--timeout", type=int, default=600)
p.add_argument("--full-minors", action="store_true",
               help="Potentially enormous; disabled by default")
args = p.parse_args()

def out(*items):
    print(*items, flush=True)

def read_data(path):
    try:
        d = json.loads(path.read_text())
        if (isinstance(d, dict)
            and isinstance(d.get("variables"), list)
            and isinstance(d.get("weights"), list)
            and isinstance(d.get("matrices"), dict)
            and any(k in d["matrices"] for k in ("D2", "D3"))):
            return d
    except (OSError, ValueError, UnicodeError):
        pass
    return None

root = Path(args.root).expanduser()
chosen = None
data = None

if args.input:
    chosen = Path(args.input).expanduser().resolve()
    data = read_data(chosen)
    if data is None:
        sys.exit("Input is absent or not a supported matrix JSON object.")
else:
    preferred = [
        Path.cwd()/"audit-input.json",
        root/"audit-input.json",
    ]
    for candidate in preferred:
        d = read_data(candidate)
        if d is not None:
            chosen, data = candidate.resolve(), d
            break
    if data is None and root.is_dir():
        matches = []
        for folder, dirs, files in os.walk(root):
            dirs[:] = [x for x in dirs
                       if x not in {".git", "node_modules", ".venv",
                                    "__pycache__"}]
            for filename in files:
                if filename.endswith(".json"):
                    candidate = Path(folder)/filename
                    if candidate.stat().st_size > 30_000_000:
                        continue
                    d = read_data(candidate)
                    if d is not None:
                        matches.append((candidate.resolve(), d))
        if len(matches) == 1:
            chosen, data = matches[0]
        elif len(matches) > 1:
            out("MULTIPLE MATRIX INPUTS: choose one explicitly.")
            for candidate, _ in matches:
                out(candidate)
            sys.exit(2)

if data is None:
    out("NO USABLE MATRIX JSON FOUND.")
    out("Reading relevant existing files; not executing repository code.")
    research = root/"AQARION-QUANTARION-AI"/"research"
    locations = [research/"explicit-resolution-q",
                 research/"termux-audits"]
    for location in locations:
        if not location.is_dir():
            continue
        for f in sorted(location.iterdir()):
            if f.suffix.lower() not in {".py", ".txt", ".csv", ".md", ".m2"}:
                continue
            out("\n==", f, "==")
            lines = f.read_text(errors="replace").splitlines()
            if f.suffix.lower() in {".csv", ".md", ".txt"}:
                for line in lines[:55]:
                    out(line[:350])
            else:
                hits = [i for i, line in enumerate(lines)
                        if re.search(
                            r'D[12345]|d[12345]|symbols|variables|weights|'
                            r'QQ\[|PolynomialRing|semigroup|degree',
                            line)]
                for i in hits[:35]:
                    out(f"{i+1}: {lines[i][:350]}")
    out("\nSTOP: actual matrices were not reconstructed or verified.")
    out("The excerpts identify what parser/export step is needed next.")
    sys.exit(2)

out("USING ACTUAL INPUT:", chosen)
old = Path.home()/"aq_resolution_audit.py"
if old.is_file():
    command = [sys.executable, str(old), str(chosen),
               "--timeout", str(args.timeout)]
    if args.ranks:
        command.append("--ranks")
    result = subprocess.run(command)
    if result.returncode:
        out("SymPy audit reported a failure or stopped; review above.")
else:
    out("Existing SymPy audit missing:", old)

names = data["variables"]
weights = data["weights"]
if (not names or len(set(names)) != len(names)
    or any(not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", n)
           for n in names)
    or len(weights) != len(names)
    or any(type(w) is not int or w <= 0 for w in weights)):
    sys.exit("Invalid variable names or positive weights.")

import sympy as sp
symbols = tuple(sp.Symbol(n) for n in names)
local = dict(zip(names, symbols))

def entry(text):
    e = sp.sympify(str(text).replace("^", "**"), locals=local)
    if e.free_symbols - set(symbols):
        raise ValueError("Undeclared variable in matrix entry.")
    poly = sp.Poly(e, *symbols, domain=sp.QQ)
    terms = []
    for mon, coefficient in poly.terms():
        c = sp.Rational(coefficient)
        factors = [f"({c.p}/{c.q})"]
        factors += [f"{name}^{power}"
                    for name, power in zip(names, mon) if power]
        terms.append("*".join(factors))
    return "(" + "+".join(terms) + ")"

def m2matrix(raw):
    return "matrix{" + ",".join(
        "{" + ",".join(entry(x) for x in row) + "}" for row in raw
    ) + "}"

shifts = [
    [0], [3]*8+[4]*6,
    [4]*3+[5]*24+[6]*8,
    [6]*8+[7]*24+[8]*3,
    [8]*6+[9]*8, [12]
]
mats = data["matrices"]
expected = {1:(1,14), 2:(14,35), 3:(35,35),
            4:(35,14), 5:(14,1)}
code = [
    "P=QQ[" + ",".join(names) + ",Degrees=>{"
    + ",".join(map(str, weights)) + "}];",
    'print "BASE RING"; print P;',
    f'print ("CONDITIONAL a = " | toString(12-{sum(weights)}));'
]
for i in range(1, 6):
    key = f"D{i}"
    if key not in mats:
        continue
    raw = mats[key]
    nr, nc = expected[i]
    if len(raw) != nr or any(len(row) != nc for row in raw):
        sys.exit(f"{key}: wrong matrix dimensions.")
    code.append(f"{key}={m2matrix(raw)};")
    code.append(
        f'print ("{key} fraction-field rank = " | toString(rank {key}));'
    )

for i in range(1, 5):
    if f"D{i}" in mats and f"D{i+1}" in mats:
        code.append(
            f'print ("D{i}D{i+1}=0: " | '
            f'toString(D{i}*D{i+1} == 0));'
        )

for i, size, target in [(2,13,4), (3,22,3)]:
    key = f"D{i}"
    if key not in mats:
        continue
    witnesses = data.get("minor_witnesses", {}).get(key, [])
    expressions = []
    for witness in witnesses:
        rows = witness["rows"]
        cols = witness["cols"]
        nr, nc = expected[i]
        if (len(rows) != size or len(cols) != size
            or len(set(rows)) != size or len(set(cols)) != size
            or any(type(x) is not int or x < 1 or x > nr for x in rows)
            or any(type(x) is not int or x < 1 or x > nc for x in cols)):
            sys.exit(f"Invalid selected minor for {key}")
        rr = ",".join(str(x-1) for x in rows)
        cc = ",".join(str(x-1) for x in cols)
        expressions.append(f"det submatrix({key},{{{rr}}},{{{cc}}})")
    if expressions:
        J = f"J{i}"
        code += [
            f"{J}=ideal(" + ",".join(expressions) + ");",
            f'print "{key}: SELECTED-MINOR IDEAL";',
            f"print {J};",
            f"if {J} == ideal(1_P) then "
            f'print "PASS: selected ideal is the unit ideal" else (',
            f"  h=codim {J};",
            '  print ("selected ideal grade = " | toString h);',
            f"  if h >= {target} then",
            f'    print "PASS: full minor ideal grade >= {target}"',
            '  else print "INCONCLUSIVE for full minor ideal";',
            ");"
        ]
    else:
        code.append(f'print "{key}: no selected-minor certificate supplied";')
    if args.full_minors:
        code += [
            f'print "WARNING: computing full {size}-minor ideal of {key}";',
            f"K{i}=minors({size},{key});",
            f"if K{i} == ideal(1_P) then "
            'print "Full minor ideal is the unit ideal" else',
            f'print ("FULL minor ideal grade = " | toString(codim K{i}));'
        ]

code.append("exit 0;")
source = "\n".join(code)
out("\n=== COMPLETE GENERATED MACAULAY2 PROGRAM ===")
out(source)
cas = shlex.split(args.cas)
if not cas or shutil.which(cas[0]) is None:
    out("\nCAS NOT AVAILABLE:", args.cas)
    out("Program printed above, but not executed.")
    sys.exit(2)

try:
    with tempfile.TemporaryDirectory(prefix="aq-cas-") as temp:
        script = Path(temp)/"audit.m2"
        script.write_text(source)
        result = subprocess.run(
            cas + ["--script", str(script)],
            text=True, capture_output=True, timeout=args.timeout
        )
        out(result.stdout)
        if result.stderr:
            out(result.stderr)
        out("CAS EXIT CODE:", result.returncode)
except subprocess.TimeoutExpired:
    out("INCONCLUSIVE: CAS timeout reached.")
    sys.exit(2)
