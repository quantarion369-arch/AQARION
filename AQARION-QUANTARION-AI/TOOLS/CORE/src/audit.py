from .models import Claim


def audit_claim(claim: Claim) -> dict:
    return {
        "claim_id": claim.claim_id,
        "status": claim.status.value,
        "dependencies": len(claim.dependencies),
        "evidence": len(claim.evidence),
        "verified_evidence": sum(
            1 for e in claim.evidence if e.verified
        ),
        "provenance_present": bool(claim.provenance),
    }
