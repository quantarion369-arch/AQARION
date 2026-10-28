"""Verify archive integrity and replay only the small scalar fixtures."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import re
import subprocess
import sys


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def verify_manifest(root, sealed=None):
    require(root.is_dir() and not root.is_symlink(), 'Unsafe package root')
    manifest = root / 'SHA256SUMS'
    require(manifest.is_file() and not manifest.is_symlink(), 'Missing manifest')
    raw = manifest.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    require(sealed is None or digest == sealed, 'Sealed manifest changed')
    expected = {}
    for line in raw.decode('utf-8').splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        require(match is not None, 'Malformed manifest entry')
        value, name = match.groups()
        path = PurePosixPath(name)
        require(not path.is_absolute() and '..' not in path.parts
                and '\\' not in name and str(path) == name
                and name not in ('SHA256SUMS', '.'), 'Unsafe manifest path')
        require(name not in expected, 'Duplicate manifest path')
        expected[name] = value
    require(bool(expected), 'Empty manifest')
    actual = set()
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'Symlink in package')
        if path.is_dir():
            continue
        require(path.is_file(), 'Nonregular package entry')
        name = path.relative_to(root).as_posix()
        if name != 'SHA256SUMS':
            actual.add(name)
    require(actual == set(expected), 'Missing or extra package files')
    for name, value in expected.items():
        require(hashlib.sha256((root / name).read_bytes()).hexdigest() == value,
                'Checksum differs: ' + name)
    return dict(files=len(expected)+1, manifest_sha256=digest)


def main():
    root = Path(__file__).resolve().parent
    old = root / 'temporal-circuits-001'
    scalar = root / 'scalar-temporal-circuits-002'
    old_seal = 'fa71b31340ea9c564f790e70100be5a0cc40d4a0854a3a03cf03dd6fc8069dde'
    packages = {
        old.name: verify_manifest(old, old_seal),
        scalar.name: verify_manifest(scalar),
    }
    require(packages[old.name]['files'] == 18, 'Archive count changed')
    require(packages[scalar.name]['files'] == 8, 'Scalar package count changed')
    status = json.loads((scalar / 'STATUS.json').read_text())
    require(status.get('preparation_status') == 'PASS', 'Preparation not PASS')
    require(status.get('formal_proof_machine_checked') is False,
            'Unexpected formal-proof status')
    saved = json.loads((scalar / 'checks.json').read_text())
    result = subprocess.run(
        [sys.executable, '-I', '-B', str(scalar / 'verify.py')],
        cwd=scalar, capture_output=True, text=True, timeout=20)
    require(result.returncode == 0, 'Targeted scalar checker failed')
    fresh = json.loads(result.stdout)
    require(fresh == saved, 'Fresh fixture output differs from saved output')
    require(fresh.get('status') == 'PASS', 'Fixture status not PASS')
    require(len(fresh.get('witness_checks', [])) == 9, 'Witness count differs')
    require(len(fresh.get('counting_formula_values', {})) == 10, 'Formula count differs')
    require(fresh.get('exhaustive_census_executed') is False, 'Wrong execution scope')
    require(verify_manifest(old, old_seal) == packages[old.name], 'Archive changed')
    require(verify_manifest(scalar) == packages[scalar.name], 'Scalar package changed')
    print(json.dumps(dict(status='PASS', packages=packages,
        fresh_witness_checks=9, fresh_formula_arithmetic_checks=10,
        exhaustive_census_executed=False, formal_proof_machine_check=False), indent=2))


if __name__ == '__main__':
    main()
