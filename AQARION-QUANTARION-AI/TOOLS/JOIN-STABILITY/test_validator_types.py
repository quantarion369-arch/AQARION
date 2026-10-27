
"""Maintained malformed-type regressions for JOIN-STABILITY.

Fixtures originate from the source-bound candidate verification.
No temporary run directory is required to execute these tests.
"""

import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parent

spec = importlib.util.spec_from_file_location(
    "_join_type_test_verifier", ROOT / "verify.py"
)
V = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = V
spec.loader.exec_module(V)
V.ROOT = ROOT

manifest = json.loads(
    (ROOT / "manifest.json").read_text(encoding="utf-8")
)

def read_records(name):
    return [
        json.loads(line)
        for line in (ROOT / name).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

claims = read_records("claims.jsonl")
evidence = read_records("evidence.jsonl")

def positives(module):
    module.check_manifest_shape(copy.deepcopy(manifest))
    module.check_audit_contract(copy.deepcopy(manifest))

    ids = module.validate_claims(copy.deepcopy(claims))
    evidence_ids = module.validate_evidence(
        copy.deepcopy(evidence), ids
    )

    return sorted(ids), sorted(evidence_ids)


base_claim = {
    "claim_id": "A",
    "version": "1.0.0",
    "statement": "test",
    "mathematical_status": "DEFINITION",
    "evidence_class": "[D]",
    "domain": "test",
    "dependencies": [],
    "proof_artifact": None,
}

base_evidence = {
    "evidence_id": "EV-A",
    "claim_id": "A",
    "class": "[R]",
    "type": "test",
    "artifact": "README.md",
    "status": "TEST",
    "description": "test",
}

cases = []

def manifest_case(name, field, value, location):
    value_manifest = copy.deepcopy(manifest)
    value_manifest[field] = value
    cases.append((
        name, location,
        lambda module, data=value_manifest:
            module.check_manifest_shape(copy.deepcopy(data)),
    ))

manifest_case(
    "policy_null", "verification_policy", None,
    "manifest.verification_policy",
)
manifest_case(
    "policy_array", "verification_policy", [],
    "manifest.verification_policy",
)
manifest_case(
    "audit_null", "audit", None,
    "manifest.audit",
)
manifest_case(
    "status_object", "status", {},
    "manifest.status",
)
manifest_case(
    "artifact_entry_integer", "required_artifacts", [7],
    "manifest.required_artifacts[0]",
)
manifest_case(
    "registry_path_null", "claim_registry", None,
    "manifest.claim_registry",
)

for name, field, value, location in [
    ("claim_class_array", "evidence_class", [],
     "claim[1].evidence_class"),
    ("claim_status_object", "mathematical_status", {},
     "claim[1].mathematical_status"),
    ("proof_artifact_false", "proof_artifact", False,
     "claim[1].proof_artifact"),
]:
    record = dict(base_claim)
    record[field] = value
    cases.append((
        name, location,
        lambda module, data=record:
            module.validate_claims([copy.deepcopy(data)]),
    ))

for name, field, value, location in [
    ("evidence_claim_object", "claim_id", {},
     "evidence[1].claim_id"),
    ("evidence_class_array", "class", [],
     "evidence[1].class"),
    ("evidence_artifact_integer", "artifact", 7,
     "evidence[1].artifact"),
]:
    record = dict(base_evidence)
    record[field] = value
    cases.append((
        name, location,
        lambda module, data=record:
            module.validate_evidence(
                [copy.deepcopy(data)], {"A"}
            ),
    ))

cases.append((
    "package_path_integer",
    "package_path",
    lambda module: module.safe_package_path(7),
))

policy_boolean = copy.deepcopy(manifest)
policy_boolean["verification_policy"][
    "reject_unknown_record_fields"
] = []

cases.append((
    "policy_flag_array",
    "manifest.verification_policy.reject_unknown_record_fields",
    lambda module:
        module.check_manifest_shape(copy.deepcopy(policy_boolean)),
))

audit_boolean = copy.deepcopy(manifest)
audit_boolean["audit"]["expected"]["1"] = [True, 0]

cases.append((
    "audit_boolean_count",
    "manifest.audit.expected.1",
    lambda module:
        module.check_audit_contract(copy.deepcopy(audit_boolean)),
))

def outcome(module, action):
    try:
        action(module)
    except Exception as exc:
        return {
            "exception": type(exc).__name__,
            "message": str(exc),
            "controlled": isinstance(exc, module.VerificationError),
        }
    return {
        "exception": None,
        "message": "ACCEPTED_BY_TARGET_FUNCTION",
        "controlled": False,
    }



if len(cases) != 15 or len({name for name, _, _ in cases}) != 15:
    raise RuntimeError("Expected fifteen unique malformed-type controls")


class TypeBoundaryTests(unittest.TestCase):
    def test_actual_manifest_and_registries(self):
        actual = positives(V)
        expected = (
            sorted(record["claim_id"] for record in claims),
            sorted(record["evidence_id"] for record in evidence),
        )
        self.assertEqual(actual, expected)

    def test_existing_in_memory_controls(self):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            V.run_negative_control_self_tests()
        text = stream.getvalue()
        self.assertIn("POSITIVE_CONTROLS=2/2", text)
        self.assertIn("NEGATIVE_CONTROLS=10/10", text)


def make_type_test(location, action):
    def test(self):
        first = outcome(V, action)
        second = outcome(V, action)
        self.assertEqual(first["exception"], "VerificationError")
        self.assertTrue(first["controlled"])
        self.assertTrue(
            first["message"].startswith(
                f"TYPE_ERROR: {location}:"
            ),
            first["message"],
        )
        self.assertEqual(first, second)
    return test


for name, location, action in cases:
    setattr(
        TypeBoundaryTests,
        "test_type_" + name,
        make_type_test(location, action),
    )


if __name__ == "__main__":
    unittest.main(verbosity=2)
