"""Run the existing checker against the identified production implementation."""
import argparse
import hashlib
import importlib.util
from pathlib import Path
import runpy
import subprocess
import sys


def resolve_paths():
    package = Path(__file__).resolve().parents[2]
    root = Path(subprocess.check_output(
        ["git", "-C", str(package), "rev-parse", "--show-toplevel"],
        text=True,
    ).strip()).resolve()

    source = root / (
        "AQARION-QUANTARION-AI/verification/"
        "defect-transport/closure_profile.py"
    )
    checker = package / "dt_check/xcheck.py"
    oracle = package / "dt_check/prof.py"

    for label, path in (
        ("production source", source),
        ("checker", checker),
        ("oracle", oracle),
    ):
        if not path.is_file():
            raise FileNotFoundError(f"Missing {label}: {path}")
    return root, source, checker, oracle


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def result_exit_code(result):
    counts = [result.get(name) for name in ("cases", "bad", "fails")]
    if any(type(value) is not int for value in counts):
        raise RuntimeError("Checker did not return integer result counters")
    cases, bad, fails = counts
    if cases <= 0 or bad < 0 or fails < 0:
        raise RuntimeError("Checker returned invalid result counters")
    return 1 if bad or fails else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("limit", nargs="?", type=int, default=4)
    args = parser.parse_args(argv)
    if args.limit < 1:
        parser.error("limit must be at least 1")

    root, source, checker, oracle = resolve_paths()
    for label, path in (
        ("Actual source", source),
        ("Checker", checker),
        ("Oracle", oracle),
    ):
        print(label + ":", path.relative_to(root), flush=True)
        print(
            label + " SHA-256:",
            hashlib.sha256(path.read_bytes()).hexdigest(),
            flush=True,
        )

    old_path = list(sys.path)
    old_argv = list(sys.argv)
    names = ("closure_profile_repo", "prof")
    missing = object()
    previous = {name: sys.modules.get(name, missing) for name in names}

    try:
        sys.path.insert(0, str(source.parent))
        sys.path.insert(0, str(checker.parent))
        module = load_module("closure_profile_repo", source)
        load_module("prof", oracle)
        print("Loaded implementation:", module.__file__, flush=True)
        sys.argv = [str(checker), str(args.limit)]
        result = runpy.run_path(str(checker), run_name="__main__")
        code = result_exit_code(result)
        print(
            "CROSSCHECK_RESULT=" + ("PASS" if code == 0 else "FAIL"),
            flush=True,
        )
        return code
    finally:
        sys.path[:] = old_path
        sys.argv = old_argv
        for name, old in previous.items():
            if old is missing:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = old


if __name__ == "__main__":
    raise SystemExit(main())
