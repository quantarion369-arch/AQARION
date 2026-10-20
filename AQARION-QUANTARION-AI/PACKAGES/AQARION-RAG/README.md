# AQARION-RAG

[![AQARION RAG Verification](https://github.com/quantarion369-arch/AQARION/actions/workflows/aqarion-rag-verify.yml/badge.svg?branch=main)](https://github.com/quantarion369-arch/AQARION/actions/workflows/aqarion-rag-verify.yml)

A local evidence workbench for inspecting pinned research passages, nearby context, and explicitly registered corrections.

AQARION-RAG helps you locate and trace evidence. It does not prove mathematical claims, independently validate reported experiments, or guarantee that retrieved material answers a question.

## Start here

You can:

- Search passages from Git-revision-pinned source documents.
- Inspect source paths, commits, exact character offsets, and lexical scores.
- View immediate neighboring paragraphs separately from ranked results.
- Discover registered corrections outside the retrieved neighborhood.
- Inspect reported follow-up evidence with its original limitations.
- Search preliminary claim records and artifact references.
- Use the browser interface or the local JSON API.

The implementation is a research prototype with tested contracts and a small development corpus, not a complete repository index.

## Run the browser application

Requirements: Python 3, Git, and a checkout containing the source revisions named in the corpus manifest. The local HTTP server uses the Python standard library.

For the existing Termux checkout:

```bash
cd "$HOME/AQARION/AQARION-QUANTARION-AI/PACKAGES/AQARION-RAG"
python3 -B api.py
```

Leave that terminal running. Open this address in the browser on the same device:

```text
http://127.0.0.1:8765/
```

Stop the server with Ctrl+C. If port 8765 is occupied, inspect the existing server instead of starting duplicate instances.

The server binds locally. This is not a public deployment.

## Try correction-aware evidence search

Choose “Passages + context” and search:

```text
ALL VERIFIED — three independent checks, all clean.
```

The registered example preserves the historical statement while exposing:

1. Its documented independence/provenance correction.
2. A separately reported production-source follow-up.
3. Pinned citations, exact offsets, and expected passage hashes.
4. The relationship's pending-review status and scope note.

The correction qualifies provenance; it is not automatically a numerical refutation. The search displays a reported follow-up, rather than executing that experiment.

This is explicit relationship tracing, not automatic detection of every correction.

## Understand the evidence layers

| Layer | What it provides | What it does not establish |
|---|---|---|
| Ranked passages | Lexically matched source text | Sufficient support or truth |
| Supplementary context | Immediate neighboring paragraphs | That proximity implies support |
| Related evidence | Explicit registry relationships | Independent approval of interpretation |
| Reported follow-up | A source's account of an execution | A fresh replay |
| Tests and CI | Checks of declared implementation contracts | General research correctness |

Retrieval, recorded execution, mathematical proof, formal verification, and independent reproduction remain separate evidence categories.

## Citation contract

Structured citations identify:

```text
path
commit_sha
char_start
char_end
passage
rank
score
```

Offsets are half-open positions in decoded snapshot text, not raw-file byte offsets:

```python
source_text[char_start:char_end] == passage
```

A reconstructible citation establishes location, not relevance or claim truth. A Git commit identifier and a SHA-256 file or passage digest are different identifiers.

## HTTP endpoints

All listed routes use GET. Query-string values should be URL-encoded.

| Route | Parameters | Purpose |
|---|---|---|
| `/` | None | Browser page served from `static/index.html` |
| `/api/search` | `q` | Legacy top-three passage response |
| `/api/search/cited` | `q` | Top-three structured passage citations |
| `/api/search/context` | `q` | Existing context response |
| `/api/search/evidence` | `q` | Context, related evidence, and diagnostics |
| `/api/claims` | Optional `status` | Parsed claim listing and count |
| `/api/claims/search` | `q`, optional `has_artifact=true` | Claim search |

The claims status filter is a case-insensitive substring filter. The artifact filter is enabled by the literal value `true`.

The browser uses the evidence route for passage searches. Its response separates:

```text
retrieval_context
related_evidence
relationship_diagnostics
```

The context endpoint preserves its existing response contract. Unknown routes return a JSON error with HTTP 404.

## Python context interface

From the package directory:

```python
from context import retrieve_with_context

result = retrieve_with_context("your research question")
seeds = result["seed_results"]
neighbors = result["supplementary_context"]
metadata = result["expansion_metadata"]
```

The function:

- Preserves the original top-three cited results.
- Adds the preceding and following nonempty paragraphs in each seed's pinned document.
- Does not expand recursively.
- Deduplicates supplementary passages while retaining seed links.
- Excludes passages already present as seeds.
- Caps supplementary output at six passages.
- Reports seed and supplementary character costs.

It enforces a passage cap, not a character cap. Character-cap selection was evaluated separately and was not installed as a production default.

## Explicit relationships

`relationships.json` stores revision-bound records. `relationships.py` checks manifest membership, integer offsets, bounds, complete paragraph identity, and expected passage hashes.

The current relationship type is `qualifies_provenance`, based on an explicit documented correction. General contradiction detection and definition-distinction relationships are not implemented by that schema.

Locator validation is not interpretation approval. Pending relationships remain candidates. Invalid or unavailable enrichment produces diagnostics rather than being displayed as valid.

Base retrieval is preserved when relationship enrichment reports a failure. No displayed relationship does not establish that no correction exists.

The browser renders source text using `textContent`, rather than treating it as trusted HTML or Markdown. That is a specific safety measure, not a complete deployment security audit.

## Corpus and evaluation

The manifest currently pins two source documents:

- The evidence ledger.
- The quadratic-stability witness document.

Referenced production code, receipts, and proof artifacts are not comprehensively indexed. A ledger summary is not a substitute for inspecting the underlying artifact.

The reviewed 24-case development benchmark measures selected supporting passages, not exhaustive relevance judgments or held-out performance.

| Historical policy | Single support | Complete multi-passage support | Evidence groups |
|---|---:|---:|---:|
| Original top three | 12/16 | 1/4 | 4/8 |
| Immediate-neighbor context | 12/16 | 3/4 | 6/8 |
| Deeper ranking at tested passage allowances | 14/16 | 2/4 | 5/8 |

The passage comparison had one allowance shortfall, and character consumption did not match. Adjacency and deeper ranking recovered different evidence; neither was a universal winner.

Separate experiments tested supplementary character caps of 0, 500, 1000, and 2000 using whole-passage accept-or-skip selection. They did not select a production default.

Stop-word and IDF experiments did not replace production ranking. The main retriever remains lexical overlap with lightweight stemming.

The M02 label correction is preserved separately from the original baseline report; no retrieval improvement is claimed for relabeling.

- [Development evidence and limitations](benchmarks/evidence/2026-10-19/README.md)
- [Reviewed benchmark cases](benchmarks/cases.json)
- [Historical evidence checksums](benchmarks/SHA256SUMS)

Historical scripts retain their original environment assumptions. Reliable semantic abstention, generated-answer evaluation, and independent held-out validation remain unestablished.

## Tests and CI

[AQARION RAG Verification workflow](../../../.github/workflows/aqarion-rag-verify.yml)

The workflow runs on qualifying pushes to main, matching pull requests, and manual dispatch. A feature-branch push alone is not a configured push trigger.

The suite covers citation reconstruction, legacy/API compatibility, context boundaries and saved replay, browser-source contracts, relationship validation, and enrichment failure behavior.

Static browser-source checks are not equivalent to comprehensive automated browser testing. Test counts should come from the receipt for the tested revision, not a permanently copied README number.

With pytest installed, run from the package directory:

```bash
package_dir="$PWD"
run_dir=$(mktemp -d "$HOME/AQARION-RAG-tests-XXXXXXXX")

(
  cd "$run_dir" || exit 1
  PYTHONPATH="$package_dir"   PYTHONDONTWRITEBYTECODE=1   PYTEST_DISABLE_PLUGIN_AUTOLOAD=1     python3 -B -m pytest       -o addopts= -p no:cacheprovider       --junitxml="$run_dir/tests.xml"       "$package_dir/tests"
)
```

The badge reports changing workflow status. It is not a certification of every historical research claim or experiment.

## Separate research replay harness

`research/closure-cost/check_actual_source.py` is a separate mathematical cross-check harness, not a search operation.

At the inspected implementation checkpoint, its repository-root/path construction requires repair and regression coverage. Application CI success does not establish that this standalone harness runs correctly.

The archived `actual-source-n4.txt` reports 3,984 cases over every map and set partition for 1 <= n <= 4. Reading that receipt is not a fresh execution, general correctness proof, or machine-checked theorem verification.

## Project layout

```text
api.py                 Local HTTP routes and browser serving
static/index.html      Browser research interface
retrieve.py            Pinned lexical retrieval and citations
context.py             Optional immediate-neighbor context
relationships.json     Explicit relationship registry
relationships.py       Locator validation and relationship lookup
claims.py              Preliminary claim parsing/search
graph.py               Initial graph navigation helpers
supersedes.py          Prose-derived supersession detection
corpus/MANIFEST.md     Pinned source inventory
tests/                 Regression and contract tests
benchmarks/            Development cases and preserved evidence
research/              Separate research artifacts and harnesses
```

Prose-derived graph navigation is separate from the explicit relationship registry. General graph target-resolution correctness is not established by the correction-tracing feature.

## Next work and boundaries

- Independently review pending relationship interpretations.
- Add distinct relationships only when their sources justify the type and scope.
- Repair and test the standalone replay harness before a fresh research replay.
- Evaluate actual research tasks, not only benchmark scores.
- Keep AQARION-LEAN proof work and ClaimLock governance separate from RAG.
- Review authentication, input handling, serving configuration, and security before external deployment.

No comprehensive correction coverage, general claim verification, independent reproduction, or public-production readiness is asserted.

## Documentation checkpoint and history

This README was reconciled against implementation commit:

```text
40680eb1bce791dc872c98869552d538f8b20ee3
```

The [previous README](docs/README-HISTORY-before-2026-10-20.md) is preserved verbatim as historical documentation. It contains superseded statements and is not the current operating guide.

The workbench helps inspect what is recorded, where it came from, and what qualifies it. It does not silently promote retrieved text into a verified conclusion.
