from graph import build_index, evidence_chain, dependents_of
from claims import parse_claims
from supersedes import find_supersedes

def test_dependents_of_artifact():
    claims = parse_claims()
    h = "e97325fedd0ee6a5d9223003b857358ce5ba303c483603b36215eb233f115db1"
    deps = dependents_of(claims, h)
    assert len(deps) == 1
    assert "Actual production-source cross-check" in deps[0]

def test_dependents_of_unknown_hash():
    claims = parse_claims()
    assert dependents_of(claims, "dead" * 16) == []

def test_evidence_chain_no_infinite_loop():
    claims = parse_claims()
    chain = evidence_chain(claims,
        "Provenance correction and actual-source check (2026-10-14)")
    assert len(chain) >= 1
    sections = [c["section"] for c in chain]
    assert len(sections) == len(set(sections))

def test_supersedes_finds_one():
    claims = parse_claims()
    pairs = find_supersedes(claims)
    assert len(pairs) == 1
    assert "Provenance correction" in pairs[0][0]
