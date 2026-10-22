"""Gate D dispatcher tests. Temporary synthetic registries; no Lean or network."""
import ast
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parents[1]
MARKER = "SYNTHETIC_REPLAY_REACHED"

class GateDIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(
            prefix="claimlock-dispatch-"
        )
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.target = (
            self.root / "AQARION-QUANTARION-AI/TOOLS/CLAIMLOCK"
        )
        (self.target / "schemas").mkdir(parents=True)

        watched = [
            HERE / "workflow_check.py",
            HERE / "formal_binding.py",
            HERE / "schemas/registry.schema.json",
            HERE / "registry.json",
        ]
        self.before = {p: p.read_bytes() for p in watched}
        self.addCleanup(self.check_originals)

        for name in (
            "workflow_check.py",
            "formal_binding.py",
            "schemas/registry.schema.json",
        ):
            shutil.copyfile(HERE / name, self.target / name)

        self.gate = self.target / "workflow_check.py"
        self.replay = (
            self.root
            / "AQARION-QUANTARION-AI/verification/CLOSURE-GAP"
            / "closure_gap_replay.py"
        )
        self.replay.parent.mkdir(parents=True)
        self.replay.write_text(
            "print(" + repr(MARKER) + ")",
            encoding="utf-8",
        )
        self.registry = self.target / "registry.json"

        self.legacy = {
            "id": "TEST-GATE-LEGACY-001",
            "title": "Synthetic fixture",
            "status": "verified",
            "governance": "blocked",
            "evidence": "Synthetic",
            "note": "Synthetic",
            "cases": 1,
            "violations": 0,
        }
        self.formal = {
            "id": "TEST-GATE-FORMAL-001",
            "title": "Synthetic binding",
            "record_type": "formal",
            "claim_text": "Synthetic statement only",
            "status": "open",
            "governance": "blocked",
            "evidence": "Synthetic",
            "note": "Synthetic",
            "formal_evidence": {
                "repo":
                    "https://github.com/quantarion369-arch/AQARION-LEAN",
                "revision": "a" * 40,
                "source_path": "Fixture.lean",
                "source_file_sha256": "1" * 64,
                "declaration": "Fixture.theorem",
                "statement_sha256": "2" * 64,
                "receipt_path": "receipt.json",
                "receipt_sha256": "3" * 64,
                "correspondence_review": {
                    "state": "pending",
                    "reviewer": None,
                },
            },
        }

    def check_originals(self):
        for path, data in self.before.items():
            self.assertEqual(
                path.read_bytes(), data,
                "Real source/registry changed: " + str(path),
            )

    def run_gate(self, records):
        self.registry.write_text(
            json.dumps(records), encoding="utf-8"
        )
        before = self.registry.read_bytes()
        env = dict(os.environ)
        env.pop("AQARION_FORMAL_LEAN_ROOT", None)
        env["PYTHONDONTWRITEBYTECODE"] = "1"

        result = subprocess.run(
            [sys.executable, "-B", "-u", str(self.gate)],
            cwd=self.root,
            env=env,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(
            self.registry.read_bytes(), before,
            "Fixture registry mutated",
        )
        return result

    def test_legacy_registry_preserves_replay(self):
        r = self.run_gate([self.legacy])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("FORMAL BINDING SCOPE: 0", r.stdout)
        self.assertIn(MARKER, r.stdout)
        self.assertIn("WORKFLOW CHECK PASSED", r.stdout)

    def test_real_formal_validator_rejects_missing_lean_root(self):
        r = self.run_gate([self.formal])
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn(
            "AQARION_FORMAL_LEAN_ROOT is required", r.stdout
        )
        self.assertNotIn("REGISTRY SCHEMA CHECK FAILED", r.stdout)
        self.assertNotIn(MARKER, r.stdout)

    def test_mixed_registry_does_not_skip_formal_binding(self):
        r = self.run_gate([self.legacy, self.formal])
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn(
            "AQARION_FORMAL_LEAN_ROOT is required", r.stdout
        )
        self.assertNotIn(MARKER, r.stdout)

    def test_removing_validator_branch_exposes_bypass(self):
        baseline = self.run_gate([self.formal])
        self.assertEqual(baseline.returncode, 1)
        self.assertIn(
            "AQARION_FORMAL_LEAN_ROOT is required",
            baseline.stdout,
        )

        tree = ast.parse(self.gate.read_text())
        hits = [
            node for node in tree.body
            if isinstance(node, ast.If)
            and isinstance(node.test, ast.Name)
            and node.test.id == "formal_count"
        ]
        self.assertEqual(
            len(hits), 1,
            "Expected the real formal-binding branch",
        )
        tree.body.remove(hits[0])
        self.gate.write_text(
            ast.unparse(tree), encoding="utf-8"
        )

        mutant = self.run_gate([self.formal])
        self.assertEqual(
            mutant.returncode, 0, mutant.stdout + mutant.stderr
        )
        self.assertIn(MARKER, mutant.stdout)
        self.assertIn("WORKFLOW CHECK PASSED", mutant.stdout)

    def test_failed_replay_exit_is_preserved(self):
        self.replay.write_text(
            "print(" + repr(MARKER) + ")"
            + chr(10) + "raise SystemExit(7)"
        )
        r = self.run_gate([self.legacy])
        self.assertEqual(r.returncode, 7, r.stdout + r.stderr)
        self.assertNotIn("WORKFLOW CHECK PASSED", r.stdout)

    def test_schema_rejects_formal_computational_counts(self):
        bad = copy.deepcopy(self.formal)
        bad["cases"] = 0
        r = self.run_gate([bad])
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("REGISTRY SCHEMA CHECK FAILED", r.stdout)
        self.assertNotIn(MARKER, r.stdout)

    def test_duplicate_id_check_still_executes(self):
        r = self.run_gate([
            self.legacy, copy.deepcopy(self.legacy)
        ])
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("Duplicate claim IDs", r.stdout)
        self.assertNotIn(MARKER, r.stdout)

    def test_dispatcher_continues_after_synthetic_validator_acceptance(self):
        # Wiring-only control, not production receipt acceptance.
        stub = (
            "def validate_formal_bindings(records, claim_root, lean_root):"
            + chr(10)
            + "    print('SYNTHETIC_VALIDATOR_CALLED')"
            + chr(10)
            + "    return []"
        )
        (self.target / "formal_binding.py").write_text(
            stub, encoding="utf-8"
        )
        r = self.run_gate([self.formal])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertLess(
            r.stdout.index("SYNTHETIC_VALIDATOR_CALLED"),
            r.stdout.index(MARKER),
        )
        self.assertIn("WORKFLOW CHECK PASSED", r.stdout)

if __name__ == "__main__":
    unittest.main(verbosity=2)
