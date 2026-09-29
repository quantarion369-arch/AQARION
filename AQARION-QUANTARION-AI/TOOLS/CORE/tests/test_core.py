from aqarion_core import Claim, EvidenceRecord, Status, audit_claim


def test_claim_audit():
    claim = Claim(
        claim_id="AQ-CORE-001",
        statement="test claim",
        status=Status.CANDIDATE,
        dependencies=["definition"],
        evidence=[
            EvidenceRecord(
                "computation",
                "test",
                verified=True,
            )
        ],
        provenance={"source": "local-test"},
    )

    result = audit_claim(claim)

    assert result["claim_id"] == "AQ-CORE-001"
    assert result["verified_evidence"] == 1
    assert result["provenance_present"] is True
