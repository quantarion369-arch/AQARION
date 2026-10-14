from supersedes import find_supersedes
from claims import parse_claims

def test_returns_list_of_pairs():
    claims = parse_claims()
    pairs = find_supersedes(claims)
    assert isinstance(pairs, list)
    for src, dst in pairs:
        assert isinstance(src, str) and isinstance(dst, str)
        assert len(src) > 0 and len(dst) > 0
