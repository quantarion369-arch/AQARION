AQARION-RAG

Evidence-preserving retrieval and navigation for AQARION research.

AQARION-RAG is a small research package for locating passages in pinned AQARION source documents and navigating claim and artifact references. It is an evidence-navigation tool, not a mathematical verification authority.

Current status

Prototype — implementation and evaluation are in progress.

Implemented in the current source:

- A Markdown corpus manifest with a pinned Git commit for each source document.
- Passage retrieval using lexical term overlap and a simple stemming function.
- An experimental BM25 ranking helper.
- Section-based extraction of status labels and artifact hashes.
- Basic supersession-reference detection and evidence-chain traversal.
- A local HTTP API for passage search, cited passage search, and claim search.
- A small known-answer and near-miss evaluation harness.

Not yet established:

- BM25 as the ranking function used by the main retrieval/API path.
- A canonical structured claim schema.
- Complete revision history across multiple source snapshots.
- Validated graph semantics for all supersession and dependency cases.
- Broad retrieval-quality measurements over a curated benchmark.
- Independent reproduction of the RAG execution and evidence receipts.
- Public deployment or production readiness.

Governing principle

Retrieval establishes what a source says.

Replay establishes what an execution produced.

Mathematical proof establishes what follows from stated assumptions.

Formal verification establishes what a proof assistant checked.

AQARION-RAG must never silently convert one category of evidence into another.

A retrieved passage is not a proof. A test result is not a universal theorem. A source hash is not mathematical validation. A claim's status must be read from the governing evidence record, not inferred from retrieval rank.

Current corpus

The corpus manifest is:

"corpus/MANIFEST.md"

Each entry identifies a document path and a pinned Git commit. Retrieval loads the document from that commit rather than silently substituting the current working-tree version.

The manifest currently contains a small corpus. It is not a complete index of the AQARION repository.

Source-reference terminology

Use "commit_sha" for the Git commit identifier. If the implementation also records a SHA-256 digest of the document bytes, store it separately as "document_sha256".

A commit identifier and a document-byte digest are different fields and must not be described interchangeably.

Retrieval behavior

The current "retrieve()" function:

1. Tokenizes the query and document passages.
2. Applies a lightweight suffix-based normalization.
3. Scores each passage by unique-term overlap.
4. Returns the highest-scoring passages with a source label, pinned commit identifier, and passage text.

The current score is a lexical overlap count. It is not a BM25 score.

The separate "bm25_search()" helper implements a BM25-style document-ranking function, but the main "retrieve()" function and HTTP search endpoint do not yet use it.

The additive retrieve_cited() interface returns path, commit_sha, char_start, char_end, rank, score, passage, and a source label. Character offsets are half-open positions in the decoded snapshot text returned by the loader, not raw-file byte offsets. The reconstruction rule is source_text[char_start:char_end] == passage. Legacy retrieve() behavior is preserved.

Claim and evidence navigation

The current claim parser treats Markdown sections as records and extracts status labels and artifact hashes from text. This is a preliminary parser, not a canonical claim schema.

The graph utilities provide initial support for:

- Finding explicit supersession references.
- Following a supersession chain.
- Finding records that directly reference an artifact hash.

These functions are navigation aids. Their outputs must not authorize claim promotion or replace ClaimLock's governing records.

Before graph results are used for governance decisions, the implementation needs stable claim identifiers, validated reference targets, explicit dependency semantics, cycle handling, and adversarial regression tests.

HTTP API

The current local API is implemented in "api.py" and binds to "127.0.0.1:8765" when run directly.

Available endpoints:

- "GET /api/claims"
- "GET /api/search?q=..."
- "GET /api/search/cited?q=..."
- "GET /api/claims/search?q=..."

The current server implements API routes only. The file "static/index.html" is a separate browser page and is not served by the current API handler.

The interface must render corpus-derived text safely. Endpoint regression tests now cover legacy search compatibility and cited search. Before any external deployment, broaden input validation, establish explicit serving configuration, and perform an appropriate security review.

Evaluation

The current evaluation harness includes known-answer retrieval cases, near-miss cases, a retrieval abstention case, and a small synthetic BM25 ranking test.

These tests are smoke/regression checks. They do not establish corpus-wide retrieval quality, semantic retrieval capability, or the correctness of claims surfaced by search.

The next evaluation stage should use a manually labelled query set and report:

- Recall@k.
- Precision@k.
- Mean reciprocal rank.
- Correct source and passage identification.
- Status-preservation accuracy.
- Stale/superseded-source handling.
- Abstention behavior.
- Conflict detection.
- Mutation-test detection.

Retrieval-only tests should remain deterministic wherever possible. Evaluation of generated answers, if added later, must be a separate layer measuring answer support and citation faithfulness.

Relationship to AQARION tooling

AQARION-RAG consumes and navigates evidence. It does not replace:

- ClaimLock — claim records, evidence classification, dependencies, and promotion governance.
- Replay — reproducible execution and runtime evidence.
- ProofGym / verification tools — executable checks and adversarial tests.
- Lean formalization — proof-assistant checking and axiom/dependency audits.

A retrieval result may point to any of these artifacts, but it cannot change their status.

Development priorities

1. Reconcile documentation with the actual retrieval implementation.
2. Integrate the intended ranking function and revise its evaluation.
3. Strengthen source citations and pinned-source validation.
4. Replace fragile section parsing with stable structured claim records.
5. Validate supersession and dependency graph semantics.
6. Test the HTTP API and browser interface.
7. Maintain the dedicated RAG CI workflow and inspect its revision-bound receipts.
8. Expand the corpus only after the source and citation contract is stable.

Reproducibility

A reproducible retrieval result should record:

- Query and retrieval parameters.
- Corpus manifest revision.
- Source commit and path.
- Stable passage locator.
- Ranking method and implementation revision.
- Python/runtime environment.
- Exact evaluation command and exit code.
- Expected and observed results.
- Known limitations.

The presence of a manifest, test file, or receipt does not by itself establish that the current source was executed successfully.

Scope boundary

AQARION-RAG is a research prototype. It is not a general-purpose semantic search engine, an answer-generating agent, a proof system, or a certification service.

The goal is narrower and more useful: make AQARION's existing research evidence easier to find, trace, compare, and reproduce without weakening the distinction between a claim and the evidence supporting it.

## Status update — 2026-10-15

Retrieval plus fixture-bound assessment is wired through `wire_assess.py` and was verified in Termux on 2026-10-14. Witness parameters remain fixture-defined. Corpus-derived witness extraction, general automatic refutation from retrieved documents, and broader end-to-end validation remain open.

## Measured development checkpoint — 2026-10-19

The dedicated AQARION RAG Verification workflow succeeded on GitHub for
commit a77f3dcc46eb89150e3e617f6648c6a49e147fae, run 39346847689.
The execution uploaded an evidence artifact. This does not establish
independent reproduction, branch-protection enforcement, or deployment.

The 24-case development benchmark uses the existing two pinned documents.
Its labels identify selected supporting passages, not exhaustive relevance
judgments. No corpus-wide precision or recall claim is made.

| Variant | Single hit@3 | MRR@3 | Complete multi-passage | Evidence groups |
|---|---:|---:|---:|---:|
| Reviewed baseline | 12/16 | 0.6771 | 1/4 | 4/8 |
| Stop-word experiment | 14/16 | 0.8438 | 0/4 | 3/8 |
| IDF overlap experiment | 12/16 | 0.7500 | 1/4 | 4/8 |

The original baseline reported 0/4 complete multi-passage cases and 3/8
evidence groups. Review found that M02 omitted a valid alternative supporting
paragraph. Rescoring the saved results corrected those counts to 1/4 and 4/8.
No retrieval rerun or ranking change produced that correction.

Neither experimental ranker replaced production behavior. Citation slices
reconstructed in the recorded executions, but evidence completeness remains
weak. Unsupported questions returning passages do not establish answerability.

Preserved reports and experimental scripts are under
benchmarks/evidence/2026-10-19/. These are historical development receipts.
They include original local paths. Historical experiment scripts retain their
original environment assumptions and are not portable entry points.

The maintained baseline runner reads benchmarks/cases.json and verifies the
baseline retrieval module and corpus manifest hashes. It does not require
documentation-only commits to retain the original repository HEAD.

Run from any directory, with a fresh output directory outside the checkout:

    python3 -B /path/to/AQARION/AQARION-QUANTARION-AI/PACKAGES/AQARION-RAG/benchmarks/retrieval_baseline.py --output-dir /path/outside/checkout/new-results

A completed benchmark is not a retrieval-quality pass. No quality threshold
has been adopted. Generated-answer evaluation and independent held-out
evaluation remain separate, unperformed tasks.

## Immediate-neighbor context experiment

At implementation commit 482af5384b280c647f976aa89602c0d99411d56d,
a local 24-case experiment reproduced every baseline top-three result and
added the immediately preceding and following nonempty paragraphs from each
seed's pinned document. Expansion was nonrecursive, deduplicated per query,
and capped at six supplementary passages.

Single-passage support remained 12/16. Complete multi-passage support increased
from 1/4 to 3/4; required evidence-group coverage increased from 4/8 to 6/8.
M01 and M03 became complete. M04 and the four single-passage misses remained
unresolved.

The experiment added 112 supplementary passage occurrences and 15,983
characters to 69 seed occurrences and 21,810 seed characters. These are
per-query totals, not globally unique passage counts. The expanded budget
must not be presented as an equal-budget ranking improvement.

All returned citation slices reconstructed. Supplementary passages remain
context-only, not adjudicated supporting evidence. Unsupported queries also
received additional context. No answer-generation or abstention validation
was performed.

The experiment is preserved under benchmarks/evidence/2026-10-19/adjacency/.
It was executed locally, not by the existing CI benchmark runner.
No production ranker, legacy API, or deployed endpoint was changed.

## Optional context module and passage-budget comparison

context.retrieve_with_context(query) preserves the original top-three cited
results and returns immediate paragraph neighbors separately. Expansion is
nonrecursive, pinned-source-local, deduplicated, and capped at six supplements.
Each supplementary record retains exact offsets and seed links. Context is
not adjudicated support. No HTTP context endpoint has been added.

Tests cover boundaries, repeated text, shared neighbors, seed deduplication,
document/revision isolation, input preservation, invalid spans, the cap, and
exact replay of all 24 saved adjacency cases.

The preserved local passage-budget comparison found:

| Method | Single supported | Complete multi-passage | Evidence groups | Characters |
|---|---:|---:|---:|---:|
| Top three | 12/16 | 1/4 | 4/8 | 21810 |
| Adjacent context | 12/16 | 3/4 | 6/8 | 37793 |
| Deeper ranked retrieval | 14/16 | 2/4 | 5/8 | 50051 |

Deeper retrieval received each query's adjacency passage allowance. L07 had
two fewer positive-scoring results than its allowance. Character budgets
were not matched. Counts aggregate passage occurrences across queries.

Adjacency uniquely recovered M03 in this comparison; deeper retrieval
recovered L06 and Q03. Neither resolved M04. The methods are complementary
on this development set, not independently validated universal improvements.

Comparison receipts are under benchmarks/evidence/2026-10-19/budget-comparison/.
Production ranking and existing HTTP response contracts remain unchanged.
