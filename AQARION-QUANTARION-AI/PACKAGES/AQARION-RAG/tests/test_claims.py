from claims import parse_claims, retrieve_claims

def test_parses_claims():
    claims = parse_claims()
    assert len(claims) > 10
    assert any(c["status"] for c in claims)

def test_artifact_backed_claim():
    hits = retrieve_claims("closure cost", has_artifact=True)
    assert len(hits) >= 1
    assert all(c["artifacts"] for c in hits)
    assert hits[0]["artifacts"][0].startswith("e97325fe")
