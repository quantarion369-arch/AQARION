import dataclasses
import unittest

from aqarion_core import Claim, EvidenceRecord, Status


class ModelTests(unittest.TestCase):
    def test_reference_keyword(self):
        record = EvidenceRecord(kind="replay", reference="receipt")
        self.assertEqual(record.reference, "receipt")

    def test_verified_default(self):
        self.assertIs(EvidenceRecord("replay", "receipt").verified, False)

    def test_frozen_reference(self):
        record = EvidenceRecord("replay", "receipt")
        with self.assertRaises(dataclasses.FrozenInstanceError):
            record.reference = "changed"

    def test_frozen_verified(self):
        record = EvidenceRecord("replay", "receipt")
        with self.assertRaises(dataclasses.FrozenInstanceError):
            record.verified = True

    def test_obsolete_keyword(self):
        with self.assertRaises(TypeError):
            EvidenceRecord(kind="replay", description="obsolete")

    def test_default_status(self):
        self.assertIs(Claim("A", "statement").status, Status.OPEN)

    def test_independent_containers(self):
        first = Claim("A", "first")
        second = Claim("B", "second")
        first.dependencies.append("BASE")
        first.evidence.append(EvidenceRecord("replay", "receipt"))
        first.provenance["source"] = "fixture"
        self.assertEqual(second.dependencies, [])
        self.assertEqual(second.evidence, [])
        self.assertEqual(second.provenance, {})


if __name__ == "__main__":
    unittest.main()
