from pathlib import Path
import hashlib
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True

repo = Path.home() / "AQARION"
pkg = repo / "AQARION-QUANTARION-AI/PACKAGES/AQARION-RAG"
page = pkg / "static/index.html"
test = pkg / "tests/test_source_scope_ui.py"
work = Path(__file__).resolve().parent

original = page.read_bytes()
relative = str(page.relative_to(repo))

if page.is_symlink() or test.exists():
    raise RuntimeError(
        "Page is a symlink or UI test already exists. Nothing changed."
    )

check = subprocess.run(
    ["git", "-C", str(repo), "diff", "--quiet", "HEAD", "--", relative]
)
if check.returncode:
    raise RuntimeError("Browser already has local changes. Nothing overwritten.")

def edit(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"Anchor mismatch: {label}; expected 1, found {count}"
        )
    return text.replace(old, new, 1)

html = original.decode("utf-8")

html = edit(
    html, "</style>",
    ".source-tools{display:flex;gap:10px;flex-wrap:wrap;align-items:center}\n"
    "#source-selector{flex:1;min-width:0;max-width:100%}\n"
    "#source-view pre{font:inherit;white-space:pre-wrap;overflow-wrap:anywhere}\n"
    "button:disabled{cursor:default;opacity:.55}\n"
    "</style>",
    "source control styles",
)

html = edit(
    html,
    '</form>\n<p id="status"',
    '''</form>
<div class="source-tools">
<label for="source-selector">Pinned source</label>
<select id="source-selector">
<option value="">All sources — global search</option>
</select>
<button id="open-source" type="button" disabled>Open complete source</button>
</div>
<p id="source-status" class="muted" role="status" aria-live="polite">
Loading source list…
</p>
<p id="status"''',
    "source controls",
)

html = edit(
    html,
    '<div id="out"></div>',
    '<div id="out"></div>\n'
    '<section id="source-view" hidden aria-label="Complete pinned source"></section>',
    "complete-source container",
)

html = edit(
    html,
    'const mode = document.getElementById("mode");\n',
    'const mode = document.getElementById("mode");\n'
    'const sourceSelect = document.getElementById("source-selector");\n'
    'const openSource = document.getElementById("open-source");\n'
    'const sourceStatus = document.getElementById("source-status");\n'
    'const sourceView = document.getElementById("source-view");\n'
    'const sourceEntries = new Map();\n',
    "source DOM references",
)

html = edit(
    html,
    "async function search() {\n",
    "async function search() {\n"
    "  syncSourceControls();\n"
    "  hideSourceView();\n"
    '  const selectedSource = mode.value === "passages" ? sourceSelect.value : "";\n',
    "search scope capture",
)

html = edit(
    html,
    '  try {\n    const response = await fetch(endpoint + "?q=" + encodeURIComponent(query),',
    '  const scopeParameter = selectedSource ?\n'
    '    "&source_id=" + encodeURIComponent(selectedSource) : "";\n\n'
    '  try {\n'
    '    const response = await fetch(endpoint + "?q=" + encodeURIComponent(query) + scopeParameter,',
    "scoped search URL",
)

html = edit(
    html,
    '    if (id !== requestId) return;\n    out.replaceChildren();\n',
    '    if (id !== requestId) return;\n'
    '    if (selectedMode === "passages" && selectedSource) {\n'
    '      validateScopedEvidence(data, selectedSource);\n'
    '    }\n'
    '    out.replaceChildren();\n'
    '    if (selectedSource) {\n'
    '      out.append(node("p", "Retrieval restricted to: " +\n'
    '        sourceEntries.get(selectedSource).doc, "warning"));\n'
    '    }\n',
    "response source-boundary check",
)

html = edit(
    html,
    '    "Explicit registry links, separate from ranking and immediate neighbors. " +\n',
    '    "Explicit registry links, separate from ranking and immediate neighbors. " +\n'
    '    "These may cite other sources; they are not selected-source retrieval. " +\n',
    "cross-source relationship explanation",
)

html = edit(
    html,
    'input.addEventListener("input", () => {\n',
    'input.addEventListener("input", () => {\n'
    '  hideSourceView();\n',
    "query invalidates source display",
)

extra = r'''
function hideSourceView() {
  sourceView.hidden = true;
  sourceView.replaceChildren();
}

function syncSourceControls() {
  const claimsMode = mode.value === "claims";
  sourceSelect.disabled = claimsMode;
  openSource.disabled = claimsMode || !sourceSelect.value;
}

function validateScopedEvidence(data, selectedSource) {
  const selected = sourceEntries.get(selectedSource);
  const bundle = data.retrieval_context;

  if (!selected || !bundle ||
      !Array.isArray(bundle.seed_results) ||
      !Array.isArray(bundle.supplementary_context)) {
    throw new Error("Invalid scoped evidence response");
  }

  for (const item of [
    ...bundle.seed_results, ...bundle.supplementary_context
  ]) {
    if (item.path !== selected.path ||
        item.commit_sha !== selected.sha ||
        item.doc !== selected.doc) {
      throw new Error("Response crossed the selected source boundary");
    }
  }
}

async function loadSources() {
  try {
    const response = await fetch("/api/sources");
    if (!response.ok) throw new Error("HTTP " + response.status);
    const data = await response.json();

    if (!Array.isArray(data.sources)) {
      throw new Error("Invalid source list");
    }

    const entries = new Map();
    const options = [node("option", "All sources — global search")];
    options[0].value = "";

    for (const item of data.sources) {
      if (!item || typeof item.source_id !== "string" ||
          !item.source_id || typeof item.doc !== "string" ||
          typeof item.path !== "string" ||
          !/^[0-9a-f]{40}$/i.test(String(item.sha || "")) ||
          item.source_id !== item.path + "@" + item.sha ||
          entries.has(item.source_id)) {
        throw new Error("Invalid or duplicate source identity");
      }
      entries.set(item.source_id, item);
      const option = node(
        "option", item.doc + " · " + item.sha.slice(0, 12)
      );
      option.value = item.source_id;
      options.push(option);
    }

    const previous = sourceSelect.value;
    sourceEntries.clear();
    for (const [key, value] of entries) sourceEntries.set(key, value);
    sourceSelect.replaceChildren(...options);
    if (entries.has(previous)) sourceSelect.value = previous;
    syncSourceControls();

    sourceStatus.textContent =
      entries.size + " pinned sources available. " +
      "Source selection constrains passages, not claim-registry search.";
  } catch (error) {
    sourceStatus.textContent =
      "Source list unavailable: " + error.message +
      ". Global search remains available.";
  }
}

async function openCompleteSource() {
  const selectedSource = sourceSelect.value;
  if (mode.value === "claims" || !selectedSource) return;

  const id = ++requestId;
  if (controller) controller.abort();
  controller = new AbortController();

  hideSourceView();
  out.replaceChildren();
  status.textContent = "Opening complete pinned source...";

  try {
    const response = await fetch(
      "/api/sources/view?source_id=" + encodeURIComponent(selectedSource),
      {signal: controller.signal}
    );
    if (!response.ok) throw new Error("HTTP " + response.status);
    const data = await response.json();

    if (id !== requestId) return;

    const expected = sourceEntries.get(selectedSource);
    const source = data.source;
    if (!expected || !source ||
        source.source_id !== selectedSource ||
        source.path !== expected.path ||
        source.sha !== expected.sha ||
        source.doc !== expected.doc ||
        typeof data.text !== "string") {
      throw new Error("Source view identity mismatch");
    }

    sourceView.append(node("h2", source.doc));
    sourceView.append(node(
      "p",
      "Complete pinned source. This is source navigation, not ranked evidence " +
      "or independent verification.",
      "warning"
    ));
    sourceView.append(node("div", "Source: " + source.path, "metadata"));
    sourceView.append(node("div", "Pinned commit: " + source.sha, "metadata"));

    const url = sourceURL({
      path: source.path,
      commit_sha: source.sha
    });
    if (url) {
      const link = node("a", "Open source at pinned revision");
      link.href = url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      sourceView.append(link);
    }

    sourceView.append(node("pre", data.text, "passage"));
    sourceView.hidden = false;
    status.textContent = "Complete pinned source loaded.";
  } catch (error) {
    if (id !== requestId || error.name === "AbortError") return;
    hideSourceView();
    status.textContent = "Source view failed: " + error.message;
  }
}

sourceSelect.addEventListener("change", () => {
  ++requestId;
  if (controller) controller.abort();
  hideSourceView();
  out.replaceChildren();
  syncSourceControls();
  status.textContent =
    "Source changed. Press Search or Open complete source.";
});

openSource.addEventListener("click", openCompleteSource);

loadSources();
search();
'''

html = edit(
    html,
    "search();\n</script>",
    extra + "\n</script>",
    "source actions and independent source-list load",
)

test_source = r'''"""Static UI guards; these are not browser race-execution tests."""
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
        'mode.addEventListener("change", search)',
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
'''

compile(test_source, str(test), "exec")
shutil.copy2(page, work / "index.before.html")
(work / "index.proposed.html").write_text(html, encoding="utf-8")
(work / "test.proposed.py").write_text(test_source, encoding="utf-8")

changed = False
created_test = False

try:
    changed = True
    page.write_bytes(html.encode("utf-8"))
    with test.open("x", encoding="utf-8") as handle:
        handle.write(test_source)
    created_test = True

    completed = subprocess.run(
        [
            sys.executable, "-B", "-m", "pytest",
            "-q", "-p", "no:cacheprovider", "tests",
        ],
        cwd=pkg,
        env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    (work / "package-tests.log").write_text(
        completed.stdout, encoding="utf-8"
    )
    print(completed.stdout, flush=True)

    if completed.returncode:
        raise RuntimeError("Package tests failed")

    subprocess.run(
        [
            "git", "-C", str(repo), "diff", "--check", "--",
            str(page.relative_to(repo)),
        ],
        check=True,
    )

    print("\nSOURCE_SCOPE_UI_STATIC_CHECKS=PASS")
    print("PACKAGE_SUITE=PASS")
    print("BROWSER_EXECUTION=AWAITING_MANUAL_TEST")
    print("BACKEND_NOT_CHANGED_BY_THIS_SCRIPT")
    print("DEFECT_COLLECTION_UNCHANGED")
    print("BACKUP_AND_LOGS:", work)
    print("NO_STAGE_COMMIT_PUSH_OR_INSTALL")
    print("HUGGING_FACE_UNCHANGED")

    subprocess.run(
        [
            "git", "-C", str(repo), "status", "--short", "--",
            str(pkg.relative_to(repo)),
        ],
        check=True,
    )

except BaseException:
    if changed:
        page.write_bytes(original)
        assert page.read_bytes() == original
        print("BROWSER_PAGE_RESTORE=VERIFIED")
    if created_test:
        shutil.move(str(test), str(work / "failed-generated-test.py"))
        print("GENERATED_TEST_PRESERVED_OUTSIDE_REPOSITORY")
    print("FAILED_ATTEMPT_SOURCE_AND_LOGS:", work)
    raise
