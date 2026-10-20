from copy import deepcopy

import pytest

import context
import relationships as rel


def record():
    return deepcopy(rel.load_relationships()[0])


def test_all_three_pinned_anchors_reconstruct():
    item = record()
    for anchor in (
        item["subject"], item["object"],
        item["supporting_evidence"][0]["anchor"],
    ):
        citation = rel.validate_anchor(anchor)
        assert citation["passage"]
        assert citation["passage_sha256"] == anchor["passage_sha256"]


def test_old_wording_discovers_nonadjacent_correction_without_changing_context():
    query = "ALL VERIFIED — three independent checks, all clean."
    before = context.retrieve_with_context(query)
    saved = deepcopy(before)
    item = record()
    correction_id = rel.identity(item["subject"])

    assert rel.identity(before["seed_results"][0]) == rel.identity(item["object"])
    assert correction_id not in {
        rel.identity(passage)
        for passage in before["seed_results"] + before["supplementary_context"]
    }

    result = rel.resolve_related(
        before["seed_results"] + before["supplementary_context"]
    )
    assert before == saved
    assert result["relationship_diagnostics"] == []
    assert len(result["related_evidence"]) == 1
    found = result["related_evidence"][0]
    assert rel.identity(found["subject"]) == correction_id
    assert found["review_status"] == "pending"
    assert found["locator_validation"] == "passed"
    assert found["match_directions"] == ["correction_for_returned_statement"]


def test_correction_resolves_back_to_original_statement():
    item = record()
    result = rel.resolve_related([item["subject"]])
    assert len(result["related_evidence"]) == 1
    assert result["related_evidence"][0]["match_directions"] == [
        "original_statement_for_returned_correction"
    ]


@pytest.mark.parametrize("change", [
    {"commit_sha": "0" * 40},
    {"char_start": 2913},
    {"passage_sha256": "0" * 64},
    {"char_start": True},
    {"char_end": 999999999},
])
def test_invalid_anchor_is_not_displayed_as_valid(change):
    item = record()
    item["subject"].update(change)
    result = rel.resolve_related([item["object"]], records=[item])
    assert result["related_evidence"] == []
    assert len(result["relationship_diagnostics"]) == 1
    assert result["relationship_diagnostics"][0]["status"] == "invalid"


def test_unrelated_passage_has_no_invented_relationship():
    item = record()
    unrelated = item["supporting_evidence"][0]["anchor"]
    result = rel.resolve_related([unrelated])
    assert result == {
        "related_evidence": [],
        "relationship_diagnostics": [],
    }


def test_approval_requires_explicit_review_metadata():
    item = record()
    item["review_status"] = "approved"
    result = rel.resolve_related([item["object"]], records=[item])
    assert result["related_evidence"] == []
    assert result["relationship_diagnostics"]


def test_invalid_follow_up_invalidates_whole_relationship_package():
    item = record()
    item["supporting_evidence"][0]["anchor"]["passage_sha256"] = "0" * 64
    result = rel.resolve_related([item["object"]], records=[item])
    assert result["related_evidence"] == []
    assert result["relationship_diagnostics"]
