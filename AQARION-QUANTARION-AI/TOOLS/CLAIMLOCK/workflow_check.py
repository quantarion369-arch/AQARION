#!/usr/bin/env python3
"""Gate D: automated registry consistency check. Run before every push. Exit 1 on failure."""
import json, sys, os, re

# AQARION REPLAY HOOK
import subprocess as _sp
from pathlib import Path as _Path
_REPLAY = _Path(__file__).resolve().parents[2] / 'verification/CLOSURE-GAP/closure_gap_replay.py'

REG = 'AQARION-QUANTARION-AI/TOOLS/CLAIMLOCK/registry.json'
from jsonschema import Draft202012Validator
_ROOT = _Path(__file__).resolve().parents[3]
with (_ROOT / REG).open() as stream:
    d = json.load(stream)
with (_Path(__file__).parent / 'schemas/registry.schema.json').open() as stream:
    schema = json.load(stream)
Draft202012Validator.check_schema(schema)
schema_errors = list(Draft202012Validator(schema).iter_errors(d))
if schema_errors:
    print('REGISTRY SCHEMA CHECK FAILED:')
    for error in schema_errors:
        location = '/'.join(str(part) for part in error.absolute_path) or '<root>'
        print(f' - {location}: {error.message}')
    raise SystemExit(1)
errors = []

# 1. Unique IDs
ids = [c['id'] for c in d]
if len(ids) != len(set(ids)):
    errors.append('Duplicate claim IDs')

# 2. Valid status/governance enums
VALID_S = set(schema['items']['properties']['status']['enum'])
VALID_G = set(schema['items']['properties']['governance']['enum'])
for c in d:
    if c.get('status') not in VALID_S: errors.append(f"{c['id']}: bad status {c.get('status')}")
    if c.get('governance') not in VALID_G: errors.append(f"{c['id']}: bad governance {c.get('governance')}")

# 3. Contradiction: conjecture status + proof language in evidence/note
PROOF_WORDS = re.compile(r'\b(proved|proof|proved symbolically|algebraic proof|combinatorial proof)\b', re.I)
for c in d:
    if c.get('status') == 'conjecture':
        text = (c.get('evidence','') or '') + (c.get('note','') or '')
        text = text.replace('proof status unconfirmed', '')
        if PROOF_WORDS.search(text):
            errors.append(f"{c['id']}: conjecture status but proof language present")

# 4. Receipt paths exist
for c in d:
    for m in re.findall(r'[\w/.-]+\.(?:json|md)', (c.get('note','') or '') + (c.get('evidence','') or '')):
        if m.startswith('AQARION') and not (_ROOT / m).exists():
            errors.append(f"{c['id']}: referenced artifact missing: {m}")

if errors:
    print('WORKFLOW CHECK FAILED:'); [print(' -', e) for e in errors]; sys.exit(1)
_r = _sp.run([sys.executable, str(_REPLAY), '11'], cwd=_ROOT)
if _r.returncode != 0:
    raise SystemExit(_r.returncode)
unknown_counts = sum(c['cases'] is None or c['violations'] is None for c in d)
print(f'WORKFLOW CHECK PASSED: {len(d)} claims; consistency and replay checks passed.')
print(f'NOTICE: {unknown_counts} records retain explicitly unknown count scope; historical claims are not comprehensively certified.')