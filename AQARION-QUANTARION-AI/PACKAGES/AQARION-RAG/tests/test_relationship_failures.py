from copy import deepcopy
import json
import subprocess

import pytest

import relationships as rel


@pytest.mark.parametrize("bad", [None, "not an object", 7, []])
def test_malformed_record_returns_diagnostic(bad):
    result = rel.resolve_related([], records=[bad])
    assert result["related_evidence"] == []
    assert len(result["relationship_diagnostics"]) == 1


@pytest.mark.parametrize("error", [
    FileNotFoundError("injected missing registry"),
    json.JSONDecodeError("injected invalid JSON", "{", 1),
    rel.RelationshipError("injected unsupported schema"),
])
def test_registry_load_failure_degrades(monkeypatch, error):
    def fail():
        raise error
    monkeypatch.setattr(rel, "load_relationships", fail)
    result = rel.resolve_related([])
    assert result["related_evidence"] == []
    diagnostic = result["relationship_diagnostics"][0]
    assert diagnostic["relationship_id"] == "registry"
    assert diagnostic["status"] == "unavailable_or_invalid"


def test_unavailable_pinned_source_degrades(monkeypatch):
    record = deepcopy(rel.load_relationships()[0])
    def fail(*args):
        raise subprocess.CalledProcessError(128, ["git", "show", "missing"])
    monkeypatch.setattr(rel.retrieve, "load_at_sha", fail)
    result = rel.resolve_related([record["object"]], records=[record])
    assert result["related_evidence"] == []
    assert len(result["relationship_diagnostics"]) == 1


def test_invalid_record_does_not_hide_valid_relationship():
    record = deepcopy(rel.load_relationships()[0])
    result = rel.resolve_related(
        [record["object"]], records=[None, record]
    )
    assert len(result["related_evidence"]) == 1
    assert result["related_evidence"][0]["review_status"] == "pending"
    assert len(result["relationship_diagnostics"]) == 1


def test_null_supporting_evidence_degrades():
    record = deepcopy(rel.load_relationships()[0])
    record["supporting_evidence"] = None
    result = rel.resolve_related([record["object"]], records=[record])
    assert result["related_evidence"] == []
    assert len(result["relationship_diagnostics"]) == 1


@pytest.mark.parametrize("records", [{}, "invalid", 42])
def test_invalid_registry_container_degrades(records):
    result = rel.resolve_related([], records=records)
    assert result["related_evidence"] == []
    assert result["relationship_diagnostics"][0]["relationship_id"] == "registry"
