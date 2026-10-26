"""Static UI guards; these are not browser race-execution tests."""
from pathlib import Path


PAGE = Path(__file__).resolve().parents[1] / "static/index.html"


def test_source_scope_controls_and_complete_view_exist():
    page = PAGE.read_text(encoding="utf-8")
    for marker in (
        'id="source-selector"',
        'id="open-source"',
        'id="source-view" hidden',
        'id="source-status"',
        "All sources — global search",
    ):
        assert marker in page


def test_source_list_loading_does_not_cancel_searches():
    page = PAGE.read_text(encoding="utf-8")
    loader = page.split("async function loadSources() {", 1)[1].split(
        "async function openCompleteSource()", 1
    )[0]
    assert 'fetch("/api/sources")' in loader
    assert "requestId" not in loader
    assert "controller.abort()" not in loader
    assert "controller =" not in loader


def test_source_actions_reuse_generation_and_safe_rendering():
    page = PAGE.read_text(encoding="utf-8")
    for marker in (
        'sourceSelect.addEventListener("change"',
        "const id = ++requestId",
        "id !== requestId",
        "validateScopedEvidence(data, selectedSource)",
        'sourceView.append(node("pre", data.text, "passage"))',
        'mode.addEventListener("change", handleModeChange)',
    ):
        assert marker in page
    for forbidden in (
        "innerHTML", "outerHTML", "insertAdjacentHTML", "document.write"
    ):
        assert forbidden not in page


def test_scoped_search_and_source_navigation_remain_distinct():
    page = PAGE.read_text(encoding="utf-8")
    assert '"&source_id=" + encodeURIComponent(selectedSource)' in page
    assert '"/api/sources/view?source_id="' in page
    assert "item.commit_sha !== selected.sha" in page
    assert "source.sha !== expected.sha" in page
    assert "not selected-source retrieval" in page
    assert "sourceSelect.disabled = claimsMode" in page
