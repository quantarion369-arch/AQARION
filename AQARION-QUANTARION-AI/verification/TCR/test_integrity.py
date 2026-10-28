"""Adversarial tests on disposable fixtures, never original evidence."""
from pathlib import Path
import hashlib
import json
import runpy
import tempfile


def main():
    check = runpy.run_path(str(Path(__file__).with_name('verify_evidence.py')))['verify_manifest']
    cases = ['valid', 'changed', 'missing', 'extra', 'traversal', 'duplicate', 'symlink']
    for case in cases:
        with tempfile.TemporaryDirectory(prefix='tcr-integrity-test.') as directory:
            root = Path(directory)
            payload = root / 'payload.txt'
            payload.write_bytes(b'fixture\n')
            line = hashlib.sha256(payload.read_bytes()).hexdigest() + '  payload.txt\n'
            manifest = root / 'SHA256SUMS'
            manifest.write_text(line)
            if case == 'changed': payload.write_bytes(b'changed\n')
            elif case == 'missing': payload.unlink()
            elif case == 'extra': (root / 'extra.txt').write_bytes(b'extra\n')
            elif case == 'traversal': manifest.write_text('0'*64 + '  ../outside.txt\n')
            elif case == 'duplicate': manifest.write_text(line + line)
            elif case == 'symlink':
                payload.unlink()
                payload.symlink_to(root / 'absent-target')
            rejected = False
            try:
                check(root)
            except Exception:
                rejected = True
            if rejected != (case != 'valid'):
                raise RuntimeError('Unexpected integrity outcome: ' + case)
    print(json.dumps(dict(status='PASS', fixture_cases=7, damaged_fixtures_rejected=6)))


if __name__ == '__main__':
    main()
