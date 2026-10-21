#!/usr/bin/env python3
"""Standalone CLAIMLOCK fixture regression runner; replay is stubbed."""
import hashlib
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[4]
AI = Path("AQARION-QUANTARION-AI")
CHECKER = AI / "TOOLS/CLAIMLOCK/workflow_check.py"
SCHEMA = AI / "TOOLS/CLAIMLOCK/schemas/registry.schema.json"
REGISTRY = AI / "TOOLS/CLAIMLOCK/registry.json"
ARTIFACT = AI / "regression-fixtures/receipt.json"
REPLAY = AI / "verification/CLOSURE-GAP/closure_gap_replay.py"


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, sort_keys=True) + chr(10),
        encoding="utf-8",
    )


def main():
    frozen = {p: (ROOT / p).read_bytes() for p in (CHECKER, SCHEMA)}
    validator = Draft202012Validator(json.loads(frozen[SCHEMA]))
    validator.check_schema(validator.schema)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    evidence = Path(tempfile.gettempdir()) / (
        "claimlock-fixtures-" + stamp
    )
    evidence.mkdir(parents=True, exist_ok=False)
    write_json(evidence / "run-status.json", {"complete": False})
    write_json(evidence / "inputs.json", {
        "source_root": str(ROOT),
        "sha256": {
            str(p): hashlib.sha256(b).hexdigest()
            for p, b in frozen.items()
        },
        "harness_sha256": hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest(),
        "python": sys.version,
        "executable": sys.executable,
        "jsonschema": importlib.metadata.version("jsonschema"),
        "mathematics_tested": False,
    })

    record = {
        "id": "TEST-CLAIM-001",
        "title": "Synthetic fixture claim",
        "status": "verified",
        "governance": "active",
        "evidence": "",
        "cases": 1,
        "violations": 0,
        "note": "Artifact: " + ARTIFACT.as_posix(),
    }
    cases = [
        "valid-root",
        "valid-foreign",
        "missing-artifact",
        "duplicate-id",
        "invalid-status",
        "proof-conflict",
        "replay-failure",
    ]
    results = []
    print("RECEIPT: " + str(evidence), flush=True)

    for name in cases:
        result = {"case": name, "pass": False}
        try:
            with tempfile.TemporaryDirectory(
                prefix="claimlock-fixture-"
            ) as tmp:
                base = Path(tmp)
                repo = base / "repo"
                foreign = base / "foreign"
                foreign.mkdir()

                for relative, data in frozen.items():
                    target = repo / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(data)
                    if target.read_bytes() != data:
                        raise AssertionError("Source copy changed")

                data = [dict(record)]
                validator.validate(data)
                write_json(repo / ARTIFACT, {"fixture": True})

                if name == "missing-artifact":
                    (repo / ARTIFACT).unlink()
                elif name == "duplicate-id":
                    data.append(dict(record))
                elif name == "invalid-status":
                    data[0]["status"] = "not-a-valid-status"
                elif name == "proof-conflict":
                    data[0]["status"] = "conjecture"
                    data[0]["evidence"] = "A proof is claimed here."

                if name != "invalid-status":
                    validator.validate(data)

                write_json(repo / REGISTRY, data)
                write_json(evidence / (name + "-registry.json"), data)

                exit_code = 23 if name == "replay-failure" else 0
                stub = chr(10).join([
                    "import json, sys",
                    "from pathlib import Path",
                    "marker = Path(__file__).with_name('replay-called.json')",
                    "marker.write_text(json.dumps({'args': sys.argv[1:], 'exit_code': "
                    + str(exit_code) + "}))",
                    "raise SystemExit(" + str(exit_code) + ")",
                    "",
                ])
                replay = repo / REPLAY
                replay.parent.mkdir(parents=True, exist_ok=True)
                replay.write_text(stub, encoding="utf-8")
                marker_path = replay.with_name("replay-called.json")

                result["registry_sha256"] = hashlib.sha256(
                    (repo / REGISTRY).read_bytes()
                ).hexdigest()
                result["stub_sha256"] = hashlib.sha256(
                    replay.read_bytes()
                ).hexdigest()

                cwd = foreign if name == "valid-foreign" else repo
                proc = subprocess.run(
                    [sys.executable, str(repo / CHECKER)],
                    cwd=cwd,
                    capture_output=True,
                    text=True,
                    timeout=45,
                )
                marker = (
                    json.loads(marker_path.read_text())
                    if marker_path.exists() else None
                )
                output = proc.stdout + chr(10) + proc.stderr
                expected = (
                    0 if name.startswith("valid-")
                    else (23 if name == "replay-failure" else 1)
                )
                checks = {
                    "return_code": proc.returncode == expected
                }

                if name.startswith("valid-") or name == "replay-failure":
                    checks["replay_marker"] = marker == {
                        "args": ["11"],
                        "exit_code": exit_code,
                    }
                    checks["pass_message"] = (
                        ("WORKFLOW CHECK PASSED" in proc.stdout)
                        == name.startswith("valid-")
                    )
                else:
                    checks["replay_not_called"] = marker is None
                    checks["no_pass_message"] = (
                        "WORKFLOW CHECK PASSED" not in output
                    )
                    phrases = {
                        "missing-artifact": [
                            "referenced artifact missing: "
                            + ARTIFACT.as_posix()
                        ],
                        "duplicate-id": ["Duplicate claim IDs"],
                        "invalid-status": [
                            "REGISTRY SCHEMA CHECK FAILED:",
                            "0/status:",
                            "not-a-valid-status",
                        ],
                        "proof-conflict": [
                            "conjecture status but proof language present"
                        ],
                    }
                    checks["diagnostic"] = all(
                        phrase in output for phrase in phrases[name]
                    )

                result.update(
                    returncode=proc.returncode,
                    expected=expected,
                    checks=checks,
                    stdout=proc.stdout,
                    stderr=proc.stderr,
                    marker=marker,
                    **{"pass": all(checks.values())},
                )

        except Exception as exc:
            result["error"] = type(exc).__name__ + ": " + str(exc)

        write_json(evidence / (name + ".json"), result)
        results.append(result)
        print(
            ("PASS " if result["pass"] else "FAIL ") + name,
            flush=True,
        )
        if "error" in result:
            print("  " + result["error"][:240], flush=True)

    passed = sum(r["pass"] for r in results)
    write_json(evidence / "summary.json", {
        "complete": True,
        "passed": passed,
        "total": len(cases),
        "mathematics_tested": False,
        "results": results,
    })
    write_json(evidence / "run-status.json", {
        "complete": True,
        "passed": passed,
        "total": len(cases),
    })
    print(str(passed) + "/" + str(len(cases)) + " passed")
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    raise SystemExit(main())
