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
- A local HTTP API for passage search and claim search.
- A small known-answer and near-miss evaluation harness.

Not yet established:

- BM25 as the ranking function used by the main retrieval/API path.
- A canonical structured claim schema.
- Complete revision history across multiple source snapshots.
- Validated graph semantics for all supersession and dependency cases.
- Broad retrieval-quality measurements over a curated benchmark.
- RAG-specific automated CI and revision-bound execution receipts.
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

The current result structure is a prototype. A stable citation contract should include a source path, commit identifier, stable passage locator, rank/score, and optional document-byte digest.

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
- "GET /api/claims/search?q=..."

The current server implements API routes only. The file "static/index.html" is a separate browser page and is not served by the current API handler.

The interface must render corpus-derived text safely. Before any external deployment, add endpoint tests, input validation, explicit serving configuration, and an appropriate security review.

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
7. Add a dedicated RAG CI workflow with revision-bound receipts.
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
