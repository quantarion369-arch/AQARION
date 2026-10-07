"""Run package integrity verification and the complete unittest suite."""

from pathlib import Path
import subprocess
import sys
import unittest


def main():
    root = Path(__file__).resolve().parents[1]
    verifier = root / "tools" / "verify_package.py"
    tests = root / "tests"

    print("REGRESSION_ROOT:", root, flush=True)

    if not verifier.is_file() or not tests.is_dir():
        print("REGRESSION_ERROR: Required verifier or tests directory missing")
        return 2

    try:
        completed = subprocess.run(
            [sys.executable, str(verifier), "--root", str(root)],
            cwd=root,
            check=False,
        )
    except OSError as exc:
        print("REGRESSION_ERROR:", str(exc))
        return 2

    if completed.returncode != 0:
        print("REGRESSION_STOPPED: Package verification failed")
        return 1

    sys.path.insert(0, str(root))
    loader = unittest.TestLoader()

    try:
        suite = loader.discover(str(tests), pattern="test*.py")
    except Exception as exc:
        print("REGRESSION_ERROR: Test discovery failed:", str(exc))
        return 2

    if loader.errors:
        for error in loader.errors:
            print(error)
        print("REGRESSION_ERROR: Test discovery reported errors")
        return 2

    count = suite.countTestCases()
    print("DISCOVERED_TESTS:", count, flush=True)

    if count == 0:
        print("REGRESSION_ERROR: No tests discovered")
        return 2

    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if not result.wasSuccessful():
        print("REGRESSION_FAILED")
        return 1

    print("REGRESSION_OK")
    print("SKIPPED_TESTS:", len(result.skipped))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
