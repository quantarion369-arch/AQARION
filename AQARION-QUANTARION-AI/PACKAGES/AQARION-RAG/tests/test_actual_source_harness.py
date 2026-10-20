import importlib.util
from pathlib import Path
import subprocess
import sys

import pytest

PACKAGE = Path(__file__).resolve().parents[1]
HARNESS = PACKAGE / "research/closure-cost/check_actual_source.py"


def import_harness():
    spec = importlib.util.spec_from_file_location("harness_under_test", HARNESS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_import_does_not_execute_crosscheck(capsys):
    module = import_harness()
    assert callable(module.resolve_paths)
    assert callable(module.main)
    assert capsys.readouterr().out == ""


def test_paths_are_independent_of_current_directory(tmp_path, monkeypatch):
    module = import_harness()
    monkeypatch.chdir(tmp_path)
    root, source, checker, oracle = module.resolve_paths()
    expected_root = Path(subprocess.check_output(
        ["git", "-C", str(PACKAGE), "rev-parse", "--show-toplevel"],
        text=True,
    ).strip()).resolve()
    assert root == expected_root
    assert source == root / (
        "AQARION-QUANTARION-AI/verification/"
        "defect-transport/closure_profile.py"
    )
    assert checker == PACKAGE / "dt_check/xcheck.py"
    assert oracle == PACKAGE / "dt_check/prof.py"


@pytest.mark.parametrize("missing_name", ["source", "checker", "oracle"])
def test_missing_dependencies_are_rejected(tmp_path, monkeypatch, missing_name):
    module = import_harness()
    fake_package = tmp_path / "package"
    fake_script = fake_package / "research/closure-cost/check_actual_source.py"
    paths = {
        "source": tmp_path / (
            "AQARION-QUANTARION-AI/verification/"
            "defect-transport/closure_profile.py"
        ),
        "checker": fake_package / "dt_check/xcheck.py",
        "oracle": fake_package / "dt_check/prof.py",
    }
    for name, path in paths.items():
        if name != missing_name:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("", encoding="utf-8")
    monkeypatch.setattr(module, "__file__", str(fake_script))
    monkeypatch.setattr(
        module.subprocess,
        "check_output",
        lambda *args, **kwargs: str(tmp_path),
    )
    with pytest.raises(FileNotFoundError):
        module.resolve_paths()


@pytest.mark.parametrize("bad,fails", [(0, 0), (1, 0), (0, 1), (1, 1)])
def test_checker_failures_propagate(bad, fails):
    module = import_harness()
    expected = 1 if bad or fails else 0
    assert module.result_exit_code({
        "cases": 1, "bad": bad, "fails": fails
    }) == expected


@pytest.mark.parametrize("result", [
    {},
    {"cases": 0, "bad": 0, "fails": 0},
    {"cases": 1, "bad": -1, "fails": 0},
    {"cases": True, "bad": 0, "fails": 0},
])
def test_invalid_checker_results_are_rejected(result):
    with pytest.raises(RuntimeError):
        import_harness().result_exit_code(result)


def test_one_case_smoke_from_unrelated_directory(tmp_path):
    result = subprocess.run(
        [sys.executable, "-B", str(HARNESS), "1"],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "n<=1: cases=1" in result.stdout
    assert "profile mismatches=0" in result.stdout
    assert "repo self-check FAIL=0" in result.stdout
    assert "CROSSCHECK_RESULT=PASS" in result.stdout
    assert "Actual source SHA-256:" in result.stdout
    assert "Checker SHA-256:" in result.stdout
    assert "Oracle SHA-256:" in result.stdout
